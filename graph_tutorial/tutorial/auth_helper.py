# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import yaml
import msal

# Load the oauth_settings.yml file
stream = open('oauth_settings.yml', 'r', encoding='utf8')
settings = yaml.load(stream, yaml.SafeLoader)

def load_cache(request):
    # Check for a token cache in the session
    cache = msal.SerializableTokenCache()
    if request.session.get('token_cache'):
        cache.deserialize(request.session['token_cache'])

    return cache

def save_cache(request, cache):
    # If cache has changed, persist back to session
    if cache.has_state_changed:
        request.session['token_cache'] = cache.serialize()

def get_msal_app(cache=None):
    # Initialize the MSAL confidential client
    auth_app = msal.ConfidentialClientApplication(
        settings['app_id'],
        authority=settings['authority'],
        client_credential=settings['app_secret'],
        token_cache=cache)

    return auth_app

# Method to generate a sign-in flow
def get_sign_in_flow():
    auth_app = get_msal_app()

    return auth_app.initiate_auth_code_flow(
        settings['scopes'],
        redirect_uri=settings['redirect'])

# Method to exchange auth code for access token
def get_token_from_code(request):
    cache = load_cache(request)
    auth_app = get_msal_app(cache)

    # Get the flow saved in session
    flow = request.session.pop('auth_flow', {})

    result = auth_app.acquire_token_by_auth_code_flow(flow, request.GET)
    save_cache(request, cache)

    return result

def store_user(request, user):
    time_zone = 'UTC'
    if 'timeZone' in user['mailboxSettings']:
        time_zone = user['mailboxSettings']['timeZone']

    request.session['user'] = {
        'is_authenticated': True,
        'name': user['displayName'],
        'email': user['mail'] if (user['mail'] is not None) else user['userPrincipalName'],
        'timeZone': time_zone
    }

def get_token(request):
    cache = load_cache(request)
    auth_app = get_msal_app(cache)

    accounts = auth_app.get_accounts()
    if accounts:
        result = auth_app.acquire_token_silent(
            settings['scopes'],
            account=accounts[0])

        save_cache(request, cache)

        return result['access_token'] if result is not None else None

def remove_user_and_token(request):
    if 'token_cache' in request.session:
        del request.session['token_cache']

    if 'user' in request.session:
        del request.session['user']
