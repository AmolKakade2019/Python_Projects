# Python_Projects

**Demo repository for LangChain’s tool‑calling agent** – a collection of small Python scripts that illustrate how to create, bind, and use custom LangChain tools.

## Overview

This repo showcases:

- **Custom LangChain tools** defined with the `@tool` decorator (`get_current_time`, `WriteToFile`, etc.).
- **External tools** such as Wikipedia search and DuckDuckGo web search.
- A **minimal agent** (`main.py`) that binds these tools to a language model and executes natural‑language queries.

The goal is to provide a clear, runnable example for anyone learning how to extend LangChain agents with their own functionality.

## Installation

```bash
# Clone the repository
git clone https://github.com/AmolKakade2019/Python_Projects.git
cd Python_Projects

# (Optional) Create a virtual environment – **Python 3.10–3.13 only**
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# or CMD
.venv\Scripts\activate.bat

# Install dependencies
pip install -r Requirements.txt
```

## Prerequisites

The project relies on a few external tools and a specific Python version range:

* **Python** – Use **Python 3.10 – 3.13** (LangChain is not yet compatible with Python 3.14).  
	**Important:** The most recent Python release (currently 3.14) will cause import/runtime errors with LangChain.
* **Rust** – Required for building some LangChain dependencies. Install it from <https://www.rust-lang.org/tools/install> before running `pip install`.
* **Docker** – Needed only if you plan to run the GitHub MCP server inside VS Code. Ensure Docker Desktop (or the Docker engine) is installed and running.

These requirements are also documented as comments in `Requirements.txt`.

## Usage

Run the main script with a query of your choice:

```bash
python main.py "what is the current UTC time?"
```

The script will:

1. Build a LangChain agent with the tools defined in `tools.py`.
2. Send the query to the LLM.
3. Invoke any required tool(s) and display the result.

## Adding New Tools

1. Define a function in `tools.py` and decorate it with `@tool`.  
	 ```python
	 @tool
	 def my_tool(arg: str) -> str:
			 """Brief description of what the tool does."""
			 ...
	 ```
2. Update any imports if you need external libraries.
3. Re‑run `main.py` – the agent will automatically discover the new tool.

## Contributing

Feel free to open issues or submit pull requests. When adding new functionality:

- Follow the existing coding style (PEP 8, type hints, docstrings).
- Include tests for new tools (if you have a test suite).
- Update the README if you add notable features.

## License

This project is licensed under the MIT License – see the `LICENSE` file for details.
