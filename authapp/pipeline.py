import requests

from django.conf import settings


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'github':
        return
    base_url = 'https://api.github.com/users'
    headers = {'Authorization': f'token {response["access_token"]}'}
    api_response = requests.get(f'{base_url}/{user}', headers=headers)

    if api_response.status_code != 200:
        return
    api_json = api_response.json()
    user.shopuserprofile.github_profile = api_json['html_url']
    if api_json['avatar_url']:
        with open(f'{settings.MEDIA_ROOT}/users/{user.pk}.jpg', 'wb') as fout:
            fout.write(requests.get(api_json['avatar_url'], headers=headers).content)
        user.avatar = f'users/{user.pk}.jpg'
    user.save()
