import pytest
from click.testing import CliRunner

from pacwrap import cli


@pytest.fixture()
def runner():
    """Return cli runner."""
    return CliRunner()


DOPTIONS = "{'debug': 1, 'output': None, 'quiet': False, 'refresh': False, 'test': True, 'verbose': 0}"  # noqa: E501


def test_cli_file_command(runner):
    """Test file."""
    fpn = "/usr/bin/bashbug"
    fruit = runner.invoke(cli.main, ["--debug", "--test", "file", fpn])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "file_cmd({0}, {1}) called!".format(DOPTIONS, fpn) in fruit.output


def test_cli_list_package(runner):
    """Test list package."""
    tparam = "bash"
    fruit = runner.invoke(cli.main, ["--debug", "--test", "list", tparam])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "list_cmd({0}, {1}) called!".format(DOPTIONS, tparam) in fruit.output


# def test_cli_list_packages(runner, phandler):
#     """Test list."""
#     tparam = "list"
#     fruit = runner.invoke(cli.main, ["--test", list])
#     assert not fruit.exception
#     assert fruit.exit_code == 0


def test_cli_find_command(runner):
    """Test find."""
    tparam = "bash"
    fruit = runner.invoke(cli.main, ["-d", "-t", "find", tparam])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "find_cmd({0}, {1}) called!".format(DOPTIONS, tparam) in fruit.output


def test_cli_info_command(runner):
    """Test info."""
    tparam = "bash"
    fruit = runner.invoke(cli.main, ["-d", "--test", "info", tparam])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "info_cmd({0}, {1}) called!".format(DOPTIONS, tparam) in fruit.output


def test_cli_install_command(runner):
    """Test install."""
    tparam = "bash"
    fruit = runner.invoke(cli.main, ["-d", "--test", "install", tparam])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "install({0}, {1}) called!".format(DOPTIONS, tparam) in fruit.output


def test_cli_uninstall_command(runner):
    """Test uninstall."""
    tparam = "bash"
    fruit = runner.invoke(cli.main, ["-d", "--test", "uninstall", tparam])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "uninstall({0}, {1}) called!".format(DOPTIONS, tparam) in fruit.output
