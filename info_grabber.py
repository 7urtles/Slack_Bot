import requests
import os

slack_token = 'your-token-here'
channels = []

kwargs = {
    'files':'https://slack.com/api/files.list',
    'users':'https://slack.com/api/users.list',
    'user_url':'https://slack.com/api/users.info',
    'headers':{'Authorization': 'Bearer %s' % slack_token}
}

def find_user(files='', users='', user_url='', headers='', user=''):
    response = requests.get(user_url+'?user='+user, headers=headers).json()
    return response['user']['name']

def get_data(files, users, user_url, headers, data_type):
    

    match data_type:
        case 'files':
            response = requests.get(files, headers=headers)
            for i in response.json()['files']:
                download_url= i['url_private']
                file_name = i['name']
                uploader = i['user']
                file_type = i['filetype']
                creation_date = i['created']
                user = find_user(user_url=user_url, headers=headers, user=uploader)
                download = requests.get(download_url, headers=headers)
                download.raise_for_status
                file_data = download.content
                download_name = f"{user}--{creation_date}--{file_name}".replace(" ", "")
                if not os.path.exists(f"files/{file_type}/"):
                    os.makedirs(f"files/{file_type}/")
                with open(f"files/{file_type}/{download_name}" , 'w+b') as new_file:
                    new_file.write(bytearray(file_data))
                    print(f"Saved {download_name}")


        case 'users':
            response = requests.get(users, headers=headers)
            keys = ['real_name','email','image_original','id','team']
            found_users = {}
            for user in response.json()['members']:
                valid_keys=[]
                user_data={}
                for key in keys:
                    if key in user['profile']:
                        valid_keys.append(key)
                        user_data[key] = user['profile'][key]
                    elif key in user:
                        user_data[key] = user[key]
                found_users[user['name']] = user_data
            return found_users

# usable data_type arguments are ['users','files']
# single_user = find_user(**kwargs, user='F02PXBXK8DA')
users = get_data(**kwargs, data_type='users')
files = get_data(**kwargs, data_type='files')
# print(single_user)