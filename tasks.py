from invoke import task

@task
def start(ctx):
    """Start the algorithm."""
    ctx.run("python3 src/main.py")

@task
def play(ctx):
    """Play the game."""
    ctx.run("python3 src/human_playtest.py")
