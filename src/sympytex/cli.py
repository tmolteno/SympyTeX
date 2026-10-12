"""Command-line interface for SympyTeX.

The 'sympytex' console script provides:

  sympytex install          install sympytex.sty into the local texmf tree
  sympytex run FILE.sympy   run the sympy pass on a generated .sympy file
  sympytex --version        print the package version
"""
import argparse
import pathlib
import runpy
import shutil
import subprocess
import sys

from sympytex import __version__


def _bundled_sty():
  return pathlib.Path(__file__).resolve().parent / 'data' / 'sympytex.sty'


def _texmfhome():
  try:
    out = subprocess.run(['kpsewhich', '-var-value=TEXMFHOME'],
                         capture_output=True, text=True)
    if out.returncode == 0 and out.stdout.strip():
      return pathlib.Path(out.stdout.strip())
  except OSError:
    pass
  return pathlib.Path('~/texmf').expanduser()


def cmd_install(args):
  src = _bundled_sty()
  if args.dest:
    dest = pathlib.Path(args.dest).expanduser()
  else:
    dest = _texmfhome() / 'tex' / 'latex' / 'sympytex' / 'sympytex.sty'
  dest.parent.mkdir(parents=True, exist_ok=True)
  shutil.copy2(src, dest)
  print('Installed SympyTeX style file')
  print('  from %s' % src)
  print('  to   %s' % dest)
  return 0


def cmd_run(args):
  path = pathlib.Path(args.file)
  if not path.is_file():
    print('sympytex: no such file: %s' % path, file=sys.stderr)
    return 1
  sys.argv = [str(path)] + args.args
  runpy.run_path(str(path), run_name='__main__')
  return 0


def main(argv=None):
  parser = argparse.ArgumentParser(
      prog='sympytex',
      description='Embed sympy symbolic computation in LaTeX documents.')
  parser.add_argument('--version', action='version',
                      version='sympytex %s' % __version__)
  sub = parser.add_subparsers(dest='command')

  p_install = sub.add_parser(
      'install', help='install sympytex.sty into the local texmf tree')
  p_install.add_argument(
      '--dest', metavar='PATH', default=None,
      help='destination path (default: TEXMFHOME/tex/latex/sympytex/sympytex.sty)')
  p_install.set_defaults(func=cmd_install)

  p_run = sub.add_parser(
      'run', help='run the sympy pass on a generated .sympy file')
  p_run.add_argument('file', metavar='FILE.sympy')
  p_run.add_argument('args', nargs='*', help=argparse.SUPPRESS)
  p_run.set_defaults(func=cmd_run)

  args = parser.parse_args(argv)
  if not getattr(args, 'func', None):
    parser.print_help()
    return 2
  return args.func(args)
