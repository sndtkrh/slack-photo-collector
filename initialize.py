import requests
import json

def init_slack_oauth_token():
    print("Input your Slack Bot User OAuth Access Token: ", end="")
    slack_oauth = input()
    return slack_oauth

def init_google_photo_oauth_token():
    print("Input your Google Photo Client ID: ", end="")
    google_client_id = input()
    print("Input your Google Photo Client Secret: ", end="")
    google_client_secret = input()
    print("Please open following URL by your browser:")
    scope = "https://www.googleapis.com/auth/photoslibrary.sharing"
    redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    print("https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=" + google_client_id
          + "&redirect_uri=" + redirect_uri
          + "&scope=" + scope
          + "&access_type=offline")
    print("Input your authorizarion code given by above url: ", end="")
    google_auth_code = input()
    data = {
        'code': google_auth_code,
        'client_id': google_client_id,
        'client_secret': google_client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'access_type': 'offline'
    }
    response = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data)
    print(response.text)
    google_refresh_token = response.json()["refresh_token"]
    google_access_token = response.json()["access_token"]
    return (google_client_id, google_client_secret, google_auth_code, google_refresh_token, google_access_token)

def make_album(access_token):
    print("Input new Google Photo album name: ", end="")
    title = input()
    data = { "album": { "title": title } }
    albuminfo = requests.post("https://photoslibrary.googleapis.com/v1/albums",
                              headers={
                                  "Content-type": "application/json",
                                  "Authorization": "Bearer %s" % access_token
                              },
                              data=json.dumps(data)).json()
    data = {
        "sharedAlbumOptions": {
            "isCollaborative": "true",
            "isCommentable": "true"
        }
    }
    r = requests.post("https://photoslibrary.googleapis.com/v1/albums/" + albuminfo['id'] + ":share",
                      headers={
                          "Content-type": "application/json",
                          "Authorization": "Bearer %s" % access_token
                      },
                      data=json.dumps(data)).json()
    return albuminfo['id']
    
if __name__ == "__main__":
    slack_api_token = init_slack_oauth_token()
    (google_client_id,
     google_client_secret,
     google_auth_code,
     google_refresh_token,
     google_access_token) = init_google_photo_oauth_token()
    album_id = make_album(google_access_token)
    token = {
        "slack": { "api_token": slack_api_token },
        "google": {
            "album_id": album_id,
            "auth_code": google_auth_code,
            "client_id": google_client_id,
            "client_secret": google_client_secret,
            "refresh_token": google_refresh_token
        }
    }
    with open('token.json', 'w') as tokenfile:
        json.dump(token, tokenfile)
