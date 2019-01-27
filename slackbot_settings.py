token = {}
with open('token.json') as f:
    token = json.load(f)
API_TOKEN = token['slack']['api_token']
DEFAULT_REPLY = ''
PLUGINS = ['plugins']
