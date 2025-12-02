PYTHON := python3
SRC_DIR := src
TESTS_DIR := tests
EXECUTABLES := $(SRC_DIR)/server.py $(SRC_DIR)/client.py

.PHONY: all test clean help server task1 task2 task3 plot

all: $(EXECUTABLES)
	@echo "Simple-FTP client and server ready"
	@echo "Run 'make help' for more options"

$(EXECUTABLES):
	@test -f $@ || (echo "Error: $@ not found"; exit 1)

test: $(EXECUTABLES)
	$(PYTHON) -m pytest $(TESTS_DIR) -v

server:
	@echo "Starting server on port 7735 with 5% loss probability..."
	@echo "Command: $(PYTHON) $(SRC_DIR)/server.py 7735 output.bin 0.05"
	@$(PYTHON) $(SRC_DIR)/server.py 7735 output.bin 0.05

task1: $(EXECUTABLES)
	@echo "Running Task 1: Effect of Window Size N on Transfer Delay"
	@echo "Server must be running separately: make server"
	@echo "Command: $(PYTHON) tasks/task_1.py --host 152.7.176.68 --file testfile_1mb.bin"
	@$(PYTHON) tasks/task_1.py --host 152.7.176.68 --file testfile_1mb.bin

task2: $(EXECUTABLES)
	@echo "Running Task 2: Effect of MSS on Transfer Delay"
	@echo "Server must be running separately: make server"
	@echo "Command: $(PYTHON) tasks/task_2.py --host 152.7.176.68 --file testfile_1mb.bin"
	@$(PYTHON) tasks/task_2.py --host 152.7.176.68 --file testfile_1mb.bin

task3: $(EXECUTABLES)
	@echo "Running Task 3: Effect of Loss Probability on Transfer Delay"
	@echo "Server must be restarted with each loss probability value"
	@echo "Command: $(PYTHON) tasks/task_3.py --host 152.7.176.68 --file testfile_1mb.bin"
	@$(PYTHON) tasks/task_3.py --host 152.7.176.68 --file testfile_1mb.bin

plot:
	@echo "Generating plots from results files..."
	@echo "Task 1 plot: $(PYTHON) plot/plot_task1.py"
	@$(PYTHON) plot/plot_task1.py
	@echo ""
	@echo "Task 2 plot: $(PYTHON) plot/plot_task2.py"
	@$(PYTHON) plot/plot_task2.py

clean:
	rm -f $(SRC_DIR)/*.pyc
	rm -rf $(SRC_DIR)/__pycache__
	rm -f $(TESTS_DIR)/*.pyc
	rm -rf $(TESTS_DIR)/__pycache__
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf plot/__pycache__

help:
	@echo "Simple-FTP with Go-Back-N Protocol"
	@echo ""
	@echo "Unit Tests:"
	@echo "  make test               - Run all unit tests (32 tests)"
	@echo ""
	@echo "Phase 5 Experiments:"
	@echo "  make server             - Start server on port 7735 (p=0.05)"
	@echo "  make task1              - Run Task 1: Window Size Effect (requires server)"
	@echo "  make task2              - Run Task 2: MSS Effect (requires server)"
	@echo "  make task3              - Run Task 3: Loss Probability Effect (requires server)"
	@echo "  make plot               - Generate plots from task results"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean              - Remove build artifacts and cache"
	@echo "  make help               - Show this message"
	@echo ""
	@echo "Typical workflow:"
	@echo "  1. make test            # Verify all tests pass"
	@echo "  2. make server          # Start server in one terminal"
	@echo "  3. make task1           # Run experiments in another terminal"
	@echo "  4. make plot            # Generate plots after experiments complete"
	@echo ""

.SILENT: help
