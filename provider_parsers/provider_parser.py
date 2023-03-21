from abc import ABC ,abstractmethod
from typing import Iterator, List, Optional
from typing import Dict

import requests
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
    def __init__(self,title: str,link: str,is_tv: bool,poster_url: str,film_info: Optional["FilmInfo"] = None,extra: Optional[str] = None,poster_data: Optional[bytes] = None) -> None:
        self.title: str = title
        self.link: str = link
        self.is_tv: bool = is_tv
        self.poster_url: str = poster_url
        self.poster_data: Optional[bytes ] = poster_data
        self.film_info: Optional[FilmInfo] = film_info
        self.extra: Optional[str] = extra


class FilmInfo:
    def __init__(self,title: str,release: str,description: str,genre: str, country: str, duration: str,recommendation: List[Film]) -> None:
        self.title: str = title
        self.release: str = release
        self.description: str = description
        self.genre: str = genre
        self.country: str = country
        self.duration: str = duration
        self.recommendation: List[Film] = recommendation

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
    session: requests.Session = requests.session()
    categories: List[str] = []
    home_categories: List[str] = []
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
    def parse_search(query: str,filter: Optional[Filter] = None,fetch_image: bool = True) -> Iterator[Film]:
        pass

    @staticmethod
    @abstractmethod
    def parse_info(url: str) -> FilmInfo:
        pass
    @staticmethod
    @abstractmethod
    def parse_category(category: str,fetch_image: bool = False) ->Iterator[Film]:
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


