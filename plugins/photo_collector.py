import requests
import shutil
import json
from slackbot.bot import listen_to
from slackbot.bot import default_reply

token = {}
with open('token.json') as f:
    token = json.load(f)

@listen_to('(.*)')
def img(message, params):
    if 'files' in message.body:
        data = {
            'refresh_token': token['google']['refresh_token'],
            'client_id': token['google']['client_id'],
            'client_secret': token['google']['client_secret'],
            'grant_type': 'refresh_token'
        }
        authtoken = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data).json()
        for file in message.body['files']:
            if file['filetype'] != 'jpg':
                continue
            # get a file from slack
            url = file['url_private']
            flag = file['filetype']
            tmpfile = '/tmp/' + file['name']
            imagedata = requests.get(url,
                                     headers={'Authorization': 'Bearer %s' % token['slack']['api_token']},
                                     stream=True)
            with open(tmpfile, 'wb') as f:
                shutil.copyfileobj(imagedata.raw, f)

            # upload the file to Google Photo
            # upload image
            headers = {
                'Authorization': 'Bearer %s' % authtoken["access_token"],
                'Content-type': 'application/octet-stream',
                'X-Goog-Upload-File-Name': file['name'],
                'X-Goog-Upload-Protocol': 'raw',
            }
            imagedata = open(tmpfile, 'rb').read()
            uploadToken = requests.post('https://photoslibrary.googleapis.com/v1/uploads',
                                        headers=headers,
                                        data=imagedata)
            print(uploadToken.text)
            uploadinfo = {
                "albumId": token['google']['album_id'],
                "newMediaItems": [{
                    "description": "",
                    "simpleMediaItem": { "uploadToken": uploadToken.text }
                }]
            }
            r = requests.post("https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate",
                              headers={
                                  "Content-type": "application/json",
                                  "Authorization": "Bearer %s" % authtoken["access_token"],
                              },
                              data=json.dumps(uploadinfo))
            print(r.text)

