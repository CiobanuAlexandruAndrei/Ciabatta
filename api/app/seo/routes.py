import os
import json
import openai
from openai import OpenAI
from flask import request, jsonify, Response, current_app, stream_with_context
from flask_httpauth import HTTPTokenAuth
from ..extensions import db
from ..security.models import Profile, User, Token
from .models import *
from .forms import *
from .serializers import *
from libs.data_client import RestClient
from libs.pricing_openai import openai_api_calculate_cost
from dotenv import load_dotenv
import pandas as pd
from . import seo  
from datetime import datetime, timedelta

load_dotenv()

MOZ_ACCESS_TOKEN = os.getenv('MOZ_ACCESS_TOKEN')
DATAFORSEO_USERNAME = os.getenv('DATAFORSEO_USERNAME')
DATAFORSEO_PASSWORD = os.getenv('DATAFORSEO_PASSWORD')

auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    # print(f"Verifying token: {token}")  # Debug statement
    token_obj = Token.query.filter_by(token=token).first()
    if token_obj:
        # print(f"Token valid for user_id: {token_obj.user_id}")  # Debug statement
        return User.query.get(token_obj.user_id)
    # print("Token invalid")  # Debug statement
    return None

@auth.login_required
def get_current_user():
    return auth.current_user()

@seo.route('/search_keyword', methods=['POST'])
@auth.login_required
def search_keyword():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()

    form = KeywordSearchForm()
    if form.validate_on_submit():
        keyword = form.name.data
        country = form.country.data
        limit = form.limit.data

        stored_keyword = KeywordData.query.filter_by(name=keyword, country=country).first()

        if stored_keyword:
            return jsonify({'message': 'Keywords found', 'result': json.loads(stored_keyword.json)}), 200
        else:
            client = RestClient(DATAFORSEO_USERNAME, DATAFORSEO_PASSWORD)
            post_data = dict()

            post_data[len(post_data)] = dict(
                keyword=keyword,
                location_name=country,
                language_name="English",
                limit=limit if limit else 10,
                include_serp_info=True,
                include_seed_keyword=True,
            )

            response = client.post("/v3/dataforseo_labs/google/keyword_suggestions/live", post_data)

            if response.get("status_code") == 20000:
                if response['tasks_error'] > 0:
                    return jsonify({'message': 'Service not available', 'details': response}), 503
                elif response.get('tasks') and response['tasks'][0].get('result'):
                    api_name = "DataForSEO"
                    api_used = APIUsed.query.filter_by(name=api_name).first()
                    if not api_used:
                        api_used = APIUsed(name=api_name)
                        db.session.add(api_used)
                        db.session.commit()

                    cost_record = APICostRecord(cost=response['cost'], api_used_name=api_used.name)
                    db.session.add(cost_record)
                    db.session.commit()

                    results = response['tasks'][0]['result'][0].get('items', [])
                    if not results:
                        return jsonify({'message': 'No results found in the response'}), 204

                    for result_dict in results:
                        trend = 'none'
                        monthly_searches = result_dict['keyword_info'].get('monthly_searches', [])
                        if monthly_searches and len(monthly_searches) > 1:
                            last_month_search_volume = monthly_searches[0].get('search_volume', 0)
                            current_search_volume = result_dict['keyword_info'].get('search_volume', 0)
                            if last_month_search_volume is None:
                                last_month_search_volume = 0
                            if current_search_volume is None:
                                current_search_volume = 0
                            if last_month_search_volume > current_search_volume:
                                trend = 'DOWN'
                            elif last_month_search_volume == current_search_volume:
                                trend = 'SAME'
                            elif last_month_search_volume < current_search_volume:
                                trend = 'UP'
                        
                        result_dict['keyword_info']['trend'] = trend
                        if 'monthly_searches' in result_dict['keyword_info']:
                            del result_dict['keyword_info']['monthly_searches']
                    
                    saved_keyword = KeywordData(name=keyword, country=country, json=json.dumps(results, indent=4))
                    db.session.add(saved_keyword)
                    db.session.commit()

                    return jsonify({'message': 'Keywords found', 'result': results}), 200
                else:
                    return jsonify({'message': 'No results found in the response'}), 204
            else: 
                print(response)
                return jsonify({'message': 'Error retrieving keywords data', 'details': response}), 500
    else:
        print(form.errors)
        return jsonify({'message': 'Invalid form data', 'errors': form.errors}), 400
    

@seo.route('/save_keyword', methods=['POST'])
@auth.login_required
def save_keyword():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()

    form = KeywordForm()
    if form.validate_on_submit():
        name = form.name.data

        keyword = Keyword(name=name)
        db.session.add(keyword)
        db.session.commit()

        return jsonify({'message': 'Keyword saved successfully'}), 201
    else:
        return jsonify({'message': 'Error adding the keyword to the database', 'errors': form.errors}), 500


@seo.route('/get_keywords_clusters', methods=['GET'])
@auth.login_required
def get_keywords_clusters():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    clusters = KeywordCluster.query.filter_by(profile_id=user_profile.id).all()
    schema = KeywordClusterSchema(many=True)
    clusters_data = schema.dump(clusters)
    return jsonify({'message': 'Keywords Clusters retrieved successfully', 'clusters': clusters_data}), 200


@seo.route('/generate_keyword_suggestions', methods=['POST'])
@auth.login_required
def generate_keyword_suggestions_view():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    form = KeywordGenerationForm()
    if form.validate_on_submit():
        topic = form.topic.data
        intent = form.intent.data
        additional_instructions = form.additional_instructions.data
        
        example_json = {
            "keywords": [
                "example keyword 1", "example keyword 2", "example keyword 3"
            ]
        }

        prompt = f'Act like a SEO expert, you are also an expert in the specified topic below. Generate 20 SEO keywords that must help rank my company on Google;\nTopic: {topic};\nSearch Intent:{intent}\nAdditional instructions:{additional_instructions}'
        client = OpenAI()
        openai_response = client.chat.completions.create(
            model='gpt-4o-mini',
            response_format={"type":"json_object"},
            messages=[
                {"role":"system","content":"Provide output in valid JSON. The data schema should be like this: "+json.dumps(example_json)},
                {"role":"user","content":prompt}
            ]
        )

        keywords = openai_response.choices[0].message.content
        cost = openai_api_calculate_cost(openai_response.usage)
        generated_keywords = json.loads(keywords)

        api_name = "OpenAI"
        api_used = APIUsed.query.filter_by(name=api_name).first()
        if not api_used:
            api_used = APIUsed(name=api_name)
            db.session.add(api_used)
            db.session.commit()

        cost_record = APICostRecord(cost=cost, api_used_name=api_used.name)
        db.session.add(cost_record)
        db.session.commit()
        
        return jsonify({'message': 'Keywords generated', 'result': generated_keywords}), 200
    else:
        print(form.errors)
        return jsonify({'message': 'Error generating keywords', 'errors': form.errors}), 500
    
@seo.route('/generate_content_ideas', methods=['POST'])
@auth.login_required
def generate_content_ideas_view():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    form = ContentIdeasForm()
    if form.validate_on_submit():
        topic = form.topic.data
        additional_instructions = form.additional_instructions.data

        example_json = {
            "topics": [
                {
                    "unique_semantically_related_topic": "Example topic",
                    "variations": [
                        {
                            "variation": "variation of example topic 1",
                            "clickbait_title": "title for variation of example topic 1"
                        },
                        {
                            "variation": "variation of example topic 2",
                            "clickbait_title": "title for variation of example topic 2"
                        },
                        {
                            "variation": "variation of example topic 3",
                            "clickbait_title": "title for variation of example topic 3"
                        },
                        {
                            "variation": "variation of example topic 4",
                            "clickbait_title": "title for variation of example topic 4"
                        },
                    ]
                }
            ]
        }

        prompt = (
            f"give me precisely 10 semantically relevant but unique topics under the main category of {topic}, "
            f"and for each, give me 10 different variations of the topic that each address a different search intent. "
            f"Make it in table format with the following columns: column 1: The unique semantically related topic, "
            f"column 2: the different variations on it, column 3: an intriguing, clickbait style title.\n\n"
            f"Additional instructions: {additional_instructions}"
        )

        usage_data = None
        client = OpenAI()

        def generate():
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Provide output in valid JSON. The data schema should be like this: " + json.dumps(example_json)},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
                stream_options={
                    "include_usage": True
                }
            )

            for chunk in stream:
                if hasattr(chunk, 'usage') and chunk.usage:
                    print(chunk.usage)
                    usage_data = chunk.usage
                    cost = openai_api_calculate_cost(usage_data)

                    api_name = "OpenAI"
                    api_used = APIUsed.query.filter_by(name=api_name).first()

                    if not api_used:
                        api_used = APIUsed(name=api_name)
                        db.session.add(api_used)
                        db.session.commit()

                    cost_record = APICostRecord(cost=cost, api_used_name=api_used.name)
                    db.session.add(cost_record)
                    db.session.commit()
                
                # Check for the choices list and its content
                if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                    if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                        if chunk.choices[0].delta.content is not None:
                            yield chunk.choices[0].delta.content

        with current_app.app_context():
            return Response(stream_with_context(generate()), content_type='application/json')
    else:
        print(form.errors)
        return jsonify({'message': 'Error generating topics', 'errors': form.errors}), 500


@seo.route('/get_all_api_usage_costs', methods=['GET'])
@auth.login_required
def get_all_api_usage_costs():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    data = {}
    schema = APICostRecordSchema(many=True)
    for api_obj in APIUsed.query.all():
        cost_records = APICostRecord.query.filter_by(api_used_name=api_obj.name).all()
        data[api_obj.name] = schema.dump(cost_records)
    
    return jsonify({'message': 'API cost data retrieved successfully', 'data': data}), 200

@seo.route('/get_api_usage_costs', methods=['POST'])
@auth.login_required
def get_api_usage_costs():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    
    form = PeriodForm()
    if form.validate_on_submit():
        period = form.period.data
    
        data = []
        schema = APICostRecordSchema(many=True)

        for api_obj in APIUsed.query.all():
            cost_records = APICostRecord.query.filter_by(api_used_name=api_obj.name).all()
            for record in cost_records:
                data.append({
                    'api_name': api_obj.name,
                    'cost': record.cost,
                    'timestamp': record.timestamp
                })

        df = pd.DataFrame(data)

        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        else:
            return jsonify({'message': 'Timestamp column not found in DataFrame'}), 400

        df_grouped = pd.DataFrame()

        if period == 'week':
            end_date = datetime.now()
            start_date = end_date - timedelta(days=6)
            df_filtered = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
            df_filtered['day'] = df_filtered['timestamp'].dt.date
            df_grouped = df_filtered.groupby(['api_name', 'day']).agg({'cost': 'sum', 'timestamp': 'count'}).reset_index()
        elif period == 'month':
            end_date = datetime.now()
            start_date = end_date - timedelta(days=29)
            df_filtered = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
            df_filtered['day'] = df_filtered['timestamp'].dt.date
            df_grouped = df_filtered.groupby(['api_name', 'day']).agg({'cost': 'sum', 'timestamp': 'count'}).reset_index()
        elif period == 'year':
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            df_filtered = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
            df_filtered['month'] = df_filtered['timestamp'].dt.to_period('M')
            df_grouped = df_filtered.groupby(['api_name', 'month']).agg({'cost': 'sum', 'timestamp': 'count'}).reset_index()
        else:
            return jsonify({'message': 'Invalid period specified'}), 400


        response_data = {}
        if period == 'year':
            df_grouped['period'] = df_grouped['month'].astype(str)
        else:
            df_grouped['period'] = df_grouped['day'].astype(str)

        for api_name in df_grouped['api_name'].unique():
            api_data = df_grouped[df_grouped['api_name'] == api_name]
            response_data[api_name] = {
                'costs': api_data['cost'].tolist(),
                'periods': api_data['period'].tolist(),
                'call_counts': api_data['timestamp'].tolist()  
            }

        return jsonify({'message': 'API cost data retrieved successfully', 'data': response_data}), 200
    
    else:
        print(form.errors)
        return jsonify({'message': 'Error with form', 'errors': form.errors}), 400

@seo.route('/add_keyword_to_cluster', methods=['POST'])
@auth.login_required
def add_keyword_to_cluster():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    form = AddKeywordToClusterForm()
    
    if form.validate_on_submit():
        keyword_name = form.keyword_name.data
        cluster_id = form.cluster_id.data
        
        cluster = KeywordCluster.query.filter_by(id=cluster_id, profile_id=user_profile.id).first()
        
        if not cluster:
            return jsonify({'message': 'Keyword cluster not found'}), 404
        
        keyword = Keyword.query.filter_by(name=keyword_name).first()
        
        if not keyword:
            keyword = Keyword(name=keyword_name)
            db.session.add(keyword)
            db.session.commit()
        else:
            if keyword in cluster.keywords:
                return jsonify({'message': 'Keyword already exists in the cluster'}), 400
        
        cluster.keywords.append(keyword)
        db.session.commit()
        
        return jsonify({'message': 'Keyword added to cluster successfully'}), 201
    else:
        print(form.errors)
        return jsonify({'message': 'Error adding keyword to cluster', 'errors': form.errors}), 400


@seo.route('/check_keyword_in_cluster', methods=['POST'])
@auth.login_required
def check_keyword_in_cluster():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    form = AddKeywordToClusterForm()
    
    if form.validate_on_submit():
        keyword_name = form.keyword_name.data
        cluster_id = form.cluster_id.data
        
        cluster = KeywordCluster.query.filter_by(id=cluster_id, profile_id=user_profile.id).first()
        
        if not cluster:
            return jsonify({'message': 'Keyword cluster not found'}), 404
        
        keyword = Keyword.query.filter_by(name=keyword_name).first()
        
        if keyword in cluster.keywords:
            return jsonify({'message': 'Keyword exists in the cluster'}), 200
        else:
            return jsonify({'message': 'Keyword does not exist in the cluster'}), 404
    else:
        return jsonify({'message': 'Invalid form data', 'errors': form.errors}), 400


@seo.route('/create_keyword_cluster', methods=['POST'])
@auth.login_required
def create_keyword_cluster():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    form = KeywordClusterForm()
    if form.validate_on_submit():
        name = form.keyword_cluster_name.data
        keyword_cluster = KeywordCluster(name=name, profile_id=user_profile.id)
        db.session.add(keyword_cluster)
        db.session.commit()

        return jsonify({'message': 'Keyword cluster created successfully'}), 201
    else:
        return jsonify({'message': 'Error creating keyword cluster', 'errors': form.errors}), 400
    
@seo.route('/delete_keyword_cluster', methods=['DELETE'])
@auth.login_required
def delete_keyword_cluster():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    form = KeywordClusterDeleteForm()

    if form.validate_on_submit():
        cluster_id = form.cluster_id.data
        cluster = KeywordCluster.query.filter_by(id=cluster_id, profile_id=user_profile.id).first()
        if not cluster:
            return jsonify({'message': 'Keyword cluster not found'}), 404
        
        db.session.delete(cluster)
        db.session.commit()

        return jsonify({'message': 'Keyword cluster deleted successfully'}), 200
    else:
        return jsonify({'message': 'Error deleting keyword cluster', 'errors': form.errors}), 400

@seo.route('/delete_keyword_from_cluster', methods=['DELETE'])
@auth.login_required
def delete_keyword_from_cluster():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    form = AddKeywordToClusterForm()
    
    if form.validate_on_submit():
        keyword_name = form.keyword_name.data
        cluster_id = form.cluster_id.data
        
        cluster = KeywordCluster.query.filter_by(id=cluster_id, profile_id=user_profile.id).first()
        
        if not cluster:
            return jsonify({'message': 'Keyword cluster not found'}), 404
        
        keyword = Keyword.query.filter_by(name=keyword_name).first()
        
        if not keyword or keyword not in cluster.keywords:
            return jsonify({'message': 'Keyword not found in the cluster'}), 404
        
        cluster.keywords.remove(keyword)
        db.session.commit()
        
        return jsonify({'message': 'Keyword deleted from cluster successfully'}), 200
    else:
        return jsonify({'message': 'Error deleting keyword from cluster', 'errors': form.errors}), 400


@seo.route('/update_keyword_cluster_name', methods=['PUT'])
@auth.login_required
def update_keyword_cluster_name():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    form = UpdateKeywordClusterNameForm()

    if form.validate_on_submit():
        cluster_id = form.keyword_cluster_id.data
        new_name = form.keyword_cluster_name.data

        cluster = KeywordCluster.query.filter_by(id=cluster_id, profile_id=user_profile.id).first()

        if not cluster:
            return jsonify({'message': 'Keyword cluster not found'}), 404

        cluster.name = new_name
        db.session.commit()

        return jsonify({'message': 'Keyword cluster name updated successfully'}), 200
    else:
        return jsonify({'message': 'Error updating keyword cluster name', 'errors': form.errors}), 400

@seo.route('/check_content_idea', methods=['POST'])
@auth.login_required
def check_content_idea():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()

    form = ContentIdeaCreationForm()
    if form.validate_on_submit():
        title = form.title.data
        topic_variation = form.topic_variation.data
        topic_category = form.topic_category.data

        content_idea = ContentIdea.query.filter_by(
            title=title,
            topic_variation=topic_variation,
            topic_category=topic_category,
            profile_id=user_profile.id
        ).first()

        if content_idea:
            return jsonify({'is_saved': True})
        else:
            return jsonify({'is_saved': False})
    else:
        print(form.errors)
        return jsonify({'message': 'Error checking content idea', 'errors': form.errors}), 400

@seo.route('/create_content_idea', methods=['POST'])
@auth.login_required
def create_content_idea():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    form = ContentIdeaCreationForm()
    if form.validate_on_submit():
        title = form.title.data
        topic_variation = form.topic_variation.data
        topic_category = form.topic_category.data
        profile_id = user_profile.id

        # Check if the content idea already exists before adding
        existing_idea = ContentIdea.query.filter_by(title=title, topic_variation=topic_variation, topic_category=topic_category, profile_id=profile_id).first()
        if existing_idea:
            return jsonify({'message': 'Content idea already exists'}), 400

        new_content_idea = ContentIdea(
            title=title,
            topic_variation=topic_variation,
            topic_category=topic_category,
            profile_id=profile_id
        )

        db.session.add(new_content_idea)
        db.session.commit()

        return jsonify({'message': 'Content idea created successfully'}), 201
    else:
        print(form.errors)
        return jsonify({'message': 'Error creating content idea', 'errors': form.errors}), 400
    

@seo.route('/delete_content_idea', methods=['DELETE'])
@auth.login_required
def delete_content_idea():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    form = ContentIdeaDeletionForm()

    if form.validate_on_submit():
        idea_id = form.id.data
        content_idea = ContentIdea.query.filter_by(id=idea_id, profile_id=user_profile.id).first()
        if not content_idea:
            return jsonify({'message': 'Content idea not found'}), 404

        db.session.delete(content_idea)
        db.session.commit()

        return jsonify({'message': 'Content idea deleted successfully'}), 200
    else:
        return jsonify({'message': 'Error deleting content idea', 'errors': form.errors}), 400
    

@seo.route('/get_content_ideas', methods=['GET'])
@auth.login_required
def get_content_ideas():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    content_ideas = ContentIdea.query.filter_by(profile_id=user_profile.id).all()
    schema = ContentIdeaSchema(many=True)
    content_ideas_data = schema.dump(content_ideas)
    return jsonify({'message': 'Content ideas retrieved successfully', 'result': content_ideas_data}), 200


@seo.route('/create_content_outline_task', methods=['POST'])
@auth.login_required
def create_content_outline_task():
    user_profile = Profile.query.filter_by(user_id=get_current_user().id).first()
    form = GenerateContentOutlineForm()

    if form.validate_on_submit():
        title = form.title.data
        target_audience = form.target_audience.data
        wrote_as = form.wrote_as.data
        additional_info = form.additional_info.data
        content_idea_id = form.content_idea_id.data
        delete_content_idea = form.delete_content_idea.data

    else:
        print(form.errors)
        return jsonify({'message': 'Error creating content outline task', 'errors': form.errors}), 400