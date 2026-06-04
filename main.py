"""
Thai AI PDF Server v3 — Railway 배포용
POST /generate-pdf  →  PDF 반환
GET  /health        →  서버 상태 확인
"""
from flask import Flask, request, jsonify, send_file, Response
import anthropic, os, json, tempfile, sys, traceback
sys.path.insert(0, os.path.dirname(__file__))
from thai_ai_engine import generate

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

PROMPTS = {
"phone": """คุณคือนักวิเคราะห์เลขศาสตร์ไทยผู้เชี่ยวชาญ ผสานวัฒนธรรมไทย พุทธศาสนา จิตวิทยา
ชื่อ:{name} | วันเกิด:{birthdate} | เบอร์:{phone} | สนใจ:{focus}
วิเคราะห์เป็นภาษาไทย 5 หัวข้อ (ขึ้นต้นด้วย emoji):
🔢 ความหมายตัวเลข (3-4 บรรทัด อ้างอิงวัฒนธรรมไทย)
🏛 วัดมงคล (ระบุชื่อวัดจริง+เหตุผล)
💰 พลังการเงิน (สถิติ+กรณีศึกษา)
🧠 บุคลิกภาพ (วิเคราะห์จากตัวเลข)
⭐ สรุปคำแนะนำ (ปฏิบัติได้จริง)
จบด้วย ###JSON### บรรทัดเดียว:
{"lucky_numbers":"X,Y","temple":"วัดXXX","lucky_color":"สีX","weekday":N,"guardian":"ช้าง","royal":75,"radar":[5,3,5,4,3,4,5,4],"monthly":[3,4,5,4,3,5,5,4,3,4,5,4]}""",

"dream": """คุณคือผู้เชี่ยวชาญทำนายฝันตามหลักไทยโบราณ+Jung
ชื่อ:{name} | วันเกิด:{birthdate} | ฝัน:{phone} | รู้สึก:{focus}
วิเคราะห์ภาษาไทย: 🌙ภาพรวม 🐍สัญลักษณ์ 🧠จิตวิทยา 🏛วัดมงคล ⭐คำแนะนำ
จบด้วย ###JSON###:
{"lucky_numbers":"X","temple":"วัด","lucky_color":"สี","weekday":N,"guardian":"นาค","royal":65,"radar":[4,4,3,5,3,4,4,5],"monthly":[4,3,5,4,5,3,4,5,3,4,5,4]}""",

"plate": """คุณคือผู้เชี่ยวชาญเลขทะเบียนรถไทย
ชื่อ:{name} | วันเกิด:{birthdate} | ทะเบียน:{phone}
วิเคราะห์ภาษาไทย: 🔢ความหมาย 🎂เลขวันเกิด 🚗การเดินทาง 🏛วัด ✅สรุป
จบด้วย ###JSON###:
{"lucky_numbers":"X","temple":"วัด","lucky_color":"สี","weekday":N,"guardian":"เสือ","royal":70,"radar":[5,4,4,3,5,4,4,3],"monthly":[4,3,4,5,3,5,4,3,5,4,4,5]}"""
}

def call_claude(service, name, birthdate, phone, focus):
    if not ANTHROPIC_API_KEY:
        # API 키 없을 때 샘플 데이터 반환
        return ("🔢 ความหมายตัวเลข\nตัวอย่างการวิเคราะห์\n\n⭐ สรุป\nตัวอย่างผล",
                {"lucky_numbers":"8,9","temple":"วัดโพธิ์","lucky_color":"สีเหลือง",
                 "weekday":1,"guardian":"ช้าง","royal":75,
                 "radar":[5,3,5,4,3,4,5,4],"monthly":[3,4,5,4,3,5,5,4,3,4,5,4]})
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    prompt = PROMPTS.get(service, PROMPTS["phone"]).format(
        name=name, birthdate=birthdate, phone=phone, focus=focus)
    resp = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=2000,
        messages=[{"role":"user","content":prompt}])
    full = resp.content[0].text
    meta = {"lucky_numbers":"8,9","temple":"วัดโพธิ์","lucky_color":"สีเหลือง",
            "weekday":1,"guardian":"ช้าง","royal":75,
            "radar":[5,3,5,4,3,4,5,4],"monthly":[3,4,5,4,3,5,5,4,3,4,5,4]}
    text = full
    if "###JSON###" in full:
        parts = full.split("###JSON###")
        text = parts[0].strip()
        try:
            raw = parts[1].strip().split('\n')[0]
            meta = json.loads(raw)
        except: pass
    return text, meta

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    try:
        d = request.json or {}
        name      = d.get("name","")
        birthdate = d.get("birthdate","")
        phone     = d.get("phone","")
        focus     = d.get("focus","การเงิน")
        service   = d.get("service_type","phone")
        report_date = d.get("report_date","")

        from datetime import datetime
        if not report_date:
            report_date = datetime.now().strftime("%d/%m/%Y")

        analysis_text, meta = call_claude(service, name, birthdate, phone, focus)

        data = {
            "name": name, "phone": phone, "birthdate": birthdate,
            "birthdate_weekday": int(meta.get("weekday",1)),
            "report_date": report_date,
            "lucky_color": meta.get("lucky_color","สีเหลือง"),
            "lucky_numbers": meta.get("lucky_numbers","8,9"),
            "temple": meta.get("temple","วัดโพธิ์"),
            "guardian_animal": meta.get("guardian","ช้าง"),
            "royal_similarity": int(meta.get("royal",75)),
            "radar_scores": meta.get("radar",[5,3,5,4,3,4,5,4]),
            "monthly_scores": meta.get("monthly",[3,4,5,4,3,5,5,4,3,4,5,4]),
            "analysis_text": analysis_text,
        }

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            out_path = f.name
        generate(data, out_path, service_type=service)

        filename = f"thai_ai_{service}_{name.replace(' ','_')}.pdf"
        return send_file(out_path, mimetype="application/pdf",
                         as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route("/health")
def health():
    return jsonify({"status":"ok","version":"3.0","service":"Thai AI PDF Server"})

@app.route("/")
def index():
    return """<html><body style="background:#060914;color:#D4A017;font-family:sans-serif;text-align:center;padding:60px">
<h1>🏛 Thai AI Spiritual Platform</h1>
<p style="color:#888">PDF Generation Server v3.0</p>
<p><a href="/health" style="color:#D4A017">Health Check</a></p>
</body></html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)), debug=False)
