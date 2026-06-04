"""Railway 빌드 시 폰트 자동 다운로드"""
import urllib.request, os, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
os.makedirs("fonts", exist_ok=True)

fonts = {
    "fonts/Sarabun-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Regular.ttf",
    "fonts/Sarabun-Bold.ttf":    "https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Bold.ttf",
    "fonts/Sarabun-Light.ttf":   "https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Light.ttf",
}
for path, url in fonts.items():
    if not os.path.exists(path):
        print(f"Downloading {path}...")
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            with open(path,"wb") as f: f.write(r.read())
        print(f"  ✅ {path}")
    else:
        print(f"  ✓ {path} exists")
