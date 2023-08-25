"""Script to open/create diary entries."""
import os
import platform
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

        mon_formatted = f"Mon {mon.day} {mon.strftime('%b')}"
        tue_formatted = f"Tue {tue.day} {tue.strftime('%b')}"
        wed_formatted = f"Wed {wed.day} {wed.strftime('%b')}"
        thu_formatted = f"Thu {thu.day} {thu.strftime('%b')}"
        fri_formatted = f"Fri {fri.day} {fri.strftime('%b')}"
        sat_formatted = f"Sat {sat.day} {sat.strftime('%b')}"
        sun_formatted = f"Sun {sun.day} {sun.strftime('%b')}"

        week_formatted = (
            f"{mon.day} {mon.strftime('%b')} - {sun.day} {sun.strftime('%b')}"
        )

        # strftime doesn't have a format for non zero padded days.
        diary_vars = {
            "mon": mon_formatted,
            "tue": tue_formatted,
            "wed": wed_formatted,
            "thu": thu_formatted,
            "fri": fri_formatted,
            "sat": sat_formatted,
            "sun": sun_formatted,
            "weekdays": [
                mon_formatted,
                tue_formatted,
                wed_formatted,
                thu_formatted,
                fri_formatted,
            ],
            "weekend": [sat_formatted, sun_formatted],
            "days": [
                mon_formatted,
                tue_formatted,
                wed_formatted,
                thu_formatted,
                fri_formatted,
                sat_formatted,
                sun_formatted,
            ],
            "week": week_formatted,
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

    template = env.get_template("diary.txt.j2")

    content = template.render(diary_vars)

    with open(diary_filepath, "w") as f:
        f.write(content)


def load_config():
    diary_dirpath = os.getenv("DIARY_DIRPATH")
    diary_editor = os.getenv("DIARY_EDITOR").split(" ")

    if diary_dirpath is None:
        diary_dirpath = Path(__file__).parent / "diary_entries"

    diary_dirpath = Path(diary_dirpath).expanduser()

    if diary_editor is None:
        # Try to use the default editor for the current platform
        # This should have the same behaviour as double clicking a file
        diary_editor = ["open"]

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
