import json
import os

from src.renamer_utils import FileRenamer
from src.scrape_episode_names_from_wiki import get_episode_titles


def scrape_episodes_name_from_wiki(wiki_url: str, output_name: str) -> str:
    episodes = get_episode_titles(url=wiki_url)
    output = f"./wiki_data/{output_name}.json"
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(episodes, f, ensure_ascii=False, indent=2)

    print(f"Saved episode list to {output}")

    return output


def rename_files_and_move_to_folders(raw_data_folder: str, show_name: str, add_names: bool, episode_names_path: str):
    renamer = FileRenamer(raw_data_folder, show_name,
                          add_names, episode_names_path)
    renamer.process_files()

    print(f"Processed files in {raw_data_folder}")
