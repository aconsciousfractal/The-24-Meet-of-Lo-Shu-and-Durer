# Building The Paper

From this directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error the_24_meet_of_lo_shu_and_durer.tex
bibtex the_24_meet_of_lo_shu_and_durer
pdflatex -interaction=nonstopmode -halt-on-error the_24_meet_of_lo_shu_and_durer.tex
pdflatex -interaction=nonstopmode -halt-on-error the_24_meet_of_lo_shu_and_durer.tex
```

The committed PDF is `the_24_meet_of_lo_shu_and_durer.pdf`.

Known build target:

```text
engine: pdfLaTeX
expected output: 17 pages
primary source: the_24_meet_of_lo_shu_and_durer.tex
bibliography: refs.bib
```

The source uses standard LaTeX packages such as `amsmath`, `amssymb`,
`mathtools`, `booktabs`, `array`, `enumitem`, `microtype`, `geometry`,
`xcolor`, `xurl`, `xspace`, `hyperref`, and `lmodern`.
