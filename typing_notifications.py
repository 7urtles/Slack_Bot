import slack
slack_token = 'xoxb-2470203358324-2551145549889-SqxHu7XO3mNF5xk2uqslj6q5'
channels = []

kwargs = {
    'files':'https://slack.com/api/files.list',
    'users':'https://slack.com/api/users.list',
    'user_url':'https://slack.com/api/users.info',
    'headers':{'Authorization': 'Bearer %s' % slack_token}
}

