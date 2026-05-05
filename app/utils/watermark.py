import base64
import io
import os
import tempfile
import ffmpeg
import filetype
from PIL import Image

default_watermark = Image.open("resources/images/watermark.png").convert("RGBA")


def detect_media_type(b64_string: str) -> str:
    """
    Detects if a base64 string is an image or video
    """

    if "," in b64_string[:50]:
        b64_string = b64_string.split(",")[1]

    header_bytes = base64.b64decode(b64_string[:400])

    kind = filetype.guess(header_bytes)

    if kind is None:
        return "unknown"

    if kind.mime.startswith("image"):
        return "image"
    elif kind.mime.startswith("video"):
        return "video"

    return "other"


def apply_image_watermark_b64(
    input_b64: str, watermark_image: Image.Image = default_watermark, offset=(20, 20)
) -> str:
    """Decodes base64 image, pastes watermark, and returns base64 string."""

    base_data = base64.b64decode(input_b64)

    base = Image.open(io.BytesIO(base_data)).convert("RGBA")
    mark = watermark_image.convert("RGBA")

    scale_factor = 0.10
    aspect_ratio = mark.height / mark.width

    new_mark_width = int(base.width * scale_factor)
    new_mark_height = int(new_mark_width * aspect_ratio)

    mark = mark.resize((new_mark_width, new_mark_height), Image.Resampling.LANCZOS)
    # Calculate position (Bottom-Right)
    x = base.width - mark.width - offset[0]
    y = base.height - mark.height - offset[1]

    base.paste(mark, (x, y), mark)

    buffered = io.BytesIO()
    base.convert("RGB").save(buffered, format="JPEG", quality=95)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def apply_video_watermark_b64(
    video_b64: str, watermark_image: Image.Image = default_watermark
) -> str:
    """Processes video watermark using temporary files for FFmpeg compatibility."""

    with (
        tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as video_tmp,
        tempfile.NamedTemporaryFile(suffix=".png", delete=False) as mark_tmp,
        tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as output_tmp,
    ):
        try:
            video_tmp.write(base64.b64decode(video_b64))
            watermark_image.save(mark_tmp, format="png")

            video_tmp.flush()
            mark_tmp.flush()

            main = ffmpeg.input(video_tmp.name)
            logo = ffmpeg.input(mark_tmp.name)
            logo = logo.filter("scale", "iw*0.10", "-1")
            (
                ffmpeg.filter(
                    [main, logo],
                    "overlay",
                    x="main_w-overlay_w-(main_w*0.02)",
                    y="main_h-overlay_h-(main_h*0.02)",
                )
                .output(
                    output_tmp.name,
                    vcodec="libx264",
                    crf=18,
                    preset="veryfast",
                    pix_fmt="yuv420p",
                )
                .overwrite_output()
                .run(quiet=True)
            )

            with open(output_tmp.name, "rb") as result_file:
                encoded_video = base64.b64encode(result_file.read()).decode("utf-8")

            return encoded_video

        finally:
            for f in [video_tmp.name, mark_tmp.name, output_tmp.name]:
                if os.path.exists(f):
                    os.remove(f)


def auto_watermark(
    media_b64: str, watermark_image: Image.Image = default_watermark
) -> str:
    """
    Automatically detects media type and applies the appropriate watermark.
    """
    media_type = detect_media_type(media_b64)

    if media_type == "image":
        return apply_image_watermark_b64(media_b64, watermark_image)
    elif media_type == "video":
        return apply_video_watermark_b64(media_b64, watermark_image)
    else:
        # raise ValueError(f"Unsupported media type detected: {media_type}")
        return media_b64
