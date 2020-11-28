from flask import Flask, request
from enum import Enum
import re


class ConstrinsType(Enum):
    any = 0
    text_only = 1
    text_only_with_space = 2
    username = 3
    email = 4
    integer = 5
    numaric = 6
    englishAlpha = 7


class ValidateConstrins:
    min_lenth = None
    max_lenth = None
    is_required = None
    type = None

    def __init__(
            self,
            min_lenth: int = None,
            max_lenth: int = None,
            type: ConstrinsType = None,
            is_required: bool = False
    ):
        _locals = locals()
        for k in locals():
            setattr(self, k, _locals[k])

    def get_value_of(self, itemName):
        getattr(self, itemName)


class Validate:
    class ValidateResult:
        is_valid = False
        reason = ""

        def __init__(self, is_valid: bool, reason: str):
            self.is_valid = is_valid
            self.reason = reason

    state = False
    reason = ""

    def is_valid(self, parameter_name, parameter_value=None, constrins: ValidateConstrins = None, ) -> ValidateResult:

        is_valid = True
        reason = ""

        if is_valid and (constrins.is_required and parameter_value == None):
            is_valid = False
            reason = parameter_name + " is required and cant be empty"

        if is_valid and (constrins.min_lenth is not None and len(parameter_value) < constrins.min_lenth):
            is_valid = False
            reason = parameter_name + " cant be shorten than " + str(constrins.min_lenth) + " chars"

        if is_valid and (constrins.max_lenth is not None and len(parameter_value) > constrins.max_lenth):
            is_valid = False
            reason = parameter_name + " cant be longer than " + str(constrins.max_lenth) + " chars"

        if is_valid and (constrins.type is not None):

            if constrins.type == ConstrinsType.integer:
                if not re.search("^\d+$", parameter_value):
                    reason = parameter_name + " is un numeric chars"
                    is_valid = False

            if constrins.type == ConstrinsType.username:
                if not re.search("^[A-Za-z0-9_]*$", parameter_value):
                    reason = parameter_name + " content invalid chars"
                    is_valid = False

            if constrins.type == ConstrinsType.englishAlpha:
                if not re.search("[A-Za-z]+", parameter_value):
                    reason = parameter_name + " content invalid chars"
                    is_valid = False

            if constrins.type == ConstrinsType.email:
                if not re.search("[^@]+@[^@]+\.[^@]+", parameter_value):
                    reason = parameter_name + " content invalid chars"
                    is_valid = False

            if constrins.type == ConstrinsType.numaric:
                try:
                    float(parameter_value)
                    is_valid = True
                except ValueError:
                    reason = parameter_name + " is un numaric chars"
                    is_valid = False

        return self.ValidateResult(
            reason=reason.replace(" ", "_"),
            is_valid=is_valid
        )
