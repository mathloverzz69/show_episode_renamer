import re

import requests
from bs4 import BeautifulSoup


def get_episode_titles(url: str) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    season_data = {}

    # Find all season headers and tables together
    season_headers = soup.find_all('h3')
    previous_episode_name = ""
    for header in season_headers:
        span = header.get("id")
        if span is None or not span.startswith("Season"):
            span = ""

        match = re.search(r"Season_(\d+)", span)
        if match:
            season_number = int(match.group(1))
        else:
            season_number = None

        table = header.find_next('table', class_='wikiepisodetable')
        if season_number is None or table is None:
            continue
        else:
            episode_data = {}

            rows = table.find_all("tr")[1:]  # skip header
            for row in rows:
                cells = row.find_all("td")
                if len(cells) < 2:
                    continue

                # extract episode number
                episode_nums = cells[0].decode_contents().split('<hr/>')

                # extract title name
                title_link = cells[1].get_text()
                matches = re.findall(r'"(.*?)"', title_link)
                episode_title = matches[0] if matches else previous_episode_name

                previous_episode_name = episode_title

                for ep in episode_nums:
                    episode_data[int(ep)] = episode_title

        season_data[season_number] = episode_data

    return season_data
