import argparse

__all__ = ["Interface"]


class Interface:
    """
    A wrapper for the command line interface.
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="flixr",
            description="A command line utility for television show information.",
        )

        self.parser.add_argument("show", help="TV show name")

    def __call__(self):
        return vars(self.parser.parse_args()).get("show")
