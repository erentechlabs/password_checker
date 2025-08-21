# Password Breach & Strength Checker

A simple command-line tool that:
- Analyzes password strength (length, character diversity).
- Checks if a password appears in known data breaches using the Have I Been Pwned (HIBP) Pwned Passwords API with k-Anonymity.

## Requirements

- Python 3.13+
- virtualenv
- Packages: requests

## Setup

1) Create and activate a virtual environment:
- Linux/macOS:
  - python3 -m venv .venv
  - source .venv/bin/activate
- Windows (PowerShell):
  - py -m venv .venv
  - .\.venv\Scripts\Activate.ps1

2) Install dependencies:
- pip install requests

## Usage

Run the script:
- python password_checker.py

You will be prompted to enter a password (input is hidden). The tool will:
- Print a strength level and suggestions for improvement.
- Query the HIBP range API to report if the password appears in known breaches and how many times.

Note: No API key is required for the HIBP range endpoint.

## How It Works

- Strength analysis checks:
  - Length threshold (with guidance to use 12+ characters)
  - Uppercase, lowercase, digits, and special characters
- Breach check:
  - Computes SHA-1 of your password locally.
  - Sends only the first 5 hex characters of the hash to HIBP (k-Anonymity).
  - Compares returned suffixes locally to determine if your password is in breaches.

## Security Notes

- Your plaintext password never leaves your machine.
- Only a 5-character SHA-1 prefix is sent to HIBP.
- Do not reuse passwords; even if not found in breaches, uniqueness per site is essential.
- Prefer passphrases (12+ chars) and consider a password manager.

## Troubleshooting

- Network/HTTP errors: Ensure internet connectivity; HIBP may rate-limit requests—try again later.
- Empty input: The tool requires a non-empty password.
- SSL issues: Ensure your environment’s certificates are up to date.

## Development

- Lint/format as desired.
- Consider adding unit tests for strength analysis and request mocking for the HIBP call.

## License

MIT (or your preferred license)