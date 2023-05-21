import base64
import binascii
import json
import re
from typing import Dict, List

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import requests

from .video_extractor import *

class Multiquality(VideoExtractor):

    def extract(self,embed: str) -> VideoContainer:
        match = re.search(r'id=(.*?)&', embed)
        if match:
            server_id: str = match.group(1)
        else:
            return VideoContainer([],[])


        key = binascii.unhexlify("3933343232313932343333393532343839373532333432393038353835373532")
        iv = binascii.unhexlify("39323632383539323332343335383235")
        aes = AES.new(key, AES.MODE_CBC, iv)
        server_id_padded: bytes = pad(bytes(server_id,"utf-8"),16)
        encrypted_server_id: bytes = aes.encrypt(server_id_padded)
        encrypted_server_id_base64 = base64.b64encode(encrypted_server_id).decode("utf-8")
        url: str = f"{self._sources_base_url}?id={encrypted_server_id_base64}"

        try:
            r: requests.Response = requests.get(url)
            video_info: Dict = r.json()
            data = base64.b64decode(video_info["data"])
            aes = AES.new(key, AES.MODE_CBC, iv)
            decrepted_data = aes.decrypt(data)
            video_info = json.loads(decrepted_data)
            video_sources: List[Dict] = video_info["source"]
            video_sources_bk: List[Dict] = video_info["source_bk"]
            video_tracks: List[Dict] = video_info["track"]
            videos: list[Video] = []
            subtitles: list[Subtitle] = []
            for video_source in video_sources:
                videos.append(Video(video_source["file"],True))
            for video_source in video_sources_bk:
                videos.append(Video(video_source["file"],True))
            for track in video_tracks:
                if(track["kind"] == "thumbnails"):continue
                subtitles.append(Subtitle(track["label"],track["file"]))

            return VideoContainer(videos,subtitles)

        except Exception as e:
            return VideoContainer([],[])
