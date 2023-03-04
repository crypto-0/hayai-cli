import pathlib
import unittest

import httpx
from hayai_cli.downloader.handle import handle_download

class TestDownloader(unittest.TestCase):

    def test_handle_download(self):
        with httpx.Client(timeout=15) as client:
            url: str = "https://devstreaming-cdn.apple.com/videos/streaming/examples/img_bipbop_adv_example_ts/master.m3u8"
            url = "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.mp4/.m3u8"
            #url = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
            path = pathlib.Path("/home/tae/videos/test")
            print(str(path))
            name = "test"
            handle_download(client,url,None,path,name)
