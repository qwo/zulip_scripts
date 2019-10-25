
#!/usr/bin/env python3

import zulip
import pandas from pd 
from datetime import datetime
ZULIP_KEY=""
ZULIP_EMAIL = "stanley@zheng.nyc"
ZULIP_SITE = "https://recurse.zulipchat.com/"
WRITE_PATH = '/content/drive/My Drive/zulip/oct_25_2019.csv'
client = zulip.Client(email= ZULIP_EMAIL,
                      api_key=ZULIP_KEY, site=ZULIP_SITE)


def get_streams():
    return client.get_streams(include_public=True)['streams']


def get_topics_in_stream(streams):
    TOPICS = {}
    # counter = 0

    for s in streams:
        stream_id = s['stream_id']
        name = s['name']
        id = (stream_id, name)
        TOPICS[id] = client.get_stream_topics(stream_id)
#       if counter == 10:
#          break
#       else:
#          counter += 1
    return TOPICS


def last_message(topic):
    request = {
        'use_first_unread_anchor': True,
        'num_before': 3,
        'num_after': 0,
    }

    request = {
        'use_first_unread_anchor': True,
        'num_before': 1,
        'num_after': 0,
        'narrow': [
            {'operator': 'stream', 'operand': topic[1]}
        ],
        'client_gravatar': True,
        'apply_markdown': True
    }  # type: Dict[str, Any]

    result = client.get_messages(request)
    return result


if __name__ == "__main__":
    last = []
    for t in get_topics_in_stream(get_streams()):
        print(t)
        topic = last_message(t)
        if topic.get('messages') == None:
            meta = (*t, None)
            last.append(meta)
            continue
        for m in topic['messages']:
            time = m['timestamp']
            dt = datetime.fromtimestamp(time)
            meta = (*t, dt)
            last.append(meta)
    df = pd.DataFrame(last)
    df.to_csv(WRITE_PATH)
