from click.testing import CliRunner

from pacwrap import cli

DOPTIONS = "{'debug': 1, 'output': None, 'quiet': False, 'refresh': False, 'test': True, 'verbose': 0}"  # noqa: E501


def test_cli_file_command(cli_runner: CliRunner) -> None:
    """Test file."""
    fpn = "/usr/bin/bashbug"
    fruit = cli_runner.invoke(cli.main, ["--debug", "--test", "file", fpn])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "file_cmd({0}, {1}) called!".format(DOPTIONS, fpn) in fruit.output


def test_cli_list_package(cli_runner: CliRunner) -> None:
    """Test list package."""
    t_param = "bash"
    fruit = cli_runner.invoke(cli.main, ["--debug", "--test", "list", t_param])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "list_cmd({0}, {1}) called!".format(DOPTIONS, t_param) in fruit.output


# def test_cli_list_packages(cli_runner: CliRunner, phandler) -> None:
#     """Test list."""
#     t_param = "list"
#     fruit = cli_runner.invoke(cli.main, ["--test", list])
#     assert not fruit.exception
#     assert fruit.exit_code == 0


def test_cli_find_command(cli_runner: CliRunner) -> None:
    """Test find."""
    t_param = "bash"
    fruit = cli_runner.invoke(cli.main, ["-d", "-t", "find", t_param])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "find_cmd({0}, {1}) called!".format(DOPTIONS, t_param) in fruit.output


def test_cli_info_command(cli_runner: CliRunner) -> None:
    """Test info."""
    t_param = "bash"
    fruit = cli_runner.invoke(cli.main, ["-d", "--test", "info", t_param])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "info_cmd({0}, {1}) called!".format(DOPTIONS, t_param) in fruit.output


def test_cli_install_command(cli_runner: CliRunner) -> None:
    """Test install."""
    t_param = "bash"
    fruit = cli_runner.invoke(cli.main, ["-d", "--test", "install", t_param])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "install({0}, {1}) called!".format(DOPTIONS, t_param) in fruit.output


def test_cli_uninstall_command(cli_runner: CliRunner) -> None:
    """Test uninstall."""
    t_param = "bash"
    fruit = cli_runner.invoke(cli.main, ["-d", "--test", "uninstall", t_param])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "uninstall({0}, {1}) called!".format(DOPTIONS, t_param) in fruit.output
