import re
from typing import Tuple

import distro
from packaging import version
from wtforglib.kinds import StrAnyDict

from pacwrap.apt import AptHandler
from pacwrap.dnf import DnfHandler
from pacwrap.pacman import PacmanHandler
from pacwrap.pkgmgr import PackageHandler
from pacwrap.yum import YumHandler


def get_osinfo() -> Tuple[str, str, str]:
    """Returns distro data sanely."""
    osid = distro.id()
    if osid in {"debian", "pop"}:
        oslike = "debin"
    elif osid in {"fedora", "rocky"}:
        oslike = "rhel"
    else:
        oslike = distro.like()
    return (osid, oslike, distro.version())


def create_rhel_handler(options: StrAnyDict, osid: str, osvers) -> PackageHandler:
    """Returns package handler for redhat family."""
    if osid == "fedora":
        threshold_ver = "22"
    else:
        threshold_ver = "8"
    if version.parse(osvers) < version.parse(threshold_ver):
        return YumHandler(options)
    return DnfHandler(options)


def create_handler(options: StrAnyDict) -> PackageHandler:
    """Returns package handler for distro."""
    osid, oslike, osvers = get_osinfo()

    phandler: PackageHandler

    if oslike == "arch":
        phandler = PacmanHandler(options)
    elif oslike == "debian":
        phandler = AptHandler(options)
    elif re.search("rhel", oslike):
        phandler = create_rhel_handler(options, osid, osvers)
    else:
        raise ValueError("Unsupported distro like => {0}".format(oslike))
    return phandler
