# Steam Market Scraper Parser

<div 
	style="display: flex; 
	align-items: center;">
  <a 
	style="text-decoration: none; color: inherit; margin-right:10px;" 
    href="https://github.com/RandomProgramm3r/Steam-Market-Scraper/actions/workflows/linting.yml/">
    <img 
        src="https://github.com/RandomProgramm3r/Steam-Market-Scraper/actions/workflows/linting.yml/badge.svg" 
        alt="pipeline status" 
        height="30" 
        width="140">
  </a>
  <a 
    href="https://steamcommunity.com/market/">
    <img 
        src="https://steamcommunity.com/favicon.ico" 
        alt="Steam logo" 
        height="30" 
        width="30">
  </a>
</div>

## TOC

- [📋 Description](#-description)
- [💻 Requirements](#-requirements)
- [🚀 Project Installation](#-project-installation)
	- [📂 Step 1: Clone the Repository](#-step-1-clone-the-repository)
	- [🖥 Step 2: Create and activate a virtual environment](#-step-2-create-and-activate-a-virtual-environment)
	- [🔃 Step 3: Installing Dependencies](#-step-3-installing-dependencies)
		- [🛠️ Dependencies for development (dev)](#%EF%B8%8F-dependencies-for-development-dev)
- [⚙ Linters](#-linters)
- [🧩 Usage](#-usage)
- [🔨 Function Signature](#-function-signature)
- [📤 Example](#-example)


## 📋 Description

This project is a parser for the steam market of such games as CS 2, Team Fortress 2, Dota 2, PUBG, RUST, etc.


This guide describes the steps to install and run the project on Linux and Windows.


## 💻 Requirements

Before you start, make sure that the following components are installed on your system:

- **Python 3** (check with `python3 --version` Linux / `python --version` Windows)
#### I'm using Python 3.13. Other versions will probably work.
- **pip** (check with `pip --version`)
- **Git** (check with `git --version`)
- **Python Virtual Environment** (venv)
- **Linux Shell** (for example, Bash)

## 🚀 Project Installation

### 📂 Step 1: Clone the Repository

Clone the project repository using Git:

```bash
git clone https://github.com/RandomProgramm3r/Steam-Market-Scraper
```

### 🖥 Step 2: Create and activate a virtual environment

Create a virtual environment using the `venv` command, which allows you to isolate project dependencies:

```bash
python3 -m venv venv # Linux
python -m venv venv # Windows
```

Activate the virtual environment:

```bash
source venv/bin/activate # Linux
source venv/Scripts/activate # Windows
```

### 🔃 Step 3: Installing Dependencies

Dependencies are divided into two groups:

- **For development (dev)** – additional dependencies for development.
- **For code analysis (flake8)** – additional dependencies for code analysis.

#### 🛠️ Dependencies for development (dev)

Install the dependencies for local development (they include all **flake8** dependencies)

```bash
pip install -r requirements/dev.txt
```

Now you can use the parser. 


## ⚙ Linters

If there are any changes, I recommend using linters:

```bash

flake8 . --count --show-source --statistics # Use to view PEP8 errors.
black . --verbose # Use to format code.
isort . --verbose # Use to format the order of imports.
```


## 🧩 Usage
##### A market_scraper function retrieves pricing information for a specified item from the Steam Community Market. 
##### It constructs the request URL using the item name, Steam application ID, and the desired currency, the fetches and decodes the JSON response.

##### the list of all available currencies is stored in data.py, as well as a list with some games from steam. (you can add your own games)

## 🔨 Function Signature
```python
import data
def market_scraper(
    item_name: str,
    app_id: int,
    currency: int = data.Currency.USD.value,
) -> str:
	pass
```

#### Parameters:
##### item_name (str): Full name of the item.
##### app_id (int): Steam Application ID.
##### currency (int, optional): Currency code (default: USD).

#### Returns:
##### A dictionary with the JSON response or a string with an error message.


## 📤 Example

```python
import data
import scraper

# Example usage: Fetch price information for 'Dreams & Nightmares Case' in USD for the CS2 app.
# see more in examples.py
print(
    scraper.market_scraper(
        'Dreams & Nightmares Case',
        data.Apps.CS2.value,
        data.Currency.USD.value,
    ),
)
```
#### Output json data:
```json
{
    "success": true,
    "lowest_price": "$1.90",
    "volume": "77,555",
    "median_price": "$1.90"
}
```