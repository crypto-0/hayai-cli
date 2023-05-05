from abc import ABC, abstractmethod
from concurrent.futures import Future, ThreadPoolExecutor, wait
import pathlib 
from typing import  Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import click
import sys

from hayai_cli.providers.extractors.video_extractor import VideoContainer
from ..downloader import VideoDownloader

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
    film_type: str
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
    _prompt_color: str = "yellow"
    _progress_color: str = "green"
    _video_downloader: VideoDownloader = VideoDownloader()

    @abstractmethod
    def load_seasons(self,film_id: str) -> List[Season]:
        pass

    @abstractmethod
    def load_episodes(self,season_id: str) -> List[Episode]:
        pass

    @abstractmethod
    def load_movie_servers(self,movie_id: str) -> List[VideoServer]:
        pass

    @abstractmethod
    def load_episode_servers(self,episode_id: str) -> List[VideoServer]:
        pass

    @abstractmethod
    def load_video(self,server: VideoServer) -> VideoContainer:
        pass

    @abstractmethod
    def load_film_info(self,url: str) -> FilmInfo:
        pass

    def print_films(self,films: List[Film]) ->None:
        alternate_color: bool = False
        for idx,film in enumerate(films):
            color = Provider._first_color if alternate_color else Provider._secondary_color
            alternate_color = not alternate_color
            formated_string = "[{idx:^2}] {item_title} ({item_info})".format(idx=idx + 1,item_title=film.title,item_info=film.extra)
            click.secho(formated_string,fg=color)


    def print_seasons(self,seasons: List[Season]) -> None:
        alternate_color: bool = False
        for idx,season in enumerate(seasons):
            color = Provider._first_color if alternate_color else Provider._secondary_color
            alternate_color = not alternate_color
            formated_string = "[{idx:^2}] Season: {season_number}".format(idx=idx + 1,season_number=season.season_number)
            click.secho(formated_string,fg=color)

    def print_episodes(self,episodes: List[Episode]) -> None:
        alternate_color: bool = False
        for idx, episode in enumerate(episodes):
            color = Provider._first_color if alternate_color else Provider._secondary_color
            alternate_color = not alternate_color
            formated_string = "[{idx:^2}] Episode: {episode_number}".format(idx=idx + 1,episode_number=episode.episode_number)
            click.secho(formated_string,fg=color)

    def print_servers(self,servers: List[VideoServer]) -> None:
        alternate_color: bool = False
        for idx, server in enumerate(servers):
            color = Provider._first_color if alternate_color else Provider._secondary_color
            alternate_color = not alternate_color
            formated_string = "[{idx:^2}] Server: {server_name}".format(idx=idx + 1,server_name=server.name)
            click.secho(formated_string,fg=color)

    def display(self,films: List[Film],mode: str,download_dir: str,quality: str):
        selected_season: Optional[int] = None

        if len(films) == 0:
            click.secho("No films were found",fg="red")
            sys.exit()
        self.print_films(films)
        film_index = click.prompt(click.style("Enter a number",fg=self._prompt_color),type=click.IntRange(1,len(films)))
        param_id: str = (films[film_index -1].link).rsplit("-",1)[-1]
        if films[film_index - 1].film_type == "tv":
            click.secho("Getting seasons...",fg=self._progress_color)
            seasons = self.load_seasons(param_id)
            if len(seasons) == 0:
                click.echo(click.style("No seasons were found",fg="red"))
                sys.exit()
            self.print_seasons(seasons=seasons)
            season_index = click.prompt(click.style("Select a Season",fg=self._prompt_color),type=click.IntRange(1,len(seasons)))
            selected_season = season_index
            param_id = seasons[season_index - 1].season_id
        if films[film_index -1].film_type == "tv" or films[film_index -1].film_type == "anime":
            click.secho("Getting episodes...",fg=self._progress_color)
            episodes = self.load_episodes(param_id)
            if len(episodes) == 0:
                click.echo(click.style("No episodes were found",fg="red"))
                sys.exit()

            self.print_episodes(episodes=episodes)
            episode_ranges: List[Tuple[int,int]] = []
            while True:
                min_episode = click.prompt(click.style("Select min episode",fg=self._prompt_color),type=click.IntRange(1,len(episodes)),default=1)
                max_episode = click.prompt(click.style("Select max episode",fg=self._prompt_color),type=click.IntRange(1,len(episodes)),default=len(episodes))
                episode_ranges.append((min_episode,max_episode))
                if(not click.confirm(click.style("Add more episodes ",fg=self._prompt_color))):break

            click.secho("Getting episode servers...",fg=self._progress_color)
            episode_servers: Dict[int,List[VideoServer]] = {}
            for episode_range in episode_ranges:
               for idx in range(episode_range[0],episode_range[1] + 1):
                   if(episode_servers.get(idx) !=None):continue
                   servers = self.load_episode_servers(episodes[idx -1].episode_id)
                   episode_servers[idx] = servers
            
            film_info: FilmInfo = self.load_film_info(films[film_index -1].link)
            season_name = "Season " + str(selected_season).zfill(2) if selected_season is not None else "Season 1"
            base_path = pathlib.Path("{base_dir}/{title_name} ({release_year})/{season_name}".format(base_dir=download_dir,title_name=film_info.title,release_year=film_info.release.split("-")[0],season_name=season_name))
            pathlib.Path.mkdir(base_path,parents=True,exist_ok=True)
            click.secho("Downloading videos...",fg=self._progress_color)
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures: List[Future] = []
                video_downloader: VideoDownloader = VideoDownloader()
                for episode, servers in episode_servers.items():
                    episode_file_name ="{title} ({release_year}) - s{selected_season}-e{episode}".format(title=film_info.title,release_year=film_info.release,selected_season=selected_season,episode=str(episode).zfill(2))
                    for server in servers:
                        video_container: VideoContainer = self.load_video(server)
                        if not video_container.videos:
                            click.echo(click.style(f"No video url were found from {server.name} server",fg="red"))
                            continue
                        url = video_container.videos[0].url
                        future = executor.submit(video_downloader.download_video,url,quality,str(base_path),episode_file_name)
                        futures.append(future)
                        break
                wait(futures)
        else:
            click.secho("Getting movie servers...",fg=self._progress_color)
            servers = self.load_movie_servers(param_id)
            film_info: FilmInfo = self.load_film_info(films[film_index -1].link)
            base_path = pathlib.Path("{base_dir}/{title_name} ({release_year})".format(base_dir=download_dir,title_name=film_info.title,release_year=film_info.release))
            pathlib.Path.mkdir(base_path,parents=True,exist_ok=True)
            video_downloader: VideoDownloader = VideoDownloader()
            for server in servers:
                video_container: VideoContainer = self.load_video(server)
                if not video_container.videos:
                    click.echo(click.style(f"No video url were found from {server.name} server",fg="red"))
                    continue
                url = video_container.videos[0].url
                video_downloader.download_video(url,quality,str(base_path),base_path.name)
                break

