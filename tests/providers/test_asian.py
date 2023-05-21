from hayai_cli.providers import VideoServer
from hayai_cli.providers import Episode
from hayai_cli.providers import FilmInfo
from hayai_cli.providers.extractors.video_extractor import VideoContainer
from typing import List
import unittest

from hayai_cli.providers.provider import Page
from hayai_cli.providers.asian import Asian

class TestAsian(unittest.TestCase):

    def test_loading_film_info(self):
        asian: Asian = Asian()
        film_info: FilmInfo = asian.load_film_info("https://asianhdplay.pro/videos/the-secret-romantic-guesthouse-2023-episode-18")
        self.assertEqual(film_info.title,"The Secret Romantic Guesthouse (2023)")
        self.assertEqual(film_info.release,"2023")
        self.assertFalse(len(film_info.description) == 0)
        self.assertEqual(film_info.duration,"unknown")
        self.assertEqual(film_info.genre,"drama")


    def test_loading_servers(self):
        asian: Asian = Asian()
        episodes: List[Episode] = asian.load_episodes("the-secret-romantic-guesthouse-2023-episode-18")
        self.assertGreater(len(episodes),0)
        episode_servers: List[VideoServer] = asian.load_episode_servers(episodes[0].episode_id)
        self.assertGreater(len(episode_servers),0)
        video_container: VideoContainer = asian.load_video(episode_servers[0])
        self.assertGreater(len(video_container.videos),0)

    def test_loading_home(self):
        asian: Asian = Asian()
        home_page: Page = asian.load_home()
        self.assertGreater(len(home_page.films),20);
        self.assertTrue(home_page.page_info.has_next_page)
        self.assertEqual(home_page.page_info.current_page,1)
        self.assertGreater(home_page.page_info.last_page,1)

    def test_loading_movies(self):
        asian: Asian = Asian()
        movies_page: Page = asian.load_movies()
        self.assertGreater(len(movies_page.films),20);
        self.assertTrue(movies_page.page_info.has_next_page)
        self.assertEqual(movies_page.page_info.current_page,1)
        self.assertGreater(movies_page.page_info.last_page,1)

    def test_loading_shows(self):
        asian: Asian = Asian()
        shows_page: Page = asian.load_shows()
        self.assertGreater(len(shows_page.films),20);
        self.assertTrue(shows_page.page_info.has_next_page)
        self.assertEqual(shows_page.page_info.current_page,1)
        self.assertGreater(shows_page.page_info.last_page,1)

    def test_loading_recently_added_raw(self):
        asian: Asian = Asian()
        recently_added_raw_page: Page = asian.load_recently_added_raw()
        self.assertGreater(len(recently_added_raw_page.films),10);
        self.assertTrue(recently_added_raw_page.page_info.has_next_page)
        self.assertEqual(recently_added_raw_page.page_info.current_page,1)
        self.assertGreater(recently_added_raw_page.page_info.last_page,1)

    def test_loading_popular_drama(self):
        asian: Asian = Asian()
        popular_drama_page: Page = asian.load_popular_drama()
        self.assertGreater(len(popular_drama_page.films),20);
        self.assertTrue(popular_drama_page.page_info.has_next_page)
        self.assertEqual(popular_drama_page.page_info.current_page,1)
        self.assertGreater(popular_drama_page.page_info.last_page,1)

    def test_loading_ongoing_series(self):
        asian: Asian = Asian()
        ongoing_series_page: Page = asian.load_ongoing_series()
        self.assertGreater(len(ongoing_series_page.films),20);
        self.assertTrue(ongoing_series_page.page_info.has_next_page)
        self.assertEqual(ongoing_series_page.page_info.current_page,1)
        self.assertGreater(ongoing_series_page.page_info.last_page,1)

