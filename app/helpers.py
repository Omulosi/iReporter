def make_token_header(token):
    """
    creates an authorization header given a
    token
    """
    return {'Authorization': 'Bearer {}'.format(token)}