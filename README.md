# Slack_Assignment_Bot

This bot is a two part application:
1. Web scraper
2. Slack chat bot

Given login credentials for a populi student account..

On first run the web scraper will log to a populi student account with provided credentials.
It will then gather all existing assignments along with their links, and pass those to the slack-bot which
in turn will post them in a specified group chat channel.

The web scraper will continue to run and check to see if a new assignment has been posted.
If so the assignment name and link will again be forwarded to the slack-bot and posted in the channel.


Additionally provided a zoom link, the slack-bot will post that link to the group channel on
specified days at a specified time.
