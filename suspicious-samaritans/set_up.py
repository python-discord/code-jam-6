from zipfile import ZipFile
from os.path import dirname, join, exists
from os import mkdir, environ, pathsep, system, chdir
from io import BytesIO
import platform
import json
import requests


team_folder = dirname(__file__) or "."
# our team folder, used to ensure we don't put binaries anywhere they shouldn't be

# locale dict for the setup program
locale = {
    "en": {
        "depinstall": "Installing dependencies...",
        "done": "Done!",
        "getsys": "Identifying OS...",
        "nolinuxmain": "It looks like you're running on a distribution of linux. "
        "Use your package manager to install FFmpeg.\n"
        "(For example, on Ubuntu this is apt)\n\n"
        "If this message has popped up erroneously, download the build relevant"
        " to you here: https://ffmpeg.zeranoe.com/builds/\n\n",
        "nolinuxstatus": " --- The script will now terminate, FFmpeg has not been installed --- ",
        "detectedos": "Detected OS: Windows ({os_bit}bit)",
        "detectedoscolour": (
            "{blue_italic}Detected OS: {light_green_italic}Mac OS "
            "{blue_italic}({light_green_italic}{{os_bit}} {blue_italic})"
        ).format(blue_italic="\x1b[0;3;34m", light_green_italic="\x1b[0;1;3;32m"),
        "macos32bit": "Your Mac OS reported as being 32bit - this isn't supported by FFmpeg",
        "ffmpegdown": "Downloading FFmpeg...",
        "extract": "Extracting files...",
        "path": "Adding FFmpeg to PATH",
        "run": "Now run main.py",
    }
}

# get user locale setting
# TODO: add multiple-language prompts here
print(f"Available languages: {' | '.join(locale.keys())}")
chosen_locale = input(
    "Enter your preferred language (this will also be used as your"
    " preference within VC:R)\n>>> "
).lower()

while chosen_locale not in locale.keys():
    chosen_locale = input(
        "That isn't a valid language. Available "
        f"languages: {' | '.join(locale.keys())}\n>>> "
    ).lower()

# TODO: think of better pun
with open(join(team_folder, ".vcrrcv"), "w") as file:
    # Video Creator: Retro - Retro Config Verifiable
    # TODO: figure out defaults and set them here
    config = {"locale": chosen_locale}
    file.write(json.dumps(config))

locale_dict = locale[chosen_locale]

# run pipenv automatically
print(locale_dict["depinstall"])
chdir(team_folder)
system("pipenv sync")
print(locale_dict["done"])

print(locale_dict["getsys"])
ffmpeg_build_url = "https://ffmpeg.zeranoe.com/builds/{os}{os_bit}/static/{zip_name}.zip"  # binary download url
zip_name_base = "ffmpeg-20200115-0dc0837-{os}{os_bit}-static"
# name of the zip file and its root folder

# identify and normalise the platform
# os = win, macos
# os_bit = 32, 64 if win, 64 if macos
# -----------------------------------
# platform.architecture() -> ('64bit', '') on macos
#                         -> ('32bit', 'WindowsPE') on win32 (?)
#                         -> ('64bit', 'WindowsPE') on win64
#                         -> ('64bit', 'ELF') on Fedora64 (linux not needed but did need to confirm different)
os_bit, os_name = platform.architecture()
os_bit = os_bit[:2]  # trim off 'bit'
os_name = "win" if os_name == "WindowsPE" else ("macos" if not os_name else "LINUX")
# Couldn't really test this line. Hopefully no false positives or false negatives
# Thanks to joseph#1337 for giving me macos output

# if you're running linux you have a package manager for this
# ...and there are no compiled binaries available
if os_name == "LINUX":
    print(
        "\x1b[33m"  # make the text YELLOW - as a 'warn' - that this script did nothing
        # should always work on unix-based OSs unless in IDLE
        + locale_dict["nolinuxmain"]
        + "\x1b[34m"  # make the text BLUE - status information
        + locale_dict["nolinuxstatus"]
        + "\x1b[39m"  # reset the text colour - so your terminal doesn't go mad
    )
    exit()

if os_name == "win":
    print(locale_dict["detectedos"].format(os_bit=os_bit))
    # no colour because it would require win32 calls and I didn't want
    # to add a dependency (colorama) just to prettify on windows terminal
    # - especially since this should only be run once
if os_name == "macos":
    print(
        locale_dict["detectedoscolour"].format(os_bit=os_bit)
        +
        # prettify output with ~[35mcolour[0m~
        "\x1b[0m"  # reset the colour so the terminal doesn't go mad
    )
    assert os_bit == "64", locale_dict["macos32bit"]

print(locale_dict["done"])

# now get FFmpeg binaries

zip_name = zip_name_base.format(os=os_name, os_bit=os_bit)
# plug our info into our base filename
print(locale_dict["ffmpegdown"])
stream = BytesIO()  # create a content buffer
distribution_data = requests.get(
    ffmpeg_build_url.format(os=os_name, os_bit=os_bit, zip_name=zip_name)
).content  # get the FFmpeg binaries
stream.write(distribution_data)  # write them into the buffer
stream.seek(0)  # move to the start of the buffer
print(locale_dict["done"])
print(locale_dict["extract"])

# work out the file extension to look for
# found by inspection of the zips
if os_name == "win":
    extension = ".exe"
if os_name == "macos":
    extension = ""

# See if the ffmpeg binaries folder exists. If it doesn't, make it
if not exists(join(team_folder, "ffmpeg_binaries")):
    mkdir(join(team_folder, "ffmpeg_binaries"))

# Open the zip file downloaded before
with ZipFile(stream) as file:
    # extract ffmpeg
    with file.open(zip_name + "/bin/ffmpeg" + extension) as ffmpeg_exe:
        with open(
            join(team_folder, "ffmpeg_binaries", "ffmpeg" + extension), "wb"
        ) as target_file:
            target_file.write(ffmpeg_exe.read())

    # extract ffplay
    with file.open(zip_name + "/bin/ffplay" + extension) as ffplay_exe:
        with open(
            join(team_folder, "ffmpeg_binaries", "ffplay" + extension), "wb"
        ) as target_file:
            target_file.write(ffplay_exe.read())

    # extract ffprobe
    with file.open(zip_name + "/bin/ffprobe" + extension) as ffprobe_exe:
        with open(
            join(team_folder, "ffmpeg_binaries", "ffprobe" + extension), "wb"
        ) as target_file:
            target_file.write(ffprobe_exe.read())

print(locale_dict["done"])
print(locale_dict["path"])
# add ffmpeg binaries to path
environ["PATH"] += pathsep + join(team_folder, "ffmpeg_binaries")
# tell the user it's done
print(locale_dict["done"])
print(locale_dict["run"])

