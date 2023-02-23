from .video_extractor import *
from .utilities import decrypt
from typing import Dict,List
import requests
import json

class Vidcloud(VideoExtractor):
    sources_base_url: str = "https://rabbitstream.net/ajax/embed-4/getSources?id="
    headers: Dict =  {
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.142 Safari/537.36',
     'X-Requested-With': 'XMLHttpRequest'
     }
    #dokicloud_url = "https://raw.githubusercontent.com/consumet/rapidclown/dokicloud/key.txt"
    #rabbitstream_url = "https://raw.githubusercontent.com/consumet/rapidclown/rabbitstream/key.txt"
    rabbitstream_url = "https://raw.githubusercontent.com/consumet/rapidclown/main/key.txt"
    @staticmethod
    def extract(embed: str) -> VideoContainer:
        s = requests.Session()
        embed = embed.rsplit("/",1)[-1].rstrip("?z=")
        r: requests.Response = s.get(Vidcloud.sources_base_url + embed,headers=Vidcloud.headers)
        video_info: Dict = r.json()
        if(isinstance(video_info.get("sources"), str)):
            key: str = s.get(Vidcloud.rabbitstream_url).text
            decrypted_url = decrypt.decrypt(video_info["sources"],key)
            video_sources: List[Dict] = json.loads(decrypted_url)
        else:
            video_sources: List[Dict] = video_info["sources"]

        video_tracks: List[Dict] = video_info["tracks"]
        videos: list[Video] = []
        subtitles: list[Subtitle] = []
        for video_source in video_sources:
            videos.append(Video("",True,video_source["file"]))
        for track in video_tracks:
            if(track["kind"] == "thumbnails"):continue
            subtitles.append(Subtitle(track["label"],track["file"]))
        s.close()
        return VideoContainer(videos,subtitles)
