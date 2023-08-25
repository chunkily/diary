"""Script to open/create diary entries."""
import os
import re
import subprocess
import sys
from datetime import datetime as dt
from datetime import timedelta
from pathlib import Path

import dateparser
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape


def main(requested_date_str):
    cfg = load_config()
    diary_dirpath = cfg["DIARY_DIRPATH"]
    diary_editor = cfg["DIARY_EDITOR"]

    if requested_date_str == "":
        requested_date = dt.today()
    else:
        requested_date = parse_date(requested_date_str)

    monday_date = requested_date - timedelta(days=requested_date.weekday())

    # Use Monday's date as part of the file name.
    diary_filepath = diary_dirpath / monday_date.strftime("%Y-%m-%d.md")

    if not diary_filepath.exists():
        print("Creating {} with template.".format(diary_filepath.name))
        mon = monday_date
        tue = monday_date + timedelta(days=1)
        wed = monday_date + timedelta(days=2)
        thu = monday_date + timedelta(days=3)
        fri = monday_date + timedelta(days=4)
        sat = monday_date + timedelta(days=5)
        sun = monday_date + timedelta(days=6)

        diary_vars = {
            "mon": mon,
            "tue": tue,
            "wed": wed,
            "thu": thu,
            "fri": fri,
            "sat": sat,
            "sun": sun,
            "weekdays": [
                mon,
                tue,
                wed,
                thu,
                fri,
            ],
            "weekend": [sat, sun],
            "days": [
                mon,
                tue,
                wed,
                thu,
                fri,
                sat,
                sun,
            ],
            "week": (mon, sun),
        }

        write_template(diary_filepath, diary_vars)

    # Open the diary entry with the configured editor
    subprocess.run([*diary_editor, diary_filepath])


def parse_date(date_str):
    # Use dateparser to parse the requested date string
    date = dateparser.parse(
        date_str,
        settings={
            "PREFER_DATES_FROM": "past",
            "PREFER_DAY_OF_MONTH": "first",
        },
    )
    return date


def write_template(diary_filepath, diary_vars):
    default_template_dirpath = Path(__file__).parent / "templates"
    diary_template_dirpath = Path(diary_filepath).parent / "templates"

    env = Environment(
        loader=FileSystemLoader([diary_template_dirpath, default_template_dirpath]),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = env.get_template("diary.md.j2")

    content = template.render(diary_vars)

    with open(diary_filepath, "w") as f:
        f.write(content)


def load_config():
    diary_dirpath_str = os.getenv("DIARY_DIRPATH", default="")
    diary_editor_str = os.getenv("DIARY_EDITOR", default="")

    if diary_dirpath_str == "":
        diary_dirpath = Path(__file__).parent / "diary_entries"

    diary_dirpath = Path(diary_dirpath).expanduser()

    if not diary_dirpath.exists():
        raise Exception(f"Diary directory {diary_dirpath} does not exist.")

    if diary_editor_str == "":
        # Try to use the default editor for the current platform
        # This should have the same behaviour as double clicking a file
        diary_editor = ["open"]
    else:
        # Split the editor string on spaces, but exclude spaces that are preceded by a backslash
        diary_editor = re.split(r"(?<!\\) ", diary_editor_str)
        # Remove the backslash from any escaped spaces
        diary_editor = [s.replace("\\ ", " ") for s in diary_editor]

    return {
        "DIARY_DIRPATH": diary_dirpath,
        "DIARY_EDITOR": diary_editor,
    }


if __name__ == "__main__":
    load_dotenv()
    args = sys.argv[1:]
    # Join all arguments into a single string.
    # example ["last", "week"] becomes "last week"
    main(" ".join(args))
