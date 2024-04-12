import ffmpeg
import time

rtsp_url="rtsp://172.21.4.110/36cam"
stream = ffmpeg.input("rtsp://172.21.4.110/36cam", ss=0)
file = stream.output("test.png", vframes=1)

start_time = time.time()


def send_bitrate(rtsp_url):
    seconds_elapsed = 0  # Переменная для отслеживания прошедших секунд

    while True:
        try:
            # Получаем данные о пакетах в течение 1 секунды
            packets = ffmpeg.probe(rtsp_url, select_streams='v:0', show_entries='packet=pts_time,pkt_size',
                                   read_intervals='%+#1')
            # Вычисляем битрейт
            bitrate = sum(int(packet['pkt_size']) for packet in packets['packets']) * 8 / float(seconds_elapsed)
            print("Битрейт трансляции RTSP:", bitrate, "бит/сек")
        except Exception as e:
            print("Ошибка:", e)  # Выводим сообщение об ошибке

        # Выводим количество секунд, которое цикл выполняется
        print("Прошло секунд:", seconds_elapsed)

        seconds_elapsed += 1  # Увеличиваем количество прошедших секунд
        time.sleep(1)  # Ждем 1 секунду перед следующей проверкой

        seconds_elapsed += 1  # Увеличиваем количество прошедших секунд
        time.sleep(1)  # Ждем 1 секунду перед следующей проверкой
# Вызываем функцию для отправки битрейта каждого пакета
#send_bitrate(rtsp_url)
rtsp_info = ffmpeg.probe(rtsp_url, show_entries='format', select_streams='v:0')

# Выводим всю информацию
#print(rtsp_info)

rtsp_info = ffmpeg.probe(rtsp_url, select_streams='v:0', show_entries='stream=bit_rate')
print(rtsp_info)
# Получить общий битрейт формата мультимедийного файла
rtsp_info = ffmpeg.probe(rtsp_url, show_entries='format=bit_rate')