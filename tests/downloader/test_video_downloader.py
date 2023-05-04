import pathlib
import unittest
from hayai_cli.downloader.video_downloader import VideoDownloader

class TestVideoDownloader(unittest.TestCase):

    def test_downloading_hls(self):
        video_downloader: VideoDownloader = VideoDownloader()
        url = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
        base_path = pathlib.Path("/home/tae/videos/test")
        video_downloader.download_video(url,"720",str(base_path),"test with spaces")
        video_downloader.close_session()
        
