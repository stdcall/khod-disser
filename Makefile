MAINSOURCE = dissertation
COMMON = $(wildcard ./common/*.tex)
BIB = $(wildcard ./*.bib) $(wildcard ./biblio/*.tex)
DISS = $(wildcard ./Dissertation/*.tex)

dissertation.pdf: $(COMMON) $(BIB) $(DISS) latexmkrc $(MAINSOURCE).tex
	echo "Измененные зависимости: $?"
	latexmk $(MAINSOURCE).tex

clean:
	latexmk -c
	rm -f $(MAINSOURCE).{aux,bcf,bbl,fls,log,out,run.xml,toc}

.PHONY: clean
