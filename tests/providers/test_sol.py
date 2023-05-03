from hayai_cli.providers import VideoServer
from hayai_cli.providers import Season
from hayai_cli.providers import Episode
from hayai_cli.providers.extractors.video_extractor import VideoContainer
from typing import List
import unittest

from hayai_cli.providers import FilmInfo
from hayai_cli.providers.provider import Page
from hayai_cli.providers.sol import Sol

class TestSol(unittest.TestCase):

    def test_loading_servers(self):
        sol: Sol = Sol()
        #blackadams
        movie_servers: List[VideoServer] = sol.load_movie_servers("82087")

        #wednesday show
        seasons: List[Season] = sol.load_seasons("90553")
        self.assertGreater(len(movie_servers),0)
        self.assertGreater(len(seasons),0)

        episodes: List[Episode] = sol.load_episodes(seasons[0].season_id)
        self.assertGreater(len(episodes),0)
        episode_servers: List[VideoServer] = sol.load_episode_servers(episodes[0].episode_id)
        self.assertGreater(len(episode_servers),0)
        container: VideoContainer = sol.extract_server(episode_servers[0].name,episode_servers[0].server_id)
        self.assertGreater(len(container.videos),0)
        self.assertGreater(len(container.subtitles),0)

    def test_loading_home(self):
        sol: Sol = Sol()
        home_page: Page = sol.load_home()
        self.assertGreater(len(home_page.films),50);
        self.assertFalse(home_page.page_info.has_next_page)
        self.assertEqual(home_page.page_info.current_page,1)
        self.assertEqual(home_page.page_info.last_page,1)

    def test_loading_movies(self):
        sol: Sol = Sol()
        movies_page: Page = sol.load_movies()
        self.assertGreater(len(movies_page.films),10);
        self.assertTrue(movies_page.page_info.has_next_page)
        self.assertEqual(movies_page.page_info.current_page,1)
        self.assertGreater(movies_page.page_info.last_page,1)

    def test_loading_shows(self):
        sol: Sol = Sol()
        shows_page: Page = sol.load_shows()
        self.assertGreater(len(shows_page.films),10);
        self.assertTrue(shows_page.page_info.has_next_page)
        self.assertEqual(shows_page.page_info.current_page,1)
        self.assertGreater(shows_page.page_info.last_page,1)

    def test_loading_imdb(self):
        sol: Sol = Sol()
        imdb_page: Page = sol.load_imdb()
        self.assertGreater(len(imdb_page.films),10);
        self.assertTrue(imdb_page.page_info.has_next_page)
        self.assertEqual(imdb_page.page_info.current_page,1)
        self.assertGreater(imdb_page.page_info.last_page,1)

    def test_loading_film_info(self):
        sol: Sol = Sol()
        info: FilmInfo = sol.load_film_info("https://solarmovie.pe/movie/watch-avatar-free-19690")
        self.assertEqual(info.title,"avatar")
        self.assertEqual(info.description,"In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.")
        self.assertEqual(info.release,"2009-12-10")
