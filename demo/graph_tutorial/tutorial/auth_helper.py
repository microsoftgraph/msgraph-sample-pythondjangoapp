# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <FirstCodeSnippet>
import yaml
import msal
import os
import time

# This is necessary for testing with non-HTTPS localhost
# Remove this if deploying to production
#os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# This is necessary because Azure does not guarantee
# to return scopes in the same case and order as requested
#os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
#os.environ['OAUTHLIB_IGNORE_SCOPE_CHANGE'] = '1'

# Load the oauth_settings.yml file
stream = open('oauth_settings.yml', 'r')
settings = yaml.load(stream, yaml.SafeLoader)
authorize_url = '{0}{1}'.format(settings['authority'], settings['authorize_endpoint'])
token_url = '{0}{1}'.format(settings['authority'], settings['token_endpoint'])

def get_msal_app():
  # Initialize the MSAL confidential client
  auth_app = msal.ConfidentialClientApplication(
    settings['app_id'],
    authority=settings['authority'],
    client_credential=settings['app_secret'])

  return auth_app

# Method to generate a sign-in flow
def get_sign_in_flow():
  auth_app = get_msal_app()

  return auth_app.initiate_auth_code_flow(
    settings['scopes'],
    redirect_uri=settings['redirect'])

# Method to exchange auth code for access token
def get_token_from_code(flow, query):
  auth_app = get_msal_app()

  return auth_app.acquire_token_by_auth_code_flow(flow, query)
# </FirstCodeSnippet>

# <SecondCodeSnippet>
def store_user(request, user):
  request.session['user'] = {
    'is_authenticated': True,
    'name': user['displayName'],
    'email': user['mail'] if (user['mail'] != None) else user['userPrincipalName'],
    'timeZone': user['mailboxSettings']['timeZone']
  }

def get_token():
  auth_app = get_msal_app()

  accounts = auth_app.get_accounts()
  if accounts:
    print(format(accounts))
    result = auth_app.acquire_token_silent(
      settings['scopes'],
      account=accounts[0])

    print(result)

    return result['access_token']

def remove_user_and_token(request):
  auth_app = get_msal_app()

  if 'user' in request.session:
    del request.session['user']
# </SecondCodeSnippet>
