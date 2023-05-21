import click
from hayai_cli.commands import zoro_cli
from hayai_cli.commands import sol_cli
from hayai_cli.commands import asian_cli
from typing import Dict

commands: Dict = {
        "sol": sol_cli,
        "zoro": zoro_cli,
        "asian": asian_cli
        }

@click.group(commands=commands)
def __hayai_cli__():
    pass

if __name__ == "__main__":
    __hayai_cli__()
