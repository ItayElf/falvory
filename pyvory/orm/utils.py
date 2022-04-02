import io

from PIL import Image


def image_to_webp(img: bytes) -> bytes:
    img = Image.open(io.BytesIO(img))
    img.convert("RGB")
    output = io.BytesIO()
    img.save(output, format="webp")
    return output.getvalue()
