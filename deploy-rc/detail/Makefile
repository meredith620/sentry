INSTALL = install -c
RMCMD = rm -rf
MKDIRCMD = mkdir -p

PREFIX = INSTALL_ROOT
BIN_PATH = BIN_INSTALL_PATH

install: 
	$(INSTALL) -m 755 catcher.py -D $(PREFIX)/$(BIN_PATH)/catcher.py
	$(INSTALL) -m 644 Makefile -D $(PREFIX)/$(BIN_PATH)/Makefile
	$(MKDIRCMD) $(PREFIX)/LOG_PATH

	cat start_sh >> $(PREFIX)/start_all.sh && chmod 755 $(PREFIX)/start_all.sh
	cat stop_sh >> $(PREFIX)/stop_all.sh && chmod 755 $(PREFIX)/stop_all.sh
	cat check_sh >> $(PREFIX)/check_all.sh && chmod 755 $(PREFIX)/check_all.sh

uninstall:
	$(RMCMD) $(PREFIX)/$(BIN_PATH)/catcher.py
	$(RMCMD) $(PREFIX)/start_all.sh
	$(RMCMD) $(PREFIX)/stop_all.sh
	$(RMCMD) $(PREFIX)/check_all.sh

deep_unistall: uninstall
	$(RMCMD) INSTALL_ROOT/BIN_INSTALL_PATH
	$(RMCMD) INSTALL_ROOT/LOG_PATH
