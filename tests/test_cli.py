import pytest
from click.testing import CliRunner
from cmp_version import cmp_version  # type: ignore[import-untyped]

from pacwrap import cli
from pacwrap.constants import VERSION
from pacwrap.mkhandler import get_osinfo


@pytest.fixture
def phandler() -> str:
    """Return handler name."""
    osid, oslike, osvers = get_osinfo({"test": True})

    if oslike == "arch":
        return "PacmanHandler"
    elif oslike == "debian":
        return "AptHandler"
    elif oslike == "rhel":
        if osid == "fedora":
            threshold_ver = "22"
        else:
            threshold_ver = "8"
        if cmp_version(osvers, threshold_ver) < 0:
            return "YumHandler"
        return "DnfHandler"
    return "dunno"


def test_cli_help(cli_runner: CliRunner) -> None:
    """Test help."""
    fruit = cli_runner.invoke(cli.main, ["-h"])
    assert fruit.exit_code == 0
    assert not fruit.exception
    assert (
        "Provides single interface to several common Linux package managers."
        in fruit.output
    )


def test_cli_version(cli_runner: CliRunner) -> None:
    """Test help."""
    fruit = cli_runner.invoke(cli.main, ["--version"])
    assert fruit.exit_code == 0
    assert not fruit.exception
    assert fruit.output.strip() == "main, version {0}".format(VERSION)


def test_cli_file_command(cli_runner: CliRunner, phandler: str) -> None:
    """Test file."""
    fruit = cli_runner.invoke(cli.main, ["--test", "file", "/usr/bin/bashbug"])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "created instance of class {0}".format(phandler) in fruit.output
    if phandler == "PacmanHandler":
        assert "noex: pacman -Qo /usr/bin/bashbug" in fruit.output
    elif phandler == "AptHandler":
        assert "noex: dpkg -S /usr/bin/bashbug" in fruit.output
    elif phandler in {"YumHandler", "DnfHandler"}:
        assert "noex: rpm -qf /usr/bin/bashbug" in fruit.output


def test_cli_list_package(cli_runner: CliRunner, phandler: str) -> None:
    """Test list package."""
    fruit = cli_runner.invoke(cli.main, ["--test", "list", "bash"])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "created instance of class {0}".format(phandler) in fruit.output
    if phandler == "PacmanHandler":
        assert "noex: pacman -Ql bash" in fruit.output
    elif phandler == "AptHandler":
        assert "noex: dpkg -L bash" in fruit.output
    elif phandler in {"YumHandler", "DnfHandler"}:
        assert "noex: rpm -ql bash" in fruit.output


def test_cli_list_packages(cli_runner: CliRunner, phandler: str) -> None:
    """Test list."""
    fruit = cli_runner.invoke(cli.main, ["--test", "list"])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "created instance of class {0}".format(phandler) in fruit.output
    if phandler == "PacmanHandler":
        assert "noex: pacman -Qe" in fruit.output
    elif phandler == "AptHandler":
        assert "noex: apt list --installed | sort" in fruit.output
    elif phandler in {"YumHandler", "DnfHandler"}:
        assert (
            "noex: rpm -qa --qf '%{name}-%{version}-%{release}.%{arch}.rpm\\n' | sort"
            in fruit.output
        )


def test_cli_find_command(cli_runner: CliRunner, phandler: str) -> None:
    """Test find."""
    fruit = cli_runner.invoke(cli.main, ["--test", "find", "bash"])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "created instance of class {0}".format(phandler) in fruit.output
    if phandler == "PacmanHandler":
        assert "noex: pacman -Ss bash" in fruit.output
    elif phandler == "AptHandler":
        assert "noex: apt search bash" in fruit.output
    elif phandler == "YumHandler":
        assert "noex: yum search bash" in fruit.output
    elif phandler == "DnfHandler":
        assert "noex: dnf search bash" in fruit.output


def test_cli_find_refresh_option(cli_runner: CliRunner, phandler: str) -> None:
    """Test find."""
    fruit = cli_runner.invoke(cli.main, ["--test", "--refresh", "find", "bash"])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "created instance of class {0}".format(phandler) in fruit.output
    if phandler == "PacmanHandler":
        assert "noex: pacman -Ssy bash" in fruit.output
    elif phandler == "AptHandler":
        assert "noex: apt search bash" in fruit.output
    elif phandler == "YumHandler":
        assert "noex: yum search bash" in fruit.output
    elif phandler == "DnfHandler":
        assert "noex: dnf --refresh search bash" in fruit.output


def test_cli_find_names_only_command(cli_runner: CliRunner, phandler: str) -> None:
    """Test find with names only option."""
    fruit = cli_runner.invoke(cli.main, ["--test", "find", "--names-only", "bash"])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "created instance of class {0}".format(phandler) in fruit.output
    if phandler == "PacmanHandler":
        assert "noex: pacman -Ss bash" in fruit.output
    elif phandler == "AptHandler":
        assert "noex: apt search --names-only bash" in fruit.output
    elif phandler == "YumHandler":
        assert "noex: yum search bash" in fruit.output
    elif phandler == "DnfHandler":
        assert "noex: dnf search bash" in fruit.output


def test_cli_info_command(cli_runner: CliRunner, phandler: str) -> None:
    """Test info."""
    fruit = cli_runner.invoke(cli.main, ["--test", "info", "bash"])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "created instance of class {0}".format(phandler) in fruit.output
    if phandler == "PacmanHandler":
        assert "noex: pacman -Qi bash" in fruit.output
    elif phandler == "AptHandler":
        assert "noex: apt show bash" in fruit.output
    elif phandler in {"YumHandler", "DnfHandler"}:
        assert "noex: rpm -qi bash" in fruit.output


def test_cli_install_command(cli_runner: CliRunner, phandler: str) -> None:
    """Test install."""
    fruit = cli_runner.invoke(cli.main, ["--test", "install", "bash"])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "created instance of class {0}".format(phandler) in fruit.output
    if phandler == "PacmanHandler":
        assert "noex: pacman -S bash" in fruit.output
    elif phandler == "AptHandler":
        assert "noex: apt install bash" in fruit.output
    elif phandler == "YumHandler":
        assert "noex: yum install bash" in fruit.output
    elif phandler == "DnfHandler":
        assert "noex: dnf install bash" in fruit.output


def test_cli_install_refresh_option(cli_runner: CliRunner, phandler: str) -> None:
    """Test install."""
    fruit = cli_runner.invoke(cli.main, ["--test", "--refresh", "install", "bash"])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "created instance of class {0}".format(phandler) in fruit.output
    if phandler == "PacmanHandler":
        assert "noex: pacman -Sy bash" in fruit.output
    elif phandler == "AptHandler":
        assert "noex: apt update" in fruit.output
        assert "noex: apt install bash" in fruit.output
    elif phandler == "YumHandler":
        assert "noex: yum install bash" in fruit.output
    elif phandler == "DnfHandler":
        assert "noex: dnf --refresh install bash" in fruit.output


def test_cli_uninstall_command(cli_runner: CliRunner, phandler: str) -> None:
    """Test uninstall."""
    fruit = cli_runner.invoke(cli.main, ["--test", "uninstall", "bash"])
    assert not fruit.exception
    assert fruit.exit_code == 0
    assert "created instance of class {0}".format(phandler) in fruit.output
    if phandler == "PacmanHandler":
        assert "noex: pacman -R bash" in fruit.output
    elif phandler == "AptHandler":
        assert "noex: apt remove bash" in fruit.output
    elif phandler == "YumHandler":
        assert "noex: yum remove bash" in fruit.output
    elif phandler == "DnfHandler":
        assert "noex: dnf remove bash" in fruit.output
