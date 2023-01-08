import io
import qrcode

from base64 import b64encode

def generate_qr(data):
    img = qrcode.make(data)
    byte_io = io.BytesIO()
    img.save(byte_io, format="PNG")
    image = b64encode(byte_io.getvalue()).decode("utf-8")
    return image
