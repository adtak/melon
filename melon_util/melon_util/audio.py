import re
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from pydub import AudioSegment


def main() -> None:
    pass


def _load_wav(path: Path) -> list[AudioSegment]:
    files = sorted(path.glob("*_lofi_*.wav"), key=lambda x: int(x.name.split("_")[0]))
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


def merge(input_path: str) -> None:
    input_dir = Path(input_path)
    audios = _load_wav(input_dir)
    combined = _combine(audios, 10)
    combined.export(input_dir / "audio.wav", format="wav")


def split(input_path: str, duration: int = 30_000) -> None:
    input_dir = Path(input_path)
    output_dir = input_dir / "split"
    output_dir.mkdir(exist_ok=True)
    for file in input_dir.glob("*.mp3"):
        logger.info(f"Split audio {file.name}")
        audio = AudioSegment.from_file(input_dir / file).set_frame_rate(44100)
        for i in range(0, len(audio), duration):
            chunk = audio[i : i + duration]
            chunk.export(
                output_dir
                / (re.sub(r"\W+", "_", file.stem) + f" - chunk{i//1000}.wav"),
                format="wav",
            )


if __name__ == "__main__":
    load_dotenv()
    main()
