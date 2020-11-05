import base64
from io import BytesIO

from flask import Blueprint, jsonify


qrcode_bp = Blueprint("qrcode", __name__, url_prefix="/qrcode")


@qrcode_bp.route("/", methods=["GET"])
def get_qrcode():
    image = qrcode.make("http://127.0.0.1:5000/sessions")
    # img = qrcode.make('Some data here', image_factory=PymagingImage)
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    some_dict = {}
    print(base64.b64encode(buffered.getvalue()))
    some_dict["imagedata"] = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return jsonify(some_dict), 200
