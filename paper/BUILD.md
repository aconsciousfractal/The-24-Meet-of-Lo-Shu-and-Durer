# Building The Paper

From this directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error the_24_meet_of_lo_shu_and_durer.tex
bibtex the_24_meet_of_lo_shu_and_durer
pdflatex -interaction=nonstopmode -halt-on-error the_24_meet_of_lo_shu_and_durer.tex
pdflatex -interaction=nonstopmode -halt-on-error the_24_meet_of_lo_shu_and_durer.tex
```

The committed PDF is `the_24_meet_of_lo_shu_and_durer.pdf`.
