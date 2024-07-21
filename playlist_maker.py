import os
import random
import shutil
from datetime import datetime
from moviepy.editor import ImageClip, concatenate_audioclips, AudioFileClip
from PIL import Image
import random

VERSION = [1, 0, 0]
FPS = 60
MUSIC_COUNT = 15

MODE = "Studying" # Coding, Studying

def create_video():
    os.makedirs("Sources/Coding/used", exist_ok=True)
    os.makedirs("Sources/Studying/used", exist_ok=True)
    os.makedirs(f"Works/{MODE}", exist_ok=True)
    images = [f for f in os.listdir(f"Sources/{MODE}") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        raise Exception("  * 이미지를 찾을 수 없습니다.")
    selected_image = random.choice(images)
    image_path = os.path.join(f"Sources/{MODE}", selected_image)
    print(f"  * 이미지가 선택되었습니다: {selected_image}")
    music_files = [f for f in os.listdir("Music") if f.lower().endswith('.mp3')]
    if len(music_files) < MUSIC_COUNT:
        raise Exception(f"  * 음악 파일이 {MUSIC_COUNT}개 미만입니다.")
    selected_music = random.sample(music_files, MUSIC_COUNT)
    print("  * 음악이 선택되었습니다")
    for i, music in enumerate(selected_music, 1):
        print(f"     - {music} ({i}/{MUSIC_COUNT})")
    music_paths = [os.path.join("Music", music) for music in selected_music]
    print("  * 영상 제작을 시작합니다")
    img = Image.open(image_path)
    img = img.resize((1920, 1080), Image.LANCZOS)
    temp_image_path = f"temp_image_{random.randint(1, 1000000000)}.jpg"
    img.save(temp_image_path)
    video = ImageClip(temp_image_path).set_duration(sum([AudioFileClip(m).duration for m in music_paths]))
    video = video.set_fps(FPS)
    audio_clips = [AudioFileClip(m) for m in music_paths]
    final_audio = concatenate_audioclips(audio_clips)
    final_video = video.set_audio(final_audio)
    today = datetime.now().strftime("%Y-%m-%d")
    output_filename = f"{today}.mp4"
    output_path = os.path.join(f"Works/{MODE}", output_filename)
    counter = 1
    while os.path.exists(output_path):
        output_filename = f"{today}-({counter}).mp4"
        output_path = os.path.join(f"Works/{MODE}", output_filename)
        counter += 1
    final_video.write_videofile(output_path, fps=FPS, codec='libx264', audio_codec='aac')
    os.remove(temp_image_path)
    print(f"  * 영상이 제작되었습니다: {output_path}")
    shutil.move(image_path, os.path.join(f"Sources/{MODE}/used", selected_image))

if __name__ == "__main__":
    try:
        create_video()
    except Exception as e:
        print(f"오류 발생: {str(e)}")
