import pytest

from packaging import version

from pacwrap.mkhandler import create_handler
from pacwrap.dnf import DnfHandler
from pacwrap.yum import YumHandler
from pacwrap.apt import AptHandler
from pacwrap.pacman import PacmanHandler



GTOPTS = {
    "test": True,
    "osid": "gentoo",
}

APTOPTS = {
    "test": True,
    "osid": "debian",
}

PMOPTS = {
    "test": True,
    "osid": "arch",
}

YUMOPTS = {
    "test": True,
    "osid": "fedora",
    "osvers": "21",
}

DNFOPTS = {
    "test": True,
    "osid": "rocky",
    "osvers": "9",
}

def test_create_apt_handler():
    pwh = create_handler(APTOPTS)
    assert isinstance(pwh, AptHandler)

def test_create_pacman_handler():
    pwh = create_handler(PMOPTS)
    assert isinstance(pwh, PacmanHandler)

def test_create_yum_handler():
    pwh = create_handler(YUMOPTS)
    assert isinstance(pwh, YumHandler)

def test_create_dnf_handler():
    pwh = create_handler(DNFOPTS)
    assert isinstance(pwh, DnfHandler)

def test_create_gentoo_handler():
    with pytest.raises(ValueError):
        create_handler(GTOPTS)
