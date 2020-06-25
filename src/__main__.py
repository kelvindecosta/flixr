from flixr.interface import Interface
from flixr.api import parse, search
from flixr.display import formatted


def main():
    print(formatted(parse(search(Interface()()))))


if __name__ == "__main__":
    main()
