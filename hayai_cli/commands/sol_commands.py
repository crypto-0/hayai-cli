from itertools import islice
import pathlib
import sys
from typing import Dict, Iterator
from typing import List

import click
import httpx
from provider_parsers import Film
from provider_parsers import VideoServer
from provider_parsers import Sol
from provider_parsers.provider_parser import FilmInfo

from hayai_cli.downloader.handle import handle_download
from hayai_cli.utilities.convert_video import convert_video


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
@click.option("-p", "--page",help="up to what pages to show at once",type=int,default = 1)
def download_cmd(query:str,index,season,episode_ranges,quality,dir,page):
    color = "blue"
    search_films_iterator: Iterator[Film] = Sol.parse_search(query=query)
    all_films: List[Film] = list(islice(search_films_iterator,10))
    if len(all_films) == 0:
        click.secho("No search results were found",fg="red")
        sys.exit()
    if index is None:
        Sol.print_films(all_films)
        index = click.prompt(click.style("Enter a number",fg=color),type=click.IntRange(1,len(all_films)))
    if all_films[index - 1].is_tv:
        click.secho("Getting seasons...",fg=color)
        link: str = (all_films[index -1].link).rsplit("-",1)[-1]
        seasons = Sol.parse_seasons(link)
        if len(seasons) == 0:
            click.echo(click.style("No seasons were found",fg="red"))
            sys.exit()
        if season is None:
            Sol.print_seasons(seasons=seasons)
            season = click.prompt(click.style("Select a Season",fg=color),type=click.IntRange(1,len(seasons)))
        click.secho("Getting episodes...",fg=color)
        link: str = seasons[season - 1].id
        episodes = Sol.parse_episodes(link)
        if len(episodes) == 0:
            click.echo(click.style("No episodes were found",fg="red"))
            sys.exit()
        if len(episode_ranges) == 0:
            Sol.print_episodes(episodes=episodes)
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
               servers = Sol.parse_episode_servers(episodes[idx -1].id)
               episode_servers[idx] = servers
        info: FilmInfo = Sol.parse_info(all_films[index -1].link)
        season = str(season).zfill(2)
        season_name = "Season " + season
        show_path = pathlib.Path("{dir}/{title_name} ({release_year})/{season_name}".format(dir=dir,title_name=info.title,release_year=info.release.split("-")[0],season_name=season_name))
        pathlib.Path.mkdir(show_path,parents=True,exist_ok=True)
        click.secho("Downloading videos...",fg=color)
        with httpx.Client(timeout=15) as client:
            for episode, servers in episode_servers.items():
                episode_name ="{title} ({release_year}) - s{season}-e{episode}".format(title=info.title,release_year=info.release.split("-")[0],season=season,episode=str(episode).zfill(2))
                for server in servers:
                    episode_container = server.extractor.extract(server.embed)
                    try:
                        if(not episode_container.videos):continue
                        url = episode_container.videos[0].url
                        handle_download(client,url,Sol.headers,show_path,episode_name)
                        episode_location_ts = str(show_path) + "/" + episode_name +".ts"
                        convert_video(episode_location_ts)
                        break
                    except Exception as e:
                        print(e)



    else:
        click.secho("Getting movie servers...",fg=color)
        link: str = (all_films[index - 1].link).rsplit("-",1)[-1]
        servers = Sol.parse_movie_servers(link)
        info: FilmInfo = Sol.parse_info(all_films[index -1].link)
        movie_path = pathlib.Path("{dir}/{title_name} ({release_year})".format(dir=dir,title_name=info.title,release_year=info.release.split("-")[0]))
        pathlib.Path.mkdir(movie_path,parents=True,exist_ok=True)
        click.secho("Downloading videos...",fg=color)
        with httpx.Client(timeout=15) as client:
            for server in servers:
                movie_container = server.extractor.extract(server.embed)
                try:
                    if(not movie_container.videos):continue
                    url = movie_container.videos[0].url
                    handle_download(client,url,Sol.headers,movie_path,movie_path.name)
                    movie_location_ts = str(movie_path) + "/" + movie_path.name + ".ts"
                    convert_video(movie_location_ts)
                    break
                except Exception as e:
                    print(e)



@sol_cli.command(name="search",help="search for movies or shows")
@click.argument("query",required=True)
def search_cmd(query:str):
    search_films_iterator: Iterator[Film] = Sol.parse_search(query=query)
    all_films: List[Film] = list(islice(search_films_iterator,20))
    Sol.print_films(all_films)
    
@sol_cli.command(name="latest",help="Show latest movies or shows")
def latest_cmd():
    latest_films_iterator: Iterator[Film] = Sol.parse_category("latest")
    all_films: List[Film] = list(islice(latest_films_iterator,20))
    Sol.print_films(all_films)
    
@sol_cli.command(name="trending",help="Show trending movies or shows")
def trending_cmd():
    trending_films_iterator: Iterator[Film] = Sol.parse_category("trending")
    all_films: List[Film] = list(islice(trending_films_iterator,20))
    Sol.print_films(all_films)

@sol_cli.command(name="coming",help="Show coming movies or shows")
def coming_cmd():
    coming_films_iterator: Iterator[Film] = Sol.parse_category("coming")
    all_films: List[Film] = list(islice(coming_films_iterator,30))
    Sol.print_films(all_films)
