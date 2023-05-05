from .provider import *
from typing import List, Optional 
import requests
import lxml.html
from .extractors.video_extractor import *
from .extractors.upcloud import *
from .extractors.vidcloud import *

class Zoro(Provider):
    _host_url: str = "https://zoro.to"
    _extractors: Dict = {
            "Vidcloud sub": Vidcloud("https://rapid-cloud.co/ajax/embed-6/getSources?id="),
            "Vidcloud dub": Vidcloud("https://rapid-cloud.co/ajax/embed-6/getSources?id=")
            }

    def __init__(self) -> None:
        super().__init__()


    def load_seasons(self, film_id: str) -> List[Season]:
        return [Season("1",film_id)]

    def load_episodes(self,season_id: str) -> List[Episode]:
        episodes_url: str = f"{self._host_url}/ajax/v2/episode/list/{season_id}"
        try:
            r = requests.get(episodes_url,headers=self._headers)
            html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.json().get("html"))
            episode_elements:List[lxml.html.HtmlElement] = html_doc.cssselect("a")
            episodes : List[Episode] = []
            for episode_element in episode_elements:
                episode_number: str = episode_element.get("data-number")
                episode_id: str = episode_element.get("data-id")
                episode_title:str = episode_element.get("title")
                episodes.append(Episode(episode_number,episode_title,episode_id))
            return episodes
        except Exception as e:
            return []

    def load_servers(self,ID: str) -> List[VideoServer]:
        server_url : str = f"{self._host_url}/ajax/v2/episode/servers?episodeId={ID}"
        try:
            r : requests.Response = requests.get(server_url,headers=self._headers)
            r.raise_for_status()
            html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.json().get("html"))
            server_elements : List[lxml.html.HtmlElement] = html_doc.cssselect(".server-item")
            servers: List[VideoServer] = [] 
            for server_element in server_elements:
                server_id: str = server_element.get("data-id")
                server_title: str = server_element.cssselect("a")[0].text
                server_type: str = server_element.get("data-type")
                server_title += " " + server_type
                servers.append(VideoServer(server_title,server_id))
            return servers
        except Exception as e:
            return []
    

    def load_episode_servers(self,episode_id: str) -> List[VideoServer]:
        return self.load_servers(episode_id)

    def load_movie_servers(self,movie_id: str) -> List[VideoServer]:
        return self.load_servers(movie_id)

    def load_video(self,server: VideoServer):
        server_embed_url: str = f"{self._host_url}/ajax/v2/episode/sources?id={server.server_id}"
        extractor: Optional[VideoExtractor] = self._extractors.get(server.name)
        if extractor is None:
            return VideoContainer([],[])
        try:
            r: requests.Response = requests.get(server_embed_url,headers=self._headers)
            embed: str = r.json()["link"]
            return extractor.extract(embed)
        except Exception as e:
            return VideoContainer([],[])



    def load_home(self):
        url = f"{self._host_url}/home"
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            print(e)
            return Page(PageInfo(),[])
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        section_block_area_home_elements: lxml.html.HtmlElement = html_doc.cssselect(".block_area.block_area_home")
        latest_episodes_FLW_items: List[lxml.html.HtmlElement] = section_block_area_home_elements[0].cssselect(".flw-item")
        new_on_zoro_FLW_items: List[lxml.html.HtmlElement] = section_block_area_home_elements[1].cssselect(".flw-item")
        latest_episodes_films: List[Film] = list(map(self.parse_FLW_element,latest_episodes_FLW_items))
        new_on_zoro_films: List[Film] = list(map(self.parse_FLW_element,new_on_zoro_FLW_items))
        return Page(PageInfo(),latest_episodes_films + new_on_zoro_films)
        
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
        url = f"{self._host_url}/tv?page={page_number}"
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

    def load_subbed_anime(self,page_number=1):
        url = f"{self._host_url}/subbed-anime?page={page_number}"
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

    def load_dubbed_anime(self,page_number=1):
        url = f"{self._host_url}/dubbed-anime?page={page_number}"
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

    def load_most_popular(self,page_number=1):
        url = f"{self._host_url}/most-popular?page={page_number}"
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

    def load_film_info(self,url: str) -> FilmInfo:
        try:
            r = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return FilmInfo()
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        item_titles_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".item.item-title")
        description = item_titles_elements[0].cssselect(".text")[0].text.strip()
        country: str = "japanese"
        release = item_titles_elements[3].cssselect(".name")[0].text.split("to")[0].strip()
        release = release.rsplit(",",1)[-1].strip()
        duration: str = item_titles_elements[5].cssselect(".name")[0].text.strip("m")
        anisc_detail_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".anisc-detail")
        bread_crumbs_elements: List[lxml.html.HtmlElement] = anisc_detail_elements[0].cssselect(".breadcrumb-item")
        title = bread_crumbs_elements[2].text.strip("!")
        flw_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
        recommendations: List[Film] = list(map(self.parse_FLW_element,flw_items))
        poster_url:str = html_doc.cssselect(".anisc-poster .film-poster-img")[0].get("src")
        poster_image: bytes = bytes()
        genre: str = html_doc.cssselect(".item.item-list a")[0].text

        return FilmInfo(title=title,release=release,description=description.strip(),genre=genre,country=country,duration=duration,recommendation=recommendations,poster_image=poster_image)

    def load_search(self,query: str,page_number: int = 1) -> Page :
        raise NotImplemented

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
        film_type: str = film_info_tags[0].text.lower()

        return Film(title,self._host_url + link,film_type,poster_url=poster_url,extra= extra_details)

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

