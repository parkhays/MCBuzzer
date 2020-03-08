#!/bin/bash

# This command should be run on the manylinux (2010 or newer) docker
# image at https://github.com/pypa/manylinux. I used the 2010 image
# for compatibility, but the 2014 version would probably work fine too.
#
# To install Python 3 on the image, I ran these commands:
# yum install centos-release-scl
# yum install rh-python36
#
# Then, to actually use the packages:
# scl enable rh-python36 bash
#
# Pip needs to install PyInstaller:
# pip install pyinstaller


pyinstaller --onefile --windowed \
	    --add-data "resources/main_banner.jpg:./resources" \
	    --add-data "LICENSE:." \
	    --add-data "resources/ABOUT.txt:./resources" \
	    --add-data "resources/main_logo1.ico:./resources" \
	    Source/mcbuzzer.py


# Note that the semicolons in the Windows version have to be replaced
# with colons because the *nix path seperator is a colon.
#
# UPX doesn't help whatsoever, so don't use it.
