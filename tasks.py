from invoke import task
from sys import executable
from os import name
use_pty = name != "nt"

@task
def start(ctx):
    """Start the algorithm."""
    ctx.run(f"{executable} src/main.py", pty=use_pty)

@task
def play(ctx):
    """Play the game."""
    ctx.run(f"{executable} src/human_playtest.py", pty=use_pty)
