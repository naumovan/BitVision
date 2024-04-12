import cv2
import time
import csv

# RTSP URL или путь к локальному видеофайлу
rtsp_url = "rtsp://172.21.4.110/test"
# rtsp_url = ""  # Или путь к локальному видеофайлу

# Открываем видеопоток
cap = cv2.VideoCapture(rtsp_url)

# Проверяем, удалось ли открыть видеопоток
if not cap.isOpened():
    print("Ошибка: Невозможно открыть видеопоток.")
    exit()

# Создаем файл CSV для записи
with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Шаг', 'Время', 'Ширина', 'Высота', 'Частота кадров', 'Кодек', 'Битрейт', 'Опорный кадр', 'Текущая секунда'])

    # Получаем начальное значение времени и счетчика байтов
    start_time = time.time()
    bytes_received = 0

    # Переменные для отслеживания ключевых кадров и шага сбора данных
    last_key_frame_number = -1
    step = 0

    # Мониторим характеристики потока и записываем в файл CSV
    while cap.isOpened():
        # Читаем кадр из потока
        ret, frame = cap.read()

        # Получаем текущее время
        current_time = time.time()

        # Получаем характеристики кадра
        height, width, _ = frame.shape
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Получаем информацию о кодеке видеопотока
        codec_info = cap.get(cv2.CAP_PROP_FOURCC)
        codec_name = "".join([chr((int(codec_info) >> 8 * i) & 0xFF) for i in range(4)])

        # Получаем текущий номер кадра
        frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)

        # Определяем, является ли текущий кадр ключевым
        is_key_frame = frame_number - last_key_frame_number > 1

        # Обновляем последний известный номер ключевого кадра
        if is_key_frame:
            last_key_frame_number = frame_number

        # Вычисляем размер кадра в байтах
        frame_size_bytes = frame.nbytes

        # Вычисляем время, прошедшее с начала мониторинга
        elapsed_time = current_time - start_time

        # Вычисляем общее количество байтов за время elapsed_time
        bytes_received += frame_size_bytes

        # Вычисляем битрейт в Kbps
        bitrate_kbps = (bytes_received * 8) / 1000 / elapsed_time

        # Вычисляем текущую секунду видео
        current_second = elapsed_time * fps

        # Записываем характеристики в файл CSV
        writer.writerow([step, current_time, width, height, fps, codec_name, bitrate_kbps, is_key_frame, current_second])

        # Выводим характеристики в консоль
        print(f"Шаг: {step}, Ширина: {width}, Высота: {height}, Частота кадров: {fps}, Кодек: {codec_name}, Битрейт: {bitrate_kbps:.2f} Kbps, Опорный кадр: {is_key_frame}, Текущая секунда: {current_second}")

        # Увеличиваем шаг сбора данных
        step += 1

        # Проверяем, удалось ли прочитать кадр
        if not ret:
            print("Ошибка: Невозможно прочитать кадр.")
            break

# Закрываем видеопоток и файл CSV
cap.release()
