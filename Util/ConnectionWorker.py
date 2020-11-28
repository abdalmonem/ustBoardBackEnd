import json

from flask import Flask, jsonify


class ConnectionWorker:
    reason: str = None,
    state: bool = False
    data: dict = None

    def create_response(self, reason: str = None, state: bool = None, data: dict = None):
        self.reason = reason
        self.state = state
        self.data = data
        _res = {
            "state": state
        }

        if reason is not None:
            _res["reason"] = reason.replace(" ", "_")
        else:
            _res["reason"] = ""

        if not data is None:
            _res["data"] = data

        return jsonify(_res)
