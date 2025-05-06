import os
from sf311ai.data_utils import load_images_from_folder

def test_load_images_from_folder(tmp_path):
    img_dir = tmp_path / "images"
    img_dir.mkdir()
    (img_dir / "a.jpg").write_bytes(b"fake")
    (img_dir / "b.png").write_bytes(b"fake")
    (img_dir / "c.txt").write_text("not an image")
    images = load_images_from_folder(str(img_dir))
    assert len(images) == 2
    assert any("a.jpg" in img for img in images)
    assert any("b.png" in img for img in images)
