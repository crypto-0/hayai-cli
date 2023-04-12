from .video_extractor import *
from .utilities import decrypt
from typing import Dict,List
import requests
import json

class Vidcloud(VideoExtractor):
    _sources_base_url: str = "https://rabbitstream.net/ajax/embed-4/getSources?id="
    _headers: Dict =  {
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.142 Safari/537.36',
     'X-Requested-With': 'XMLHttpRequest'
     }
    _movkey_key_url =  "https://raw.githubusercontent.com/mov-cli/movkey/main/key.txt"
    _rapidclown_key_url = "https://raw.githubusercontent.com/consumet/rapidclown/main/key.txt"
    _enimax_key_url = "https://raw.githubusercontent.com/enimax-anime/key/e4/key.txt"
    _key_urls = [_movkey_key_url,_rapidclown_key_url,_enimax_key_url]

    def extract(self,embed: str) -> VideoContainer:
        embed = embed.rsplit("/",1)[-1].rstrip("?z=")
        r: requests.Response = requests.get(Vidcloud._sources_base_url + embed,headers=Vidcloud._headers)
        video_info: Dict = r.json()
        if(isinstance(video_info.get("sources"), str)):
            decrypted_url = ""
            for key_url in Vidcloud._key_urls:
                key: str = requests.get(key_url).text
                decrypted_url = decrypt.decrypt(video_info["sources"],key)
                if(decrypted_url.endswith("hls\"}]")):
                    break
                else:
                    decrypted_url = ""

            if not decrypted_url:
                return VideoContainer([],[])
            video_sources: List[Dict] = json.loads(decrypted_url)
        else:
            video_sources: List[Dict] = video_info["sources"]

        video_tracks: List[Dict] = video_info["tracks"]
        videos: list[Video] = []
        subtitles: list[Subtitle] = []
        for video_source in video_sources:
            videos.append(Video(video_source["file"],True))
        for track in video_tracks:
            if(track["kind"] == "thumbnails"):continue
            subtitles.append(Subtitle(track["label"],track["file"]))

        return VideoContainer(videos,subtitles)
