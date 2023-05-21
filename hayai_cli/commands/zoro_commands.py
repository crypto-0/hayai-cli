import click
from hayai_cli.providers import Zoro
from hayai_cli.providers import Page

@click.group(name="zoro",help="zoro provider")
def zoro_cli():
    pass

@zoro_cli.command(name="search",help="search for movies or shows")
@click.argument("query",required=True)
@click.option("-p", "--page",help="page to display",type=int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default ="1080")
@click.option("--server_type",help="type of server dub or sub ",type=click.Choice(["dub","sub"]),default ="sub")
def search_cmd(query:str,page: int,mode: str,download_dir: str,quality: str,server_type: str):
    zoro: Zoro = Zoro()
    zoro.server_type = server_type
    search_page: Page = zoro.load_search(query=query,page_number=page)
    zoro.display(search_page.films,mode,download_dir,quality)

@zoro_cli.command(name="home",help="show home")
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default ="1080")
@click.option("--server_type",help="type of server dub or sub",type=click.Choice(["dub","sub"]),default ="sub")
def home_cmd(mode: str,download_dir: str,quality: str,server_type: str):
    zoro: Zoro = Zoro()
    zoro.server_type = server_type
    home_page: Page = zoro.load_home()
    zoro.display(home_page.films,mode,download_dir,quality)

    
@zoro_cli.command(name="movies",help="Show movies")
@click.option("-p", "--page",help="page to display",type= int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default = "1080")
@click.option("--server_type",help="type of server dub or sub ",type=click.Choice(["dub","sub"]),default ="sub")
def movies_cmd(page: int,mode: str,download_dir: str,quality: str,server_type: str):
    zoro: Zoro = Zoro()
    zoro.server_type = server_type
    movies_page: Page = zoro.load_movies(page_number=page)
    zoro.display(movies_page.films,mode,download_dir,quality)
    
@zoro_cli.command(name="shows",help="Show shows")
@click.option("-p", "--page",help="page to display",type= int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default = "1080")
def shows_cmd(page: int,mode: str,download_dir: str,quality: str,server_type: str):
    zoro: Zoro = Zoro()
    zoro.server_type = server_type
    shows_page: Page = zoro.load_shows(page_number=page)
    zoro.display(shows_page.films,mode,download_dir,quality)
    
@zoro_cli.command(name="subbed_anime",help="Show subbed anime")
@click.option("-p", "--page",help="page to display",type= int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default = "1080")
@click.option("--server_type",help="type of server dub or sub ",type=click.Choice(["dub","sub"]),default ="sub")
def subbed_anime_cmd(page: int,mode: str,download_dir: str,quality: str,server_type: str):
    zoro: Zoro = Zoro()
    zoro.server_type = server_type
    subbed_anime_page: Page = zoro.load_subbed_anime(page)
    zoro.display(subbed_anime_page.films,mode,download_dir,quality)
    
@zoro_cli.command(name="dubbed_anime",help="Show dubbed anime")
@click.option("-p", "--page",help="page to display",type= int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default = "1080")
@click.option("--server_type",help="type of server dub or sub ",type=click.Choice(["dub","sub"]),default ="sub")
def dubbed_anime_cmd(page: int,mode: str,download_dir: str,quality: str,server_type: str):
    zoro: Zoro = Zoro()
    zoro.server_type = server_type
    dubbed_anime_page: Page = zoro.load_dubbed_anime(page)
    zoro.display(dubbed_anime_page.films,mode,download_dir,quality)
    
