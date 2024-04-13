import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('/Users/user/PycharmProjects/ByteRateAnalyse/inputs_for_vae_processing_csv/36cam.csv')
plt.figure(figsize=(12, 12))

# График resolution
plt.subplot(3, 1, 1)
plt.plot(data['Шаг'], data['Ширина'], label='Ширина')
plt.plot(data['Шаг'], data['Высота'], label='Высота')
plt.xlabel('Шаг')
plt.ylabel('Размеры')
plt.title('Изменение размеров видео')
plt.legend()

# График fps
plt.subplot(3, 1, 2)
plt.plot(data['Шаг'], data['Частота кадров'])
plt.xlabel('Шаг')
plt.ylabel('Частота кадров')
plt.title('Изменение частоты кадров')

# График битрейта от шага
plt.subplot(3, 1, 3)
plt.plot(data['Шаг'], data['Битрейт (КБ/сек)'])
plt.xlabel('Шаг')
plt.ylabel('Битрейт (КБ/сек)')
plt.title('Изменение битрейта от шага чтения')

plt.figure(figsize=(12, 6))
# График битрейта от времени
plt.plot(data['Шаг'], data['Битрейт (КБ/сек)'])
plt.xlabel('Время видео')
plt.ylabel('Битрейт (КБ/сек)')
plt.title('Изменение битрейта от времени чтения')

# Отображение графиков
plt.tight_layout()
plt.show()
