import click

from hayai_cli.commands.sol_commands import sol_cli
from typing import Dict

commands: Dict = {
        #"download": download.sol_cli_download,
        #"search": search.sol_cli_search,
        "sol": sol_cli,
        #"trending": trending.sol_cli_trending
        }

@click.group(commands=commands)
def __hayai_cli__():
    pass

if __name__ == "__main__":
    __hayai_cli__()
