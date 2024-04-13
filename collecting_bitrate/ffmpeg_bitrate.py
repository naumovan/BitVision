import ffmpeg
import time
import csv

# RTSP URL или путь к локальному видеофайлу
rtsp_url = "rtsp://172.21.4.110/angle"
# rtsp_url = ""  # Или путь к локальному видеофайлу

# Получаем информацию о видео с помощью FFmpeg
probe = ffmpeg.probe(rtsp_url)
video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')

# Получаем разрешение видео и частоту кадров
width = video_info['width']
height = video_info['height']
fps = video_info['avg_frame_rate'].split('/')[0]  # Преобразуем "60/1" в "60"

# Получаем информацию о кодеке
codec_name = video_info['codec_name']

# Открываем поток и читаем каждый пакет
stream = ffmpeg.input(rtsp_url, rtsp_transport='tcp')  # Указываем rtsp_transport='tcp' для обеспечения надежности
output = ffmpeg.output(stream, 'pipe:', format='rawvideo', pix_fmt='rgb24')
process = ffmpeg.run_async(output, pipe_stdout=True)

# Открываем файл CSV для записи
with open('data_ffmpeg.csv', mode='a', newline='') as file:  # 'a' - режим дозаписи
    writer = csv.writer(file)

    # Записываем заголовки только если файл пустой
    if file.tell() == 0:
        writer.writerow(['Шаг', 'Время', 'Ширина', 'Высота', 'Частота кадров', 'Кодек', 'Битрейт (КБ/сек)'])

    # Получаем начальное значение времени и счетчика байтов
    start_time = time.time()
    bytes_received = 0
    step = 0

    try:
        # Читаем каждый пакет и вычисляем количество информации в секунду
        for packet in process.stdout:
            # Обновляем количество полученных байт
            bytes_received += len(packet)

            # Проверяем прошла ли секунда
            if time.time() - start_time >= 1:
                # Вычисляем битрейт и записываем в файл CSV
                bitrate = bytes_received / 1024
                elapsed_time = time.time() - start_time
                writer.writerow([step, elapsed_time, width, height, fps, codec_name, bitrate])

                # Немедленная запись данных на диск
                file.flush()

                # Выводим количество информации в секунду
                print(
                    f"Шаг: {step}, Время: {elapsed_time:.2f}, Ширина: {width}, Высота: {height}, Частота кадров: {fps}, Кодек: {codec_name}, Битрейт: {bitrate:.2f} КБ/сек")

                # Сбрасываем счетчики
                start_time = time.time()
                bytes_received = 0
                step += 1

    finally:
        # Дожидаемся завершения процесса FFmpeg
        process.wait()
