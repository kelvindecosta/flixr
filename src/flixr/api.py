import asyncio
import json
import requests

__all__ = ["parse", "search"]

BASE_URL = "https://api.tvmaze.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
}


def search(query):
    """
    Searches for a single show based on the query string.

    Args:
        query (str): search query

    Returns:
        dict: dictionary from parsing JSON response
    """

    try:
        response = requests.get(
            f"{BASE_URL}/singlesearch/shows?q={query}", headers=HEADERS
        )
        response.raise_for_status()

        return json.loads(response.content)
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            raise SystemExit(f"No TV show for query '{query}'")
        raise SystemExit(err)


def parse(result):
    """
    Returns selected information about a show based on a search result.

    Args:
        result (dict): search result

    Returns:
        dict: dictionary of information about the show.
    """
    show = {}

    # Title, URL, Genres
    show["title"] = result["name"]
    show["url"] = result["_links"]["self"]["href"]
    show["genres"] = result["genres"]

    # Status
    show["status"] = result["status"] == "Running"

    # Network
    network = result.get("network")
    show["network"] = network["name"] if network is not None else None

    # Retrieve '/cast', '/crew' & '/episodes'
    async def run():
        loop = asyncio.get_event_loop()
        responses = {}

        for sub in ["cast", "crew", "episodes"]:
            responses[sub] = await loop.run_in_executor(
                None, requests.get, f"{show['url']}/{sub}", HEADERS
            )

        return responses

    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(run())
    responses = {k: json.loads(v.content) for k, v in responses.items()}

    # Cast
    show["cast"] = list(
        dict.fromkeys(member["person"]["name"] for member in responses["cast"]).keys()
    )

    # Creators
    show["creators"] = list(
        dict.fromkeys(
            member["person"]["name"]
            for member in responses["crew"]
            if member["type"] == "Creator"
        ).keys()
    )

    # Activity Period
    start_year = int(result["premiered"][:4])
    end_year = int(responses["episodes"][-1]["airdate"][:4])
    show["period"] = (
        f"Since {start_year}" if show["status"] else f"{start_year} - {end_year}"
    )

    # Link
    show["link"] = result["officialSite"]

    return show
