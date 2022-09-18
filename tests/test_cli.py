import re

import distro
import pytest
from click.testing import CliRunner

from pacwrap import cli


@pytest.fixture
def runner():
    return CliRunner()


def handler():
    osid = distro.id()
    oslike = distro.like()
    if re.match(r"(fedora)", osid):
        return "DnfHandler"
    if re.match(r"(arch|manjaro)", osid):
        return "PacmanHandler"
    elif re.match(r"(ubuntu|debian|pop)", osid) or re.search(r"debian", oslike):
        return "AptHandler"
    else:
        return "dunno"


def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert not result.exception
    assert (
        "Provides single interface to several common Linux package managers."
        in result.output
    )


def test_cli_file_command(runner):
    result = runner.invoke(cli.main, ["--test", "file", "/usr/bin/bashbug"])
    cname = handler()
    assert not result.exception
    assert result.exit_code == 0
    assert f"created instance of class {cname}" in result.output
    if cname == "PacmanHandler":
        assert "noex: pacman -Qo /usr/bin/bashbug" in result.output
    elif cname == "AptHandler":
        assert "noex: dpkg -S /usr/bin/bashbug" in result.output
    elif cname == "YumHandler" or cname == "DnfHandler":
        assert "noex: rpm -qf /usr/bin/bashbug" in result.output


def test_cli_list_package(runner):
    result = runner.invoke(cli.main, ["--test", "list", "bash"])
    cname = handler()
    assert not result.exception
    assert result.exit_code == 0
    assert f"created instance of class {cname}" in result.output
    if cname == "PacmanHandler":
        assert "noex: pacman -Ql bash" in result.output
    elif cname == "AptHandler":
        assert "noex: dpkg -L bash" in result.output
    elif cname == "YumHandler" or cname == "DnfHandler":
        assert "noex: rpm -ql bash" in result.output


def test_cli_list_packages(runner):
    result = runner.invoke(cli.main, ["--test", "list"])
    cname = handler()
    assert not result.exception
    assert result.exit_code == 0
    assert f"created instance of class {cname}" in result.output
    if cname == "PacmanHandler":
        assert "noex: pacman -Qe" in result.output
    elif cname == "AptHandler":
        assert "noex: apt list --installed | sort" in result.output
    elif cname == "YumHandler" or cname == "DnfHandler":
        assert (
            "noex: rpm -qa --qf '%{name}-%{version}-%{release}.%{arch}.rpm\\n' | sort"
            in result.output
        )


def test_cli_find_command(runner):
    result = runner.invoke(cli.main, ["--test", "find", "bash"])
    cname = handler()
    assert not result.exception
    assert result.exit_code == 0
    assert f"created instance of class {cname}" in result.output
    if cname == "PacmanHandler":
        assert "noex: pacman -Ss bash" in result.output
    elif cname == "AptHandler":
        assert "noex: apt search --names-only bash" in result.output
    elif cname == "YumHandler":
        assert "noex: yum search bash" in result.output
    elif cname == "DnfHandler":
        assert "noex: dnf search bash" in result.output


def test_cli_info_command(runner):
    result = runner.invoke(cli.main, ["--test", "info", "bash"])
    cname = handler()
    assert not result.exception
    assert result.exit_code == 0
    assert f"created instance of class {cname}" in result.output
    if cname == "PacmanHandler":
        assert "noex: pacman -Qi bash" in result.output
    elif cname == "AptHandler":
        assert "noex: apt show bash" in result.output
    elif cname == "YumHandler" or cname == "DnfHandler":
        assert "noex: rpm -qi bash" in result.output


def test_cli_install_command(runner):
    result = runner.invoke(cli.main, ["--test", "install", "bash"])
    cname = handler()
    assert not result.exception
    assert result.exit_code == 0
    assert f"created instance of class {cname}" in result.output
    if cname == "PacmanHandler":
        assert "noex: pacman -S bash" in result.output
    elif cname == "AptHandler":
        assert "noex: apt install bash" in result.output
    elif cname == "YumHandler":
        assert "noex: yum install bash" in result.output
    elif cname == "DnfHandler":
        assert "noex: dnf install bash" in result.output


def test_cli_uninstall_command(runner):
    result = runner.invoke(cli.main, ["--test", "uninstall", "bash"])
    cname = handler()
    assert not result.exception
    assert result.exit_code == 0
    assert f"created instance of class {cname}" in result.output
    if cname == "PacmanHandler":
        assert "noex: pacman -R bash" in result.output
    elif cname == "AptHandler":
        assert "noex: apt remove bash" in result.output
    elif cname == "YumHandler":
        assert "noex: yum remove bash" in result.output
    elif cname == "DnfHandler":
        assert "noex: dnf remove bash" in result.output
