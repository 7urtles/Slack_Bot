slack_token = 'xoxb-2470203358324-2551145549889-kkOPq1COylop2HP7V2GDKqLA'
import slack
from Newest_Assignement import Populi_Bot

def post_new_assignemnt():
    client = slack.WebClient(slack_token)
    try:
        latest_assignment_title,latest_assignemt_link = Populi_Bot.assignment_checker()
        print('New assignment found')
    except:
        print('No new assignments')
        return

    message = f'{latest_assignment_title} --> {latest_assignemt_link}'
    client.chat_postMessage(channel='#bot_testing', text=message)

while True:
    post_new_assignemnt()
