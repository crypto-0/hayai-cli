from .provider import *
from typing import List, Optional 
import requests
import lxml.html
from .extractors.video_extractor import *
from .extractors.upcloud import *
from .extractors.vidcloud import *

class Sol(Provider):
    _host_url: str = "https://solarmovie.pe"
    _extractors: Dict = {
            "Server UpCloud": UpCloud("https://dokicloud.one/ajax/embed-4/getSources?id="),
            "UpCloud": UpCloud("https://dokicloud.one/ajax/embed-4/getSources?id="),
            "Server Vidcloud": Vidcloud("https://rabbitstream.net/ajax/embed-4/getSources?id="),
            "Vidcloud": Vidcloud("https://rabbitstream.net/ajax/embed-4/getSources?id=")
            }
    def __init__(self) -> None:
        super().__init__()

    def load_movie_servers(self,movie_id: str) -> List[VideoServer]:
        movie_server_url : str = f"{self._host_url}/ajax/movie/episodes/"
        server_embed_url: str = f"{self._host_url}/ajax/get_link/"
        r : requests.Response = requests.get(movie_server_url + movie_id,headers=self._headers)
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        server_elements : List[lxml.html.HtmlElement] = html_doc.cssselect(".nav-item a")
        servers: List[VideoServer] = [] 
        for server_element in server_elements:
            server_id: str = server_element.get("data-linkid")
            server_title: str = server_element.get("title")
            r: requests.Response = requests.get(server_embed_url + server_id,headers=self._headers)
            embed: str = r.json()["link"]
            servers.append(VideoServer(server_title,embed))
        return servers

    def load_seasons(self,film_id: str) -> List[Season]:
        season_url: str = f"{self._host_url}/ajax/v2/tv/seasons/" + film_id
        r: requests.Response = requests.get(season_url,headers=self._headers)
        html_doc: lxml.html.HtmlElement= lxml.html.fromstring(r.text)
        season_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".dropdown-item")
        seasons: List[Season] =[]
        for season_element in season_elements:
            season_number: str = season_element.text.split()[-1]
            season_id: str = season_element.get("data-id")
            seasons.append(Season(season_number,season_id))
        return seasons

    def load_episodes(self,season_id: str) -> List[Episode]:
        episodes_url: str = f"{self._host_url}/ajax/v2/season/episodes/"
        r = requests.get(episodes_url + season_id,headers=self._headers)
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        episode_elements:List[lxml.html.HtmlElement] = html_doc.cssselect("a")
        episodes : List[Episode] = []
        for episode_element in episode_elements:
            episode_number: str = episode_element.get("title").split(":")[0].split()[-1]
            episode_id = episode_element.get("data-id")
            episode_title = episode_element.get("title").split(":")[-1]
            episodes.append(Episode(episode_number,episode_title,episode_id))
        return episodes

    def load_episode_servers(self,episode_id: str) -> List[VideoServer]:
        episodes_server_url : str = f"{self._host_url}/ajax/v2/episode/servers/"
        server_embed_url: str = f"{self._host_url}/ajax/get_link/"
        try:
            r : requests.Response = requests.get(episodes_server_url + episode_id,headers=self._headers)
            r.raise_for_status()
            html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
            server_elements : List[lxml.html.HtmlElement] = html_doc.cssselect(".nav-item a")
            servers: List[VideoServer] = [] 
            for server_element in server_elements:
                server_id: str = server_element.get("data-id")
                server_title: str = server_element.get("title")
                r: requests.Response = requests.get(server_embed_url + server_id,headers=self._headers)
                embed: str = r.json()["link"]
                if self._extractors.get(server_title) == None:
                    continue
                servers.append(VideoServer(server_title,embed))
            return servers
        except Exception as e:
            return []

    def extract_server(self, server_name, embed: str) -> VideoContainer:
        extractor: Optional[VideoExtractor] = self._extractors.get(server_name)
        if extractor:
            return extractor.extract(embed)
        return VideoContainer()

    def load_home(self):
        url = f"{self._host_url}/home"
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(),[])
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        trending_movies_FLW_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".section-id-01 #trending-movies .flw-item")
        trending_shows_FLW_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".section-id-01 #trending-tv .flw-item")
        section_elements : List[lxml.html.HtmlElement] = html_doc.cssselect(".section-id-02")
        latest_movies_FLW_items: List[lxml.html.HtmlElement] = section_elements[0].cssselect(".flw-item" )
        latest_shows_FLW_items: List[lxml.html.HtmlElement] = section_elements[1].cssselect(".flw-item")
        #coming_soon_FLW_items: List[lxml.html.HtmlElement] = section_elements[2].cssselect(".flw-item")
        trending_movies: List[Film] = list(map(self.parse_FLW_element, trending_movies_FLW_items))
        trending_shows: List[Film] = list(map(self.parse_FLW_element, trending_shows_FLW_items))
        latest_movies: List[Film] = list(map(self.parse_FLW_element, latest_movies_FLW_items))
        latest_shows: List[Film] = list(map(self.parse_FLW_element, latest_shows_FLW_items))
        #coming_soon_films: List[Film] = list(map(self.parse_FLW_element, coming_soon_FLW_items))
        return Page(PageInfo(),trending_movies + trending_shows + latest_movies + latest_shows)

    def load_movies(self,page_number=1):
        url = f"{self._host_url}/movie?page={page_number}"
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(),[])
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        pagination_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination.pagination-lg li")
        page_info: PageInfo = self.parse_pagination_elements(pagination_elements)
        flw_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
        films: List[Film] = list(map(self.parse_FLW_element, flw_items))
        return Page(page_info,films)

    def load_shows(self,page_number=1):
        url = f"{self._host_url}/tv-show?page={page_number}"
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(),[])
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        pagination_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination.pagination-lg li")
        page_info: PageInfo = self.parse_pagination_elements(pagination_elements)
        flw_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
        films: List[Film] = list(map(self.parse_FLW_element, flw_items))
        return Page(page_info,films)

    def load_imdb(self,page_number=1):
        url = f"{self._host_url}/top-imdb?page={page_number}"
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(),[])
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        pagination_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination.pagination-lg li")
        page_info: PageInfo = self.parse_pagination_elements(pagination_elements)
        flw_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
        films: List[Film] = list(map(self.parse_FLW_element, flw_items))
        return Page(page_info,films)

    def load_search(self,query: str,page_number=1) -> Page:
        query = query.strip().replace(" ","-")
        search_url: str = f"{self._host_url}/search/{query}?page={page_number}"
        try:
            r: requests.Response = requests.get(search_url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(1,1,False),[])
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        pagination_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination.pagination-lg li")
        page_info: PageInfo = self.parse_pagination_elements(pagination_elements)
        flw_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
        films: List[Film] = list(map(self.parse_FLW_element, flw_items))
        return Page(page_info,films)



    def load_film_info(self,url: str) -> FilmInfo:
        try:
            r = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return FilmInfo()
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        description = html_doc.cssselect(".description")[0].text_content()
        elements: lxml.html.HtmlElement = html_doc.cssselect(".row-line")
        release = elements[0].text_content().split("Released: ")[-1].strip()
        genre: str = elements[1].cssselect("a")[0].text
        duration: str = elements[3].text_content().split("Duration: ")[-1].split()[0].strip()
        country: str = elements[4].cssselect("a")[0].text.strip()
        title = url.split("watch-")[-1].split("-free")[0].replace("-"," ")
        flw_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
        recommendations: List[Film] = list(map(self.parse_FLW_element,flw_items))
        poster_url:str = html_doc.cssselect(".detail_page-infor .film-poster-img")[0].get("src")
        poster_image: bytes = self.load_poster_image(poster_url)
        return FilmInfo(title=title,release=release,description=description.strip(),genre=genre,country=country,duration=duration,recommendation=recommendations,poster_image=poster_image)

    def parse_FLW_element(self,element: lxml.html.HtmlElement) -> Film:
        poster_url: lxml.html.HtmlElement = element.cssselect(".film-poster > img")[0].get("data-src")
        link_tag: lxml.html.HtmlElement = element.cssselect(".film-poster > a")[0]
        title: str = link_tag.get("title")
        link: str = link_tag.get("href")
        film_info_tags: List[lxml.html.HtmlElement] = element.cssselect(".film-detail .fd-infor span")
        
        extra_details: str = ""
        for info_tag in film_info_tags:
            extra_details += (info_tag.text + " . ") if info_tag.text is not None else ""
        extra_details = extra_details.strip()
        extra_details = extra_details.strip("  .  ")
        is_tv: bool = True if film_info_tags[-1].text == "TV" else False

        return Film(title,self._host_url + link,is_tv,poster_url=poster_url,extra= extra_details)

    def parse_pagination_elements(self,elements: List[lxml.html.HtmlElement]) -> PageInfo:
        current_page: int = 1
        last_page: int = 1
        has_next_page: bool = False

        for page_item in elements:
            class_name: str = page_item.get("class",0)
            aTag: lxml.html.HtmlElement =  page_item.cssselect("a")[0]
            if class_name.endswith("active"):
                current_page = int(aTag.text)
            else:
                title: str = aTag.get("title","")
                href: str = aTag.get("href","")
                if title == "Last":
                    last_page = int(href.rsplit("=",1)[1].strip())
                if title == "Next":
                    has_next_page = True

        return PageInfo(current_page,last_page,has_next_page)


    def load_poster_image(self, url: str) -> bytes:
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
            poster_data  = r.content
            return poster_data
        except:
            return bytes()
