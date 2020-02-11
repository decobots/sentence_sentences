import pytest

from preparation.environment_variables import get_env


def test_environment_variables_correct(global_variable):
    assert get_env(global_variable[0]) == global_variable[1]


def test_environment_variables_not_defined():
    with pytest.raises(OSError):
        get_env("undefined_variable_name")
