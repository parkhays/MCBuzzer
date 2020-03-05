# --windowed means no console will open
# The resources/main_banner.jpg must be added, code changes to
# mcbuzzer.py were required to make it work
# --onefile produces a single executable

pyinstaller --windowed --onefile --add-data "resources/main_banner.jpg;./resources" --add-data "resources/LICENSE.txt;./resources" --add-data "resources/ABOUT.txt;./resources" mcbuzzer.py 