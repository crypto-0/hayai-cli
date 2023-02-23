
import unittest
from hayai_cli.provider_parsers.extractors.vidcloud import Vidcloud
from hayai_cli.provider_parsers.extractors.video_extractor import *
import requests

class TestVidcloud(unittest.TestCase):

    def test_extract(self):
        r: requests.Response = requests.get("https://solarmovie.pe/ajax/get_link/9179407")
        embed: str = r.json()["link"].rsplit("/")[-1]
        container: VideoContainer = Vidcloud.extract(embed=embed)
        self.assertIsNotNone(container)
        self.assertIsNotNone(container.videos)
        self.assertIsNotNone(container.subtitles)
        self.assertGreater(len(container.videos),0)
        self.assertGreater(len(container.subtitles),0)
        self.assertTrue(container.videos[0].url.endswith("m3u8"))
        self.assertTrue(container.subtitles[0].link.endswith(".vtt"))
