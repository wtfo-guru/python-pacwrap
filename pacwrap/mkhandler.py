import re
from typing import Tuple

import distro
from packaging import version
from typing import Optional
from wtforglib.kinds import StrAnyDict

from pacwrap.apt import AptHandler
from pacwrap.dnf import DnfHandler
from pacwrap.pacman import PacmanHandler
from pacwrap.pkgmgr import PackageHandler
from pacwrap.yum import YumHandler


def get_osinfo(options: StrAnyDict) -> Tuple[str, str, str]:
    """Returns distro data sanely."""
    osid: Optional[str] = distro.id()
    oslike: Optional[str] = distro.like()
    osvers: Optional[str] = distro.version()
    otest = options.get("test")
    if otest:
        osid = options.get("osid", osid)
        osvers = options.get("osvers", osvers)
    if osid in {"debian", "pop"}:
        oslike = "debian"
    elif osid in {"fedora", "rocky"}:
        oslike = "rhel"
    elif osid in {"arch", "manjaro"}:
        oslike = "arch"
    else:
        if otest:
            oslike = options.get("oslike", oslike)
    return (osid, oslike, osvers)


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
    osid, oslike, osvers = get_osinfo(options)

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
