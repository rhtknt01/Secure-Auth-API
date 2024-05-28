import requests

# Assuming you're making a login request
url = 'http://127.0.0.1:8000/api/auth/login/'

# Assuming your login data is in JSON format
login_data = {
    'email': 'ganesh@gmail.com',
    'password': 'myname'
}

# Making a POST request to login
login_response = requests.post(url, json=login_data)
# print(response.cookies)

# Assuming you're trying to access the user profile after login
profile_url = 'http://127.0.0.1:8000/api/auth/profile/'

# Extracting cookies from the login response
cookies = login_response.cookies

# # Assuming you have obtained the access token from the login response
# access_token = login_response.json().get('tokens', {}).get('access')
# refresh_token = login_response.json().get('tokens',{}).get('refresh')

access_token = cookies.get('access_token')
refresh_token = cookies.get('refresh_token')

print(refresh_token, access_token)
# Constructing the Authorization header
headers = {'Authorization': f'Bearer {access_token}'}
print(headers)
# print(cookies)
# Assuming you're trying to access the user profile after login
refresh_token_url = 'http://127.0.0.1:8000/api/auth/token/refresh/'
# Making a GET request to access user profile with cookies and Authorization header
profile_response = requests.get(profile_url, headers=headers)

if profile_response.status_code == 200:
    print('login success')

if profile_response.status_code == 401:
    requests.get(refresh_token_url, json={'refresh':refresh_token})
