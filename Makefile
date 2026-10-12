# Copyright (C) 2009-2014 by Tim Molteno <tim@physics.otago.ac.nz>
#
# This file may be redistributed and/or
# modified under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 2 of the
# License, or (at your option) any later version. To view a copy of this
# license, see http://www.gnu.org/licenses/ or send a letter to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

# To create everything necessary to use the SympyTeX package, type
# 
#      make all
# and the files sympytex.sty and sympytex.py will be created
# 
# Requires makecmds.sty, for Debian-based distributions try
#      aptitude install texlive-latex-extra python3-matplotlib
#
# SympyTeX requires Python 3, with sympy and matplotlib installed:
#
#	aptitude install python3 python3-sympy python3-matplotlib
PYTHON=python3

all: clean
	latex sympytexpackage.ins

docs:
	rm -f *.sout
	pdflatex -interaction=nonstopmode sympytexpackage.dtx
	mkindex sympytexpackage.idx
	${PYTHON} sympytexpackage.sympy
	pdflatex -interaction=nonstopmode sympytexpackage.dtx

# This builds the example document. The example uses matplotlib (aptitude install python3-matplotlib)
test:
	pdflatex -interaction=nonstopmode example.tex
	${PYTHON} example.sympy
	pdflatex -interaction=nonstopmode example.tex

# Copy the docstrip-generated files into the installable Python package
# in src/sympytex/. Run this after every change to sympytexpackage.dtx.
sync-package: all
	${PYTHON} tools/sync_package.py

# Build the PyPI sdist and wheel (requires: pip install build).
package: sync-package
	${PYTHON} -m build

ctan:	
	cp README.md README
	/home/tim/Downloads/ctan/scripts/ctanify/ctanify sympytexpackage.ins README sympytexpackage.pdf example.pdf
	
clean:
	rm -f sympytex.* example.s* sympytexpackage.dvi sympytexpackage.aux
	rm -rf sympy-plots-for-*

dist:
	tar -cf SympyTeX.tar sympytex.sty sympytex.py sympytexpackage.ins sympytexpackage.dtx example.tex README TODO Makefile
	gzip -9 SympyTeX.tar

DOCS=/usr/share/doc/latex-sympytex
deb:	dist
	rm -rf debian/usr
	rm -rf debian/DEBIAN
	mkdir -p debian/usr/share/texmf-texlive/tex/latex/sympytex
	cp sympytex.sty debian/usr/share/texmf-texlive/tex/latex/sympytex 
	mkdir -p debian/DEBIAN
	cp debian/control debian/DEBIAN
	mkdir -p debian${DOCS}
	cp debian/copyright debian${DOCS}
	cp example.tex debian${DOCS}
	find ./debian -type d | xargs chmod 755
	fakeroot dpkg-deb --build debian
	mv debian.deb latex-sympytex_1.0-1_all.deb


deb2: dist
	dh_make -p latex-sympytex_1.0-1 -e tim@physics.otago.ac.nz -f SympyTeX.tar.gz
