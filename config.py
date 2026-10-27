from pathlib import Path
import os

LAUD_music_root     = Path(os.getenv("NAS") + "/Music")
LAUD_database_path  = LAUD_music_root / "laudable" / "music.sqlite3"
LAUD_html_root      = LAUD_music_root / "laudable" / "html"

