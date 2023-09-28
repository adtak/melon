import json
from pathlib import Path

import librosa
import numpy as np


def main(datasets_dir: str, custom_model_keywords: str) -> None:
    datasets_path = Path(datasets_dir)
    train, test = train_test_split(list(datasets_path.glob("*.wav")), 0.8)
    save_metadata(train, datasets_path / "train.jsonl", custom_model_keywords)
    save_metadata(test, datasets_path / "eval.jsonl", custom_model_keywords)
    save_config(datasets_path)


def train_test_split(data: list[str], train_size: float) -> tuple[list[str], list[str]]:
    shuffle_data = np.take(data, np.random.default_rng().permutation(len(data)))
    return np.split(shuffle_data, [int(len(data) * train_size)])


def save_metadata(files: list[Path], output: Path, custom_model_keywords: str) -> None:
    for file in files:
        genres = []
        moods = []
        instruments = []
        y, sr = librosa.load(file)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        key = np.argmax(np.sum(chroma, axis=1))
        key = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][key]
        length = librosa.get_duration(y=y, sr=sr)
        entry = {
            "key": key,
            "artist": "",
            "sample_rate": 44100,
            "file_extension": "wav",
            "description": "",
            "keywords": custom_model_keywords,
            "duration": length,
            "bpm": round(tempo),
            "genre": genres,
            "title": file.stem,
            "name": "",
            "instrument": instruments,
            "moods": moods,
            "path": str(file),
        }
        with output.open("w") as f:
            f.write(json.dumps(entry) + "\n")


def save_config(output: Path) -> None:
    config_file = output / "train.yaml"
    package_str = "package"
    yaml_contents = f"""#@{package_str} __global__

    datasource:
    max_channels: 2
    max_sample_rate: 44100

    evaluate: egs/eval
    generate: egs/train
    train: egs/train
    valid: egs/eval
    """
    with config_file.open("w") as f:
        f.write(yaml_contents)


if __name__ == "__main__":
    pass
