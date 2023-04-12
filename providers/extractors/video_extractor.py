from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

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

    @abstractmethod
    def extract(self,embed: str) -> VideoContainer:
        raise NotImplemented

