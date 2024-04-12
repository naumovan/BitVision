import ffmpeg
import time
import csv
from datetime import datetime

# RTSP URL или путь к локальному видеофайлу
rtsp_url = "rtsp://172.21.4.110/test"
# rtsp_url = ""  # Или путь к локальному видеофайлу

# Открываем поток и читаем каждый пакет
stream = ffmpeg.input(rtsp_url, rtsp_transport='tcp')  # Указываем rtsp_transport='tcp' для обеспечения надежности
output = ffmpeg.output(stream, 'pipe:', format='rawvideo', pix_fmt='rgb24')
process = output.run_async(pipe_stdout=True)

# Открываем файл CSV для записи
with open('data_test.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Таймштамп', 'Битрейт (КБ/сек)'])

    # Читаем каждый пакет и вычисляем количество информации в секунду
    for packet in process.stdout:
        # Вычисляем битрейт
        bitrate = len(packet) / 1024

        # Получаем текущий таймштамп
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        # Записываем данные в файл CSV
        writer.writerow([timestamp, bitrate])

        # Выводим количество информации в секунду
        print(f"Таймштамп: {timestamp}, Скорость потока данных: {bitrate:.2f} КБ/сек")
