from .provider_parser import *
from typing import List 
from typing import Iterator
import requests
import lxml.html
from .extractors.video_extractor import *
from .extractors.upcloud import *
from .extractors.vidcloud import *


class Sol(ProviderParser):
    name : str = "sol"
    host_url: str = "https://solarmovie.pe"
    genre: Dict[str,str] = {
            "Action": "10-",
            "Action & Adventure": "24-",
            "Adventure": "18-",
            "Animation": "3-",
            "Biography": "37-",
            "Comedy": "7-",
            "Crime": "2-",
            "Documentary": "11-",
            "Drama": "4-",
            "Family": "9-",
            "Fantasy": "13-",
            "History": "19-",
            "Horror": "14-",
            "Kids": "27-",
            "Music": "15-",
            "Mystery": "1-",
            "News": "34-",
            "Reality": "22-",
            "Romance": "12-",
            "Sci-Fi & Fantasy": "31-",
            "Science Fiction": "5-",
            "Soap": "35-",
            "Talk": "29-",
            "Thriller": "16-",
            "TV Movie": "8-",
            "War": "17-",
            "War & Politics": "28-",
            "Western": "6-",
            }
    type: Dict[str,str] = {
            "Movie": "movie",
            "Show": "tv"
            }

    categories: List[str] = ["top imdb" ]
    home_categories: List[str] = ["latest","trending","coming soon"]
    extractors: Dict = {
            "Server UpCloud": UpCloud,
            "UpCloud": UpCloud,
            "Server Vidcloud": Vidcloud,
            "Vidcloud": Vidcloud
            }

    @staticmethod
    def parse_movie_servers(id: str) -> List[VideoServer]:
        movie_server_url : str = f"{Sol.host_url}/ajax/movie/episodes/"
        server_embed_url: str = f"{Sol.host_url}/ajax/get_link/"
        r : requests.Response = Sol.session.get(movie_server_url + id,headers=Sol.headers)
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        server_elements : List[lxml.html.HtmlElement] = html_doc.cssselect(".nav-item a")
        servers: List[VideoServer] = [] 
        for server_element in server_elements:
            server_id: str = server_element.get("data-linkid")
            server_title: str = server_element.get("title")
            r: requests.Response = Sol.session.get(server_embed_url + server_id,headers=Sol.headers)
            embed: str = r.json()["link"]
            if Sol.extractors.get(server_title) == None:
                continue
            extractor: type[VideoExtractor] = Sol.extractors[server_title]
            servers.append(VideoServer(server_title,embed,extractor))
        return servers

    @staticmethod
    def parse_seasons(id: str) -> List[Season]:
        season_url: str = f"{Sol.host_url}/ajax/v2/tv/seasons/" + id
        r: requests.Response = Sol.session.get(season_url,headers=Sol.headers)
        html_doc: lxml.html.HtmlElement= lxml.html.fromstring(r.text)
        season_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".dropdown-item")
        seasons: List[Season] =[]
        for season_element in season_elements:
            season_number: str = season_element.text.split()[-1]
            season_id: str = season_element.get("data-id")
            seasons.append(Season(season_number,season_id))
        return seasons

    @staticmethod
    def parse_episodes(id: str) -> List[Episode]:
        episodes_url: str = f"{Sol.host_url}/ajax/v2/season/episodes/"
        r = Sol.session.get(episodes_url + id,headers=Sol.headers)
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        episode_elements:List[lxml.html.HtmlElement] = html_doc.cssselect("a")
        episodes : List[Episode] = []
        for episode_element in episode_elements:
            episode_number: str = episode_element.get("title").split(":")[0].split()[-1]
            episode_id = episode_element.get("data-id")
            episode_title = episode_element.get("title")
            episodes.append(Episode(episode_number,episode_id,episode_title))
        return episodes


    @staticmethod
    def parse_episode_servers(id: str) -> List[VideoServer]:
        episodes_server_url : str = f"{Sol.host_url}/ajax/v2/episode/servers/"
        server_embed_url: str = f"{Sol.host_url}/ajax/get_link/"
        r : requests.Response = Sol.session.get(episodes_server_url + id,headers=Sol.headers)
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        server_elements : List[lxml.html.HtmlElement] = html_doc.cssselect(".nav-item a")
        servers: List[VideoServer] = [] 
        for server_element in server_elements:
            server_id: str = server_element.get("data-id")
            server_title: str = server_element.get("title")
            r: requests.Response = Sol.session.get(server_embed_url + server_id,headers=Sol.headers)
            embed: str = r.json()["link"]
            if Sol.extractors.get(server_title) == None:
                continue
            extractor: type[VideoExtractor] = Sol.extractors[ server_title ]
            servers.append(VideoServer(server_title,embed,extractor))
        return servers

    @staticmethod
    def parse_movies(fetch_image: bool = False) -> Iterator[Film]:
        movies_ur: str = f"{Sol.host_url}/movie"
        r: requests.Response = Sol.session.get(movies_ur + "?page=1",headers=Sol.headers)
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        last_page_link = html_doc.cssselect(".pagination.pagination-lg a")
        max_page = 1
        if len(last_page_link) > 0:
            max_page = int(last_page_link[-1].get("href").rsplit("=",1)[1])

        for i in range(1,max_page + 1):
            r: requests.Response = Sol.session.get(movies_ur + "?page=" + str(i),headers=Sol.headers)
            html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
            movie_results: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
            for movie_result in movie_results:
                yield Sol.extract_film_element(movie_result,fetch_image)
    @staticmethod
    def parse_shows(fetch_image: bool = False) -> Iterator[Film]:
        shows_ur: str = f"{Sol.host_url}/tv-show"
        r: requests.Response = Sol.session.get(shows_ur + "?page=1",headers=Sol.headers)
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        last_page_link = html_doc.cssselect(".pagination.pagination-lg a")
        max_page = 1
        if len(last_page_link) > 0:
            max_page = int(last_page_link[-1].get("href").rsplit("=",1)[1])

        for i in range(1,max_page + 1):
            r: requests.Response = Sol.session.get(shows_ur + "?page=" + str(i),headers=Sol.headers)
            html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
            show_results: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
            for show_result in show_results:
                yield Sol.extract_film_element(show_result,fetch_image)

    @staticmethod
    def parse_top_imdb(fetch_image: bool = False) -> Iterator[Film]:
        shows_ur: str = f"{Sol.host_url}/top-imdb"
        r: requests.Response = Sol.session.get(shows_ur + "?page=1",headers=Sol.headers)
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        last_page_link = html_doc.cssselect(".pagination.pagination-lg a")
        max_page = 1
        if len(last_page_link) > 0:
            max_page = int(last_page_link[-1].get("href").rsplit("=",1)[1])

        for i in range(1,max_page + 1):
            r: requests.Response = Sol.session.get(shows_ur + "?page=" + str(i),headers=Sol.headers)
            html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
            imdb_results: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
            for imdb_result in imdb_results:
                yield Sol.extract_film_element(imdb_result,fetch_image)

    @staticmethod
    def parse_latest_shows(fetch_image: bool = False) -> Iterator[Film]:
        home_url: str = f"{Sol.host_url}/home"
        r: requests.Response = Sol.session.get(home_url,headers=Sol.headers)
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        section_elements : List[lxml.html.HtmlElement] = html_doc.cssselect(".section-id-02")
        flw_show_elements: List[lxml.html.HtmlElement] = section_elements[1].cssselect(".flw-item")
        for flw_element in flw_show_elements:
            yield Sol.extract_film_element(flw_element,fetch_image)
            
    @staticmethod
    def parse_latest_movies(fetch_image: bool = False) -> Iterator[Film]:
        home_url: str = f"{Sol.host_url}/home"
        r: requests.Response = Sol.session.get(home_url,headers=Sol.headers)
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        section_elements : List[lxml.html.HtmlElement] = html_doc.cssselect(".section-id-02")
        flw_movie_elements: List[lxml.html.HtmlElement] = section_elements[0].cssselect(".flw-item")
        for flw_element in flw_movie_elements:
            yield Sol.extract_film_element(flw_element,fetch_image)

    @staticmethod
    def parse_latest(fetch_image: bool = False) -> Iterator[Film]:
        tv_shows_generator: Iterator[Film] = Sol.parse_latest_shows(fetch_image)
        movies_generator: Iterator[Film] = Sol.parse_latest_movies(fetch_image)
        more_shows: bool = True
        more_movies: bool = True
        while(more_shows or more_movies):
            if(more_shows):
                try:
                    film = next(tv_shows_generator)
                    yield film
                except StopIteration:
                    more_shows = False
            if(more_movies):
                try:
                    film = next(movies_generator)
                    yield film
                except StopIteration:
                    more_movies = False

    @staticmethod
    def parse_trending_movies(fetch_image: bool = False) -> Iterator[Film]:
        home_url: str = f"{Sol.host_url}/home"
        r: requests.Response = Sol.session.get(home_url,headers=Sol.headers)
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        trending_movie_elements : List[lxml.html.HtmlElement] = html_doc.cssselect("#trending-movies")
        flw_movie_elements: List[lxml.html.HtmlElement] = trending_movie_elements[0].cssselect(".flw-item")
        for flw_element in flw_movie_elements:
            yield Sol.extract_film_element(flw_element,fetch_image)


    @staticmethod
    def parse_trending_shows(fetch_image: bool = False) -> Iterator[Film]:
        home_url: str = f"{Sol.host_url}/home"
        r: requests.Response = Sol.session.get(home_url,headers=Sol.headers)
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        trending_show_elements : List[lxml.html.HtmlElement] = html_doc.cssselect("#trending-tv")
        flw_show_elements: List[lxml.html.HtmlElement] = trending_show_elements[0].cssselect(".flw-item")
        for flw_element in flw_show_elements:
            yield Sol.extract_film_element(flw_element,fetch_image)

    @staticmethod
    def parse_trending(fetch_image: bool = False) -> Iterator[Film]:
        tv_shows_generator: Iterator[Film] = Sol.parse_trending_shows(fetch_image)
        movies_generator: Iterator[Film] = Sol.parse_trending_movies(fetch_image)
        more_shows: bool = True
        more_movies: bool = True
        while(more_shows or more_movies):
            if(more_shows):
                try:
                    film = next(tv_shows_generator)
                    yield film
                except StopIteration:
                    more_shows = False
            if(more_movies):
                try:
                    film = next(movies_generator)
                    yield film
                except StopIteration:
                    more_movies = False

    @staticmethod
    def parse_coming_soon(fetch_image: bool = False) -> Iterator[Film]:
        home_url: str = f"{Sol.host_url}/home"
        r: requests.Response = Sol.session.get(home_url,headers=Sol.headers)
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        section_elements : List[lxml.html.HtmlElement] = html_doc.cssselect(".section-id-02")
        flw_movie_elements: List[lxml.html.HtmlElement] = section_elements[2].cssselect(".flw-item")
        for flw_element in flw_movie_elements:
            yield Sol.extract_film_element(flw_element,fetch_image)

    @staticmethod
    def parse_info(url: str) -> FilmInfo:
        r = Sol.session.get(url,headers=Sol.headers)
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        description = html_doc.cssselect(".description")[0].text_content()
        element: lxml.html.HtmlElement = html_doc.cssselect(".row-line")[0]
        release = element.text_content().split("Released: ")[-1].strip()
        title = url.split("watch-")[-1].split("-free")[0].replace("-"," ")
        recommendation: list[Film] = []
        return FilmInfo(title=title,release=release,description=description.strip(),recommendation=recommendation)

    @staticmethod
    def parse_search( query: str,filter: Optional[Filter] = None,fetch_image: bool = False) -> Iterator[Film]:
        query = query.strip().replace(" ","-")
        search_url: str = Sol.host_url + "/search/" + query
        if(filter):
            type_parameter = Sol.type.get(filter.type,"all")
            genre_parameter = ""
            for g in filter.genre:
                genre_parameter += Sol.genre.get(g,"")
            genre_parameter = genre_parameter if(len(genre_parameter) > 0) else "all"
            genre_parameter = genre_parameter.strip("-")
            search_url: str = "{host_url}/filter?type={type}&quality=all&release_year=all&genre={genre}&country=all".format(host_url=Sol.host_url,type=type_parameter,genre=genre_parameter)

        r: requests.Response = Sol.session.get(search_url + "?page=1",headers=Sol.headers)
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        last_page_link = html_doc.cssselect(".pagination.pagination-lg a")
        max_page = 1
        if len(last_page_link) > 0:
            max_page = int(last_page_link[-1].get("href").rsplit("=",1)[1])

        for i in range(1,max_page + 1):
            r: requests.Response = Sol.session.get(search_url + "?page=" + str(i),headers=Sol.headers)
            html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
            search_results: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
            for search_result in search_results:
                yield Sol.extract_film_element(search_result,fetch_image)

    @staticmethod
    def parse_category(category: str,fetch_image: bool = False) ->Optional[Iterator[Film]]:
        if(category == "latest"):
            return Sol.parse_latest(fetch_image)
        if(category == "trending"):
            return Sol.parse_trending(fetch_image)

        if(category == "coming soon" or category == "coming"):
            return Sol.parse_coming_soon(fetch_image)

        if(category == "movies"):
            return Sol.parse_movies(fetch_image)

        if(category == "tv shows"):
            return Sol.parse_shows(fetch_image)

        if(category == "top imdb"):
            return Sol.parse_top_imdb(fetch_image)
        return None
        
    @staticmethod
    def get_available_genres() -> List[str]:
        return List(Sol.genre.keys())
    @staticmethod
    def extract_film_element(element: lxml.html.HtmlElement,fetch_image = False) -> Film:
        poster_url: lxml.html.HtmlElement = element.cssselect(".film-poster > img")[0].get("data-src")
        link_tag: lxml.html.HtmlElement = element.cssselect(".film-poster > a")[0]
        title: str = link_tag.get("title")
        link: str = link_tag.get("href")
        film_info_tags: List[lxml.html.HtmlElement] = element.cssselect(".film-detail .fd-infor span")
        extra_details: str = film_info_tags[0].text
        is_tv: bool = True if film_info_tags[-1].text == "TV" else False
        r: requests.Response = Sol.session.get(poster_url,headers=Sol.headers)
        poster_data  = r.content

        return Film(title,Sol.host_url + link,is_tv,poster_url,extra= extra_details,poster_data=poster_data)

