import os
import mimetypes
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
import shutil
from .models import ConvertedFile
from .utils import convert_image, convert_audio, convert_video
from pydub import AudioSegment
from moviepy.editor import VideoFileClip

def file_converter_view(request):
    return render(request, 'core/upload.html')

def save_converted_file(original_file, converted_path, original_format, converted_format):
    """
    Salva o arquivo convertido no banco de dados.
    """
    converted_file_instance = ConvertedFile(
        original_file=original_file,
        converted_file=converted_path,
        original_format=original_format,
        converted_format=converted_format
    )
    converted_file_instance.save()


def get_compatible_formats(mime_type):
    """
    Retorna os formatos compatíveis baseados no tipo MIME do arquivo.
    """
    if not mime_type:
        return []
    if mime_type.startswith('image'):
        return [('png', 'PNG'), ('jpeg', 'JPEG')]
    elif mime_type.startswith('video'):
        return [('mp4', 'MP4')]
    elif mime_type.startswith('audio'):
        return [('mp3', 'MP3')]
    elif mime_type in ['application/pdf', 'text/plain']:
        return [('pdf', 'PDF')]
    return []


def convert_file(input_path, output_format):
    """
    Converte o arquivo para o formato desejado.
    """
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_name = f"{base_name}.{output_format}"
    output_dir = os.path.join(settings.MEDIA_ROOT, 'converted')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_name)

    # Identificar o tipo de arquivo e fazer a conversão adequada
    mime_type, _ = mimetypes.guess_type(input_path)

    if mime_type and mime_type.startswith('image'):
        try:
            with Image.open(input_path) as img:
                img = img.convert('RGB')
                img.save(output_path, output_format.upper())
        except Exception as e:
            return {"error": f"Erro na conversão da imagem: {str(e)}"}
    elif mime_type and mime_type.startswith('audio'):
        try:
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format=output_format)
        except Exception as e:
            return {"error": f"Erro na conversão de áudio: {str(e)}"}
    elif mime_type and mime_type.startswith('video'):
        try:
            video = VideoFileClip(input_path)
            video.write_videofile(output_path, codec='libx264')
        except Exception as e:
            return {"error": f"Erro na conversão de vídeo: {str(e)}"}
    elif mime_type == 'application/pdf' or mime_type == 'text/plain':
        shutil.copy(input_path, output_path)
    else:
        shutil.copy(input_path, output_path)

    return output_path


import os

def ajax_upload(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        file_name = file.name
        file_path = os.path.join('media', 'uploads', file_name)

        # Criar o diretório 'uploads' se não existir
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Salvar o arquivo
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Determinar o tipo de arquivo para conversão
        mime_type, _ = mimetypes.guess_type(file_path)
        compatible_formats = []

        if mime_type and mime_type.startswith('image'):
            compatible_formats = [('png', 'PNG'), ('jpeg', 'JPEG')]
        elif mime_type and mime_type.startswith('audio'):
            compatible_formats = [('mp3', 'MP3')]
        elif mime_type and mime_type.startswith('video'):
            compatible_formats = [('mp4', 'MP4')]
        elif mime_type == 'application/pdf' or mime_type == 'text/plain':
            compatible_formats = [('pdf', 'PDF')]

        if not compatible_formats:
            return JsonResponse({'error': 'Formato não suportado.'})

        return JsonResponse({
            'success': True,
            'compatible_formats': compatible_formats,
            'file_path': file_path
        })

    return JsonResponse({'error': 'Nenhum arquivo enviado ou campo "file" não encontrado.'})
