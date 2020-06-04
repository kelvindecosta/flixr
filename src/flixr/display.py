from sty import fg, ef, rs
import random

__all__ = ["formatted"]


def color(text, rgb):
    """
    Colors a string for terminal output

    Args:
        text (str): text
        rgb (tuple(int)): RGB values for color

    Returns:
        str: colored string
    """
    return f"{fg(*rgb)}{text}{fg.rs}"


def bold(text):
    """
    Increases the font weight of a string for terminal output

    Args:
        text (str): text

    Returns:
        str: bold string
    """
    return f"{ef.bold}{text}{rs.bold_dim}"


def hex2rgb(hexcode):
    """
    Converts a color's hexcode to its RGB values

    Args:
        hexcode (str): color hexcode (eg: `#fffff`)

    Returns:
        tuple(int): RGB values for color
    """
    hexcode = hexcode.strip("#")
    return [int(hexcode[i : i + 2], base=16) for i in (0, 2, 4)]


TAILWIND = {
    "red": ["#fff5f5", "#feb2b2", "#f56565", "#c53030", "#742a2a",],
    "orange": ["#fffaf0", "#fbd38d", "#ed8936", "#c05621", "#7b341e",],
    "yellow": ["#fffff0", "#faf089", "#ecc94b", "#b7791f", "#744210",],
    "green": ["#f0fff4", "#9ae6b4", "#48bb78", "#2f855a", "#22543d",],
    "teal": ["#e6fffa", "#81e6d9", "#38b2ac", "#2c7a7b", "#234e52",],
    "blue": ["#ebf8ff", "#90cdf4", "#4299e1", "#2b6cb0", "#2a4365",],
    "indigo": ["#ebf4ff", "#a3bffa", "#667eea", "#4c51bf", "#3c366b",],
    "purple": ["#faf5ff", "#d6bcfa", "#9f7aea", "#6b46c1", "#44337a",],
    "pink": ["#fff5f7", "#fbb6ce", "#ed64a6", "#b83280", "#702459",],
}


def formatted(show):
    """
    Formats the information of the show

    Args:
        show (dict): dictionary of information of the show

    Returns:
        str: formatted output
    """
    output = []

    # Chose a random color
    gradient = list(map(hex2rgb, TAILWIND[random.choice(list(TAILWIND.keys()))]))

    # title
    output.append(bold(color(show["title"], gradient[1])))

    # genre and network
    genres = list(map(lambda x: bold(color(str.lower(x), gradient[1])), show["genres"]))
    determiner = "An" if show["genres"][0][0] in "AEIOU" else "A"
    network = (
        f"on {bold(color(show['network'], gradient[2]))} "
        if show["network"] is not None
        else ""
    )
    output.append(
        f"{determiner} {', '.join(genres)} show {network}({bold(color(show['period'], gradient[1]))})"
    )

    # creators
    creators = list(map(lambda x: bold(color(x, gradient[2])), show["creators"]))
    if len(creators) == 1:
        creators = creators[0]
    elif len(creators) == 2:
        creators = " & ".join(creators)
    else:
        creators = " & ".join([", ".join(creators[:-1]), creators[-1]])
    output.append(f"Created by {creators}")

    # Cast
    cast = list(map(lambda x: bold(color(x, gradient[2])), show["cast"]))
    output.append(f"Starring {', '.join(cast[:3])} & more")

    # Watch
    link = show.get("link")
    if link is not None:
        output.append(f"Watch it here: {color(link, gradient[1])}")

    return "\n".join(output)
