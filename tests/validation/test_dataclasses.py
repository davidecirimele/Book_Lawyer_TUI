from dataclasses import dataclass

import pytest

from validation.dataclasses import validate_dataclass


def test_validate_dataclass():
    @dataclass
    class Foo:
        bar: str

    validate_dataclass(Foo('ok'))
    with pytest.raises(TypeError):
        validate_dataclass(Foo(1))


def test_validate_dataclass_using_post_init():
    @dataclass
    class Foo:
        bar: str

        def __post_init__(self):
            validate_dataclass(self)

    Foo('ok')
    with pytest.raises(TypeError):
        Foo(1)
