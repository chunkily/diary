# Diary

Simple utility to create and open weekly diary entries.

## Requirements

You will need Python 3.6 or higher to run this program.

## Installation

First clone the repository to your system. The rest of the installation steps
assume that you have cloned the repository to your home directory.

```bash
cd ~
git clone https://github.com/chunkily/diary.git
cd diary
```

The script should work across both Windows and Linux systems but the
installation steps differ a little.

### Linux

Setup the virtual environment using Make

```bash
make install
```

Or manually with the following commands

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Lastly run the following command to add the alias to your `.bashrc` file to make
the script available anywhere on your system

```bash
echo "alias diary=\"$(pwd)/venv/bin/python3 $(pwd)/diary.py\"" >> ~/.bashrc
```

### Windows

Create the virtual environment and install the dependencies

```cmd
python -m venv venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt
```

The following instructions will allow you to run the script from anywhere on
your system.

#### Windows CMD

Create a `diary.bat` file somewhere in your path with the following contents:

```cmd
@echo off
%USERPROFILE%\diary\venv\Scripts\python.exe %USERPROFILE%\diary\diary.py %*
```

Adjust the paths to the virtualenv and diary.py as necessary if you did not
clone the repository to your home directory.

#### PowerShell

Open an editor to the PowerShell profile file using `notepad $PROFILE` and add
the following function to the file, changing the paths to the virtualenv and
diary.py as appropriate:

```powershell
function diary {
    & "$HOME\diary\venv\Scripts\Activate.ps1"
    & python "$HOME\diary\diary.py" @args
    & deactivate
}
```

Adjust the paths to the virtualenv and diary.py as necessary if you did not
clone the repository to your home directory.

## Configure

The script uses 2 environment variables for configuration:

- `DIARY_DIRPATH` - The directory where the diary entries are stored. Defaults
  to the `diary_entries` folder here if unset.
- `DIARY_EDITOR` - The editor to use to open the diary entries. Defaults to the
  system default editor if unset.

You can optionally create a `.env` file in the root of the project to set these
variables. The values in this file will not override if the environment variable
has already been set.

Use the `.env.sample` file as a template.

```bash
cp .env.sample .env
```

### DIARY_EDITOR Examples

The following examples show how to set the `DIARY_EDITOR` environment variable
to use different editors. The path to the diary entry is passed as the last
argument to the editor.

Visual Studio Code:

```dotenv
DIARY_EDITOR=code --new-window
```

Notepad++:

```dotenv
# Escape spaces with a backslash
DIARY_EDITOR=C:\Program\ Files\ (x86)\Notepad++\notepad++.exe -multiInst -notabbar -nosession -noPlugin
```

## Usage

Call without any arguments to open the diary entry for the current day. If the
entry does not exist one is created for you using a template.

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

Date parsing functionality is provided via the
[dateparser library](https://dateparser.readthedocs.io/en/v1.0.0/).

## Custom Templates

You can use custom templates to generate new diary entries. The template files
are rendered using [Jinja2](https://jinja.palletsprojects.com/).

Reference the
[Jinja2 documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)
for more information on how to use the templating language.

Place your custom template files in the `templates` folder under the diary
entries folder. The system will look for a file named `diary.md.j2` in that
folder for new diary entries.

```txt
.
├── 2023-08-07.md
├── 2023-08-14.md
├── 2023-08-21.md
└── templates
    └── diary.md.j2
```

You can use `{% include "filename" %}` to include other files in that template.
For example if you wanted to render a template for each day of the week you
could create a file called `day.md.j2` and include it in the `diary.md.j2`
template.

```jinja2
templates/diary.md.j2
# {{mon}} - {{sun}}
{% for day in days %}
{% include "day.md.j2" %}
{% endfor %}
```

```jinja2
templates/day.md.j2
## {{day}}

### Project 1

### Project 2
```

### Variables

The template is passed the following variables:

- `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun` - The dates of the diary entry
  as datetime.date objects
- `week` - A tuple of the start and end dates (Monday and Sunday) of the diary
  entry as datetime.date objects
- `weekdays` - An array of the weekdays (Monday to Friday) of the diary entry as
  datetime.date objects
- `weekend` - An array of the weekend days (Saturday and Sunday) of the diary
  entry as datetime.date objects
- `days` - An array of the days (Monday to Sunday) of the diary entry as
  datetime.date objects
