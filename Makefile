PYTHON := python3
SRC_DIR := src
TESTS_DIR := tests
EXECUTABLES := $(SRC_DIR)/server.py $(SRC_DIR)/client.py

.PHONY: all test test-checksum test-packet test-server test-integration clean help experiments experiments-quick

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

experiments: $(EXECUTABLES)
	$(PYTHON) experiments.py --file-size-mb 5 --runs 5 --task all

experiments-quick: $(EXECUTABLES)
	$(PYTHON) experiments.py --file-size-mb 1 --runs 3 --task all

experiments-task1: $(EXECUTABLES)
	$(PYTHON) experiments.py --file-size-mb 5 --runs 5 --task 1

experiments-task2: $(EXECUTABLES)
	$(PYTHON) experiments.py --file-size-mb 5 --runs 5 --task 2

experiments-task3: $(EXECUTABLES)
	$(PYTHON) experiments.py --file-size-mb 5 --runs 5 --task 3

clean:
	rm -f $(SRC_DIR)/*.pyc
	rm -rf $(SRC_DIR)/__pycache__
	rm -f $(TESTS_DIR)/*.pyc
	rm -rf $(TESTS_DIR)/__pycache__
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf experiment_results

help:
	@echo "Simple-FTP with Go-Back-N Protocol"
	@echo ""
	@echo "Usage:"
	@echo "  make                    - Verify all source files exist"
	@echo "  make test               - Run all tests (requires pytest)"
	@echo "  make test-checksum      - Run checksum tests only"
	@echo "  make test-packet        - Run packet tests only"
	@echo "  make test-server        - Run server tests only"
	@echo "  make test-integration   - Run integration tests only"
	@echo ""
	@echo "Experiments (Phase 5):"
	@echo "  make experiments        - Run all experiments (full: 5MB, 5 runs each)"
	@echo "  make experiments-quick  - Run all experiments (quick: 1MB, 3 runs each)"
	@echo "  make experiments-task1  - Run Task 1 (window size effect) only"
	@echo "  make experiments-task2  - Run Task 2 (MSS effect) only"
	@echo "  make experiments-task3  - Run Task 3 (loss probability effect) only"
	@echo ""
	@echo "Other:"
	@echo "  make clean              - Remove build artifacts and cache"
	@echo "  make help               - Show this message"
	@echo ""
	@echo "Manual execution:"
	@echo "  $(PYTHON) $(SRC_DIR)/server.py <port> <output_file> <loss_prob>"
	@echo "  $(PYTHON) $(SRC_DIR)/client.py <host> <port> <input_file> <window_size> <mss>"

.SILENT: help
