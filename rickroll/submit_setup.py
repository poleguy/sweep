from mastodon import Mastodon

SCOPES = ["read", "write"]

Mastodon.create_app(
    'thread-uploader',
    api_base_url='https://mastodon.social',
    scopes=SCOPES,
    to_file='clientcred.secret'
)

# mastodon = Mastodon(client_id='clientcred.secret')
# mastodon.log_in(
#     'mastodon@poleguy.com',
#     'mastodon8977',
#     to_file='usercred.secret'
# )
