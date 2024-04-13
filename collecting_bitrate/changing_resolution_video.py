import ffmpeg

input_file = "/Users/user/Downloads/Test/anomaly/1.mp4"
output_file = "/Users/user/Downloads/Test/anomaly/1_960x540.mp4"
width = 960
height = 540

# Изменяем размер видео
ffmpeg.input(input_file).output(output_file, vf=f"scale={width}:{height}").run()