import sys
from mastodon import Mastodon
import time

INSTANCE = "https://mastodon.social"
BOT = "@icepi-zero-bot@wafrn.jcm.re"
DELAY_SECONDS = 60
MASTODON_LIMIT = 500

# Reserve room for "@bot "
PREFIX = BOT + " "
MAX_LEN = MASTODON_LIMIT - len(PREFIX)

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
            PREFIX + text,
            in_reply_to_id=last_id,
            visibility="direct"
        )
        last_id = status["id"]
        print(f"Sent {i}/{len(parts)}")
        # try to make sure bot doesn't see the ask until all the other messages get there.
        time.sleep(DELAY_SECONDS)


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
