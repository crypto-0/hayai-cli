from .provider import *
from typing import List, Optional 
import requests
import lxml.html
from .extractors.video_extractor import *
from .extractors.multiquality import *
from dataclasses import replace

class Asian(Provider):
    _host_url: str = "https://asianhdplay.pro"
    _extractors: Dict = {
            "Multiquality Server": Multiquality("https://asianhdplay.pro/encrypt-ajax.php")
            }

    def __init__(self) -> None:
        super().__init__()


    def load_seasons(self, film_id: str) -> List[Season]:
        return [Season("1",film_id)]

    def load_episodes(self,season_id: str) -> List[Episode]:
        episodes_url: str = f"{self._host_url}/videos/{season_id}"
        try:
            r = requests.get(episodes_url,headers=self._headers)
            html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
            episode_elements:List[lxml.html.HtmlElement] = html_doc.cssselect(".lists .video-block")
            episodes : List[Episode] = []
            for episode_element in episode_elements:
                episode_title:str = episode_element.cssselect(".name")[0].text
                episode_title = episode_title.strip()
                episode_number: str = episode_title.rsplit(" ",1)[-1]
                episode_id: str = episode_element.cssselect("a")[0].get("href").rsplit("/",1)[-1]
                episodes.append(Episode(episode_number,episode_title,episode_id))
            episodes.sort(key= lambda x: x.episode_number)
            return episodes
        except Exception as e:
            return []

    def load_servers(self,ID: str) -> List[VideoServer]:
        video_url: str = f"{self._host_url}/videos/{ID}"
        try:
            r : requests.Response = requests.get(video_url,headers=self._headers)
            r.raise_for_status()
            html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
            server_url: str = html_doc.cssselect("iframe")[0].get("src")
            server_url = "https:" + server_url
        except Exception as e:
            return []
        try:
            r : requests.Response = requests.get(server_url,headers=self._headers)
            r.raise_for_status()
            html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
            server_elements : List[lxml.html.HtmlElement] = html_doc.cssselect(".linkserver")
            servers: List[VideoServer] = [] 
            for server_element in server_elements:
                server_id: str = server_element.get("data-video")
                server_title: str = server_element.text
                if server_title in self._extractors:
                    servers.append(VideoServer(server_title,server_id))
            return servers
        except Exception as e:
            return []
    

    def load_episode_servers(self,episode_id: str) -> List[VideoServer]:
        return self.load_servers(episode_id)

    def load_movie_servers(self,movie_id: str) -> List[VideoServer]:
        return self.load_servers(movie_id)

    def load_video(self,server: VideoServer):
        extractor: Optional[VideoExtractor] = self._extractors.get(server.name)
        if extractor is None:
            return VideoContainer([],[])
        return extractor.extract(server.server_id)


    def load_home(self):
        url = f"{self._host_url}"
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            print(e)
            return Page(PageInfo(),[])
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        pagination_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination li")
        page_info: PageInfo = self.parse_pagination_elements(pagination_elements)
        video_block_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".video-block")
        films: List[Film] = list(map(self.parse_video_block_element,video_block_items))
        return Page(page_info,films)
        
    def load_movies(self,page_number=1):
        url = f"{self._host_url}/movies?page={page_number}"
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(),[])
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        pagination_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination li")
        page_info: PageInfo = self.parse_pagination_elements(pagination_elements)
        video_block_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".video-block")
        films: List[Film] = list(map(self.parse_video_block_element,video_block_items))
        for i in range(len(films)):
            films[i] = replace(films[i],film_type="movie")
        return Page(page_info,films)

    def load_shows(self,page_number=1):
        url = f"{self._host_url}/kshow?page={page_number}"
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(),[])
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        pagination_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination li")
        page_info: PageInfo = self.parse_pagination_elements(pagination_elements)
        video_block_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".video-block")
        films: List[Film] = list(map(self.parse_video_block_element,video_block_items))
        return Page(page_info,films)

    def load_recently_added_raw(self,page_number=1):
        url = f"{self._host_url}/recently-added-raw?page={page_number}"
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(),[])
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        pagination_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination li")
        page_info: PageInfo = self.parse_pagination_elements(pagination_elements)
        video_block_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".video-block")
        films: List[Film] = list(map(self.parse_video_block_element,video_block_items))
        return Page(page_info,films)

    def load_popular_drama(self,page_number=1):
        url = f"{self._host_url}/popular?page={page_number}"
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(),[])
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        pagination_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination li")
        page_info: PageInfo = self.parse_pagination_elements(pagination_elements)
        video_block_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".video-block")
        films: List[Film] = list(map(self.parse_video_block_element,video_block_items))
        return Page(page_info,films)

    def load_ongoing_series(self,page_number=1):
        url = f"{self._host_url}/ongoing-series?page={page_number}"
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(),[])
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        pagination_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination li")
        page_info: PageInfo = self.parse_pagination_elements(pagination_elements)
        video_block_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".video-block")
        films: List[Film] = list(map(self.parse_video_block_element,video_block_items))
        return Page(page_info,films)

    def load_search(self,query: str,page_number: int = 1) -> Page :
        query = query.strip().replace(" ","-")
        search_url: str = f"{self._host_url}/search.html?keyword={query}&page={page_number}"
        try:
            r: requests.Response = requests.get(search_url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(1,1,False),[])
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        pagination_elements: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination li")
        page_info: PageInfo = self.parse_pagination_elements(pagination_elements)
        video_block_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".video-block")
        films: List[Film] = list(map(self.parse_video_block_element,video_block_items))
        return Page(page_info,films)

    def load_film_info(self,url: str) -> FilmInfo:
        try:
            r = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return FilmInfo()
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        title: str = html_doc.cssselect(".video-details .date")[0].text
        title = title.rsplit("(")[0]
        title = title.strip()
        description_element: lxml.html.HtmlElement = html_doc.cssselect(".video-details .post-entry p")
        description: str = description_element[0].text if description_element else ""
        country: str = "asian"
        release: str = title.rsplit(" ", 1)[-1]
        release = release.strip("()")
        duration: str = "unknown"
        video_block_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".video-info-right .video-block")
        recommendations: List[Film] = list(map(self.parse_video_block_element,video_block_items))
        poster_image: bytes = bytes()
        genre: str = "drama"

        return FilmInfo(title=title,release=release,description=description.strip(),genre=genre,country=country,duration=duration,recommendation=recommendations,poster_image=poster_image)


    def parse_video_block_element(self,element: lxml.html.HtmlElement) -> Film:
        poster_url: str = element.cssselect(".picture > img")[0].get("src")
        title: str = element.cssselect(".name")[0].text
        title = title.strip()
        link: str = element.cssselect("a")[0].get("href")
        film_info_tags: List[lxml.html.HtmlElement] = element.cssselect(".date")
        
        extra_details: str = ""
        for info_tag in film_info_tags:
            extra_details += (info_tag.text + " . ") if info_tag.text is not None else ""
        extra_details = extra_details.strip()
        extra_details = extra_details.strip(" . ")
        film_type: str = "tv"
        film_id: str = link.rsplit("/")[-1]

        return Film(title,self._host_url + link,film_type,poster_url=poster_url,extra= extra_details,film_id=film_id)

    def parse_pagination_elements(self,elements: List[lxml.html.HtmlElement]) -> PageInfo:
        current_page: int = 1
        last_page: int = 1
        has_next_page: bool = False

        for page_item in elements:
            class_name: str = page_item.get("class","")
            a_tag: lxml.html.HtmlElement =  page_item.cssselect("a")[0]
            if class_name.endswith("active"):
                current_page = int(a_tag.get("data-page"))
            elif class_name.endswith("next"):
                has_next_page = True
        if elements:
            a_tag: lxml.html.HtmlElement =  elements[-1].cssselect("a")[0]
            last_page =  int(a_tag.get("data-page"))

        return PageInfo(current_page,last_page,has_next_page)

