import pandas as pd
import matplotlib.pyplot as plt
#from data_processing import output_file_path

# Загрузка данных
#data_with_losses_unscaled_test = pd.read_csv(output_file_path)
data_with_losses_unscaled_test = pd.read_csv('../outputs_after_vae/test.csv')
normals_value = data_with_losses_unscaled_test[data_with_losses_unscaled_test['anomaly'] == False]
anomalies_ts = data_with_losses_unscaled_test.loc[data_with_losses_unscaled_test['anomaly'],
('Время видео', 'Битрейт (КБ/сек)')]
anomalies_value = data_with_losses_unscaled_test[data_with_losses_unscaled_test['anomaly'] == True]

plt.figure(figsize=(8,8))
plt.hist([normals_value['Битрейт (КБ/сек)'], anomalies_value['Битрейт (КБ/сек)']], bins=500,
         stacked=True, label=['Обычные', 'Аномальные'])
plt.title("Распределение видеобитрейта на тестовом наборе данных")
plt.xlabel("Видеобитрейт (биннед)")
plt.ylabel("Количество")
plt.legend()

fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(data_with_losses_unscaled_test['Время видео'], data_with_losses_unscaled_test['Битрейт (КБ/сек)'], alpha=0.3)
ax.scatter(anomalies_ts['Время видео'], anomalies_ts['Битрейт (КБ/сек)'], color='red', label='Аномалии')
plt.legend()
plt.xlabel("Время")
plt.ylabel("Видеобитрейт")
plt.title("Изменение видеобитрейта во времени с выделением аномальных значений")

plt.show()
