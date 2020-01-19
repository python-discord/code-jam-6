from zipfile import ZipFile
from os.path import dirname, join, exists
from os import mkdir, environ, pathsep
from io import BytesIO
import requests
import platform


ffmpeg_build_url = (
    "https://ffmpeg.zeranoe.com/builds/{os}{os_bit}/static/{zip_name}.zip"
)
zip_name_base = "ffmpeg-20200115-0dc0837-{os}{os_bit}-static"
# os = win, macos
# os_bit = 32, 64 if win, 64 if macos

# platform.architecture() -> ('64bit', '') on macos
#                         -> ('32bit', 'WindowsPE') on win32 (?)
#                         -> ('64bit', 'WindowsPE') on win64
#                         -> ('64bit', 'ELF') on Fedora64 (linux not needed but did need to confirm different)
team_folder = dirname(__file__)

os_bit, os_name = platform.architecture()
os_bit = os_bit[:2]  # trim off 'bit'
os_name = "win" if os_name == "WindowsPE" else ("macos" if not os_name else "LINUX")

if os_name == "LINUX":
    print(
        "\x1b[33mIt looks like you're running on a distribution of linux."
        " Use your package manager to install ffmpeg."
    )
    exit()

zip_name = zip_name_base.format(os=os_name, os_bit=os_bit)

stream = BytesIO()
distribution_data = requests.get(
    ffmpeg_build_url.format(os=os_name, os_bit=os_bit, zip_name=zip_name)
).content
stream.write(distribution_data)
stream.seek(0)

if os_name == "win":
    extension = ".exe"
else:
    extension = ""

if not exists(join(team_folder, "ffmpeg_binaries")):
    mkdir(join(team_folder, "ffmpeg_binaries"))

with ZipFile(stream) as file:
    with file.open(zip_name + "/bin/ffmpeg" + extension) as ffmpeg_exe:
        with open(
            join(team_folder, "ffmpeg_binaries", "ffmpeg" + extension), "wb"
        ) as target_file:
            target_file.write(ffmpeg_exe.read())
    with file.open(zip_name + "/bin/ffplay" + extension) as ffplay_exe:
        with open(
            join(team_folder, "ffmpeg_binaries", "ffplay" + extension), "wb"
        ) as target_file:
            target_file.write(ffplay_exe.read())
    with file.open(zip_name + "/bin/ffprobe" + extension) as ffprobe_exe:
        with open(
            join(team_folder, "ffmpeg_binaries", "ffprobe" + extension), "wb"
        ) as target_file:
            target_file.write(ffprobe_exe.read())

environ["PATH"] += pathsep + join(team_folder, "ffmpeg_binaries")

