import os
from pathlib import Path

import yt_dlp
from dotenv import load_dotenv
from loguru import logger


def main(output_dir: str, playlist_url: str) -> None:
    params = {
        "format": "bestaudio/best",
        "outtmpl": str(Path(output_dir) / "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            },
        ],
        "quiet": True,
        "extract_flat": True,
    }
    with yt_dlp.YoutubeDL(params) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        entries = playlist_info.get("entries", [])
        for i, entry in enumerate(entries):
            logger.info(
                f"Extracting {entry['title']} {entry['url']} ({i+1}/{len(entries)})",
            )
            try:
                ydl.download([entry["url"]])
            except yt_dlp.DownloadError:
                logger.info(f"Failed to download {entry['url']}")


if __name__ == "__main__":
    load_dotenv()
    main(
        "./outputs",
        os.environ["PLAYLIST_URL"],
    )
