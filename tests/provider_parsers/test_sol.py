from hayai_cli.provider_parsers.provider_parser import *
from hayai_cli.provider_parsers.sol import Sol
from hayai_cli.provider_parsers.extractors.video_extractor import VideoContainer
from typing import Iterator
import unittest

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

        latest_shows_generator: Iterator[List[Film]] = Sol.parse_latest_shows()
        latest_shows: List[Film] = next(latest_shows_generator)

        latest_movies_generator: Iterator[List[Film]] = Sol.parse_latest_movies()
        latest_movies: List[Film] = next(latest_movies_generator)
        self.assertGreater(len(latest_shows),10);
        self.assertGreater(len(latest_movies),10)

        search_generator = Sol.parse_search("wed")
        search_results = next(search_generator)
        self.assertGreater(len(search_results),20)
        search_results = next(search_generator)
        self.assertGreater(len(search_results),0)

        trending_movies_generator: Iterator[List[Film]]= Sol.parse_trending_movies()
        trending_movies = next(trending_movies_generator)
        self.assertGreater(len(trending_movies),10)

        trending_shows_generator: Iterator[List[Film]]= Sol.parse_trending_shows()
        trending_shows = next(trending_shows_generator)
        self.assertGreater(len(trending_shows),10)

        coming_soon_generator: Iterator[List[Film]] = Sol.parse_coming_soon()
        coming_soon = next(coming_soon_generator)

        parse_category_generator: Iterator[List[Film]] = Sol.parse_category("coming soon")
        coming_soon_category: List[Film] = next(parse_category_generator)
        self.assertEqual(coming_soon[-1].title,coming_soon_category[-1].title)
        info: Info = Sol.parse_info("https://solarmovie.pe/movie/watch-avatar-free-19690")
        self.assertEqual(info.title,"avatar")
        self.assertEqual(info.description,"In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.")
        self.assertEqual(info.release,"2009-12-10")
