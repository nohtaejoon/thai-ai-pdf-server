FROM python:3.11-slim

WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 파일 복사
COPY . .

# 폰트 다운로드
RUN python download_fonts.py

# 포트 노출
EXPOSE 8080

# 서버 실행
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120"]
