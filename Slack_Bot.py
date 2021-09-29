slack_token = 'xoxb-2470203358324-2551145549889-kkOPq1COylop2HP7V2GDKqLA'
import slack
from Populi_Crawler import Populi_Bot
import multiprocessing as mp
import time 
import os
from selenium import webdriver
from datetime import date


username = 'charles.parmley@codeimmersives.com'
password = 'earthday19!@'
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
week_days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]


# Calls the Populi bot to potentially post new assignement
def post_new_assignemnt():
    client = slack.WebClient(slack_token)
    try:
        # print('Checking for assignments')
        # Call the Populi_Bot to check for assignments
        latest_assignment_title,latest_assignemt_link = Populi_Bot.assignment_checker(username,password,options)
        # Construct the message for posting
        message = f'{latest_assignment_title} --> {latest_assignemt_link}'
        # Post the message
        client.chat_postMessage(channel='#bot_testing', text=message)
        # print('New assignment posted')

    # If no new assignment was noticed
    except:
        # print('No new assignments')
        pass
    
    




# Calls the Populi bot to potentially post zoom link for class
def post_zoom_link():
    client = slack.WebClient(slack_token)
    # try:
    zoom_link = Populi_Bot.todays_zoom_link(username,password,options)
    if zoom_link == None:
        return
    # Post the message
    message = f'Class Link: {zoom_link}'
    # print(message)
    client.chat_postMessage(channel='#bot_testing', text=message)


# Main loop for the app
while True:

    # Get day of the week
    today = date.today()
    week_day=today.weekday()
    week_day_sring = week_days[week_day]
    # Retrieve the hour of the day
    current_hour_of_day = int(time.strftime("%H"))
    
    # If it is Monday-Thursday
    if week_day_sring != 'Friday' or week_day_sring != 'Saturday' or week_day_sring != 'Sunday':
        # And the time is between 9pm and 4pm
        if  current_hour_of_day >= 9 and current_hour_of_day < 16: 

            link_process = mp.Process(target=post_zoom_link())
            # run `worker` in a subprocess
            link_process.start()
            # make the main process wait for `worker` to end
            link_process.join()
            # Free up memory from the instance
            os.system('pkill firefox')

            assignment_process = mp.Process(target=post_new_assignemnt())
            # run `worker` in a subprocess
            assignment_process.start()
            # make the main process wait for `worker` to end
            assignment_process.join()
            # Free up memory from the instance
            os.system('pkill firefox')


        
    
