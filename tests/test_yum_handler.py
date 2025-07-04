import pytest

from pacwrap.mkhandler import create_handler
from pacwrap.pkgmgr import PackageHandler
from pacwrap.yum import YumHandler


@pytest.fixture
def pwhandler() -> PackageHandler:
    """Return handler."""
    options = {
        "test": True,
        "osid": "fedora",
        "osvers": "21",
    }
    return create_handler(options)


@pytest.fixture
def refresh() -> PackageHandler:
    """Return handler."""
    options = {
        "refresh": True,
        "test": True,
        "osid": "fedora",
        "osvers": "21",
    }
    return create_handler(options)


@pytest.fixture
def names() -> PackageHandler:
    """Return handler."""
    options = {
        "names_only": True,
        "test": True,
        "osid": "fedora",
        "osvers": "21",
    }
    return create_handler(options)


def test_file_command(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test dnf handler file command."""
    assert isinstance(pwhandler, YumHandler)
    tresult = pwhandler.file_action("/usr/bin/bashbug")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: rpm -qf /usr/bin/bashbug" in out


def test_list_package(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test list package."""
    tresult = pwhandler.list_package("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: rpm -ql bash" in out


def test_list_packages(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test list package."""
    tresult = pwhandler.list_packages()
    out, err = capfd.readouterr()
    assert tresult == 0
    assert (
        "noex: rpm -qa --qf '%{name}-%{version}-%{release}.%{arch}.rpm\\n' | sort"
        in out
    )


def test_find_action(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test find action."""
    tresult = pwhandler.find_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: yum search bash" in out


def test_find_action_refresh(
    capfd: pytest.CaptureFixture[str], refresh: PackageHandler
) -> None:
    """Test find action with refresh."""
    assert isinstance(refresh, YumHandler)
    tresult = refresh.find_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: yum --refresh search bash" in out


def test_find_action_names_only(
    capfd: pytest.CaptureFixture[str], names: PackageHandler
) -> None:
    """Test find action with names_only."""
    assert isinstance(names, YumHandler)
    tresult = names.find_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: yum search bash" in out


def test_info_action(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test find action with names_only."""
    tresult = pwhandler.info_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: rpm -qi bash" in out


def test_install_action(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test install action."""
    tresult = pwhandler.install_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: yum install bash" in out


def test_install_action_refresh(
    capfd: pytest.CaptureFixture[str], refresh: PackageHandler
) -> None:
    """Test install action with refresh."""
    tresult = refresh.install_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: yum --refresh install bash" in out


def test_uninstall_action(
    capfd: pytest.CaptureFixture[str], pwhandler: PackageHandler
) -> None:
    """Test uninstall action with refresh."""
    tresult = pwhandler.uninstall_action("bash")
    out, err = capfd.readouterr()
    assert tresult == 0
    assert "noex: yum remove bash" in out
