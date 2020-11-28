from flask import Flask, Blueprint, request, jsonify
from Util.Validate import Validate, ValidateConstrins, ConstrinsType
from Util.ConnectionWorker import ConnectionWorker

testfun = Blueprint('test', __name__, url_prefix='/api')


@testfun.route('/test', methods=["GET", "POST"])
def testPage():
    response = ConnectionWorker().create_response(
        reason="gfgf",
        state=True,
        data={
            "id": 54
        }
    )
    return response