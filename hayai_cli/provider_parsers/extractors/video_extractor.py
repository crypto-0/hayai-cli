from abc import ABC, abstractmethod
from typing import List

class Video:

    def __init__(self,quality: str,is_m3u8: bool,url: str) -> None:
        self.quality: str = quality
        self.is_m3u8: bool = is_m3u8
        self.url: str = url


class Subtitle:

    def __init__(self,language: str,link: str,sdh: bool = False,forced: bool = False) -> None:
        self.language: str = language
        self.link: str = link
        self.sdh = sdh
        self.forced = forced
        

class VideoContainer:

    def __init__(self,videos: List[Video],subtitles: List[Subtitle]) -> None:
        self.videos: List[Video] = videos
        self.subtitles: List[Subtitle] = subtitles


class VideoExtractor(ABC):

    @staticmethod
    @abstractmethod
    def extract(embed: str) -> VideoContainer:
        pass


