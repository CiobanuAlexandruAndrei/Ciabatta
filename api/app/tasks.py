from .celery_app import celery
from .celery_app import app 

from openai import OpenAI
import json
import redis
from .seo.models import ContentOutlineTask, ContentOutline, APICostRecord, APIUsed
import uuid
from .config import Config
from .extensions import db
from libs.pricing_openai import openai_api_calculate_cost
from flask import current_app

redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB, decode_responses=Config.REDIS_DECODE_RESPONSES)


@celery.task(bind=True)
def generate_content_outline_task(self, prompt, example_json, profile_id, content_outline_id):
    # Push application context
    with app.app_context():
        client = OpenAI()

        task_id = str(uuid.uuid4().hex)
        task = ContentOutlineTask(
            id=task_id,
            content_outline_task_status='Processing',
            content_outline_id=content_outline_id,
            profile_id=profile_id,
            task_status_name='Processing'
        )
        db.session.add(task)
        db.session.commit()

        # Save streaming data to Redis
        redis_client.delete(task_id)  # Clear previous data

        def generate():
            try:
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Provide output in valid JSON. For text line breaks insert '<br>', be sure to add line breaks correctly for readability. The data schema should be like this: " + json.dumps(example_json)},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type":"json_object"},
                    stream=True,
                    stream_options={
                        "include_usage": True
                    }
                )

                outline_content = ""
                for chunk in stream:
                    if hasattr(chunk, 'usage') and chunk.usage:
                        print(chunk.usage)
                        usage_data = chunk.usage
                        cost = openai_api_calculate_cost(usage_data)
                        print(cost)

                        api_name = "OpenAI"
                        api_used = APIUsed.query.filter_by(name=api_name).first()

                        if not api_used:
                            api_used = APIUsed(name=api_name)
                            db.session.add(api_used)
                            db.session.commit()

                        cost_record = APICostRecord(cost=cost, api_used_name=api_used.name)
                        db.session.add(cost_record)
                        db.session.commit()

                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                            if chunk.choices[0].delta.content is not None:
                                content = chunk.choices[0].delta.content
                                redis_client.rpush(task_id, content)
                                outline_content += content
                                print(content)

                redis_client.rpush(task_id, 'END')  # Mark end of data

                # Update the ContentOutline with the generated content
                content_outline = ContentOutline.query.get(content_outline_id)
                if content_outline:
                    content_outline.content = outline_content
                    db.session.commit()

                # Update task status to Completed
                task.content_outline_task_status = 'Completed'
                db.session.commit()

            except Exception as e:
                # Update task status to Failed
                task.content_outline_task_status = 'Failed'
                db.session.commit()
                redis_client.rpush(task_id, f'ERROR: {str(e)}')  # Store error in Redis
                self.retry(exc=e, countdown=60)  # Retry after 60 seconds if necessary
        
        generate()