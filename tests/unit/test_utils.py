import pytest

from blat_cli.utils import camel_to_snake_case


@pytest.mark.parametrize(
    "camel,snake",
    [
        ("OneObject", "one_object"),
        ("OneObjectTwo", "one_object_two"),
        ("oneObject", "one_object"),
        ("oneObjectTwo", "one_object_two"),
        ("1OneObject", "1_one_object"),
        ("1oneObject", "1one_object"),
    ],
)
def test_camel_to_snake_case(camel, snake):
    assert camel_to_snake_case(camel) == snake
