from mastodon import Mastodon
import webbrowser

INSTANCE = "https://mastodon.social"
SCOPES = ["read", "write"]

mastodon = Mastodon(
    client_id="clientcred.secret",
    api_base_url=INSTANCE
)

url = mastodon.auth_request_url(scopes=["read", "write"])
print("Open this URL in your browser:\n", url)
webbrowser.open(url)

code = input("Paste the authorization code: ").strip()

mastodon.log_in(
    code=code,
    scopes=SCOPES,
    to_file="usercred.secret"
)

print("Login complete.")
