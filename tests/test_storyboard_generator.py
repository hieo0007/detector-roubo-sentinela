import os
import cv2
import numpy as np
import pytest
from src.storyboard import StoryboardVerifier


def test_generate_storyboard_synthetic_video(tmp_path):
    video_path = os.path.join(tmp_path, "synthetic_test.mp4")
    width, height = 320, 240
    fps = 10
    total_frames = 20

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for i in range(total_frames):
        frame = np.full((height, width, 3), fill_value=int(i * 10), dtype=np.uint8)
        out.write(frame)
    out.release()

    verifier = StoryboardVerifier(snapshots_dir=str(tmp_path))
    jpeg_bytes, save_path = verifier.generate_storyboard(
        video_path=video_path,
        num_frames=4,
        target_sec=1.0,
        window_sec=2.0
    )

    assert jpeg_bytes is not None
    assert len(jpeg_bytes) > 0
    assert save_path is not None
    assert os.path.exists(save_path)
