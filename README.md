This is the SympyTeX package. This package allows you to embed symbolic calculations
and their results into LaTeX documents. SympyTex uses sympy, the symbolic python engine (http://www.sympy.org), to manipulate
symbolic expressions. Using SympyTeX, sympy code can be embedded into your document, either hidden from view, or as part of the document, and
sympy expressions can be rendered into LaTeX expressions and included in your document output.

SympyTex was written by Tim Molteno (tim@physics.otago.ac.nz)

====================================================================

##Using SympyTex

To use SympyTeX, you need the files, sympytex.sty and sympytex.py. See below for instructions.

You also need to have installed the Sympy (Symbolic Python) package

    aptitude install python-sympy

Create a LaTeX document that uses the sympytex package.

    \usepackage{sympytex}

...

    \begin{sympyblock}
    x = sympy.Symbol('x')
    h = sympy.integrate(1+x**4,x)
    \end{sympyblock}

    The integral of $1+x^4$ is also \sympy{sympy.integrate(1+x**4,x)}.
    or you can use a sympy variable, $h = \sympy{h}$

Now run:

    latex mydoc.tex
    python mydoc.sympy
    latex mydoc.tex

See the include example.tex for more details.

====================================================================

##Building the Package

###The easy way

Use the provided Makefile

    make 
    make test

This will build the SympyTeX package, and also create a sample document.

###The hard way
To build the SympyTeX package you will need to install some extra LaTeX
packages (makecmds.sty)

    aptitude install texlive-latex-extra

Then do:

  0. Run `latex sympytexpackage.ins'

If a PDF file of the documentation wasn't included with this
distribution of SympyTeX, you will need to build the documentation
yourself. To do that:

  1. Run `latex sympytexpackage.dtx'
  2. Run `python sympytexpackage.sympy'
  3. Run the indexing commands that the .ins file told you about.
  4. Run `latex sympytexpackage.dtx' again.

You can skip step 3 if you don't care about the index. You will need the
pgf and tikz packages installed to typeset the figures.

The file example.tex has, as you likely guessed, a bunch of examples
showing you how this package works.


##Credits

SympyTeX builds on a lot of work by others; in particular the work of
Dan Drake <ddrake@member.ams.org> who created the sagetex package on which
sympytex is based. See the "Credits" section
of the documentation for credits. The source code may be modified and
distributed under the terms of the GPL, v2 or later; the documentation
may be modified and distributed under a Creative Commons Attribution -
Noncommercial - Share Alike 3.0 License. See the "Copying and licenses"
section of the documentation.

Please let me know if you find any bugs or have any ideas for
improvement!

- Tim Molteno <tim@physics.otago.ac.nz>
