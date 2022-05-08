import io
from PIL import Image


def image_to_webp(img: bytes, width: int) -> bytes:
    img = Image.open(io.BytesIO(img))
    img.convert("RGBA")
    output = io.BytesIO()
    img = img.resize((width, (img.height * width) // img.width), Image.ANTIALIAS)
    print(img.width, img.height)
    img.save(output, format="webp")
    return output.getvalue()
