from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass(frozen=True)
class Video:
    url: str = ""
    is_m3u8: bool = False

@dataclass(frozen=True)
class Subtitle:
    language: str = ""
    link: str = ""



@dataclass(frozen=True)
class VideoContainer:
    videos: List[Video] = field(default_factory=list)
    subtitles: List[Subtitle] = field(default_factory=list)

class VideoExtractor(ABC):
    _headers: Dict =  {
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.142 Safari/537.36',
     'X-Requested-With': 'XMLHttpRequest'
     }

    def __init__(self,source_base_url: str) -> None:
        self._sources_base_url: str = source_base_url

    @abstractmethod
    def extract(self,embed: str) -> VideoContainer:
        raise NotImplemented

