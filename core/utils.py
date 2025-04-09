from PIL import Image
import pydub
import moviepy.editor as mp

# Função para conversão de imagem
def convert_image(input_path, output_path, format):
    try:
        img = Image.open(input_path)
        img.save(output_path, format=format)
        return output_path
    except Exception as e:
        return str(e)

# Função para conversão de áudio
def convert_audio(input_path, output_path, format):
    try:
        audio = pydub.AudioSegment.from_file(input_path)
        audio.export(output_path, format=format)
        return output_path
    except Exception as e:
        return str(e)

# Função para conversão de vídeo
def convert_video(input_path, output_path):
    try:
        video = mp.VideoFileClip(input_path)
        video.write_videofile(output_path, codec='libx264')
        return output_path
    except Exception as e:
        return str(e)
