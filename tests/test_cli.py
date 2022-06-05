from pytest import fixture
from typer.testing import CliRunner

from cli import app


@fixture(scope="module")
def runner():
    return CliRunner()


def test_hello_world(runner):
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert result.stdout == "Hello World\n"
