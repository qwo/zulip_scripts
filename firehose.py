from __future__ import print_function
import os
import re
import zulip


from dotenv import load_dotenv

load_dotenv()

from typing import Any, Dict

ZULIP_EMAIL = os.getenv("ZULIP_EMAIL")
ZULIP_KEY = os.getenv("ZULIP_KEY")
ZULIP_SITE = os.getenv("ZULIP_SITE")

# TO_STREAM = "firehose"
# TO_STREAM = "test-stream"

client = zulip.Client(email=ZULIP_EMAIL, api_key=ZULIP_KEY, site=ZULIP_SITE)


last_sent = {}


def print_message(message):
    # type: (Dict[str, Any]) -> None
    print(message)
    send_message(message)


def narrow_link(REALM_STREAM, stream_id, stream_name, topic, near):
    """
    https://recurse.zulipchat.com/#narrow/stream/102312-consciousness/topic/Stanley.20Zheng
    {REALM_STREAM}/{stream-id}-{stream-name}/topic/{topic}
    """
    REALM_STREAM = "https://recurse.zulipchat.com/#narrow"
    stream_name = re.sub(r"\W+", "-", stream_name)
    topic = topic
    url = "{REALM_STREAM}/stream/{stream_id}-{stream_name}/topic/{topic}/near/{near}".format(
        REALM_STREAM=REALM_STREAM,
        stream_id=stream_id,
        stream_name=stream_name,
        topic=topic,
        near=near,
    )
    return url


def send_message(message):
    """
    Send messages to test stream
    """

    PRIVATE = message.get("type") == "private"
    FROM_STREAM = message.get("display_recipient")
    stream_topic_hash = "{display_recipient}>{subject}"

    narrow = narrow_link(
        "",
        message.get("stream_id"),
        FROM_STREAM,
        message.get("subject"),
        message.get("id"),
    )

    content = "In topic: #**{subject}** from **{sender_full_name}**. #**{display_recipient}>{subject}**. [deeplink]({narrow}) ".format(
        narrow=narrow, **message
    )

    # content2 = " #**{display_recipient}>{subject}**.  from **{sender_full_name}**. [deeplink]({narrow}) ".format(
    #     narrow=narrow, **message
    # )

    if last_sent.get(stream_topic_hash):
        return

    request = {
        "type": "stream",
        "to": TO_STREAM,
        "subject": FROM_STREAM,
        "content": content,
    }

    if TO_STREAM != FROM_STREAM and not PRIVATE:

        client.send_message(request)
        last_sent[stream_topic_hash] = True


# This is a blocking call, and will continuously poll for new messages

if __name__ == "__main__":

    client.call_on_each_message(print_message)
