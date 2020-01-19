from zipfile import ZipFile
from os.path import dirname, join, exists
from os import mkdir, environ, pathsep, system, chdir
from io import BytesIO
import platform
import requests

team_folder = dirname(__file__)
# our team folder, used to ensure we don't put binaries anywhere they shouldn't be

# run pipenv automatically
chdir(team_folder)
system("pipenv sync")

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
        "It looks like you're running on a distribution of linux. "
        "Use your package manager to install ffmpeg.\n\n"
        "If this message has popped up erroneously, download the build relevant"
        " to you here: https://ffmpeg.zeranoe.com/builds/\n\n"
        "\x1b[34m"  # make the text BLUE - status information
        " --- The script will now terminate, no changes were made ---"
        "\x1b[39m"  # reset the text colour - so your terminal doesn't go mad
    )
    exit()

if os_name == "win":
    print(f"Detected OS: Windows ({os_bit}bit)")
    # no colour because it would require win32 calls and I didn't want
    # to add a dependency (colorama) just to prettify on windows terminal
    # - especially since this should only be run once
if os_name == "macos":
    print(
        (
            "{blue_italic}Detected OS: {light_green_italic}Mac OS "
            f"{{blue_italic}}({{light_green_italic}}{os_bit} {{blue_italic}})"
            "\x1b[0m"  # reset the colour so the terminal doesn't go mad
        ).format(blue_italic="\x1b[0;3;34m", light_green_italic="\x1b[0;1;3;32m")
        # prettify output with ~[35mcolour[0m~
    )
    assert os_bit == "64"

# now get FFmpeg binaries

zip_name = zip_name_base.format(os=os_name, os_bit=os_bit)
# plug our info into our base filename

stream = BytesIO()  # create a content buffer
distribution_data = requests.get(
    ffmpeg_build_url.format(os=os_name, os_bit=os_bit, zip_name=zip_name)
).content  # get the FFmpeg binaries
stream.write(distribution_data)  # write them into the buffer
stream.seek(0)  # move to the start of the buffer

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

# add ffmpeg binaries to path
environ["PATH"] += pathsep + join(team_folder, "ffmpeg_binaries")
# tell the user it's done
print("Done! Now run main.py")

