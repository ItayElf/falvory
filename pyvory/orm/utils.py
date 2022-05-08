import io
from PIL import Image


def image_to_webp(img: bytes, resize: bool) -> bytes:
    img = Image.open(io.BytesIO(img))
    img.convert("RGBA")
    output = io.BytesIO()
    if resize:
        img = img.resize((640, (img.height * 640) // img.width), Image.ANTIALIAS)
    print(img.width, img.height)
    img.save(output, format="webp")
    return output.getvalue()
