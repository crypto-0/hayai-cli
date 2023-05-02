from .video_extractor import *
from typing import Dict,List
from .utilities import decrypt
import requests
import json

class UpCloud(VideoExtractor):
    _movkey_key_url =  "https://raw.githubusercontent.com/mov-cli/movkey/main/key.txt"
    _rapidclown_key_url = "https://raw.githubusercontent.com/consumet/rapidclown/main/key.txt"
    _enimax_key_url_e4 = "https://raw.githubusercontent.com/enimax-anime/key/e4/key.txt"
    _enimax_key_url_e6 = "https://github.com/enimax-anime/key/raw/e6/key.txt"
    _key_urls = [_movkey_key_url,_rapidclown_key_url,_enimax_key_url_e4,_enimax_key_url_e6]

    def extract(self,embed: str) -> VideoContainer:
        embed = embed.rsplit("/",1)[-1].rsplit("?",1)[0]
        r: requests.Response = requests.get(self._sources_base_url + embed,headers=self._headers)
        video_info: Dict = r.json()
        if(isinstance(video_info.get("sources"), str)):
            decrypted_url = ""
            for key_url in UpCloud._key_urls:
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
        videos: List[Video] = []
        subtitles: List[Subtitle] = []
        for video_source in video_sources:
            videos.append(Video(video_source["file"],True))
        for track in video_tracks:
            if(track["kind"] == "thumbnails"):continue
            subtitles.append(Subtitle(track["label"],track["file"]))
        return VideoContainer(videos,subtitles)
