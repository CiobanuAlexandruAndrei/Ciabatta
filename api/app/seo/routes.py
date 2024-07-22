import os
import json
import openai
from openai import OpenAI
from flask import request, jsonify
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

        prompt = f'give me 10 semantically relevant but unique topics under the main category of {topic}, and for each, give me 10 different variations of the topic that each address a different search intent. Make it in table format with the following columns: column 1: The unique semantically related topic, column the different variations on it, column 3: an intriguing, clickbait style title.\n\nAdditional instructions: {additional_instructions}'
        client = OpenAI()
        openai_response = client.chat.completions.create(
            model='gpt-4o-mini',
            response_format={"type":"json_object"},
            messages=[
                {"role":"system","content":"Provide output in valid JSON. The data schema should be like this: "+json.dumps(example_json)},
                {"role":"user","content":prompt}
            ]
        )

        topics = openai_response.choices[0].message.content
        cost = openai_api_calculate_cost(openai_response.usage)
        generated_topics = json.loads(topics)

        api_name = "OpenAI"
        api_used = APIUsed.query.filter_by(name=api_name).first()
        if not api_used:
            api_used = APIUsed(name=api_name)
            db.session.add(api_used)
            db.session.commit()

        cost_record = APICostRecord(cost=cost, api_used_name=api_used.name)
        db.session.add(cost_record)
        db.session.commit()
        
        return jsonify({'message': 'Topics generated', 'result': generated_topics}), 200
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

        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Initialize an empty DataFrame for grouped data
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

        # Prepare the response data
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
                'call_counts': api_data['timestamp'].tolist()  # This line adds the call count
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

