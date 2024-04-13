# ffmpeg_bitrate_makefile.py

from pathlib import Path
import ffmpeg
import time
import csv
import sys

# Получение переменных из аргументов командной строки
RTSP_URL = sys.argv[1]
CSV_NAME = sys.argv[2]
OUTPUT_DIR = sys.argv[3]

# Создание пути для CSV файла
datapath_csv = Path(OUTPUT_DIR).joinpath(CSV_NAME + '.csv')

# Информация о видео с помощью FFmpeg
probe = ffmpeg.probe(RTSP_URL)
video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')

# Разрешение видео и частота кадров
width = video_info['width']
height = video_info['height']
fps = eval(video_info['avg_frame_rate'])  # Преобразуем "frames/1" в FPS

# Кодек
codec_name = video_info['codec_name']

# Эмуляция реального потока под FPS видео, а не FPS чтения потока
frame_interval = 1.0 / fps

# Открываем поток и читаем каждый пакет
stream = ffmpeg.input(RTSP_URL, rtsp_transport='tcp')  # Указываем rtsp_transport='tcp' для обеспечения надежности
output = ffmpeg.output(stream, 'pipe:', format='rawvideo', pix_fmt='rgb24')
process = ffmpeg.run_async(output, pipe_stdout=True)

# Файл CSV сохраняем
with open(datapath_csv, mode='a', newline='') as file:  # 'a' - режим дозаписи
    writer = csv.writer(file)

    # Заголовки
    if file.tell() == 0:
        writer.writerow(['Шаг', 'Время', 'Ширина', 'Высота', 'Частота кадров', 'Кодек', 'Битрейт (КБ/сек)', 'Продолжительность видео'])

    # Получаем начальное значение времени и счетчика байтов
    start_time = time.time()
    bytes_received = 0
    step = 0

    try:
        # Читаем каждый пакет и вычисляем количество информации в секунду
        for packet in process.stdout:
            bytes_received += len(packet)
            current_time = time.time()
            if current_time - start_time >= frame_interval:
                # Вычисляем битрейт и записываем в файл CSV
                bitrate = bytes_received / 1024
                elapsed_time = current_time - start_time
                human_readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
                # Рассчитываем продолжительность видео
                video_duration = step / fps
                writer.writerow([step, elapsed_time, width, height, fps, codec_name, bitrate, video_duration])
                file.flush()
                print(
                    f"Шаг: {step}, Время чтения одного кадра {elapsed_time:.2f}, Ширина: {width}, Высота: {height},"
                    f" Частота кадров: {fps}, Кодек: {codec_name},"
                    f" Битрейт: {bitrate:.2f} КБ/сек, Продолжительность чтения кадров: {video_duration:.2f} сек")
                start_time = current_time
                bytes_received = 0
                step += 1

    finally:
        # Дожидаемся завершения процесса FFmpeg
        process.wait()
