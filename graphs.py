import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных из CSV файла
df = pd.read_csv('data.csv')

# Построение графика
plt.plot(df['Секунда просмотра'], df['Битрейт (КБ/сек)'])
plt.title('График битрейта по времени')
plt.xlabel('Секунда передачи данных')
plt.ylabel('Битрейт (КБ/сек)')
plt.grid(True)
plt.show()
