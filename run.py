"""
Railway 서버 실행 파일 — Python이 직접 PORT 처리
"""
import os
import subprocess
import sys

port = os.environ.get("PORT") or os.environ.get("port") or "8080"

print(f"=== Thai AI Server Starting ===")
print(f"All env PORT vars: PORT={os.environ.get('PORT')}, port={os.environ.get('port')}")
print(f"Using port: {port}")

cmd = [
    sys.executable, "-m", "gunicorn",
    "main:app",
    f"--bind=0.0.0.0:{port}",
    "--workers=1",
    "--timeout=120",
    "--log-level=info"
]
print(f"Command: {' '.join(cmd)}")
os.execvp(sys.executable, cmd)
