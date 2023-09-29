import os
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    img_path = Path(os.environ["PROJECT_PATH"])
    img_name = "image.png"
    img = Image.open(img_path / img_name)
    font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 200)
    ImageDraw.Draw(img).text(
        (960, 540),
        "Mix",
        "white",
        font=font,
        anchor="mm",
    )
    img.save(img_path / ("font_" + img_name))


if __name__ == "__main__":
    load_dotenv()
    main()
