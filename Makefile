BINDIR = $(HOME)/bin
SHORTCUTS_DIR = $(HOME)/.shortcuts

install:
	@mkdir -p $(BINDIR)
	@install firefox.sh $(BINDIR)/firefox
	@install termux-url-opener.py $(BINDIR)/termux-url-opener
	@mkdir -p $(SHORTCUTS_DIR)
	@install 'PyPI Project.sh' $(SHORTCUTS_DIR)/'PyPI Project'
	@install clipproxy/pushsel.py $(SHORTCUTS_DIR)/'Push Clipboard'
