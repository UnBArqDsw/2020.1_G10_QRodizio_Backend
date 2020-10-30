import base64
import qrcode as qrcode_generator
from io import BytesIO

from flask import Blueprint, jsonify
from random import randint


qrcode_bp = Blueprint("qrcode", __name__, url_prefix="/qrcode")


from abc import ABC, abstractmethod


class Qrcode(ABC):
    @abstractmethod
    def generate(self):
        pass


class QrcodeTable(Qrcode):
    def __init__(self):
        self.table_id = None
        self.image_data = None

    def generate(self):
        image = qrcode_generator.make("https://google.com.br")
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        self.image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")
        self.table_id = randint(0, 1000)


class QrcodeProxy(Qrcode):
    def __init__(self):
        self.qrcode = QrcodeTable()

    def generate(self):
        self.qrcode.generate()

    @property
    def image_data(self):
        return self.qrcode.image_data


@qrcode_bp.route("/", methods=["GET"])
def get_qrcode():
    qrcode = QrcodeProxy()
    qrcode.generate()

    resp = {"imagedata": qrcode.image_data}
    return jsonify(resp), 200
