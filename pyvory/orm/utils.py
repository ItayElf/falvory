import io

from PIL import Image


def image_to_webp(img: bytes) -> bytes:
    img = Image.open(io.BytesIO(img))
    w, h = img.size
    if w > 640 and w / h != 16 / 9:
        new = int(640 * h / w)
        img = img.resize((640, new))
        img = img.crop((0, new // 2 - 180, 640, new // 2 + 180))
    img.convert("RGBA")
    output = io.BytesIO()
    img.save(output, format="webp")
    return output.getvalue()
