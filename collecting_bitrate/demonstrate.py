import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data_ffmpeg.csv')
plt.figure(figsize=(12, 6))

# График resolution
plt.subplot(2, 2, 1)
plt.plot(data['Шаг'], data['Ширина'], label='Ширина')
plt.plot(data['Шаг'], data['Высота'], label='Высота')
plt.xlabel('Шаг')
plt.ylabel('Размеры')
plt.title('Изменение размеров видео')
plt.legend()

# График fps
plt.subplot(2, 2, 2)
plt.plot(data['Шаг'], data['Частота кадров'])
plt.xlabel('Шаг')
plt.ylabel('Частота кадров')
plt.title('Изменение частоты кадров')

# График битрейта
plt.subplot(2, 1, 2)
plt.plot(data['Шаг'], data['Битрейт (КБ/сек)'])
plt.xlabel('Шаг')
plt.ylabel('Битрейт (КБ/сек)')
plt.title('Изменение битрейта')

# Отображение графиков
plt.tight_layout()
plt.show()
