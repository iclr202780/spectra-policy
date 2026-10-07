"""Prepare two short website excerpts from a local source folder.

Usage: python scripts/prepare_videos.py /path/to/source/videos
Requires ffmpeg. Originals are never changed. Public outputs are written to site/static/.
"""
from pathlib import Path
import argparse
import hashlib
import subprocess

CLIPS = [
    ('wet-wipe-extract-chest-cam.mp4', 'wipe-extraction', 0.6, 8.0),
    ('erase-whiteboard-chest-cam.mp4', 'whiteboard-erasing', 0.4, 8.0),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    output = Path(__file__).resolve().parents[1] / 'site/static/videos'
    output.mkdir(parents=True, exist_ok=True)
    for source_name, name, start, duration in CLIPS:
        source = args.source / source_name
        before = hashlib.sha256(source.read_bytes()).digest()
        subprocess.run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
            '-ss', str(start), '-i', str(source), '-t', str(duration),
            '-map', '0:v:0', '-an', '-sn', '-dn',
            '-map_metadata', '-1', '-map_chapters', '-1',
            '-c:v', 'libx264', '-preset', 'slow', '-crf', '23',
            '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
            str(output / f'{name}.mp4'),
        ], check=True)
        subprocess.run([
            'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
            '-i', str(output / f'{name}.mp4'), '-frames:v', '1',
            '-map_metadata', '-1', '-q:v', '2',
            str(output / f'{name}.jpg'),
        ], check=True)
        assert hashlib.sha256(source.read_bytes()).digest() == before
        print(f'{name}: {start:.1f}–{start + duration:.1f}s, original speed, no audio or source metadata')


if __name__ == '__main__':
    main()
