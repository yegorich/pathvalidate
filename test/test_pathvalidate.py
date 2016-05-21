# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''


import itertools
import random
import string

import pytest

from pathvalidate import *


random.seed(0)

char_list = [x for x in string.digits + string.ascii_letters + "/"]


def make_random_str(length):
    return "".join([random.choice(char_list) for _i in range(length)])


class Test_validate_filename:
    VALID_CHAR_LIST = [
        "!", "#", "$", '&', "'", "_",
        "=", "~", "^", "@", "`", "[", "]", "+", "-", ";", "{", "}",
        ",", ".", "(", ")", "%",
    ]
    INVALID_CHAR_LIST = [
        "\\", ":", "*", "?", '"', "<", ">", "|",
    ]

    @pytest.mark.parametrize(["value"], [
        [make_random_str(64) + invalid_char + make_random_str(64)]
        for invalid_char in VALID_CHAR_LIST
    ])
    def test_normal(self, value):
        validate_filename(value)

    @pytest.mark.parametrize(["value"], [
        [make_random_str(64) + invalid_char + make_random_str(64)]
        for invalid_char in INVALID_CHAR_LIST
    ])
    def test_exception_0(self, value):
        with pytest.raises(ValueError):
            validate_filename(value)

    @pytest.mark.parametrize(["value", "expected"], [
        [None, ValueError],
        [1, ValueError],
        [True, ValueError],
    ])
    def test_exception_1(self, value, expected):
        with pytest.raises(expected):
            validate_filename(value)


class Test_sanitize_filename:
    SANITIZE_CHAR_LIST = Test_validate_filename.INVALID_CHAR_LIST
    NOT_SANITIZE_CHAR_LIST = Test_validate_filename.VALID_CHAR_LIST
    REPLACE_TEXT_LIST = ["", "_"]

    @pytest.mark.parametrize(
        ["value", "replace_text", "expected"],
        [
            ["A" + c + "B", rep, "A" + rep + "B"]
            for c, rep in itertools.product(
                SANITIZE_CHAR_LIST, REPLACE_TEXT_LIST)
        ] + [
            ["A" + c + "B", rep, "A" + c + "B"]
            for c, rep in itertools.product(
                NOT_SANITIZE_CHAR_LIST, REPLACE_TEXT_LIST)
        ]
    )
    def test_normal(self, value, replace_text, expected):
        assert sanitize_filename(value, replace_text) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [None, AttributeError],
        [1, AttributeError],
        [True, AttributeError],
    ])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            sanitize_filename(value)


class Test_replace_symbol:
    TARGET_CHAR_LIST = [
        "\\", ":", "*", "?", '"', "<", ">", "|",
        ",", ".", "%", "(", ")", "/", " ",
    ]
    NOT_TARGET_CHAR_LIST = [
        "!", "#", "$", '&', "'", "_",
        "=", "~", "^", "@", "`", "[", "]", "+", "-", ";", "{", "}",
    ]
    REPLACE_TEXT_LIST = ["", "_"]

    @pytest.mark.parametrize(
        ["value", "replace_text", "expected"],
        [
            ["A" + c + "B", rep, "A" + rep + "B"] for c, rep in itertools.product(
                TARGET_CHAR_LIST, REPLACE_TEXT_LIST)
        ] + [
            ["A" + c + "B", rep, "A" + c + "B"] for c, rep in itertools.product(
                NOT_TARGET_CHAR_LIST, REPLACE_TEXT_LIST)
        ]
    )
    def test_normal_1(self, value, replace_text, expected):
        assert replace_symbol(value, replace_text) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        [None, AttributeError],
        [1, AttributeError],
        [True, AttributeError],
    ])
    def test_abnormal(self, value, expected):
        with pytest.raises(expected):
            replace_symbol(value)
