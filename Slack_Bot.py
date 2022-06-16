slack_token = 'your-token-here'
import slack
from Populi_Crawler import Populi_Bot
import multiprocessing as mp
import time 
import os
from selenium import webdriver
from datetime import date


username = 'your-user-name'
password = 'your-password'
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
week_days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

class Slack_Bot():
    def __init__(self) -> None:
        self.client = slack.WebClient(slack_token)
        pass
    # Calls the Populi bot to potentially post new assignement
    def post_new_assignemnt(self):
        
        try:
            # print('Checking for assignments')
            # Call the Populi_Bot to check for assignments
            latest_assignment_title,latest_assignemt_link = Populi_Bot.assignment_checker(username,password,options)
            # Construct the message for posting
            message = f'{latest_assignment_title} --> {latest_assignemt_link}'
            # Post the message
            self.client.chat_postMessage(channel='channel-code-here', text=message)
            # print('New assignment posted')

        # If no new assignment was noticed
        except:
            # print('No new assignments')
            pass


    # Calls the Populi bot to potentially post zoom link for class
    def post_zoom_link(self):
        # try:
        zoom_link = Populi_Bot.todays_zoom_link(username,password,options)
        if zoom_link == None:
            return
        # Post the message
        message = f'Class Link: {zoom_link}'
        # print(message)
        self.client.chat_postMessage(channel='channel-code-here', text=message)

    def delete_messages(self):
        # The ts of the message you want to delete
        message_id = "12345.9876"
        # The ID of the channel that contains the message
        channel_id = "C12345"

        try:
            # Call the chat.chatDelete method using the built-in WebClient
            result = self.client.chat_delete(
                channel=channel_id,
                ts=message_id
            )
            logger.info(result)

        except SlackApiError as e:
            logger.error(f"Error deleting message: {e}")


    def assignment_grabber(self):
        """
        Infinite loop ok? Will sleep until it's daytime or a weekday,
        Then checks for new assignments every minute
        """
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
                if  current_hour_of_day >= 9 and current_hour_of_day < 22: 
                    # seleniuming for the days class link
                    link_process = mp.Process(target=post_zoom_link())
                    # run worker in a subprocess
                    link_process.start()
                    # make the main process wait for worker to end
                    link_process.join()
                    # Free up memory from the instance
                    os.system('pkill firefox')
                    # seleniuming for new assignments
                    assignment_process = mp.Process(target=post_new_assignemnt())
                    # run `worker` in a subprocess
                    assignment_process.start()
                    # make the main process wait for `worker` to end
                    assignment_process.join()
                    # Free up memory from the instance
                    os.system('pkill firefox')
                else:
                    time.sleep(600)
            else:
                time.sleep(3600)
                
bot = Slack_Bot()
bot.assignment_grabber()

        
    
