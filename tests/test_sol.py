from providers import VideoServer
from providers import Season
from providers import Episode
from providers.extractors.video_extractor import VideoContainer
from typing import List
import unittest

from providers import FilmInfo
from providers.provider import Page
from providers.sol import Sol

class TestSol(unittest.TestCase):

    def test_parsing_servers(self):
        sol: Sol = Sol()
        #blackadams
        movie_servers: List[VideoServer] = sol.load_movie_servers("82087")

        #wednesday show
        seasons: List[Season] = sol.load_seasons("90553")
        self.assertGreater(len(movie_servers),0)
        self.assertGreater(len(seasons),0)

        episodes: List[Episode] = sol.load_episodes(seasons[0].id)
        self.assertGreater(len(episodes),0)
        episode_servers: List[VideoServer] = sol.load_episode_servers(episodes[0].id)
        self.assertGreater(len(episode_servers),0)
        container: VideoContainer = sol.extract_server(episode_servers[0].name,episode_servers[0].embed)
        self.assertGreater(len(container.videos),0)
        self.assertGreater(len(container.subtitles),0)

    def test_parsing_catogories(self):
        sol: Sol = Sol()
        home_page: Page = sol.load_home()
        self.assertFalse(home_page.pageInfo.has_next_page)
        self.assertEqual(home_page.pageInfo.current_page,1)
        self.assertEqual(home_page.pageInfo.last_page,1)

        movies_page: Page = sol.load_movies()
        self.assertGreater(len(movies_page.films),10);
        self.assertTrue(movies_page.pageInfo.has_next_page)
        self.assertEqual(movies_page.pageInfo.current_page,1)
        self.assertGreater(movies_page.pageInfo.last_page,1)

        shows_page: Page = sol.load_shows()
        self.assertGreater(len(shows_page.films),10);
        self.assertTrue(shows_page.pageInfo.has_next_page)
        self.assertEqual(shows_page.pageInfo.current_page,1)
        self.assertGreater(shows_page.pageInfo.last_page,1)

        imdb_page: Page = sol.load_imdb()
        self.assertGreater(len(imdb_page.films),10);
        self.assertTrue(imdb_page.pageInfo.has_next_page)
        self.assertEqual(imdb_page.pageInfo.current_page,1)
        self.assertGreater(imdb_page.pageInfo.last_page,1)

        info: FilmInfo = sol.load_film_info("https://solarmovie.pe/movie/watch-avatar-free-19690")
        self.assertEqual(info.title,"avatar")
        self.assertEqual(info.description,"In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.")
        self.assertEqual(info.release,"2009-12-10")
