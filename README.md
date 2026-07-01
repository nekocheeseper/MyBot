# MyBot

A modular Discord bot framework for learning, experimentation, and future extensions.
I will add some interesting features from time to time, which you can use or delete in the mod/ directory.

## Goals

- Reusable architecture
- Maintainable architecture
- Easy to extend
- Easy to debug
- Clean project structure

## Status

Early development.

## Project Structure

```text
MyBot/
├── _src
│   ├── app/
│   ├── core/
│   ├── mod/
│   └── utils/
├── data/
│   └── token
├── logs/
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
├── run.bat
├── run.py
└── run.sh
```

## Requirements

- Python 3.13
- discord.py

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Place your Discord Bot token in:

```text
data/token
```

## Run

```bash
python run.py
```

or

```bash
# Windows
run.bat

# Linux
run.sh
```

## License

MIT License.