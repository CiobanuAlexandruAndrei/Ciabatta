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

from .models import *
from .forms import *
from .serializers import *
from blog.libs.data_client import RestClient
from blog.libs.calculate import calculate_keyword_difficulty

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
        
        print(keyword)
        print(country)

        try:
            stored_keyword = KeywordData.objects.get(name=keyword, country=country)
        except Exception as e:
            stored_keyword = None

        if stored_keyword:
            print('Keyword was stored')
            print(stored_keyword.name)
            return Response({'message': 'Keywords found', 'result': json.loads(stored_keyword.json)}, status=status.HTTP_200_OK)
        else:
            client = RestClient(DATAFORSEO_USERNAME, DATAFORSEO_PASSWORD)
            post_data = dict()

            post_data[len(post_data)] = dict(
                keyword=keyword,
                location_name=country,
                language_name="English",
                filters=[
                    ["keyword_data.keyword_info.search_volume", ">", 10]
                ],
                limit=10,
                include_serp_info=True,
                include_seed_keyword=True,

            )

            response = client.post("/v3/dataforseo_labs/google/keyword_suggestions/live", post_data)

            if response["status_code"] == 20000:
                print(response)
                results = response['tasks'][0]['result'][0]['items']
                
                for result_dict in results:
                    trend = 'none'
                    monthly_searches = result_dict['keyword_data'].get('keyword_info', {}).get('monthly_searches', [])
                    if monthly_searches and len(monthly_searches) > 1:
                        last_month_search_volume = monthly_searches[0]['search_volume']
                        if last_month_search_volume > result_dict['keyword_data']['keyword_info']['search_volume']:
                            trend = 'UP'
                        elif last_month_search_volume == result_dict['keyword_data']['keyword_info']['search_volume']:
                            trend = 'SAME'
                        elif last_month_search_volume < result_dict['keyword_data']['keyword_info']['search_volume']:
                            trend = 'DOWN'
                    
                    result_dict['keyword_data']['trend'] = trend
                    del result_dict['keyword_data']['keyword_info']['monthly_searches']
                
                saved_keyword = KeywordData(name=keyword, country=country, json=json.dumps(results, indent=4))
                saved_keyword.save()

                return Response({'message': 'Keywords found', 'result': results}, status=status.HTTP_200_OK)
            else: 
                return Response({'message': 'Error retrieving keywords data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # return Response({'message': 'Keywords found', 'response' : response}, status=status.HTTP_200_OK)
    else:
        print(form.errors)
        return Response({'message': 'Invalid form data'}, status=status.HTTP_400_BAD_REQUEST)
    

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
def get_keywords(request):
    user_profile = Profile.objects.get(user=request.user)
    keywords = Keyword.objects.filter(profile=user_profile)
    keywords = KeywordSerializer(keywords, many=True)
    return Response({'message': 'Keywords retrieved successfully', 'keywords': keywords.data}, status=status.HTTP_200_OK)
