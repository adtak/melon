from pathlib import Path

from moviepy.editor import CompositeVideoClip, ImageClip


def main() -> None:
    project_path = Path()
    image = ImageClip(project_path / "image.png", duration=5)
    image = image.set_position(lambda t: ("center", t * 10 + 50))
    image.fps = 30
    composite = CompositeVideoClip([image], size=image.size)
    composite.write_videofile("video.mp4")


if __name__ == "__main__":
    main()
