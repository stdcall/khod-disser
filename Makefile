SHELL = /bin/bash
MAINSOURCE = dissertation
COMMON = $(wildcard ./common/*.tex)
BIB = $(wildcard ./*.bib) $(wildcard ./biblio/*.tex)
DISS = $(wildcard ./Dissertation/*.tex)

# If BUILD_DIR is set, use it as output directory
ifdef BUILD_DIR
OUTDIR_FLAG = -outdir=$(BUILD_DIR)
TARGET = $(BUILD_DIR)/$(MAINSOURCE).pdf
else
OUTDIR_FLAG =
TARGET = $(MAINSOURCE).pdf
endif

$(TARGET): $(COMMON) $(BIB) $(DISS) latexmkrc $(MAINSOURCE).tex
	latexmk $(OUTDIR_FLAG) $(MAINSOURCE).tex

# Convenience target - only when BUILD_DIR is set
ifdef BUILD_DIR
dissertation.pdf: $(TARGET)
endif

clean:
	latexmk -c
	rm -rf `biber --cache`
	rm -f $(MAINSOURCE).{aux,bcf,bbl,fls,log,out,run.xml,toc}

archive:
	git ls-files | grep -v '\.pdf$$' | tar -czf archive-$$(date +%Y-%m-%d).tar.gz -T -

release: $(TARGET)
	@mkdir -p releases
	@DATE=$$(date +%Y-%m-%d); \
	BASE_NAME="khod-disser-$$DATE"; \
	if [ ! -f "releases/$$BASE_NAME.pdf" ]; then \
		cp $(TARGET) "releases/$$BASE_NAME.pdf"; \
		echo "Released PDF as releases/$$BASE_NAME.pdf"; \
	else \
		COUNTER=1; \
		while [ -f "releases/$$BASE_NAME-$$COUNTER.pdf" ]; do \
			COUNTER=$$((COUNTER + 1)); \
		done; \
		cp $(TARGET) "releases/$$BASE_NAME-$$COUNTER.pdf"; \
		echo "Released PDF as releases/$$BASE_NAME-$$COUNTER.pdf"; \
	fi; \
	ARCHIVE_NAME="archive-$$DATE"; \
	if [ ! -f "releases/$$ARCHIVE_NAME.tar.gz" ]; then \
		git ls-files | grep -v '\.pdf$$' | tar -czf "releases/$$ARCHIVE_NAME.tar.gz" -T -; \
		echo "Released archive as releases/$$ARCHIVE_NAME.tar.gz"; \
	else \
		COUNTER=1; \
		while [ -f "releases/$$ARCHIVE_NAME-$$COUNTER.tar.gz" ]; do \
			COUNTER=$$((COUNTER + 1)); \
		done; \
		git ls-files | grep -v '\.pdf$$' | tar -czf "releases/$$ARCHIVE_NAME-$$COUNTER.tar.gz" -T -; \
		echo "Released archive as releases/$$ARCHIVE_NAME-$$COUNTER.tar.gz"; \
	fi

.PHONY: clean archive release
