import openai

def generate_keyword_suggestions(topic, intent, additional_instructions):
    openai_response = "BOPI BOPI"
    try:
        # openai_response = openai.Completion.create(
        #     model='gpt-3.5-turbo-1106',
        #     prompt=f'Generate 10 SEO keyword suggestions;\nTopic: {topic};\nSearch Intent:{intent}\nAdditional instructions:{additional_instructions}',
        # )
        print(openai_response)
    except:
        print('error')
    return openai_response
