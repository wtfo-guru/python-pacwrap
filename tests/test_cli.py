import pytest
from click.testing import CliRunner

from pacwrap import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert not result.exception
    assert (
        "Provides single interface to several common Linux package managers."
        in result.output
    )
    # assert result.output.strip() == "Hello, world."


def test_cli_with_option(runner):
    result = runner.invoke(cli.main, ["--debug", "--test", "list", "bash"])
    assert not result.exception
    assert result.exit_code == 0
    with open("/tmp/test.txt", "w") as to:
        print(result.output, file=to)
    # assert 'bash' in result.output


# def test_cli_with_arg(runner):
#     result = runner.invoke(cli.main, ["Quien"])
#     assert result.exit_code == 0
#     assert not result.exception
#     assert result.output.strip() == "Hello, Quien."
