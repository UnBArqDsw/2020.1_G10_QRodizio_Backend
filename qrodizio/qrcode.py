import base64
import qrcode as qrcode_generator
from io import BytesIO

from qrodizio.ext.configuration import get_config


def qrcode_table_url_builder(table_id):
    base_url = get_config("BACK_BASE_URL")
    table_url = f"{base_url}/tables/{table_id}/session"

    return table_url


def qrcode_builder(text: str) -> str:
    """Given a text produces a qrcode image base64 stringifyed of that text"""
    image = qrcode_generator.make(text)

    buffered = BytesIO()
    image.save(buffered, format="JPEG")

    encoded = base64.b64encode(buffered.getvalue())

    return encoded.decode("utf-8")
