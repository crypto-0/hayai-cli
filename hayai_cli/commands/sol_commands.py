from concurrent.futures import Future, ThreadPoolExecutor, wait
from itertools import islice
import pathlib
import sys
from typing import Dict, Iterator, Optional
from typing import List

import click
from providers import Film
from providers import VideoServer
from providers import Sol
from providers import FilmInfo
from providers import Page

from hayai_cli.downloader.video_downloader import VideoDownloader

@click.group(name="sol",help="solarmovie provider")
def sol_cli():
    pass

@sol_cli.command(name="download",help="download movies or shows")
@click.argument("query",required=True)
@click.option("-i", "--index",help="automatic choose index of query",type = int)
@click.option("-ss", "--season",help="automatic select season index",type=int)
@click.option("-e", "--episode_ranges",help="select range of episodes",type=(int, int),multiple=True)
@click.option("-q", "--quality",help="select quality if available")
@click.option("-d", "--dir",help="download directory",default = ".")
@click.option("-b", "--batch",help="up to how many films to show at once at once",type=int,default = 15)
def download_cmd(query:str,index,season,episode_ranges,quality,dir,batch):
    sol: Sol = Sol()
    color = "blue"
    search_page: Page = sol.load_search(query=query)
    all_films: List[Film] = search_page.films
    if len(all_films) == 0:
        click.secho("No search results were found",fg="red")
        sys.exit()
    if index is None:
        sol.print_films(all_films)
        index = click.prompt(click.style("Enter a number",fg=color),type=click.IntRange(1,len(all_films)))
    if all_films[index - 1].is_tv:
        click.secho("Getting seasons...",fg=color)
        film_id: str = (all_films[index -1].link).rsplit("-",1)[-1]
        seasons = sol.load_seasons(film_id)
        if len(seasons) == 0:
            click.echo(click.style("No seasons were found",fg="red"))
            sys.exit()
        if season is None:
            Sol.print_seasons(seasons=seasons)
            season = click.prompt(click.style("Select a Season",fg=color),type=click.IntRange(1,len(seasons)))
        click.secho("Getting episodes...",fg=color)
        season_id: str = seasons[season - 1].season_id
        episodes = sol.load_episodes(season_id)
        if len(episodes) == 0:
            click.echo(click.style("No episodes were found",fg="red"))
            sys.exit()
        if len(episode_ranges) == 0:
            sol.print_episodes(episodes=episodes)
            while True:
                min_episode = click.prompt(click.style("Select min episode",fg=color),type=click.IntRange(1,len(episodes)),default=1)
                max_episode = click.prompt(click.style("Select max episode",fg=color),type=click.IntRange(1,len(episodes)),default=len(episodes))
                episode_ranges = episode_ranges + ((min_episode,max_episode),)
                if(not click.confirm(click.style("Add more episodes ",fg=color))):break

        click.secho("Getting servers...",fg=color)
        episode_servers: Dict[int,List[VideoServer]] = {}
        for episode_range in episode_ranges:
           for idx in range(episode_range[0],episode_range[1] + 1):
               if(episode_servers.get(idx) !=None):continue
               servers = sol.load_episode_servers(episodes[idx -1].episode_id)
               episode_servers[idx] = servers
        info: FilmInfo = sol.load_film_info(all_films[index -1].link)
        season = str(season).zfill(2)
        season_name = "Season " + season
        show_path = pathlib.Path("{dir}/{title_name} ({release_year})/{season_name}".format(dir=dir,title_name=info.title,release_year=info.release.split("-")[0],season_name=season_name))
        pathlib.Path.mkdir(show_path,parents=True,exist_ok=True)
        click.secho("Downloading videos...",fg=color)
        video_downloader: VideoDownloader = VideoDownloader()
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures: List[Future] = []
            for episode, servers in episode_servers.items():
                episode_name ="{title} ({release_year}) - s{season}-e{episode}".format(title=info.title,release_year=info.release.split("-")[0],season=season,episode=str(episode).zfill(2))
                for server in servers:
                    episode_container = server.extractor.extract(server.embed)
                    try:
                        if not episode_container.videos:
                            click.echo(click.style(f"No video url were found from {server.name} server",fg="red"))
                            continue
                        url = episode_container.videos[0].url
                        #handle_download(client,url,Sol.headers,show_path,episode_name)
                        #video_downloader.download_video(url=url,quality=quality,output_dir=str(show_path),output_file=episode_name)
                        future = executor.submit(video_downloader.download_video,url,quality,str(show_path),episode_name)
                        futures.append(future)
                        #episode_location_ts = str(show_path) + "/" + episode_name +".ts"
                        #convert_video(episode_location_ts)
                        break
                    except Exception as e:
                        click.echo(click.style(f"Encounter an Exception getting video url from {server.name} server: " + str(e),fg="red"))
            wait(futures)


    else:
        click.secho("Getting movie servers...",fg=color)
        link: str = (all_films[index - 1].link).rsplit("-",1)[-1]
        servers = Sol.parse_movie_servers(link)
        info: FilmInfo = Sol.parse_info(all_films[index -1].link)
        movie_path = pathlib.Path("{dir}/{title_name} ({release_year})".format(dir=dir,title_name=info.title,release_year=info.release.split("-")[0]))
        pathlib.Path.mkdir(movie_path,parents=True,exist_ok=True)
        click.secho("Downloading videos...",fg=color)
        video_downloader: VideoDownloader = VideoDownloader()

        for server in servers:
            movie_container = server.extractor.extract(server.embed)
            try:
                if(not movie_container.videos):continue
                url = movie_container.videos[0].url
                video_downloader.download_video(url,quality,str(movie_path),movie_path.name)
                break
            except Exception as e:
                click.echo(click.style(f"Encounter an Exception getting video url from {server.name} server: " + str(e),fg="red"))



@sol_cli.command(name="search",help="search for movies or shows")
@click.argument("query",required=True)
@click.option("-b", "--batch",help="up to how many films to show at once at once",type=int,default = 15)
def search_cmd(query:str,batch: int):
    search_films_iterator: Iterator[Film] = Sol.parse_search(query=query)
    all_films: List[Film] = list(islice(search_films_iterator,batch))
    Sol.print_films(all_films)
    
@sol_cli.command(name="latest",help="Show latest movies or shows")
@click.option("-b", "--batch",help="up to how many films to show at once at once",type= int,default = 15)
def latest_cmd(batch: int):
    latest_films_iterator: Optional[Iterator[Film]] = Sol.parse_category("latest")
    if latest_films_iterator is None:
        click.secho("No results were found",fg="red")
        return
    all_films: List[Film] = list(islice(latest_films_iterator,batch))
    if len(all_films) == 0:
        click.secho("No results were found",fg="red")
        return
    Sol.print_films(all_films)
    
@sol_cli.command(name="trending",help="Show trending movies or shows")
@click.option("-b", "--batch",help="up to how many films to show at once at once",type=int,default = 15)
def trending_cmd(batch: int):
    trending_films_iterator: Optional[Iterator[Film]] = Sol.parse_category("trending")
    if trending_films_iterator is None:
        click.secho("No results were found",fg="red")
        return
    all_films: List[Film] = list(islice(trending_films_iterator,batch))
    if len(all_films) == 0:
        click.secho("No results were found",fg="red")
        return
    Sol.print_films(all_films)

@sol_cli.command(name="coming",help="Show coming movies or shows")
@click.option("-b", "--batch",help="up to how many films to show at once at once",type=int,default = 15)
def coming_cmd(batch: int):
    coming_films_iterator: Optional[Iterator[Film]] = Sol.parse_category("coming")
    if coming_films_iterator is None:
        click.secho("No results were found",fg="red")
        return
    all_films: List[Film] = list(islice(coming_films_iterator,30))
    if len(all_films) == 0:
        click.secho("No results were found",fg="red")
        return
    Sol.print_films(all_films)
