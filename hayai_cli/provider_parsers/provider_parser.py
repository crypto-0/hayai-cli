from abc import ABC ,abstractmethod
from typing import List
from typing import Dict
from typing import Union
from .extractors.video_extractor import VideoExtractor
import click


class VideoServer:

    def __init__(self,name: str,embed: str,extractor: type[VideoExtractor]) -> None:
        self.name: str = name
        self.embed: str = embed
        self.extractor: type[VideoExtractor] = extractor


class Episode:
    def __init__(self,episode_number: str,id: str,title: str) -> None:
        self.episode_number: str = episode_number
        self.id: str = id
        self.title: str =title


class Season:
    def __init__(self,season_number: str,id: str) -> None:
        self.season_number: str = season_number
        self.id: str = id


class Film:
    def __init__(self,title: str,link: str,is_tv: bool,extra: str) -> None:
        self.title: str = title
        self.link: str = link
        self.is_tv: bool = is_tv
        self.extra: str = extra


class Info:
    def __init__(self,title: str,release: str,description: str,recommendation: List[Film]) -> None:
        self.title: str = title
        self.release: str = release
        self.description: str = description
        self.recommendation = recommendation

class Filter:
    def __init__(self,type: str, genre: List[str]) -> None:
        self.type: str = type
        self.genre: List[str] = genre
        

class ProviderParser(ABC):
    name : str = ""
    host_url: str = ""
    headers =  {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
            }
    categories: List[str] = []
    genre: Dict[str,str] = {}
    first_color: str = "cyan"
    secondary_color: str = "white"

    @staticmethod
    @abstractmethod
    def parse_seasons(id: str) -> List[Season]:
        pass

    @staticmethod
    @abstractmethod
    def parse_episodes(id: str) -> List[Episode]:
        pass

    @staticmethod
    @abstractmethod
    def parse_movie_servers(id: str) -> List[VideoServer]:
        pass

    @staticmethod
    @abstractmethod
    def parse_episode_servers(id: str) -> List[VideoServer]:
        pass

    @staticmethod
    @abstractmethod
    def parse_search(query: str,filter: Union[Filter,None] = None) -> List[Film]:
        pass

    @staticmethod
    @abstractmethod
    def parse_info(url: str) -> List[Info]:
        pass
    @staticmethod
    @abstractmethod
    def parse_category(category: str) ->List[Film]:
        pass
    @staticmethod
    def print_films(films: List[Film]) ->None:
        alternate_color: bool = False
        for idx,film in enumerate(films):
            color = ProviderParser.first_color if alternate_color else ProviderParser.secondary_color
            alternate_color = not alternate_color
            formated_string = "[{idx:^2}] {item_title} ({item_info})".format(idx=idx + 1,item_title=film.title,item_info=film.extra)
            click.secho(formated_string,fg=color)


    @staticmethod
    def print_seasons(seasons: List[Season]) -> None:
        alternate_color: bool = False
        for idx,season in enumerate(seasons):
            color = ProviderParser.first_color if alternate_color else ProviderParser.secondary_color
            alternate_color = not alternate_color
            formated_string = "[{idx:^2}] Season: {season_number}".format(idx=idx + 1,season_number=season.season_number)
            click.secho(formated_string,fg=color)

    @staticmethod
    def print_episodes(episodes: List[Episode]) -> None:
        alternate_color: bool = False
        for idx, episode in enumerate(episodes):
            color = ProviderParser.first_color if alternate_color else ProviderParser.secondary_color
            alternate_color = not alternate_color
            formated_string = "[{idx:^2}] Episode: {episode_number}".format(idx=idx + 1,episode_number=episode.episode_number)
            click.secho(formated_string,fg=color)


