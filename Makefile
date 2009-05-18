# This makefile creates all the documentation for the SympyTeX package
# Run:
#    make all
# and the files sympytex.sty and sympytex.py will be created
#
#

all: clean
	latex sympytexpackage.ins

docs:
	pdflatex sympytexpackage.dtx
	- python sympytexpackage.sympy
	pdflatex sympytexpackage.dtx
	
clean:
	rm -f sympytex.* example.s* rm sympytexpackage.dvi  sympytexpackage.aux

dist:
	tar -cf SympyTeX.tar sympytex.sty sympytex.py sympytexpackage.ins sympytexpackage.dtx example.tex README TODO Makefile
	bzip2 -f SympyTeX.tar
