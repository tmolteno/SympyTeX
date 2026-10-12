#!/usr/bin/env python3
"""Regenerate the src/sympytex/ package from the docstrip outputs.

sympytexpackage.dtx is the single source of truth for both the LaTeX
style file and the Python module. Run `make all` first (docstrip), then
this script copies the generated files into the installable package and
verifies that every copy of the version string agrees:

  1. \\ProvidesPackage{sympytex}[... v<ver> ...]   (dtx)
  2. \\newcommand{\\ST@version}{<ver>}             (dtx)
  3. __version__ = '<ver>'                        (python section of dtx)

and that the generated .sty writes the sympytex.checkversion(...) line
that carries \\ST@version into every .sympy file.

Usage:
  python3 tools/sync_package.py            # write src/sympytex/
  python3 tools/sync_package.py --check    # exit 1 if anything would change
"""
import argparse
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DTX = ROOT / 'sympytexpackage.dtx'
GEN_PY = ROOT / 'sympytex.py'
GEN_STY = ROOT / 'sympytex.sty'
PKG = ROOT / 'src' / 'sympytex'


def versions():
  """Extract the version from the three places it is literally recorded,
  and check that the style file writes the handshake line."""
  dtx = DTX.read_text(encoding='utf-8')
  m = re.search(r'\\ProvidesPackage\{sympytex\}.*?\[([^\]]+)\]', dtx, re.S)
  provides = re.match(r'\d{4}/\d{2}/\d{2}\s+v([0-9.]+)', m.group(1)).group(1)
  macro = re.search(r'\\newcommand\{\\ST\@version\}\{([0-9.]+)\}', dtx)
  pymod = re.search(r"^__version__ = '([0-9.]+)'", dtx, re.M)
  sty = GEN_STY.read_text(encoding='utf-8') if GEN_STY.exists() else ''
  wired = re.search(r"sympytex\.checkversion\('\\ST\@version'\)", sty)
  return [provides,
          macro.group(1) if macro else None,
          pymod.group(1) if pymod else None], bool(wired)


def module_body():
  """The python section as sympytex/__init__.py: sympytex.py with the
  trailing docstrip postamble (r\"\"\"...\\endinput...\"\"\") removed."""
  lines = GEN_PY.read_text(encoding='utf-8').splitlines(keepends=True)
  for i, line in enumerate(lines):
    if line.strip() == 'r"""' and i + 1 < len(lines) and \
       lines[i + 1].startswith('\\endinput'):
      return ''.join(lines[:i]).rstrip() + '\n'
  sys.exit('could not find the docstrip postamble in %s' % GEN_PY)


def main():
  ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
  ap.add_argument('--check', action='store_true',
                  help='only verify consistency; do not write anything')
  args = ap.parse_args()

  if not GEN_PY.exists() or not GEN_STY.exists():
    sys.exit('%s is missing; run `make all` first' %
             ('sympytex.py' if not GEN_PY.exists() else 'sympytex.sty'))

  found, wired = versions()
  if None in found or not wired:
    sys.exit('incomplete: versions=%s, handshake wired into .sty: %s' %
             (found, wired))
  if len(set(found)) != 1:
    sys.exit('version mismatch: provides=%s, ST@version=%s, '
             '__version__=%s' % tuple(found))

  init_py = module_body()
  targets = {
    PKG / '__init__.py': init_py,
    PKG / 'data' / 'sympytex.sty': GEN_STY.read_text(encoding='utf-8'),
  }
  changed = [t for t, c in targets.items()
             if not t.exists() or t.read_text(encoding='utf-8') != c]

  if changed and args.check:
    print('out of date: %s; run `make sync-package`' %
          ', '.join(str(t.relative_to(ROOT)) for t in changed))
    return 1
  for t in changed:
    t.parent.mkdir(parents=True, exist_ok=True)
    t.write_text(targets[t], encoding='utf-8')
    print('wrote %s' % t.relative_to(ROOT))
  print('sympytex package is in sync, version %s' % found[0])
  return 0


if __name__ == '__main__':
  sys.exit(main())
