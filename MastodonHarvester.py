from mastodon import Mastodon, MastodonNotFoundError, MastodonRatelimitError, StreamListener
import csv, os, time, json

m = Mastodon(
        api_base_url=f'https://mastodon.social/home',
        access_token='LxfzUD6zKcJm_Pftu584QdAf5h-liNsyLYmxAvW3OQM'
    )

class Listener(StreamListener):
    def on_update(self, status):
        print(json.dumps(status, indent=2, sort_keys=True, default=str))

m.stream_public(Listener())

