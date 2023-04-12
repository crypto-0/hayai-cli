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
        movie_servers: List[VideoServer] = sol.get_movie_servers("82087")

        #wednesday show
        seasons: List[Season] = sol.get_seasons("90553")
        self.assertGreater(len(movie_servers),0)
        self.assertGreater(len(seasons),0)

        episodes: List[Episode] = sol.get_episodes(seasons[0].id)
        self.assertGreater(len(episodes),0)
        episode_servers: List[VideoServer] = sol.get_episode_servers(episodes[0].id)
        self.assertGreater(len(episode_servers),0)
        container: VideoContainer = sol.extract_server(episode_servers[0].name,episode_servers[0].embed)
        self.assertGreater(len(container.videos),0)
        self.assertGreater(len(container.subtitles),0)

    def test_parsing_catogories(self):
        sol: Sol = Sol()

        """
        latest_shows_page: Page = sol.get_category("latest shows")
        self.assertGreater(len(latest_shows_page.films),5);
        self.assertFalse(latest_shows_page.pageInfo.has_next_page)
        self.assertEqual(latest_shows_page.pageInfo.current_page,1)
        self.assertEqual(latest_shows_page.pageInfo.last_page,1)

        latest_movies_page: Page = sol.get_category("latest movies")
        self.assertGreater(len(latest_movies_page.films),5);
        self.assertFalse(latest_movies_page.pageInfo.has_next_page)
        self.assertEqual(latest_movies_page.pageInfo.current_page,1)
        self.assertEqual(latest_movies_page.pageInfo.last_page,1)

        trending_show_page: Page = sol.get_category("trending shows")
        self.assertGreater(len(trending_show_page.films),5);
        self.assertFalse(trending_show_page.pageInfo.has_next_page)
        self.assertEqual(trending_show_page.pageInfo.current_page,1)
        self.assertEqual(trending_show_page.pageInfo.last_page,1)

        trending_movies_page: Page = sol.get_category("trending movies")
        self.assertGreater(len(trending_movies_page.films),5);
        self.assertFalse(trending_movies_page.pageInfo.has_next_page)
        self.assertEqual(trending_movies_page.pageInfo.current_page,1)
        self.assertEqual(trending_movies_page.pageInfo.last_page,1)

        coming_soon_page: Page = sol.get_category("coming soon")
        self.assertGreater(len(coming_soon_page.films),5);
        self.assertFalse(coming_soon_page.pageInfo.has_next_page)
        self.assertEqual(coming_soon_page.pageInfo.current_page,1)
        self.assertEqual(coming_soon_page.pageInfo.last_page,1)

        imdb_page: Page = sol.get_category("top imdb")
        self.assertGreater(len(imdb_page.films),5);
        self.assertTrue(imdb_page.pageInfo.has_next_page)
        self.assertEqual(imdb_page.pageInfo.current_page,1)
        self.assertGreater(imdb_page.pageInfo.last_page,1)

        
        not_valid_page: Page = sol.get_category("this is not valid")
        self.assertEqual(len(not_valid_page.films),0);
        self.assertFalse(not_valid_page.pageInfo.has_next_page)
        self.assertEqual(not_valid_page.pageInfo.current_page,1)
        self.assertEqual(not_valid_page.pageInfo.last_page,1)

        info: FilmInfo = sol.get_film_info("https://solarmovie.pe/movie/watch-avatar-free-19690")
        self.assertEqual(info.title,"avatar")
        self.assertEqual(info.description,"In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.")
        self.assertEqual(info.release,"2009-12-10")
        """
