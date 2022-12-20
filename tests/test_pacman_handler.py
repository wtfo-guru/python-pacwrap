import pytest

from pacwrap.mkhandler import create_handler
from pacwrap.pacman import PacmanHandler
from pacwrap.pkgmgr import PackageHandler


@pytest.fixture()
def pwhandler() -> PackageHandler:
    """Return handler name."""
    options = {
        "test": True,
        "osid": "arch",
    }
    return create_handler(options)


@pytest.fixture()
def refresh() -> PackageHandler:
    """Return handler."""
    options = {
        "refresh": True,
        "test": True,
        "osid": "arch",
    }
    return create_handler(options)


@pytest.fixture()
def names() -> PackageHandler:
    """Return handler."""
    options = {
        "names_only": True,
        "test": True,
        "osid": "arch",
    }
    return create_handler(options)


def test_file_command(capfd, pwhandler):
    """Test dnf handler file command."""
    assert isinstance(pwhandler, PacmanHandler)
    tresult = pwhandler.file_action("/usr/bin/bashbug")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: pacman -Qo /usr/bin/bashbug" in out


def test_list_package(capfd, pwhandler):
    """Test list package."""
    tresult = pwhandler.list_package("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: pacman -Ql bash" in out


def test_list_packages(capfd, pwhandler):
    """Test list package."""
    tresult = pwhandler.list_packages()
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: pacman -Qe" in out


def test_find_action(capfd, pwhandler):
    """Test find action."""
    tresult = pwhandler.find_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: pacman -Ss bash" in out


def test_find_action_refresh(capfd, refresh):
    """Test find action."""
    assert isinstance(refresh, PacmanHandler)
    tresult = refresh.find_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: pacman -Ssy bash" in out


def test_find_action_names_only(capfd, names):
    """Test find action with names_only."""
    assert isinstance(names, PacmanHandler)
    tresult = names.find_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: pacman -Ss bash" in out


def test_info_action(capfd, pwhandler):
    """Test find action with names_only."""
    tresult = pwhandler.info_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: pacman -Qi bash" in out


def test_install_action(capfd, pwhandler):
    """Test install action."""
    tresult = pwhandler.install_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: pacman -S bash" in out


def test_install_action_refresh(capfd, refresh):
    """Test install action with refresh."""
    tresult = refresh.install_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: pacman -Sy bash" in out


def test_uninstall_action(capfd, pwhandler):
    """Test uninstall action with refresh."""
    tresult = pwhandler.uninstall_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: pacman -R bash" in out
