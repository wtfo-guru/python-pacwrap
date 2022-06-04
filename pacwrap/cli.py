# import re
import sys

import click

# import os.path
# import pkgmgrs
# import distro
# from optparse import OptionParser
from . import __version__
from .pkgmgrs import PackageHandler


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
def list_cmd(ctx, output, quiet, package):
    """Lists files in PACKAGE or installed packages when no PACKAGE specified."""
    options = ctx.obj.copy()
    options["output"] = output
    options["quiet"] = quiet
    if options["debug"] > 0:
        print(f"list_cmd({ctx.obj}, {output}, {quiet}, {package}) called!")
    handler = PackageHandler.create_handler(options)
    if package is None:
        rtnVal = handler.list_packages()
    else:
        rtnVal = handler.list_package(package)
    return rtnVal


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    print(__version__)
    ctx.exit()


@click.group
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
    # usage = """usage: %prog [options] action

    # Actions:
    #   pacwrap find PACKAGE       # Searches repositories for PACKAGE
    #   pacwrap info PACKAGE       # Display information about PACKAGE
    #   pacwrap install PACKAGE    # Installs PACKAGE
    #   pacwrap uninstall PACKAGE  # Uninstalls PACKAGE
    # """
    # parser = OptionParser(usage)

    # (opts, args) = parser.parse_args()

    # options = vars(opts)
    # if options['debug']>1:
    #   print (options)
    #   print (args)

    # if options['version']:
    #   basenm = os.path.basename(sys.argv[0])
    #   print('%s Version: 1.0.1' % basenm)
    #   exit(0)

    # args_nbr = len(args)
    # if args_nbr < 1:
    #   sys.stderr.write("ParameterError: Missing parameter.\n")
    #   parser.print_help()
    #   exit(1)

    # try:
    #   exit(handler.action(args.pop(0), args))
    # except pkgmgrs.UsageError as ex:
    #   sys.stderr.write("UsageErrror: %s!!!" % ex.messager)
    #   parser.print_help()
    #   exit(1)


main.add_command(file_cmd, name="file")
main.add_command(list_cmd, name="list")

if __name__ == "__main__":
    sys.exit(main(obj={}))
