import click
from hayai_cli.providers import Asian
from hayai_cli.providers import Page

@click.group(name="asian",help="asian provider")
def asian_cli():
    pass

@asian_cli.command(name="search",help="search for movies or shows")
@click.argument("query",required=True)
@click.option("-p", "--page",help="page to display",type=int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default ="1080")
def search_cmd(query:str,page: int,mode: str,download_dir: str,quality: str):
    asian: Asian = Asian()
    search_page: Page = asian.load_search(query=query,page_number=page)
    asian.display(search_page.films,mode,download_dir,quality)
    
@asian_cli.command(name="home",help="show home")
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default ="1080")
def home_cmd(mode: str,download_dir: str,quality: str):
    asian: Asian = Asian()
    home_page: Page = asian.load_home()
    asian.display(home_page.films,mode,download_dir,quality)

@asian_cli.command(name="movies",help="Show movies")
@click.option("-p", "--page",help="page to display",type= int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default = "1080")
def movies_cmd(page: int,mode: str,download_dir: str,quality: str):
    asian: Asian = Asian()
    movies_page: Page = asian.load_movies(page_number=page)
    asian.display(movies_page.films,mode,download_dir,quality)
    
@asian_cli.command(name="shows",help="Show shows")
@click.option("-p", "--page",help="page to display",type= int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default = "1080")
def shows_cmd(page: int,mode: str,download_dir: str,quality: str):
    asian: Asian = Asian()
    shows_page: Page = asian.load_shows(page_number=page)
    asian.display(shows_page.films,mode,download_dir,quality)
    
@asian_cli.command(name="recently_added_raw",help="Show what was added that has no subtitles")
@click.option("-p", "--page",help="page to display",type= int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default = "1080")
def recently_added_raw_cmd(page: int,mode: str,download_dir: str,quality: str):
    asian: Asian = Asian()
    recently_added_raw_page: Page = asian.load_recently_added_raw(page_number=page)
    asian.display(recently_added_raw_page.films,mode,download_dir,quality)
    
@asian_cli.command(name="popular",help="Show popular movies or shows")
@click.option("-p", "--page",help="page to display",type= int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default = "1080")
def popular_cmd(page: int,mode: str,download_dir: str,quality: str):
    asian: Asian = Asian()
    popuar_drama_page: Page = asian.load_popular_drama(page)
    asian.display(popuar_drama_page.films,mode,download_dir,quality)
    
@asian_cli.command(name="ongoing_series",help="Show shows that has not finished yet")
@click.option("-p", "--page",help="page to display",type= int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default = "1080")
def ongoing_series_cmd(page: int,mode: str,download_dir: str,quality: str):
    asian: Asian = Asian()
    popuar_drama_page: Page = asian.load_popular_drama(page)
    asian.display(popuar_drama_page.films,mode,download_dir,quality)
    
