from __future__ import print_function
import os

from dotenv import load_dotenv

load_dotenv()

from typing import Any, Dict

usage = """print-messages [options]
Prints out each message received by the indicated bot or user.
Example: print-messages
Specify your Zulip API credentials and server in a ~/.zuliprc file or using the options.
"""

import zulip

ZULIP_EMAIL = os.getenv("ZULIP_EMAIL")
ZULIP_KEY = os.getenv("ZULIP_KEY")
ZULIP_SITE = os.getenv("ZULIP_SITE")

# parser = zulip.add_default_arguments(argparse.ArgumentParser(usage=usage))
# options = parser.parse_args()

client = zulip.Client(email=ZULIP_EMAIL, api_key=ZULIP_KEY, site=ZULIP_SITE)
# client = zulip.Client(config_file="./zuliprc")
last_sent = {}

def print_message(message):
    # type: (Dict[str, Any]) -> None
    print(message)
    send_message(message)

import re


def narrow_link(REALM_STREAM, stream_id, stream_name, topic):
    """
    https://recurse.zulipchat.com/#narrow/stream/102312-consciousness/topic/Stanley.20Zheng
    {REALM_STREAM}/{stream-id}-{stream-name}/topic/{topic}
    """
    REALM_STREAM = "https://recurse.zulipchat.com/#narrow"
    stream_name = re.sub(r"\W+", "-", stream_name)
    topic = topic
    url = "{REALM_STREAM}/stream/{stream_id}-{stream_name}/topic/{topic}".format(
        REALM_STREAM=REALM_STREAM,
        stream_id=stream_id,
        stream_name=stream_name,
        topic=topic,
    )
    return url


def send_message(message):
    TO_STREAM = "test-stream"
    PRIVATE = message.get("type") == "private"
    FROM_STREAM = message.get("display_recipient")

    narrow = narrow_link(
        "", message.get("stream_id"), FROM_STREAM, message.get("subject")
    )

    content = "in topic:{subject} from {sender_full_name}. [link]({narrow}) ".format(
        narrow=narrow, **message
    )
    if last_sent.get(content):
        return

    request = {
        "type": "stream",
        "to": "test-stream",
        "subject": FROM_STREAM,
        "content": content,
    }
    if TO_STREAM != FROM_STREAM and not PRIVATE:

        client.send_message(request)
        last_sent[content] = True


# This is a blocking call, and will continuously poll for new messages

if __name__ == "__main__":

    client.call_on_each_message(print_message)      

# https://recurse.zulipchat.com/#narrow/stream/101477-virtual-check-in/topic/2019-10-27
