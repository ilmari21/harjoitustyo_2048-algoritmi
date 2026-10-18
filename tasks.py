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

@task
def test(ctx):
    """Run the tests."""
    ctx.run("pytest src", pty=use_pty)

@task
def coverage(ctx):
    """Run the tests with coverage."""
    ctx.run("coverage run --branch -m pytest src", pty=use_pty)

@task(coverage)
def coverage_report(ctx):
    """Generate a coverage report as HTML."""
    ctx.run("coverage html", pty=use_pty)

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src", pty=use_pty)

@task
def lint(ctx):
    ctx.run("pylint src", pty=use_pty)
