from pathlib import Path
import subprocess


def convert_audio_to_wav(input_path: str | Path) -> Path:
    input_file = Path(input_path)

    if input_file.suffix.lower() == ".wav":
        return input_file

    output_file = input_file.with_suffix(".wav")

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_file),
        "-ac",
        "1",
        "-ar",
        "16000",
        "-sample_fmt",
        "s16",
        str(output_file),
    ]

    subprocess.run(command, check=True)

    return output_file