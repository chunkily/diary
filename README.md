# Diary

Simple utility to create and open diary entries.

## Installation

Install the dependencies and create an alias to run the script.

```bash
pip install -r requirements.txt
echo "alias diary=\"python3 $(pwd)/diary.py\"" >> ~/.bashrc
```

Alternatively use pyinstaller and place built executable somewhere in your PATH.

```bash
pip install -r requirements.txt
pyinstaller -F diary.py
cp dist/diary ~/bin/
```

Set the environment variables

```bash
echo "DIARY_DIRPATH=~/mydiary/" >> ~/.bashrc
echo "DIARY_EDITOR=vim" >> ~/.bashrc
```

## Usage

Open the diary entry for the current day. If the entry does not exist one is created for you.

```shell
diary
```

Open the diary entry for last week

```shell
diary last week
```

Open the diary entry for a given date

```shell
diary 20 April 2020
```

Date parsing functionality is provided via the [dateparser library](https://dateparser.readthedocs.io/en/latest/).
