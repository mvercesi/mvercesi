import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import shutil
from tqdm import tqdm

ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(image, width=100, font_size=10):
    """Convert an image to an ASCII version and return it as an image."""
    height = int((image.shape[0] / image.shape[1]) * width * 1.5)
    image = cv2.resize(image, (width, height))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    font = ImageFont.load_default()
    img_out = Image.new("RGB", (width * font_size, height * font_size), (0, 0, 0))
    draw = ImageDraw.Draw(img_out)

    for y, row in enumerate(gray):
        for x, pixel in enumerate(row):
            char = ASCII_CHARS[pixel // (255 // (len(ASCII_CHARS) - 1))]
            draw.text((x * font_size, y * font_size), char, font=font, fill=(255, 255, 255))

    return img_out

def video_to_ascii(input_video, output_video, width=100, fps=15):
    """Convert a video to an ASCII-stylized video."""
    cap = cv2.VideoCapture(input_video)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    temp_dir = "ascii_frames"

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    print("Processing frames...")
    for i in tqdm(range(frame_count)):
        ret, frame = cap.read()
        if not ret:
            break
        ascii_frame = image_to_ascii(frame, width=width)
        ascii_frame.save(f"{temp_dir}/frame_{i:05d}.png")

    cap.release()

    print("Encoding video...")
    os.system(f'ffmpeg -framerate {fps} -i {temp_dir}/frame_%05d.png -c:v libx264 -pix_fmt yuv420p {output_video}')

    shutil.rmtree(temp_dir)
    print(f"ASCII video saved as {output_video}")

# Convert video to ASCII
video_to_ascii("input.mp4", "ascii_output.mp4", width=120, fps=30)
