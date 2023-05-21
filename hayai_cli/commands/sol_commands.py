import click
from hayai_cli.providers import Sol
from hayai_cli.providers import Page

@click.group(name="sol",help="solarmovie provider")
def sol_cli():
    pass

@sol_cli.command(name="search",help="search for movies or shows")
@click.argument("query",required=True)
@click.option("-p", "--page",help="page to display",type=int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default ="1080")
def search_cmd(query:str,page: int,mode: str,download_dir: str,quality: str):
    sol: Sol = Sol()
    search_page: Page = sol.load_search(query=query,page_number=page)
    sol.display(search_page.films,mode,download_dir,quality)

@sol_cli.command(name="home",help="show home")
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default ="1080")
def home_cmd(mode: str,download_dir: str,quality: str):
    sol: Sol = Sol()
    home_page: Page = sol.load_home()
    sol.display(home_page.films,mode,download_dir,quality)

    
@sol_cli.command(name="movies",help="Show movies")
@click.option("-p", "--page",help="page to display",type= int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default = "1080")
def movies_cmd(page: int,mode: str,download_dir: str,quality: str):
    sol: Sol = Sol()
    movies_page: Page = sol.load_movies(page_number=page)
    sol.display(movies_page.films,mode,download_dir,quality)
    
@sol_cli.command(name="shows",help="Show shows")
@click.option("-p", "--page",help="page to display",type= int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default = "1080")
def shows_cmd(page: int,mode: str,download_dir: str,quality: str):
    sol: Sol = Sol()
    shows_page: Page = sol.load_shows(page_number=page)
    sol.display(shows_page.films,mode,download_dir,quality)
    
@sol_cli.command(name="top imdb",help="Show top imbd movies or shows")
@click.option("-p", "--page",help="page to display",type= int,default = 1)
@click.option("-m", "--mode",help="play or download",type=click.Choice(["play","download"]),default = "download")
@click.option("-d", "--download_dir",help="download directory ",type=str,default = ".")
@click.option("-q", "--quality",help="quality of stream",type=str,default = "1080")
def top_imdb_cmd(page: int,mode: str,download_dir: str,quality: str):
    sol: Sol = Sol()
    top_imdb_page: Page = sol.load_imdb(page_number=page)
    sol.display(top_imdb_page.films,mode,download_dir,quality)
    
