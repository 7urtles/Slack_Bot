# Slack_Assignment_Bot

NOTE: Included geckodriver is compiled for arm (M1 Compatable)

This bot is a two part application:
1. Web scraper
2. Slack App (channel posts, scraper, backup)

Given login credentials for a populi student account..

On first run the web scraper will log to a populi student account with provided credentials.
It will then gather all existing assignments along with their links, and pass those to the slack-bot which
in turn will post them in a specified group chat channel.

The web scraper will continue to run and check to see if a new assignment has been posted.
If so the assignment name and link will again be forwarded to the slack-bot and posted in the channel.


Slack_Bot can:
 - Post to channels at specific times
 - Scrape user/channel/chat data from slacks api
 - Backup any found data to a db
 - Delete user chats & messages

