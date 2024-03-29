import os
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    img_path = Path(os.environ["PROJECT_PATH"])
    img_name = "image.png"
    img = Image.open(img_path / img_name)
    font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 128)
    ImageDraw.Draw(img).text(
        (540, 960),
        "AI Chill Beats",
        "white",
        font=font,
        anchor="md",
    )
    img.save(img_path / ("font_" + img_name))


if __name__ == "__main__":
    load_dotenv()
    main()
