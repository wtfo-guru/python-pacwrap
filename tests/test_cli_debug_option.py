from pacwrap import cli

DOPTIONS = "{'debug': 1, 'output': None, 'quiet': False, 'refresh': False, 'test': True, 'verbose': 0}"  # noqa: E501


def test_cli_file_command(cli_runner):
    """Test file."""
    fpn = "/usr/bin/bashbug"
    fruit = cli_runner.invoke(cli.main, ["--debug", "--test", "file", fpn])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "file_cmd({0}, {1}) called!".format(DOPTIONS, fpn) in fruit.output


def test_cli_list_package(cli_runner):
    """Test list package."""
    tparam = "bash"
    fruit = cli_runner.invoke(cli.main, ["--debug", "--test", "list", tparam])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "list_cmd({0}, {1}) called!".format(DOPTIONS, tparam) in fruit.output


# def test_cli_list_packages(cli_runner, phandler):
#     """Test list."""
#     tparam = "list"
#     fruit = cli_runner.invoke(cli.main, ["--test", list])
#     assert not fruit.exception
#     assert fruit.exit_code == 0


def test_cli_find_command(cli_runner):
    """Test find."""
    tparam = "bash"
    fruit = cli_runner.invoke(cli.main, ["-d", "-t", "find", tparam])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "find_cmd({0}, {1}) called!".format(DOPTIONS, tparam) in fruit.output


def test_cli_info_command(cli_runner):
    """Test info."""
    tparam = "bash"
    fruit = cli_runner.invoke(cli.main, ["-d", "--test", "info", tparam])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "info_cmd({0}, {1}) called!".format(DOPTIONS, tparam) in fruit.output


def test_cli_install_command(cli_runner):
    """Test install."""
    tparam = "bash"
    fruit = cli_runner.invoke(cli.main, ["-d", "--test", "install", tparam])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "install({0}, {1}) called!".format(DOPTIONS, tparam) in fruit.output


def test_cli_uninstall_command(cli_runner):
    """Test uninstall."""
    tparam = "bash"
    fruit = cli_runner.invoke(cli.main, ["-d", "--test", "uninstall", tparam])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "uninstall({0}, {1}) called!".format(DOPTIONS, tparam) in fruit.output
