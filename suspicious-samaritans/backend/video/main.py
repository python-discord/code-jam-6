import ffmpeg


def create_thumbnail(source):
    (
        ffmpeg
        .input(source, ss=0)
        .output(".thumbnail.png", vframes=1)
        .run()
    )
