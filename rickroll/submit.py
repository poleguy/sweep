import sys
from mastodon import Mastodon

INSTANCE = "https://mastodon.social"
BOT = "@icepi-zero-bot@wafrn.jcm.re"
MAX_LEN = 500

def split_file_by_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    chunks = []
    current = ""

    for line in lines:
        if len(current) + len(line) > MAX_LEN:
            chunks.append(current.rstrip())
            current = ""
        current += line

    if current.strip():
        chunks.append(current.rstrip())

    return chunks


def main(filename):
    mastodon = Mastodon(
        access_token="usercred.secret",
        api_base_url=INSTANCE
    )

    parts = split_file_by_lines(filename)

    last_id = None

    for i, text in enumerate(parts, 1):
        status = mastodon.status_post(
            f"{BOT} {text}",
            in_reply_to_id=last_id,
            visibility="direct"
        )
        last_id = status["id"]
        print(f"Sent {i}/{len(parts)}")

    # Final summon
    mastodon.status_post(
        f"!ask {BOT}",
        in_reply_to_id=last_id,
        visibility="direct"
    )

    print("✔ Private thread sent to bot.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python thread_post.py yourfile.txt")
        sys.exit(1)

    main(sys.argv[1])
