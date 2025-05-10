import json
import os
import re
import shutil
from pathlib import Path

# common video file extensions
VIDEO_EXTENSIONS = {'mp4', 'mkv', 'avi', 'mov', 'flv', 'webm'}

# pattern to match season and episode number
PATTERN = r"(?:[sS])?(\d{1,2})[eExX](\d{1,2})(?!\d)"


class VideoFile:
    def __init__(self, filename: str, show_name: str, episode_dict: dict) -> None:
        self.filename = filename
        _, extension = os.path.splitext(filename)
        self.suffix = extension.lstrip(".")
        self.show_name = show_name
        self.season = None
        self.episode = None
        self.new_name = None
        self.season_folder = None

        self.extract_season_episode()
        self.generate_new_name(episode_dict)

    def extract_season_episode(self) -> None:
        """Extracts season and episode numbers from the filename using regex"""
        match = re.search(PATTERN, self.filename)
        if match:
            self.season = match.group(1).zfill(2)
            self.episode = match.group(2).zfill(2)

    def generate_new_name(self, episode_name_dict: dict) -> None:
        """Generates the new filename based on prefix, season, and episode"""
        if self.season is not None and self.episode is not None:
            ep_name = self.add_episode_name(episode_name_dict)
            self.new_name = f"{self.show_name}_S{self.season}E{self.episode}{ep_name}.{self.suffix}"
            self.season_folder = f"S{self.season}"

    def is_video_file(self) -> bool:
        """Checks if a file is a video based on its extension"""
        return self.suffix.lower() in VIDEO_EXTENSIONS

    def add_episode_name(self, episode_name_dict: dict) -> str:
        if not episode_name_dict:
            return ""
        s, e = int(self.season), int(self.episode)
        try:
            name = episode_name_dict[str(s)][str(e)]
            return f"_{self.sanitize_filename(name)}"
        except KeyError:
            return ""

    @staticmethod
    def sanitize_filename(text: str) -> str:
        text = text.replace(" ", "_")
        text = re.sub(r'[\\/:"*?<>|]', '', text)
        text = re.sub(r'_+', '_', text)

        return text.strip('_')


class FileRenamer:
    def __init__(self, folder: str, show_name: str, add_names: bool, episode_names_path: str):
        self.folder = folder
        self.show_name = show_name
        self.renamed_files = set()
        self.add_names = add_names
        self.episode_name_dict = self.load_data(episode_names_path)

    def create_season_folder(self, season_folder: str) -> str:
        """Creates a season folder if it does not exist"""
        season_folder_path = os.path.join(self.folder, season_folder)
        if not os.path.exists(season_folder_path):
            os.makedirs(season_folder_path)
        return season_folder_path

    def rename_and_move(self, video_file: VideoFile):
        """Renames and moves the video file to its season folder"""
        if not video_file.new_name:
            return  # file that does not match the pattern

        # define source and destination paths
        src = os.path.join(self.folder, video_file.filename)
        dst = os.path.join(self.folder, video_file.new_name)

        # rename the file
        os.rename(src, dst)

        # create season folder and move the file there
        if not self.is_in_season_folder(src):
            season_folder_path = self.create_season_folder(
                video_file.season_folder)
            shutil.move(dst, os.path.join(
                season_folder_path, video_file.new_name))

        # track the renamed file
        self.renamed_files.add(video_file.new_name)

    @staticmethod
    def is_in_season_folder(filepath: Path) -> bool:
        parent_folder = os.path.basename(os.path.dirname(filepath))
        return re.fullmatch(r"S\d{2}", parent_folder) is not None

    def load_data(self, path: str) -> dict:
        if self.add_names:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}

        return data

    def process_files(self):
        """Processes all video files in the folder"""
        for filename in os.listdir(self.folder):
            if not os.path.isfile(os.path.join(self.folder, filename)):
                continue
            video_file = VideoFile(
                filename, self.show_name, self.episode_name_dict)
            if not video_file.is_video_file():
                continue  # skip non-video files

            if video_file.season is not None and video_file.episode is not None:
                self.rename_and_move(video_file)
            else:
                print(f"Skipping file (no season/episode found): {filename}")
