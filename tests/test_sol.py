from provider_parsers import VideoServer
from provider_parsers import Season
from provider_parsers import Episode
from provider_parsers import Sol
from provider_parsers import Film
from provider_parsers.extractors.video_extractor import VideoContainer
from typing import Iterator, Optional
from typing import List
from itertools import islice
import unittest

from provider_parsers.provider_parser import FilmInfo

class TestSol(unittest.TestCase):

    def test_parsing_servers(self):
        #blackadams
        movie_servers: List[VideoServer] = Sol.parse_movie_servers("82087")

        #wednesday show
        seasons: List[Season] = Sol.parse_seasons("90553")
        self.assertIsNotNone(movie_servers)
        self.assertIsNotNone(seasons)
        self.assertGreater(len(movie_servers),0)
        self.assertGreater(len(seasons),0)

        episodes: List[Episode] = Sol.parse_episodes(seasons[0].id)
        self.assertIsNotNone(episodes)
        self.assertGreater(len(episodes),0)
        episode_servers: List[VideoServer] = Sol.parse_episode_servers(episodes[0].id)
        self.assertIsNotNone(episode_servers)
        self.assertGreater(len(episode_servers),0)
        self.assertIsNotNone(episode_servers[0].extractor)
        container: VideoContainer = episode_servers[0].extractor.extract(episode_servers[0].embed)
        self.assertGreater(len(container.videos),0)
        self.assertGreater(len(container.subtitles),0)

    def test_parsing_catogories(self):

        latest_shows_generator: Iterator[Film] = Sol.parse_latest_shows()
        latest_shows: List[Film] = list(islice(latest_shows_generator,6))
        self.assertGreater(len(latest_shows),5);

        latest_movies_generator: Iterator[Film] = Sol.parse_latest_movies()
        latest_movies: List[Film] = list(islice(latest_movies_generator,6))
        self.assertGreater(len(latest_movies),5)

        search_generator = Sol.parse_search("wed")
        search_results: List[Film] = list(islice(search_generator,6))
        self.assertGreater(len(search_results),5)

        trending_movies_generator: Iterator[Film]= Sol.parse_trending_movies()
        trending_movies = list(islice(trending_movies_generator,6))
        self.assertGreater(len(trending_movies),5)

        trending_shows_generator: Iterator[Film]= Sol.parse_trending_shows()
        trending_shows: List[Film] = list(islice(trending_shows_generator,6))
        self.assertGreater(len(trending_shows),5)

        movies_generator: Iterator[Film]= Sol.parse_movies()
        movies: List[Film] = list(islice(movies_generator,6))
        self.assertGreater(len(movies),5)

        shows_generator: Iterator[Film]= Sol.parse_shows()
        shows: List[Film] = list(islice(shows_generator,6))
        self.assertGreater(len(shows),5)

        parse_category_generator: Optional[Iterator[Film]] = Sol.parse_category("coming soon")
        if parse_category_generator is not None:
            coming_soon_category: List[Film] = list(islice(parse_category_generator,6))
            self.assertEqual(coming_soon_category[-1].title,coming_soon_category[-1].title)
            info: FilmInfo = Sol.parse_info("https://solarmovie.pe/movie/watch-avatar-free-19690")
            self.assertEqual(info.title,"avatar")
            self.assertEqual(info.description,"In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.")
            self.assertEqual(info.release,"2009-12-10")
