import cv2
import numpy as np

# Определяем параметры видео
frame_width = 1920
frame_height = 1080
fps = 30

# Создаем объект VideoWriter
out = cv2.VideoWriter('white_background_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

# Создаем белый кадр
white_frame = np.ones((frame_height, frame_width, 3), dtype=np.uint8) * 255  # Белый фон

# Записываем кадры в видео
for _ in range(140):  # Создаем 100 кадров
    out.write(white_frame)

# Освобождаем объект VideoWriter
out.release()

print("Видео успешно создано.")
