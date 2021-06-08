"""Script to open/create diary entries."""
from datetime import datetime as dt, timedelta
from pathlib import Path
import os
import subprocess
import sys
import dateparser

DIARY_TEMPLATE = """# Mon {mon}

# Tue {tue}

# Wed {wed}

# Thu {thu}

# Fri {fri}
"""


def main(requested_date_str):
    cfg = load_config()
    diary_dirpath = Path(cfg["DIARY_DIRPATH"]).expanduser()
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

        # strftime doesn't have a format for non zero padded days.
        diary_contents = DIARY_TEMPLATE.format(
            mon="{} {}".format(mon.day, mon.strftime("%b")),
            tue="{} {}".format(tue.day, tue.strftime("%b")),
            wed="{} {}".format(wed.day, wed.strftime("%b")),
            thu="{} {}".format(thu.day, thu.strftime("%b")),
            fri="{} {}".format(fri.day, fri.strftime("%b")),
        )
        with diary_filepath.open("w") as f:
            f.write(diary_contents)

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


def load_config():
    DIARY_DIRPATH = os.getenv("DIARY_DIRPATH")

    DIARY_EDITOR = os.getenv("DIARY_EDITOR").split(" ")

    if DIARY_DIRPATH is None:
        raise ValueError("DIARY_DIRPATH is unset!")

    if DIARY_EDITOR is None:
        raise ValueError("DIARY_EDITOR is unset!")

    return {
        "DIARY_DIRPATH": DIARY_DIRPATH,
        "DIARY_EDITOR": DIARY_EDITOR,
    }


if __name__ == "__main__":
    args = sys.argv[1:]
    # Join all arguments into a single string.
    # example ["last", "week"] becomes "last week"
    main(" ".join(args))
