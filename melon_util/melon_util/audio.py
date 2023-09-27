import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from pydub import AudioSegment


def main() -> None:
    path = Path(os.environ["PROJECT_PATH"])
    audios = load_wav(path)
    combined = combine(audios, 10)
    combined.export(path / "audio.wav", format="wav")


def load_wav(path: Path) -> list[AudioSegment]:
    files = sorted(path.glob("*_lofi_*.wav"), key=lambda x: int(x.name.split("_")[0]))
    logger.debug([f.name for f in files])
    return [AudioSegment.from_wav(audio_path) for audio_path in files]


def combine(audios: list[AudioSegment], fade_sec: int) -> AudioSegment:
    combined = AudioSegment.empty()
    for audio in audios:
        combined += fade_inout(audio, fade_sec)
        combined += AudioSegment.silent(duration=100)
    return combined


def fade_inout(audio: AudioSegment, fade_sec: int) -> AudioSegment:
    return audio.fade_in(fade_sec * 1000).fade_out(fade_sec * 1000)


if __name__ == "__main__":
    load_dotenv()
    main()
