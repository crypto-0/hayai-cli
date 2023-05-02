from providers import VideoServer
from providers import Episode
from providers.extractors.video_extractor import VideoContainer
from typing import List
import unittest

from providers.provider import Page
from providers.zoro import Zoro

class TestZoro(unittest.TestCase):

    def test_loading_servers(self):
        zoro: Zoro = Zoro()
        episodes: List[Episode] = zoro.load_episodes("112")
        self.assertGreater(len(episodes),0)
        episode_servers: List[VideoServer] = zoro.load_episode_servers(episodes[0].episode_id)
        self.assertGreater(len(episode_servers),0)
        video_container: VideoContainer = zoro.load_video(episode_servers[1])
        self.assertGreater(len(video_container.videos),0)

    def test_loading_home(self):
        zoro: Zoro = Zoro()
        home_page: Page = zoro.load_home()
        self.assertGreater(len(home_page.films),20);
        self.assertFalse(home_page.page_info.has_next_page)
        self.assertEqual(home_page.page_info.current_page,1)
        self.assertEqual(home_page.page_info.last_page,1)


    def test_loading_movies(self):
        zoro: Zoro = Zoro()
        movies_page: Page = zoro.load_movies()
        self.assertGreater(len(movies_page.films),10);
        self.assertTrue(movies_page.page_info.has_next_page)
        self.assertEqual(movies_page.page_info.current_page,1)
        self.assertGreater(movies_page.page_info.last_page,1)

    def test_loading_shows(self):
        zoro: Zoro = Zoro()
        shows_page: Page = zoro.load_shows()
        self.assertGreater(len(shows_page.films),10);
        self.assertTrue(shows_page.page_info.has_next_page)
        self.assertEqual(shows_page.page_info.current_page,1)
        self.assertGreater(shows_page.page_info.last_page,1)

    def test_loading_subbed_anime(self):
        zoro: Zoro = Zoro()
        subbed_anime_page: Page = zoro.load_subbed_anime()
        self.assertGreater(len(subbed_anime_page.films),10);
        self.assertTrue(subbed_anime_page.page_info.has_next_page)
        self.assertEqual(subbed_anime_page.page_info.current_page,1)
        self.assertGreater(subbed_anime_page.page_info.last_page,1)

    def test_loading_dubbed_anime(self):
        zoro: Zoro = Zoro()
        dubbed_anime_page: Page = zoro.load_dubbed_anime()
        self.assertGreater(len(dubbed_anime_page.films),10);
        self.assertTrue(dubbed_anime_page.page_info.has_next_page)
        self.assertEqual(dubbed_anime_page.page_info.current_page,1)
        self.assertGreater(dubbed_anime_page.page_info.last_page,1)

    def test_loading_most_popular(self):
        zoro: Zoro = Zoro()
        most_popular_page: Page = zoro.load_most_popular()
        self.assertGreater(len(most_popular_page.films),10);
        self.assertTrue(most_popular_page.page_info.has_next_page)
        self.assertEqual(most_popular_page.page_info.current_page,1)
        self.assertGreater(most_popular_page.page_info.last_page,1)
