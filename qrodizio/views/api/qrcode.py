import base64
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
        image = qrcode.make("https://google.com.br")
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        self.image_data=base64.b64encode(buffered.getvalue()).decode("utf-8")
        self.table_id = randint(0, 1000)

class QrcodeProxy(Qrcode):
    def __init__(self):
        self.qrcode = QrcodeTable()
        
    def generate(self):
        qrcode = QrcodeProxy()
        if(self.qrcode is not None):
            qrcode.generate()
            
        qrcode.generate()

@qrcode_bp.route("/", methods=["GET"])
def get_qrcode():
    qrcode = QrcodeProxy()
    some_dict["imagedata"] = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return jsonify(some_dict), 200
