import os
import logging
import urllib
import calendar
import datetime
import boto3
from botocore.exceptions import ClientError

import re
import unicodedata


# Grab the Bot OAuth token from the environment.
BOT_TOKEN = os.environ["BOT_TOKEN"]
MODEL_NAME = os.environ["MODEL_NAME"]

# Define the URL of the targeted Slack API resource.
# We'll send our replies there.
SLACK_URL = "https://slack.com/api/chat.postMessage"

MAX_LENGTH = 10  # Maximum sentence length to consider
corpus_name = "cornell movie-dialogs corpus"

# Default word tokens
PAD_token = 0  # Used for padding short sentences
SOS_token = 1  # Start-of-sentence token
EOS_token = 2  # End-of-sentence token


def chatbot(input_text):
    s3 = boto3.client('s3')
    
    if os.path.isfile('/tmp/' + MODEL_NAME) != True:
        try:
            s3.download_file('chatbot-mark', 'chatbot-model/' + MODEL_NAME, '/tmp/' + MODEL_NAME)
        except ClientError:
            print('bla')
    
    output_text = input_text
     
    return(output_text)

def timesheet():
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    current_weekday = now.weekday()
    
    day, num_days = calendar.monthrange(current_year, current_month + 1)
    last_day = (day - 1) % 7
    
    if(last_day > 4):
        last_working_day = 4
    else:
        last_working_day = last_day
    
    if(current_weekday == last_working_day):
        print("trigger")

def send(channel_id, text):
    data = urllib.parse.urlencode(
        (
            ("token", BOT_TOKEN),
            ("channel", channel_id),
            ("text", text)
        )
    )
    data = data.encode("ascii")
        
    # Construct the HTTP request that will be sent to the Slack API.
    request = urllib.request.Request(
        SLACK_URL, 
        data=data, 
        method="POST"
    )
    # Add a header mentioning that the text is URL-encoded.
    request.add_header(
        "Content-Type", 
        "application/x-www-form-urlencoded"
    )
        
    # Fire off the request!
    urllib.request.urlopen(request).read()

def lambda_handler(event, context):
    print(event)
    
    if "detail-type" in event:
        if event['detail-type'] == 'Scheduled Event':
            timesheet()
            return("OK")
    
    if "challenge" in event:
        return(event["challenge"])
    
    slack_event = event['event']
    
    # @harry == '<@UF6GEAV2L>'
    print(slack_event)
    
    if "bot_id" in slack_event:
        logging.warn("Ignore bot event")
    else:
        # Get the text of the message the user sent to the bot,
        # and reverse it.
        text = slack_event["text"]
        #reversed_text = 'I do not understand this, ' + text
        bot_text = chatbot(text)
        # Get the ID of the channel where the message was posted.
        channel_id = slack_event["channel"]

        send(channel_id, bot_text)
        
    return "200 OK"