import unittest

from xquik_export import load_xquik_tweets


class XquikExportTests(unittest.TestCase):
    def test_loads_nested_json_tweets(self):
        payload = b'{"data":[{"tweet":"Great launch"},{"text":"Needs docs"}]}'

        tweets = load_xquik_tweets(payload)

        self.assertEqual(tweets, ["Great launch", "Needs docs"])

    def test_loads_jsonl_full_text(self):
        payload = b'{"full_text":"Fast reply"}\n{"content":"Helpful update"}'

        tweets = load_xquik_tweets(payload)

        self.assertEqual(tweets, ["Fast reply", "Helpful update"])

    def test_loads_csv_tweet_text(self):
        payload = b"tweet_text\nClean chart\n"

        tweets = load_xquik_tweets(payload)

        self.assertEqual(tweets, ["Clean chart"])

    def test_skips_blank_rows(self):
        payload = b'[{"tweet":"  "},{"body":"Useful filter"}]'

        tweets = load_xquik_tweets(payload)

        self.assertEqual(tweets, ["Useful filter"])


if __name__ == "__main__":
    unittest.main()
