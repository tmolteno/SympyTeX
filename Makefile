# Copyright (C) 2009-2011 by Tim Molteno <tim@physics.otago.ac.nz>
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
#      aptitude install texlive-latex-extra python-matplotlib

all: clean
	latex sympytexpackage.ins

docs:
	pdflatex sympytexpackage.dtx
	python sympytexpackage.sympy
	pdflatex sympytexpackage.dtx

# This builds the example document. The example uses matplotlib (aptitude install python-matplotlib)
test:
	pdflatex example.tex
	python example.sympy
	pdflatex example.tex

	
clean:
	rm -f sympytex.* example.s* rm sympytexpackage.dvi  sympytexpackage.aux

dist:
	tar -cf SympyTeX.tar sympytex.sty sympytex.py sympytexpackage.ins sympytexpackage.dtx example.tex README TODO Makefile
	bzip2 -f SympyTeX.tar

