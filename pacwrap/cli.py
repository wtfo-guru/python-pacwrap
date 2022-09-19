# import re
import sys

import click

# import os.path
# import pkgmgrs
# import distro
# from optparse import OptionParser
from . import __version__
from .pkgmgrs import PackageHandler

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(name="file")
@click.argument("file", required=True, nargs=1)
@click.pass_context
def file_cmd(ctx, file):
    """Displays package if any that include the FILE"""
    options = ctx.obj.copy()
    if options["debug"] > 0:
        print(f"file_cmd({ctx.obj}, {file}) called!")
    handler = PackageHandler.create_handler(options)
    return handler.file_action(file)


@click.command(name="list")
@click.argument("package", required=False, nargs=1)
@click.pass_context
def list_cmd(ctx, package):
    """Lists files in PACKAGE or installed packages when no PACKAGE specified"""
    options = ctx.obj.copy()
    if options["debug"] > 0:
        print(f"list_cmd({ctx.obj}, {package}) called!")
    handler = PackageHandler.create_handler(options)
    if package is None:
        rtnVal = handler.list_packages()
    else:
        rtnVal = handler.list_package(package)
    return rtnVal


@click.command(name="find")
@click.option("--names-only/--no-names-only", default=False, help="specify quiet mode")
@click.argument("package", required=True, nargs=1)
@click.pass_context
def find_cmd(ctx, names_only, package):
    """Searches repositories for PACKAGE"""
    options = ctx.obj.copy()
    options["names_only"] = names_only
    if options["debug"] > 0:
        print(f"find_cmd({ctx.obj}, {names_only}, {package}) called!")
    handler = PackageHandler.create_handler(options)
    return handler.find_action(package)


@click.command(name="info")
@click.argument("package", required=True, nargs=1)
@click.pass_context
def info_cmd(ctx, package):
    """Display information about PACKAGE"""
    options = ctx.obj.copy()
    if options["debug"] > 0:
        print(f"info_cmd({ctx.obj}, {package}) called!")
    handler = PackageHandler.create_handler(options)
    return handler.info_action(package)


@click.command()
@click.argument("package", required=True, nargs=1)
@click.pass_context
def install(ctx, package):
    """Installs PACKAGE"""
    options = ctx.obj.copy()
    if options["debug"] > 0:
        print(f"install({ctx.obj}, {package}) called!")
    handler = PackageHandler.create_handler(options)
    return handler.install_action(package)


@click.command()
@click.argument("package", required=True, nargs=1)
@click.pass_context
def uninstall(ctx, package):
    """Unistalls PACKAGE"""
    options = ctx.obj.copy()
    if options["debug"] > 0:
        print(f"uninstall({ctx.obj}, {package}) called!")
    handler = PackageHandler.create_handler(options)
    return handler.uninstall_action(package)


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    print(__version__)
    ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("-d", "--debug", count=True, default=0, help="increment debug level")
@click.option("-o", "--out", "output", help="specify output file")
@click.option("-q", "--quiet/--no-quiet", default=False, help="specify quiet mode")
@click.option(
    "-r",
    "--refresh/--no-refresh",
    default=False,
    help="specify refresh synchronized data",
)
@click.option("-t", "--test/--no-test", default=False, help="specify test mode")
@click.option(
    "-v", "--verbose", count=True, default=0, help="increment verbosity level"
)
@click.option(
    "-V",
    "--version",
    is_flag=True,
    expose_value=False,
    callback=print_version,
    is_eager=True,
    help="show version and exit",
)
@click.pass_context
def main(ctx, debug, output, quiet, refresh, test, verbose):
    """Provides single interface to several common Linux package managers."""
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    ctx.obj["output"] = output
    ctx.obj["quiet"] = quiet
    ctx.obj["refresh"] = refresh
    ctx.obj["test"] = test
    ctx.obj["verbose"] = verbose


main.add_command(file_cmd, name="file")
main.add_command(list_cmd, name="list")
main.add_command(find_cmd, name="find")
main.add_command(info_cmd, name="info")
main.add_command(install)
main.add_command(uninstall)


if __name__ == "__main__":
    sys.exit(main(obj={}))
