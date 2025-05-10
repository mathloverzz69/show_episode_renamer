# Show Episode Renamer

**`Show Episode Renamer`** is a Python utility designed to help organize and rename TV show episode files in your media library to a consistent, uniform format. The tool identifies and renames files using various episode naming patterns (like `S01E01`, `1x02`, `3e5`) and optionally includes episode titles for clarity.

## Features

- **Uniform Naming**: Detects episode patterns and renames them to a consistent format like `S01E01_Title`.
- **Season Folders**: Automatically organizes episodes into season-specific folders (e.g., `S01/`, `S02/`).
- **Supports Multiple Patterns**: Handles various episode naming schemes, such as `S01E01`, `1x02`, and `3e5`.
- **Customizable Filenames**: Optionally integrates episode titles scraped from Wikipedia page.  

## Example Output

### Before renaming:
- Friends.S01E01.mkv  
- Friends.S01x02.mkv  
- friends.s02e03.avi  

### After renaming:
- S01E01_Pilot.mkv  
- S01E02_The_One_With_The_Sonogram_at_the_End.mkv  
- S02E03_The_One_With_the_Prom_Video.mkv

## 👤 Author
Created by @mathloverzz69. 


