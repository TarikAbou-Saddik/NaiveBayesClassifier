# Basic Makefile for running the Indonesian Dot Puzzle Application

# Make sure that Anaconda enviroment is set up.
# Ex: conda create --name environmentName python=3

# Find all our output files
DATA = data
FILE_PATTERN = $(DATA)/*_*_*_*.txt

all:
	@echo "===================================="
	@echo "Running Python program..."
	@echo "===================================="
	@python main.py

# V=0 n=1 d=0
experiment1:
	@echo "===================================="
	@echo "Running Python program..."
	@echo "===================================="
	@python main.py 0 1 0

# V=1 n=2 d=0.5
experiment2:
	@echo "===================================="
	@echo "Running Python program..."
	@echo "===================================="
	@python main.py 1 2 0.5

# V=1 n=3 d=1
experiment3:
	@echo "===================================="
	@echo "Running Python program..."
	@echo "===================================="
	@python main.py 1 3 1

# V=2 n=2 d=0.3
experiment4:
	@echo "===================================="
	@echo "Running Python program..."
	@echo "===================================="
	@python main.py 2 2 0.3

clean:
ifeq (,$(wildcard $(FILE_PATTERN)))
	@echo "===================================="
	@echo "There are no files to delete."
	@echo "===================================="
else 
	@rm $(FILE_PATTERN)
endif



