from abc import ABC 
from typing import  List
from dataclasses import dataclass, field
import click

@dataclass(frozen=True)
class VideoServer:
    name: str
    server_id: str


@dataclass(frozen=True)
class Episode:
    episode_number: str 
    title: str 
    episode_id: str 


@dataclass(frozen=True)
class Season:
    season_number: str
    season_id: str


@dataclass(frozen=True,eq=True)
class Film:
    title: str
    link: str
    is_tv: bool
    extra: str
    poster_url: str

@dataclass(frozen=True)
class FilmInfo:
    title: str = ""
    release: str = ""
    description: str = ""
    genre: str = ""
    country: str = ""
    duration: str = ""
    recommendation: List[Film] = field(default_factory=list,compare=False,repr=False,hash=False)
    poster_image: bytes = field(default_factory=bytes)

@dataclass(frozen=True)
class PageInfo:
    current_page: int = 1
    last_page: int = 1
    has_next_page: bool = False

@dataclass(frozen=True)
class Page:
    page_info: PageInfo 
    films: List

class Provider(ABC):
    _headers =  {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
            }
    _first_color: str = "cyan"
    _secondary_color: str = "white"


    @staticmethod
    def print_films(films: List[Film]) ->None:
        alternate_color: bool = False
        for idx,film in enumerate(films):
            color = Provider._first_color if alternate_color else Provider._secondary_color
            alternate_color = not alternate_color
            formated_string = "[{idx:^2}] {item_title} ({item_info})".format(idx=idx + 1,item_title=film.title,item_info=film.extra)
            click.secho(formated_string,fg=color)


    @staticmethod
    def print_seasons(seasons: List[Season]) -> None:
        alternate_color: bool = False
        for idx,season in enumerate(seasons):
            color = Provider._first_color if alternate_color else Provider._secondary_color
            alternate_color = not alternate_color
            formated_string = "[{idx:^2}] Season: {season_number}".format(idx=idx + 1,season_number=season.season_number)
            click.secho(formated_string,fg=color)

    @staticmethod
    def print_episodes(episodes: List[Episode]) -> None:
        alternate_color: bool = False
        for idx, episode in enumerate(episodes):
            color = Provider._first_color if alternate_color else Provider._secondary_color
            alternate_color = not alternate_color
            formated_string = "[{idx:^2}] Episode: {episode_number}".format(idx=idx + 1,episode_number=episode.episode_number)
            click.secho(formated_string,fg=color)

