import json
import logging
import openai
import os


# get environment variables
DEBUG = os.getenv("DEBUG", False)
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

# set openai api key
openai.api_key = OPENAI_API_KEY

# define logger
log = logging.getLogger()

if DEBUG:
    log.setLevel(logging.DEBUG)


# serverless api python function that makes a call to the openai completion api and returns its output
def generate(event, context):
    log.debug("Received event {}".format(json.dumps(event)))
 
    # default to no prompt
    prompt = None

    # check if body exists and if it contains a prompt
    if 'body' in event:
        body = json.loads(event['body'])
       # if prompt exists assign it to variable
        if 'prompt' in body:
            prompt = body['prompt']

    # abort if prompt does not exist
    if prompt is None:
        return {
            'statusCode': 400,
            'body': json.dumps({ 'message': 'prompt is undefined' })
        }

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    # return the response
    return {
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
        'statusCode': 200,
        'body': json.dumps({ 'completion': response['choices'][0]['text'] })
    }

