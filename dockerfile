# 使用官方Python镜像作为基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 安装ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 将Python脚本复制到容器中
COPY video_processor.py /app/

# 运行Python脚本
CMD ["python", "video_processor.py"]
