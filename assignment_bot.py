slack_token = 'xoxb-2470203358324-2551145549889-kkOPq1COylop2HP7V2GDKqLA'
import slack
from Newest_Assignement import Populi_Bot
import multiprocessing as mp
import os


def post_new_assignemnt():
    client = slack.WebClient(slack_token)
    try:
        print('Checking for assignments')
        latest_assignment_title,latest_assignemt_link = Populi_Bot.assignment_checker()
        print('New assignment found')
    except:
        print('No new assignments')
        return
    # Post the message
    message = f'{latest_assignment_title} --> {latest_assignemt_link}'
    client.chat_postMessage(channel='#general', text=message)

while True:
    p = mp.Process(target=post_new_assignemnt())
    # run `worker` in a subprocess
    p.start()
    # make the main process wait for `worker` to end
    p.join()
    # all memory used by the subprocess will be freed to the OS
    os.system('pkill firefox')
    
