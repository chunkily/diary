dist/diary: diary.py requirements.txt
	pip install -r requirements.txt
	pyinstaller -F diary.py
