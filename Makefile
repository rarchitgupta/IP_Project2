PYTHON := python3
SRC_DIR := src
TESTS_DIR := tests
EXECUTABLES := $(SRC_DIR)/server.py $(SRC_DIR)/client.py

.PHONY: all test test-checksum test-packet test-server test-integration clean help

all: $(EXECUTABLES)
	@echo "Simple-FTP client and server ready"
	@echo "Run 'make help' for more options"

$(EXECUTABLES):
	@test -f $@ || (echo "Error: $@ not found"; exit 1)

test: $(EXECUTABLES)
	$(PYTHON) -m pytest $(TESTS_DIR) -v

test-checksum: $(EXECUTABLES)
	$(PYTHON) -m pytest $(TESTS_DIR)/test_checksum.py -v

test-packet: $(EXECUTABLES)
	$(PYTHON) -m pytest $(TESTS_DIR)/test_packet.py -v

test-server: $(EXECUTABLES)
	$(PYTHON) -m pytest $(TESTS_DIR)/test_server_basic.py -v

test-integration: $(EXECUTABLES)
	$(PYTHON) -m pytest $(TESTS_DIR)/test_integration.py -v

clean:
	rm -f $(SRC_DIR)/*.pyc
	rm -rf $(SRC_DIR)/__pycache__
	rm -f $(TESTS_DIR)/*.pyc
	rm -rf $(TESTS_DIR)/__pycache__
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf .pytest_cache

help:
	@echo "Simple-FTP with Go-Back-N Protocol"
	@echo ""
	@echo "Usage:"
	@echo "  make                 - Verify all source files exist"
	@echo "  make test            - Run all tests (requires pytest)"
	@echo "  make test-checksum   - Run checksum tests only"
	@echo "  make test-packet     - Run packet tests only"
	@echo "  make test-server     - Run server tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make clean           - Remove build artifacts and cache"
	@echo "  make help            - Show this message"
	@echo ""
	@echo "Run server:  $(PYTHON) $(SRC_DIR)/server.py <port> <output_file> <loss_prob>"
	@echo "Run client:  $(PYTHON) $(SRC_DIR)/client.py <host> <port> <input_file> <window_size> <mss>"

.SILENT: help
