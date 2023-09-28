import re
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from pydub import AudioSegment


def main() -> None:
    pass


def _load_wav(file_path: Path) -> list[AudioSegment]:
    files = sorted(
        file_path.glob("*_lofi_*.wav"),
        key=lambda x: int(x.name.split("_")[0]),
    )
    logger.debug([f.name for f in files])
    return [AudioSegment.from_wav(audio_path) for audio_path in files]


def _combine(audios: list[AudioSegment], fade_sec: int) -> AudioSegment:
    combined = AudioSegment.empty()
    for audio in audios:
        combined += _fade_inout(audio, fade_sec)
        combined += AudioSegment.silent(duration=100)
    return combined


def _fade_inout(audio: AudioSegment, fade_sec: int) -> AudioSegment:
    return audio.fade_in(fade_sec * 1000).fade_out(fade_sec * 1000)


def merge(input_dir: str) -> None:
    input_path = Path(input_dir)
    audios = _load_wav(input_path)
    combined = _combine(audios, 10)
    combined.export(input_path / "audio.wav", format="wav")


def split(input_dir: str, duration: int = 30_000) -> None:
    input_path = Path(input_dir)
    output_path = input_path / "split"
    output_path.mkdir(exist_ok=True)
    for file in input_path.glob("*.mp3"):
        logger.info(f"Split audio {file.name}")
        audio = AudioSegment.from_file(input_path / file).set_frame_rate(44100)
        for i in range(0, len(audio), duration):
            chunk = audio[i : i + duration]
            chunk.export(
                output_path
                / (re.sub(r"\W+", "_", file.stem) + f" - chunk{i//1000}.wav"),
                format="wav",
            )


if __name__ == "__main__":
    load_dotenv()
    main()
