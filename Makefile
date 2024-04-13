# Определение переменных
RTSP_URL = rtsp://172.21.4.110/36cam
CSV_NAME = 36cam
OUTPUT_DIR = ../inputs_for_vae_processing_csv
#PYTHON_PATH = /Users/user/PycharmProjects/ByteRateAnalyse/.venv/bin/python

# Основная цель для вызова скрипта
process_video:
    python collecting_bitrate/ffmpeg_bitrate_makefile.py $(RTSP_URL) $(CSV_NAME) $(OUTPUT_DIR)

