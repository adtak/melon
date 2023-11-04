from pathlib import Path

from moviepy.editor import (
    CompositeVideoClip,
    ImageClip,
    VideoFileClip,
    concatenate_videoclips,
)


def main() -> None:
    project_path = Path("/")
    merge_movie(project_path)


def merge_movie(project_path: Path) -> None:
    clip_1 = VideoFileClip(
        str(project_path / "1_fade_video_1.mp4"),
    )
    clip_2 = VideoFileClip(
        str(project_path / "1_fade_video_2.mp4"),
    )
    clip_1 = clip_1.set_start(0).set_position((0, 0))
    clip_2 = clip_2.set_start(10).set_position((0, 0))
    merged_clip = CompositeVideoClip([clip_1, clip_2])
    merged_clip.write_videofile(str(project_path / "1_fade_video.mp4"), fps=60)


def fade_movie(project_path: Path) -> None:
    before_clip = VideoFileClip(
        str(project_path / "image-1_animation.mp4"),
    ).loop(duration=18)
    change_clip = VideoFileClip(
        str(project_path / "image-2_animation.mp4"),
    ).loop(duration=18)
    before_clip = before_clip.set_start(0).set_position((0, 0))
    change_clip = change_clip.crossfadein(12).set_start(0).set_position((0, 0))
    merged_clip = CompositeVideoClip([before_clip, change_clip])
    merged_clip.write_videofile(str(project_path / "1_fade_video_1.mp4"), fps=60)


def fade_image(project_path: Path) -> None:
    before_clip = ImageClip(str(project_path / "1_image-1-.png"), duration=20)
    change_clip = ImageClip(str(project_path / "1_image-2-.png"), duration=20)
    before_clip = before_clip.set_start(0).set_position((0, 0))
    change_clip = change_clip.crossfadein(15).set_start(0).set_position((0, 0))
    merged_clip = CompositeVideoClip([before_clip, change_clip])
    merged_clip.write_videofile(str(project_path / "1_fade_video_1.mp4"), fps=60)


def challenge(project_path: Path) -> None:
    before_clip = ImageClip(str(project_path / "image.png"), duration=8)
    change_clip = ImageClip(str(project_path / "image_c.png"), duration=0.1)
    after_clip = ImageClip(str(project_path / "image.png"), duration=3.9)
    base_clip = concatenate_videoclips(
        [before_clip, change_clip, after_clip],
        method="compose",
    )
    bar_clip = ImageClip(str(project_path / "bar.png"), duration=12)
    bar_clip = bar_clip.set_position(("center", 800))
    target_clip = ImageClip(str(project_path / "target.png"), duration=12)
    target_clip = target_clip.set_position((400, 800))
    seek_clip = ImageClip(str(project_path / "seek.png"), duration=12)
    seek_clip = seek_clip.set_position(lambda t: (t * 50, 800))
    composite = CompositeVideoClip(
        [base_clip, bar_clip, target_clip, seek_clip],
        size=base_clip.size,
    )
    composite.write_videofile(str(project_path / "challenge_video.mp4"), fps=30)


if __name__ == "__main__":
    main()
