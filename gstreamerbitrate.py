import mediainfo

# Путь к видеофайлу
video_path = "путь_к_вашему_видеофайлу.mp4"

# Получение информации о видеофайле
media_info = mediainfo.MediaInfo.parse(video_path)

# Получение битрейта видео
bitrate = media_info.video.bit_rate if media_info.video.bit_rate else "Недоступно"

print("Битрейт видео:", bitrate, "бит/с")
