
import unittest
from provider_parsers.extractors import UpCloud
from provider_parsers.extractors  import VideoContainer
import requests

class TestUpcloud(unittest.TestCase):

    def test_extract(self):
        r: requests.Response = requests.get("https://solarmovie.pe/ajax/get_link/9179590")
        embed: str = r.json()["link"].rsplit("/")[-1]
        container: VideoContainer = UpCloud.extract(embed=embed)
        self.assertIsNotNone(container)
        self.assertIsNotNone(container.videos)
        self.assertIsNotNone(container.subtitles)
        self.assertGreater(len(container.videos),0)
        self.assertGreater(len(container.subtitles),0)
        self.assertTrue(container.videos[0].url.endswith("m3u8"))
        self.assertTrue(container.subtitles[0].link.endswith(".vtt"))
