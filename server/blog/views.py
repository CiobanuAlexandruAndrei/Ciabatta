import base64
import hmac
import hashlib
import time
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
import os
import json
import openai
from openai import OpenAI

from .models import *
from .forms import *
from .serializers import *
from blog.libs.data_client import RestClient
from blog.libs.keyword_suggestions import generate_keyword_suggestions

load_dotenv()

MOZ_ACCESS_TOKEN = os.getenv('MOZ_ACCESS_TOKEN')
DATAFORSEO_USERNAME = os.getenv('DATAFORSEO_USERNAME')
DATAFORSEO_PASSWORD = os.getenv('DATAFORSEO_PASSWORD')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_keyword(request):
    user_profile = Profile.objects.get(user=request.user)

    form = KeywordSearchForm(request.POST)
    if form.is_valid():
        keyword = form.cleaned_data['name']
        country = form.cleaned_data['country']
        
        try:
            stored_keyword = KeywordData.objects.get(name=keyword, country=country)
        except KeywordData.DoesNotExist:
            stored_keyword = None

        if stored_keyword:
            return Response({'message': 'Keywords found', 'result': json.loads(stored_keyword.json)}, status=status.HTTP_200_OK)
        else:
            client = RestClient(DATAFORSEO_USERNAME, DATAFORSEO_PASSWORD)
            post_data = dict()

            post_data[len(post_data)] = dict(
                keyword=keyword,
                location_name=country,
                language_name="English",
                limit=10,
                include_serp_info=True,
                include_seed_keyword=True,
            )

            response = client.post("/v3/dataforseo_labs/google/keyword_suggestions/live", post_data)

            if response.get("status_code") == 20000:
                if response.get('tasks') and response['tasks'][0].get('result'):
                    results = response['tasks'][0]['result'][0].get('items', [])
                    
                    for result_dict in results:
                        trend = 'none'
                        monthly_searches = result_dict['keyword_info'].get('monthly_searches', [])
                        if monthly_searches and len(monthly_searches) > 1:
                            last_month_search_volume = monthly_searches[0]['search_volume']
                            current_search_volume = result_dict['keyword_info']['search_volume']
                            if last_month_search_volume > current_search_volume:
                                trend = 'DOWN'
                            elif last_month_search_volume == current_search_volume:
                                trend = 'SAME'
                            elif last_month_search_volume < current_search_volume:
                                trend = 'UP'
                        
                        result_dict['keyword_info']['trend'] = trend
                        del result_dict['keyword_info']['monthly_searches']
                    
                    saved_keyword = KeywordData(name=keyword, country=country, json=json.dumps(results, indent=4))
                    saved_keyword.save()

                    return Response({'message': 'Keywords found', 'result': results}, status=status.HTTP_200_OK)
                else:
                    print('NO RESULTS!!!!')
                    return Response({'message': 'No results found in the response'}, status=status.HTTP_204_NO_CONTENT)
            else: 
                return Response({'message': 'Error retrieving keywords data', 'details': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message': 'Invalid form data', 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_keyword(request):
    user_profile = Profile.objects.get(user=request.user)

    form = KeywordForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']

        keyword = Keyword(name=name, profile=user_profile)
        keyword.save()

        return Response({'message': 'Keyword saved successfully'}, status=status.HTTP_201_CREATED)
    else:
        print(form.errors)
        return Response({'message': 'Error adding the keyword to the database'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_keywords_clusters(request):
    user_profile = Profile.objects.get(user=request.user)
    clusters = KeywordCluster.objects.filter(profile=user_profile)
    clusters = KeywordClusterSerializer(clusters, many=True)
    return Response({'message': 'Keywords Clusters retrieved successfully', 'clusters': clusters.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_keywords_cluster(request):
    user_profile = Profile.objects.get(user=request.user)

    form = KeywordClusterCreationForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']

        keyword = Keyword(name=name, profile=user_profile)
        keyword.save()

        return Response({'message': 'Keyword saved successfully'}, status=status.HTTP_201_CREATED)
    else:
        print(form.errors)
        return Response({'message': 'Error adding the keyword to the database'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_keyword_suggestions(request):
    user_profile = Profile.objects.get(user=request.user)
    form = KeywordGenerationForm(request.POST)
    if form.is_valid():
        topic = form.cleaned_data['topic']
        intent = form.cleaned_data['intent']
        additional_instructions = form.cleaned_data['additional_instructions']
        
        #print(generate_keyword_suggestions(topic, intent, additional_instructions))
        #generated_keywords = json.loads(generate_keyword_suggestions(topic, intent, additional_instructions), indent=4)
        
        example_json = {
            "keywords": [
                "example keyword 1", "example keyword 2", "example keyword 3"
            ]
        }

        prompt = f'Generate 20 SEO keyword suggestions;\nTopic: {topic};\nSearch Intent:{intent}\nAdditional instructions:{additional_instructions}'
        client = OpenAI()
        openai_response = client.chat.completions.create(
            model='gpt-3.5-turbo-1106',
            response_format={"type":"json_object"},
            messages=[
                {"role":"system","content":"Provide output in valid JSON. The data schema should be like this: "+json.dumps(example_json)},
                {"role":"user","content":prompt}
            ]
        )

        openai_response = openai_response.choices[0].message.content
        generated_keywords = json.loads(openai_response)
        return Response({'message': 'Keywords generated', 'result': generated_keywords}, status=status.HTTP_200_OK)
    else:
        print(form.errors)
        return Response({'message': 'Error generating keywords'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_keyword_to_cluster(request):
#     user_profile = Profile.objects.get(user=request.user)
    
#     form = KeywordForm(request.POST)
#     if form.is_valid():
#         name = form.cleaned_data['name']
#         cluster = None

#         try:
#             cluster = KeywordCluster.objects.get(id=cluster_id, profile=user_profile)
#         except KeywordCluster.DoesNotExist:
#             return Response({'message': 'Keyword cluster not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         if cluster:
#             keyword = Keyword(name=name, profile=user_profile)
#             keyword.save()
        
#             cluster.keywords.add(keyword)
        
#         return Response({'message': 'Keyword added to cluster successfully'}, status=status.HTTP_201_CREATED)
#     else:
#         return Response({'message': 'Error adding keyword to cluster', 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)


