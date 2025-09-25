


# Makefile for TikTok Live Viewer Bot project

.PHONY: install test generate_accounts run clean help

# Default target
help:
	@echo "Usage:"
	@echo "  make install       - Install dependencies"
	@echo "  make test          - Run tests (if available)"
	@echo "  make generate_accounts - Generate fake accounts for testing"
	@echo "  make run           - Run the bot"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make help          - Show this help message"

install:
	pip install -r requirements.txt

test:
	# Add test commands here
	@echo "No tests available yet."

generate_accounts:
	python generate_fake_accounts.py

run: install
	python tiktok_bot.py

clean:
	rm -rf *.pyc __pycache__ build dist *.egg-info

