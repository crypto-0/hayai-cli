from .provider import *
from typing import List, Optional 
import requests
import lxml.html
from .extractors.video_extractor import *
from .extractors.upcloud import *
from .extractors.vidcloud import *

class Sol(Provider):
    _host_url: str = "https://solarmovie.pe"
    _available_general_categories: set[str] = {"top imdb"}
    _available_home_categories: set[str] = {"latest movies","latest shows","trending movies","trending shows","coming soon"}
    _extractors: Dict = {
            "Server UpCloud": UpCloud(),
            "UpCloud": UpCloud(),
            "Server Vidcloud": Vidcloud(),
            "Vidcloud": Vidcloud()
            }
    def __init__(self) -> None:
        super().__init__()


    @property
    def available_general_categories(self):
        return self._available_general_categories

    def available_home_categories(self):
        return self._available_home_categories

    def get_movie_servers(self,id: str) -> List[VideoServer]:
        movie_server_url : str = f"{self._host_url}/ajax/movie/episodes/"
        server_embed_url: str = f"{self._host_url}/ajax/get_link/"
        r : requests.Response = requests.get(movie_server_url + id,headers=self._headers)
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

    def get_seasons(self,id: str) -> List[Season]:
        season_url: str = f"{self._host_url}/ajax/v2/tv/seasons/" + id
        r: requests.Response = requests.get(season_url,headers=self._headers)
        html_doc: lxml.html.HtmlElement= lxml.html.fromstring(r.text)
        season_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".dropdown-item")
        seasons: List[Season] =[]
        for season_element in season_elements:
            season_number: str = season_element.text.split()[-1]
            season_id: str = season_element.get("data-id")
            seasons.append(Season(season_number,season_id))
        return seasons

    def get_episodes(self,id: str) -> List[Episode]:
        episodes_url: str = f"{self._host_url}/ajax/v2/season/episodes/"
        r = requests.get(episodes_url + id,headers=self._headers)
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        episode_elements:List[lxml.html.HtmlElement] = html_doc.cssselect("a")
        episodes : List[Episode] = []
        for episode_element in episode_elements:
            episode_number: str = episode_element.get("title").split(":")[0].split()[-1]
            episode_id = episode_element.get("data-id")
            episode_title = episode_element.get("title").split(":")[-1]
            episodes.append(Episode(episode_number,episode_title,episode_id))
        return episodes

    def get_episode_servers(self,id: str) -> List[VideoServer]:
        episodes_server_url : str = f"{self._host_url}/ajax/v2/episode/servers/"
        server_embed_url: str = f"{self._host_url}/ajax/get_link/"
        try:
            r : requests.Response = requests.get(episodes_server_url + id,headers=self._headers)
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

    def get_category(self,category: str,page_number: int = 1) -> Page:
        category_space_replaced: str = category.replace(" ","-")
        url: str = f"{self._host_url}/{category_space_replaced}"
        section_class: str = ""
        section_index: int = 0
        trending_id: str = ""
        if category in self._available_home_categories:
            url = f"{self._host_url}/home"
            if category == "trending movies":
                section_class = ".section-id-01"
                trending_id = "#trending-movies "
            elif category == "trending shows":
                section_class = ".section-id-01"
                trending_id = "#trending-tv "
            elif category == "latest movies":
                section_class = ".section-id-02"
            elif category == "latest shows":
                section_class = ".section-id-02"
                section_index = 1
            else:
                section_class = ".section-id-02"
                section_index = 2

        try:
            r: requests.Response = requests.get(f"{url}?page={page_number}",headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(1,1,False),[])
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        page_navigation: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination.pagination-lg li")
        current_page: int = 1
        last_page: int = 1
        has_next_page: bool = False

        for page_item in page_navigation:
            class_name: str = page_item.get("class",0)
            a_tag: lxml.html.HtmlElement =  page_item.cssselect("a")[0]

            if class_name.endswith("active"):
                current_page = int(a_tag.text)
            else:
                title: str = a_tag.get("title","")
                href: str = a_tag.get("href","")
                if title == "Last":
                    last_page = int(href.rsplit("=",1)[1].strip())
                if title == "Next":
                    has_next_page = True

        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        if section_class:
            section_elements : List[lxml.html.HtmlElement] = html_doc.cssselect(section_class)
            flw_items: List[lxml.html.HtmlElement] = section_elements[section_index].cssselect(f"{trending_id}.flw-item")
        else:
            flw_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")

        films: List[Film] = list(map(self._extract_film_element, flw_items))
        page_info: PageInfo = PageInfo(current_page,last_page,has_next_page)
        return Page(page_info,films)

    def get_film_info(self,url: str) -> FilmInfo:
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
        recommendations: List[Film] = list(map(self._extract_film_element,flw_items))
        return FilmInfo(title=title,release=release,description=description.strip(),genre=genre,country=country,duration=duration,recommendation=recommendations)

    def search(self,query: str,page_number) -> Page:
        query = query.strip().replace(" ","-")
        search_url: str = f"{self._host_url}/search/{query}"
        try:
            r: requests.Response = requests.get(f"{search_url}?page={page_number}",headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(-1,-1,False),[])
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        page_navigation: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination.pagination-lg li")
        current_page: int = -1
        last_page: int = -1
        has_next_page: bool = False
        if not page_navigation:
            page_info: PageInfo = PageInfo(current_page,last_page,has_next_page)
            return Page(page_info,[])

        for page_item in page_navigation:
            class_name: str = page_item.get("class",0)
            a_tag: lxml.html.HtmlElement =  page_item.cssselect("a")[0]
            if class_name.endswith("active"):
                current_page = a_tag.text
            else:
                title: str = a_tag.get("title","")
                href: str = page_item.get("href","")
                if title == "Last":
                    last_page = int(href.rsplit("=",1)[1])
                if title == "Next":
                    has_next_page = True

        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        flw_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
        films: List[Film] = list(map(self._extract_film_element, flw_items))
        page_info: PageInfo = PageInfo(current_page,last_page,has_next_page)
        return Page(page_info,films)

    def _extract_film_element(self,element: lxml.html.HtmlElement) -> Film:
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

    def get_poster_image(self, url: str) -> bytes:
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
            poster_data  = r.content
            return poster_data
        except:
            return bytes()
