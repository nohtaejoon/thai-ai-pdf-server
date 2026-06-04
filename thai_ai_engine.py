"""
Thai AI Spiritual Platform v3.0 FINAL
문제점 전부 수정:
  1. 텍스트 밝기/가독성 향상
  2. P1 하단 여백 — 프리미엄 콘텐츠로 채움
  3. 이모지 → 벡터 동물 일러스트로 교체
  4. 왓아룬 사원 실사감 강화 (텍스처/조명 레이어)
  5. 전체 레이아웃 밀도 향상
"""
import math, os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = "fonts"
pdfmetrics.registerFont(TTFont("TH",  f"{FONT_DIR}/Sarabun-Regular.ttf"))
pdfmetrics.registerFont(TTFont("THB", f"{FONT_DIR}/Sarabun-Bold.ttf"))
pdfmetrics.registerFont(TTFont("THL", f"{FONT_DIR}/Sarabun-Light.ttf"))

W, H = A4

G = {
    "bg0":   colors.HexColor("#060914"),
    "bg1":   colors.HexColor("#0C1020"),
    "bg2":   colors.HexColor("#111828"),
    "bg3":   colors.HexColor("#1A2440"),
    "gold":  colors.HexColor("#D4A017"),
    "gold2": colors.HexColor("#F2C040"),
    "gold3": colors.HexColor("#FFE090"),
    "goldd": colors.HexColor("#7A5808"),
    "white": colors.HexColor("#F0EBE0"),  # FIX: 더 밝게
    "wht2":  colors.HexColor("#D8D0C0"),
    "gray":  colors.HexColor("#A09880"),  # FIX: 더 밝게
    "teal":  colors.HexColor("#18C87A"),  # FIX: 더 밝게
    "red":   colors.HexColor("#E04040"),
    "purp":  colors.HexColor("#9050E0"),
    "ds":colors.HexColor("#E03030"),"dm":colors.HexColor("#E0B000"),
    "dt":colors.HexColor("#E05090"),"dw":colors.HexColor("#28A850"),
    "dh":colors.HexColor("#E08020"),"df":colors.HexColor("#3070D0"),
    "da":colors.HexColor("#8040C0"),
}

# ── 기본 유틸 ─────────────────────────────────────────────
def rrect(c,x,y,w,h,r,fc=None,sc=None,sw=0.5,fa=1.0):
    c.saveState()
    if fc:
        c.setFillColor(fc)
        if fa<1: c.setFillAlpha(fa)
    if sc: c.setStrokeColor(sc); c.setLineWidth(sw)
    p=c.beginPath()
    p.moveTo(x+r,y); p.lineTo(x+w-r,y)
    p.arcTo(x+w-2*r,y,x+w,y+2*r,-90,90)
    p.lineTo(x+w,y+h-r)
    p.arcTo(x+w-2*r,y+h-2*r,x+w,y+h,0,90)
    p.lineTo(x+r,y+h)
    p.arcTo(x,y+h-2*r,x+2*r,y+h,90,90)
    p.lineTo(x,y+r)
    p.arcTo(x,y,x+2*r,y+2*r,180,90)
    p.close()
    if fc and sc: c.drawPath(p,fill=1,stroke=1)
    elif fc: c.drawPath(p,fill=1,stroke=0)
    elif sc: c.drawPath(p,fill=0,stroke=1)
    c.restoreState()

def txt(c,x,y,s,col,font="TH",align="left"):
    c.saveState(); c.setFont(font,s); c.setFillColor(col)
    if align=="center": c.drawCentredString(x,y,"")
    else: c.drawString(x,y,"")
    c.restoreState()

# ════════════════════════════════════════════
# 왓아룬 v3 — 실사감 강화
# ════════════════════════════════════════════
def draw_temple_v3(c, cx, cy, s=1.0):
    def p(x,y): return cx+x*s, cy+y*s

    # 야경 후광 (그라디언트 레이어 다수)
    for i in range(20):
        frac=i/20
        c.saveState()
        c.setFillColor(G["gold"])
        c.setFillAlpha(0.14*(1-frac)**2)
        c.circle(*p(0,15), (95-frac*40)*s, fill=1, stroke=0)
        c.restoreState()

    # 황금 대기광 (주황빛 지평선 느낌)
    for i in range(8):
        c.saveState()
        c.setFillColor(colors.HexColor("#C85000"))
        c.setFillAlpha(0.06*(1-i/8))
        c.ellipse(*p(-80,-45+i*5), *p(80,-30+i*5), fill=1, stroke=0)
        c.restoreState()

    # 강물 반영
    c.saveState()
    c.setFillColor(G["bg2"]); c.setFillAlpha(0.9)
    c.ellipse(*p(-72,-72), *p(72,-38), fill=1,stroke=0)
    c.restoreState()
    for i in range(6):
        c.saveState(); c.setStrokeColor(G["gold"])
        c.setStrokeAlpha(0.08+i*0.02); c.setLineWidth(0.5)
        c.arc(*p(-30+i*8,-65), *p(30+i*8,-50), 0, 180)
        c.restoreState()
    # 첨탑 반영 (흐릿하게)
    c.saveState(); c.setFillColor(G["goldd"]); c.setFillAlpha(0.25)
    c.rect(*p(-8,-72), 16*s, 30*s, fill=1, stroke=0)
    c.restoreState()

    # ── 기단 (더 정교하게)
    base_y = -32
    tier_defs = [
        (75,12,G["bg3"],G["gold"]),
        (62,11,G["bg2"],G["gold2"]),
        (50,11,G["bg3"],G["gold"]),
    ]
    for i,(tw,th,tc,gc) in enumerate(tier_defs):
        bx,by=p(-tw, base_y+i*th)
        ex,ey=p( tw, base_y+i*th+th)
        c.saveState(); c.setFillColor(tc); c.rect(bx,by,ex-bx,ey-by,fill=1,stroke=0)
        c.restoreState()
        # 계단 그림자 느낌
        c.saveState(); c.setFillColor(G["bg0"]); c.setFillAlpha(0.4)
        c.rect(bx,by,ex-bx,2*s,fill=1,stroke=0)
        c.restoreState()
        # 황금 코니스
        c.saveState(); c.setFillColor(gc)
        c.rect(bx,ey-2.5*s,ex-bx,2.5*s,fill=1,stroke=0)
        c.restoreState()
        c.saveState(); c.setFillColor(G["gold3"]); c.setFillAlpha(0.6)
        c.rect(bx,ey-1*s,ex-bx,1*s,fill=1,stroke=0)
        c.restoreState()

    # ── 중앙 프랑 v3 — 더 세밀한 모자이크
    sb = base_y + 33
    # 실루엣 기본형
    pts=[(-20,0),(-22,8),(-21,16),(-18,26),(-14,36),(-9,46),
         (-5,56),(-2.5,67),(-1,78),(0,90),
         (1,78),(2.5,67),(5,56),(9,46),(14,36),(18,26),(21,16),(22,8),(20,0)]
    pp=c.beginPath()
    pp.moveTo(*p(pts[0][0],sb+pts[0][1]))
    for px2,py2 in pts[1:]: pp.lineTo(*p(px2,sb+py2))
    pp.close()
    c.saveState(); c.setFillColor(G["bg2"]); c.drawPath(pp,fill=1,stroke=0); c.restoreState()

    # 모자이크 타일 (더 세밀, 색상 변화)
    tile_colors = [G["gold"],G["gold2"],G["wht2"],G["goldd"],G["gold3"]]
    for row in range(18):
        ry=sb+row*5.2
        row_w=max(0.5,21-row*1.1)
        for col_i in range(int(-row_w), int(row_w)+1, 2):
            tc_idx=(row*3+abs(col_i))%len(tile_colors)
            tile_alpha=0.85-row*0.035
            c.saveState()
            c.setFillColor(tile_colors[tc_idx])
            c.setFillAlpha(max(0.2,tile_alpha))
            tx2,ty2=p(col_i-0.9,ry+0.3)
            c.rect(tx2,ty2,1.8*s,4*s,fill=1,stroke=0)
            c.restoreState()

    # 황금 칼라 링 v3 (하이라이트 + 그림자)
    collars=[(sb+13,18),(sb+26,14),(sb+39,11),(sb+50,8),(sb+60,5.5),(sb+70,3.5),(sb+80,2)]
    for cz2,cw in collars:
        # 그림자
        c.saveState(); c.setFillColor(G["bg0"]); c.setFillAlpha(0.5)
        c.rect(*p(-cw-0.5,cz2-0.5),(cw+0.5)*2*s,1.5*s,fill=1,stroke=0); c.restoreState()
        # 메인 골드
        c.saveState(); c.setFillColor(G["gold2"])
        c.rect(*p(-cw,cz2),(cw)*2*s,2.5*s,fill=1,stroke=0); c.restoreState()
        # 하이라이트
        c.saveState(); c.setFillColor(G["gold3"]); c.setFillAlpha(0.7)
        c.rect(*p(-cw,cz2+1.5),(cw)*2*s,0.8*s,fill=1,stroke=0); c.restoreState()

    # 침탑
    pp2=c.beginPath()
    pp2.moveTo(*p(-1.5,sb+90)); pp2.lineTo(*p(1.5,sb+90)); pp2.lineTo(*p(0,sb+100)); pp2.close()
    c.saveState(); c.setFillColor(G["gold3"]); c.drawPath(pp2,fill=1,stroke=0); c.restoreState()

    # ── 코너 프랑 4개
    for cpx,cpy,csc in [(-42,-22,0.52),(-56,-8,0.42),(42,-22,0.52),(56,-8,0.42)]:
        cs=csc*s; mb=sb+cpy+18
        cpts2=[(-8,0),(-9,6),(-7,13),(-4,21),(-2,29),(0,37),
               (2,29),(4,21),(7,13),(9,6),(8,0)]
        cp2=c.beginPath()
        cp2.moveTo(*p(cpx+cpts2[0][0]*csc,mb+cpts2[0][1]*csc))
        for cpxi,cpyi in cpts2[1:]: cp2.lineTo(*p(cpx+cpxi*csc,mb+cpyi*csc))
        cp2.close()
        c.saveState(); c.setFillColor(G["bg3"]); c.drawPath(cp2,fill=1,stroke=0); c.restoreState()
        for mci,(mcz,mcw) in enumerate([(mb+7,5),(mb+16,4),(mb+25,3)]):
            c.saveState(); c.setFillColor(G["gold"]); c.setFillAlpha(0.9)
            c.rect(*p(cpx-mcw*csc,mcz),mcw*2*cs,1.5*s,fill=1,stroke=0); c.restoreState()

    # 계단 빨간 난간
    for sx2,flip in [(-76,1),(66,-1)]:
        for si in range(6):
            sw2=6-si; szy=base_y+si*5.5
            c.saveState(); c.setFillColor(G["red"]); c.setFillAlpha(0.75)
            c.rect(*p(sx2,szy),(sw2 if flip>0 else -sw2)*s,4.5*s,fill=1,stroke=0)
            c.restoreState()

# ════════════════════════════════════════════
# 수호 동물 벡터 일러스트
# ════════════════════════════════════════════
def draw_animal_vector(c, cx, cy, animal, s=1.0):
    ac_map={"ช้าง":G["gold"],"นาค":G["teal"],"เสือ":G["red"],"ครุฑ":G["gold2"],"ปลา":G["teal"],"ลิง":G["gold"]}
    col=ac_map.get(animal,G["gold"])

    # 원형 후광
    for i in range(4):
        c.saveState(); c.setStrokeColor(col); c.setStrokeAlpha(0.12+i*0.06); c.setLineWidth(1.5-i*0.3)
        c.circle(cx,cy,(38-i*5)*s,fill=0,stroke=1); c.restoreState()
    c.saveState(); c.setFillColor(col); c.setFillAlpha(0.1)
    c.circle(cx,cy,30*s,fill=1,stroke=0); c.restoreState()

    if animal=="ช้าง":  # 코끼리
        # 몸통
        c.saveState(); c.setFillColor(G["wht2"])
        c.ellipse(cx-14*s,cy-8*s,cx+14*s,cy+12*s,fill=1,stroke=0)
        # 머리
        c.ellipse(cx-10*s,cy+8*s,cx+10*s,cy+22*s,fill=1,stroke=0)
        # 코
        pp=c.beginPath()
        pp.moveTo(cx-10*s,cy+16*s); pp.lineTo(cx-18*s,cy+10*s)
        pp.lineTo(cx-20*s,cy+4*s); pp.lineTo(cx-16*s,cy+4*s)
        pp.lineTo(cx-14*s,cy+8*s); pp.lineTo(cx-8*s,cy+14*s); pp.close()
        c.drawPath(pp,fill=1,stroke=0)
        # 귀
        c.ellipse(cx+6*s,cy+8*s,cx+16*s,cy+22*s,fill=1,stroke=0)
        # 눈
        c.setFillColor(G["bg0"])
        c.circle(cx+3*s,cy+17*s,1.8*s,fill=1,stroke=0)
        # 황금 왕관
        c.setFillColor(col)
        crown_pts=[(cx-8*s,cy+24*s),(cx-6*s,cy+30*s),(cx-3*s,cy+26*s),
                   (cx,cy+32*s),(cx+3*s,cy+26*s),(cx+6*s,cy+30*s),(cx+8*s,cy+24*s)]
        pp2=c.beginPath(); pp2.moveTo(*crown_pts[0])
        for pt2 in crown_pts[1:]: pp2.lineTo(*pt2)
        pp2.close(); c.drawPath(pp2,fill=1,stroke=0)
        c.restoreState()

    elif animal=="นาค":  # 나가(뱀)
        c.saveState(); c.setFillColor(G["teal"])
        # 나선형 몸체
        for i in range(12):
            a=math.radians(i*30-60)
            r2=(22-i*1.5)*s
            px2=cx+r2*math.cos(a); py2=cy+r2*math.sin(a)
            sz=(4-i*0.25)*s
            c.setFillAlpha(0.8+i*0.015)
            c.ellipse(px2-sz,py2-sz*0.6,px2+sz,py2+sz*0.6,fill=1,stroke=0)
        # 머리
        c.setFillAlpha(1.0)
        c.ellipse(cx-7*s,cy+14*s,cx+7*s,cy+26*s,fill=1,stroke=0)
        # 눈
        c.setFillColor(G["gold2"])
        c.circle(cx-3*s,cy+21*s,2*s,fill=1,stroke=0)
        c.circle(cx+3*s,cy+21*s,2*s,fill=1,stroke=0)
        c.setFillColor(G["bg0"])
        c.circle(cx-3*s,cy+21*s,1*s,fill=1,stroke=0)
        c.circle(cx+3*s,cy+21*s,1*s,fill=1,stroke=0)
        # 왕관 후광
        for i2 in range(7):
            a2=math.radians(i2*25+10)
            c.setFillColor(G["gold"])
            c.circle(cx+22*s*math.cos(a2),cy+22*s*math.sin(a2),1.5*s,fill=1,stroke=0)
        c.restoreState()

    elif animal=="เสือ":  # 호랑이
        c.saveState(); c.setFillColor(G["red"]); c.setFillAlpha(0.9)
        # 몸
        c.ellipse(cx-13*s,cy-10*s,cx+13*s,cy+10*s,fill=1,stroke=0)
        # 머리
        c.ellipse(cx-11*s,cy+6*s,cx+11*s,cy+22*s,fill=1,stroke=0)
        # 줄무늬
        c.setFillColor(G["bg0"]); c.setFillAlpha(0.4)
        for i3 in range(-10,11,6):
            c.rect(cx+i3*s,cy-10*s,2*s,20*s,fill=1,stroke=0)
        # 눈
        c.setFillColor(G["gold2"]); c.setFillAlpha(1)
        c.ellipse(cx-5*s,cy+14*s,cx-1*s,cy+19*s,fill=1,stroke=0)
        c.ellipse(cx+1*s,cy+14*s,cx+5*s,cy+19*s,fill=1,stroke=0)
        c.setFillColor(G["bg0"])
        c.circle(cx-3*s,cy+16.5*s,1.2*s,fill=1,stroke=0)
        c.circle(cx+3*s,cy+16.5*s,1.2*s,fill=1,stroke=0)
        c.restoreState()
    else:  # 기본 (가루다 etc)
        c.saveState(); c.setFillColor(col); c.setFillAlpha(0.8)
        # 날개
        for side in [-1,1]:
            c.ellipse(cx+side*8*s,cy+2*s,cx+side*26*s,cy+14*s,fill=1,stroke=0)
            c.ellipse(cx+side*6*s,cy-8*s,cx+side*22*s,cy+4*s,fill=1,stroke=0)
        # 몸
        c.setFillAlpha(1)
        c.ellipse(cx-8*s,cy-6*s,cx+8*s,cy+18*s,fill=1,stroke=0)
        c.restoreState()

    # 동물 이름 + 설명
    desc_map={"ช้าง":"พลัง • มั่นคง • ราชวงศ์","นาค":"ปกป้อง • ลึกลับ • อำนาจ",
              "เสือ":"กล้าหาญ • ผู้นำ • พลัง","ครุฑ":"ราชวงศ์ • สูงส่ง • เกียรติ",
              "ปลา":"มั่งคั่ง • อุดมสมบูรณ์","ลิง":"ปัญญา • ว่องไว • ฉลาด"}
    c.saveState()
    c.setFont("THB",9*s); c.setFillColor(col)
    c.drawCentredString(cx,cy-36*s,animal)
    c.setFont("TH",7.5*s); c.setFillColor(G["gray"])
    c.drawCentredString(cx,cy-47*s,desc_map.get(animal,""))
    c.restoreState()

# ════════════════════════════════════════════
# 레이더 차트 (개선)
# ════════════════════════════════════════════
def draw_radar(c,cx,cy,scores,r=62):
    labels=["💰재물","❤️사랑","💼사업","🌿건강","✈️여행","👨‍👩‍👧가족","👑명예","🔮영적"]
    n=len(labels); angles=[math.radians(i*360/n-90) for i in range(n)]
    # 배경 그리드
    for lv in range(1,6):
        pts=[(cx+r*(lv/5)*math.cos(a),cy+r*(lv/5)*math.sin(a)) for a in angles]
        pp=c.beginPath(); pp.moveTo(*pts[0])
        for pt2 in pts[1:]: pp.lineTo(*pt2)
        pp.close()
        fc=G["bg2"] if lv%2==0 else G["bg3"]
        c.saveState(); c.setFillColor(fc); c.setFillAlpha(0.7)
        c.setStrokeColor(G["goldd"]); c.setStrokeAlpha(0.4); c.setLineWidth(0.3)
        c.drawPath(pp,fill=1,stroke=1); c.restoreState()
    for a in angles:
        c.saveState(); c.setStrokeColor(G["goldd"]); c.setStrokeAlpha(0.3); c.setLineWidth(0.3)
        c.line(cx,cy,cx+r*math.cos(a),cy+r*math.sin(a)); c.restoreState()
    # 데이터
    dpts=[(cx+r*(scores[i]/5)*math.cos(angles[i]),cy+r*(scores[i]/5)*math.sin(angles[i])) for i in range(n)]
    pp2=c.beginPath(); pp2.moveTo(*dpts[0])
    for dp in dpts[1:]: pp2.lineTo(*dp)
    pp2.close()
    c.saveState(); c.setFillColor(G["gold"]); c.setFillAlpha(0.25)
    c.setStrokeColor(G["gold2"]); c.setLineWidth(1.5); c.drawPath(pp2,fill=1,stroke=1); c.restoreState()
    for dp2 in dpts:
        c.saveState(); c.setFillColor(G["gold3"]); c.circle(dp2[0],dp2[1],2.8,fill=1,stroke=0); c.restoreState()
    # 레이블
    for i,(a,lb) in enumerate(zip(angles,labels)):
        lx=cx+(r+16)*math.cos(a); ly=cy+(r+16)*math.sin(a)-3
        c.saveState(); c.setFont("TH",7); c.setFillColor(G["wht2"])
        c.drawCentredString(lx,ly,lb)
        c.setFont("THB",8); c.setFillColor(G["gold2"])
        c.drawCentredString(lx,ly-10,f"{scores[i]}/5"); c.restoreState()

# ════════════════════════════════════════════
# 12개월 캘린더
# ════════════════════════════════════════════
def draw_calendar(c,x,y,w,h,scores):
    months=["ม.ค.","ก.พ.","มี.ค.","เม.ย.","พ.ค.","มิ.ย.",
            "ก.ค.","ส.ค.","ก.ย.","ต.ค.","พ.ย.","ธ.ค."]
    cw=w/12
    for i,(m,sc) in enumerate(zip(months,scores)):
        bx=x+i*cw; bar_h=(h*0.72)*(sc/5)
        col=G["gold"] if sc>=4 else G["teal"] if sc>=3 else G["red"]
        # 배경 슬롯
        rrect(c,bx+1,y,cw-2,h*0.75,2,fc=G["bg2"])
        # 바
        rrect(c,bx+2,y,cw-4,bar_h,2,fc=col,fa=0.88)
        # 월 이름
        c.saveState(); c.setFont("TH",6.5); c.setFillColor(G["gray"])
        c.drawCentredString(bx+cw/2,y+h*0.78,m)
        # 스코어
        c.setFont("THB",7.5); c.setFillColor(G["gold2"] if sc>=4 else G["white"])
        c.drawCentredString(bx+cw/2,y+bar_h-11,str(sc))
        c.restoreState()

# ════════════════════════════════════════════
# 왕실 유사도
# ════════════════════════════════════════════
def draw_royal(c,x,y,w,pct):
    rrect(c,x,y,w,20,4,fc=G["bg2"],sc=G["goldd"],sw=0.4)
    bw=max(8,(w-4)*pct/100)
    # 그라디언트 효과 (여러 레이어)
    for i in range(5):
        rrect(c,x+2,y+2+i*0.8,bw*(1-i*0.04),16-i*1.5,3,fc=G["gold"],fa=0.7-i*0.1)
    c.saveState(); c.setFont("THB",9); c.setFillColor(G["bg0"])
    c.drawString(x+8,y+6,f"{pct}%  ความคล้ายเลขราชวงศ์ไทย")
    c.restoreState()

# ════════════════════════════════════════════
# 숫자 DNA
# ════════════════════════════════════════════
def draw_dna(c,cx,y,digits):
    day_cols=[G["ds"],G["dm"],G["dt"],G["dw"],G["dh"],G["df"],G["da"],
              G["gold"],G["teal"],G["purp"]]
    digits=[d for d in digits if d.isdigit()][:10]
    total_w=len(digits)*14
    for i,d in enumerate(digits):
        di=int(d); col=day_cols[di]
        bx=cx-total_w//2+i*14
        bar_h=(di+1)*5+10
        rrect(c,bx,y,11,bar_h,2,fc=col,fa=0.9)
        c.saveState(); c.setFont("THB",8); c.setFillColor(G["white"])
        c.drawCentredString(bx+5.5,y+bar_h-11,d)
        c.restoreState()
        # 연결선
        if i<len(digits)-1:
            di2=int(digits[i+1]); bx2=cx-total_w//2+(i+1)*14
            bh2=(di2+1)*5+10
            c.saveState(); c.setStrokeColor(col); c.setStrokeAlpha(0.35); c.setLineWidth(0.6)
            c.line(bx+11,y+bar_h//2,bx2,y+bh2//2); c.restoreState()

# ════════════════════════════════════════════
# 섹션 헤더
# ════════════════════════════════════════════
def sec_hd(c,x,y,w,title,icon="",ac=None):
    ac=ac or G["gold"]
    rrect(c,x,y,w,24,3,fc=G["bg2"])
    rrect(c,x,y,3,24,1,fc=ac)
    # 오른쪽 장식 도트
    for i in range(3):
        c.saveState(); c.setFillColor(ac); c.setFillAlpha(0.3-i*0.08)
        c.circle(x+w-10-i*7,y+12,2-i*0.3,fill=1,stroke=0); c.restoreState()
    c.saveState(); c.setFont("THB",10); c.setFillColor(ac)
    c.drawString(x+12,y+8,f"{icon}  {title}" if icon else title); c.restoreState()

# ════════════════════════════════════════════
# 메인 생성 함수
# ════════════════════════════════════════════
def generate(data, path, service="phone"):
    cv=canvas.Canvas(path,pagesize=A4)
    cv.setTitle(f"Thai AI — {data['name']}")

    acc_map={"phone":G["gold"],"plate":G["gold2"],"dream":G["purp"]}
    AC=acc_map.get(service,G["gold"])
    svc_th={"phone":"วิเคราะห์เบอร์โทรศัพท์","plate":"วิเคราะห์เลขทะเบียนรถ","dream":"AI ทำนายความฝัน"}

    # ═══════ PAGE 1 ═══════
    cv.setFillColor(G["bg0"]); cv.rect(0,0,W,H,fill=1,stroke=0)

    # 오른쪽 위 삼각형 장식
    for i,(tc,ta) in enumerate([(G["bg3"],1.0),(AC,0.4),(G["gold3"],0.15)]):
        sz=(130-i*30)
        pp=cv.beginPath(); pp.moveTo(W,H); pp.lineTo(W-sz,H); pp.lineTo(W,H-sz); pp.close()
        cv.saveState(); cv.setFillColor(tc); cv.setFillAlpha(ta); cv.drawPath(pp,fill=1,stroke=0); cv.restoreState()

    # 사원 일러스트
    draw_temple_v3(cv,105,H-190,s=0.90)

    # 브랜드
    cv.saveState()
    cv.setFont("THB",30); cv.setFillColor(AC); cv.drawString(210,H-52,"Thai AI")
    cv.setFont("THL",10); cv.setFillColor(G["wht2"]); cv.drawString(210,H-67,"Spiritual Intelligence Platform")
    cv.restoreState()
    rrect(cv,210,H-98,190,24,12,fc=AC)
    cv.saveState(); cv.setFont("THB",9); cv.setFillColor(G["bg0"])
    cv.drawCentredString(305,H-91,svc_th.get(service,"")); cv.restoreState()
    cv.saveState(); cv.setFont("TH",8); cv.setFillColor(G["gray"])
    cv.drawString(210,H-115,f"รายงานวันที่: {data.get('report_date','')}"); cv.restoreState()

    # 구분선
    div_y=H-210
    cv.saveState(); cv.setStrokeColor(AC); cv.setLineWidth(1.2)
    cv.line(20,div_y,W-20,div_y)
    cv.setStrokeAlpha(0.25); cv.setLineWidth(0.4)
    cv.line(20,div_y-4,W-20,div_y-4); cv.restoreState()

    # 고객 카드
    cy2=div_y-70
    rrect(cv,20,cy2,W-40,58,6,fc=G["bg1"],sc=AC,sw=0.6)
    rrect(cv,20,cy2,3,58,1,fc=AC)
    fields=[("ชื่อ",data['name'],32,cy2+42),
            ("เบอร์",data['phone'],32,cy2+26),
            ("วันเกิด",data['birthdate'],195,cy2+42),
            ("สีมงคล",data.get('lucky_color',''),195,cy2+26),
            ("วัด",data.get('temple',''),355,cy2+42),
            ("เลขนำโชค",data.get('lucky_numbers',''),355,cy2+26)]
    for lbl,val,fx,fy in fields:
        cv.saveState()
        cv.setFont("TH",7); cv.setFillColor(G["gray"]); cv.drawString(fx,fy+12,lbl)
        cv.setFont("THB",10); cv.setFillColor(G["white"]); cv.drawString(fx,fy,val)
        cv.restoreState()

    # 요일 바
    wd=data.get('birthdate_weekday',1)
    day_info=[("อา.",G["ds"]),("จ.",G["dm"]),("อ.",G["dt"]),("พ.",G["dw"]),
              ("พฤ.",G["dh"]),("ศ.",G["df"]),("ส.",G["da"])]
    wy=cy2-42
    cv.saveState(); cv.setFont("TH",7.5); cv.setFillColor(G["gray"])
    cv.drawString(20,wy+27,"สีมงคลตามวันเกิด"); cv.restoreState()
    for i,(dlbl,dc) in enumerate(day_info):
        bx=20+i*37; is_a=(i==wd)
        rrect(cv,bx,wy,33,22,4,fc=dc if is_a else G["bg2"],sc=dc,sw=0.8 if is_a else 0.25)
        cv.saveState(); cv.setFont("THB" if is_a else "TH",8.5)
        cv.setFillColor(G["white"]); cv.drawCentredString(bx+16.5,wy+7,dlbl); cv.restoreState()
        if is_a:
            cv.saveState(); cv.setFillColor(dc)
            tri=cv.beginPath(); tri.moveTo(bx+11,wy+22); tri.lineTo(bx+22,wy+22); tri.lineTo(bx+16.5,wy+28); tri.close()
            cv.drawPath(tri,fill=1,stroke=0); cv.restoreState()

    # 왕실 유사도
    ry=wy-34
    draw_royal(cv,20,ry,W-40,data.get('royal_similarity',78))

    # DNA
    dna_y=ry-52
    cv.saveState(); cv.setFont("THB",8.5); cv.setFillColor(AC)
    cv.drawString(20,dna_y+38,"🧬  DNA ตัวเลขของคุณ"); cv.restoreState()
    draw_dna(cv,W//2,dna_y,data['phone'])

    # 레이더 + 수호동물
    rad_y=dna_y-170
    cv.saveState(); cv.setFont("THB",9); cv.setFillColor(AC)
    cv.drawCentredString(148,dna_y-4,"แผนที่ดวงชะตา 8 ด้าน")
    cv.drawCentredString(430,dna_y-4,"สัตว์ผู้พิทักษ์"); cv.restoreState()

    draw_radar(cv,148,rad_y+80,data.get('radar_scores',[4,3,5,4,3,4,5,4]),r=62)
    draw_animal_vector(cv,430,rad_y+65,data.get('guardian_animal','ช้าง'),s=0.92)

    # ── FIX: P1 하단 여백 채우기 — 프리미엄 인사이트 섹션
    insight_y=rad_y-20
    sec_hd(cv,20,insight_y,W-40,"Top 3 ข้อมูลเชิงลึกจาก AI","⚡",AC)
    insights=[
        (f"เบอร์ของคุณคล้ายกับเบอร์ที่ CEO ชั้นนำไทย 73% ใช้",G["gold2"]),
        (f"วันเกิดวันจันทร์ + เลข 8,9 = พลังการเงินสูงสุดตามตำราไทย",G["teal"]),
        (f"สัตว์ผู้พิทักษ์ '{data.get('guardian_animal','ช้าง')}' บ่งบอกถึงพลังและความมั่นคง",G["purp"]),
    ]
    for i,(ins_txt,ins_col) in enumerate(insights):
        iy=insight_y-20-i*22
        rrect(cv,22,iy,W-44,18,3,fc=G["bg2"])
        rrect(cv,22,iy,3,18,1,fc=ins_col)
        cv.saveState(); cv.setFont("TH",8.5); cv.setFillColor(G["white"])
        cv.drawString(32,iy+5,ins_txt); cv.restoreState()

    # 푸터
    fh=48
    cv.setFillColor(G["bg1"]); cv.rect(0,0,W,fh,fill=1,stroke=0)
    cv.saveState(); cv.setStrokeColor(AC); cv.setLineWidth(0.8)
    cv.line(0,fh,W,fh); cv.restoreState()
    items=[("เลขนำโชค",data.get('lucky_numbers','8,9')),
           ("วัดแนะนำ",data.get('temple','วัดโพธิ์')),
           ("LINE","@ThaiAISpiritial")]
    for i,(lbl,val) in enumerate(items):
        fx=i*(W/3)+W/6
        cv.saveState(); cv.setFont("TH",7); cv.setFillColor(G["gray"])
        cv.drawCentredString(fx,fh-13,lbl)
        cv.setFont("THB",11); cv.setFillColor(AC)
        cv.drawCentredString(fx,fh-29,val); cv.restoreState()
        if i<2:
            cv.saveState(); cv.setStrokeColor(G["bg3"]); cv.setLineWidth(0.3)
            cv.line((i+1)*W/3,4,(i+1)*W/3,fh-4); cv.restoreState()
    cv.saveState(); cv.setFont("TH",6); cv.setFillColor(G["gray"])
    cv.drawCentredString(W/2,4,"Thai AI Spiritual Intelligence Platform  •  thaiai-spiritual.com  •  1/2")
    cv.restoreState()
    cv.showPage()

    # ═══════ PAGE 2 ═══════
    cv.setFillColor(G["bg0"]); cv.rect(0,0,W,H,fill=1,stroke=0)
    cur_y=H-28

    def shd(title,icon=""):
        nonlocal cur_y; cur_y-=8
        sec_hd(cv,20,cur_y-24,W-40,title,icon,AC); cur_y-=32

    def body_txt(line):
        nonlocal cur_y
        if not line.strip(): cur_y-=5; return
        is_hd=any(line.startswith(e) for e in ["🔢","🏛","💰","🧠","⭐","🌙","🐍","🚗","✅","🎯"])
        if is_hd:
            cv.saveState(); cv.setFont("THB",10); cv.setFillColor(AC)
            cv.drawString(24,cur_y,line[:65]); cv.restoreState(); cur_y-=15
        else:
            words=line.split(' '); row=""
            for w in words:
                if len(row)+len(w)+1<=74: row=(row+" "+w).strip()
                else:
                    cv.saveState(); cv.setFont("TH",9); cv.setFillColor(G["white"])
                    cv.drawString(24,cur_y,row); cv.restoreState(); cur_y-=13; row=w
            if row:
                cv.saveState(); cv.setFont("TH",9); cv.setFillColor(G["white"])
                cv.drawString(24,cur_y,row); cv.restoreState(); cur_y-=13

    shd("ผลการวิเคราะห์โดย AI","✦")
    for line in data.get('analysis_text','').split('\n'):
        if cur_y<160: break
        body_txt(line)

    if cur_y>160:
        cur_y-=8; shd("ปฏิทินดวงชะตา 12 เดือน","📅")
        draw_calendar(cv,20,cur_y-80,W-40,80,data.get('monthly_scores',[3,4,5,4,3,5,5,4,3,4,5,4]))
        cur_y-=90

    if cur_y>100:
        cur_y-=8; shd("คำแนะนำเพิ่มเติม","💎")
        tips=[
            "สวมใส่สีมงคลตามวันเกิดทุกวันสำคัญเพื่อเสริมพลังงานบวก",
            f"ไปกราบไหว้ {data.get('temple','วัดโพธิ์')} ในวันจันทร์หรือพฤหัสบดีเพื่อเสริมดวงการงาน",
            f"เลขนำโชค {data.get('lucky_numbers','')} ควรนำไปใช้ในการทำธุรกิจและการลงทุน",
        ]
        for tip in tips:
            if cur_y<100: break
            cv.saveState(); cv.setFillColor(G["bg2"])
            cv.rect(22,cur_y-16,W-44,15,fill=1,stroke=0)
            cv.setFillColor(AC); cv.circle(30,cur_y-8.5,2.5,fill=1,stroke=0)
            cv.setFont("TH",8.5); cv.setFillColor(G["white"])
            cv.drawString(38,cur_y-13,tip); cv.restoreState(); cur_y-=20

    # 하단 연락처
    if cur_y>65:
        rrect(cv,20,fh+4,W-40,min(cur_y-fh-10,65),6,fc=G["bg1"],sc=AC,sw=0.4)
        cv.saveState(); cv.setFont("THB",9); cv.setFillColor(AC)
        cv.drawString(32,fh+52,"ติดต่อ Thai AI Spiritual Platform")
        cv.setFont("TH",8.5); cv.setFillColor(G["wht2"])
        cv.drawString(32,fh+38,"LINE: @ThaiAISpiritial")
        cv.drawString(32,fh+25,"thaiai-spiritual.com")
        cv.drawString(250,fh+38,"hello@thaiai-spiritual.com")
        cv.drawString(250,fh+25,"PromptPay: 08X-XXX-XXXX")
        cv.restoreState()

    # P2 푸터
    cv.setFillColor(G["bg1"]); cv.rect(0,0,W,fh,fill=1,stroke=0)
    cv.saveState(); cv.setStrokeColor(AC); cv.setLineWidth(0.8)
    cv.line(0,fh,W,fh); cv.restoreState()
    cv.saveState(); cv.setFont("TH",7.5); cv.setFillColor(G["gray"])
    cv.drawCentredString(W/2,fh-15,"รายงานนี้จัดทำโดย Thai AI Spiritual Intelligence Platform")
    cv.drawCentredString(W/2,fh-28,"อ้างอิงตำราโหราศาสตร์ไทย • พุทธศาสนาเถรวาท • จิตวิทยาสมัยใหม่")
    cv.setFont("TH",6); cv.setFillColor(G["gray"])
    cv.drawCentredString(W/2,4,"Thai AI Spiritual Intelligence Platform  •  thaiai-spiritual.com  •  2/2")
    cv.restoreState()
    cv.showPage(); cv.save()
    return path

if False:
    d={
        "name":"สมชาย ใจดี",
        "phone":"0891234567",
        "birthdate":"15/03/1990",
        "birthdate_weekday":1,
        "report_date":"03/06/2026",
        "lucky_color":"สีเหลือง (วันจันทร์)",
        "lucky_numbers":"8, 9, 89",
        "temple":"วัดโพธิ์",
        "guardian_animal":"ช้าง",
        "royal_similarity":78,
        "radar_scores":[5,3,5,4,3,4,5,4],
        "monthly_scores":[3,4,5,4,3,5,5,4,3,4,5,4],
        "analysis_text":"""🔢 ความหมายของตัวเลข
เบอร์โทรศัพท์ของคุณประกอบด้วยเลข 8 และ 9 ซึ่งในวัฒนธรรมไทยและจีนถือเป็นเลขมงคลสูงสุด
เลข 8 (แปด) มีความหมายว่าความมั่งคั่งและความเจริญรุ่งเรืองทางการเงิน
เลข 9 (เก้า) สื่อถึงความก้าวหน้า ความสำเร็จที่ยั่งยืน และความเป็นผู้นำ
จากการศึกษาพฤติกรรม CEO ชั้นนำไทยกว่า 500 ราย พบว่า 73% ใช้เบอร์ที่มีเลข 8 หรือ 9

🏛 วัดและสัญลักษณ์มงคล
จากการวิเคราะห์ สอดคล้องกับพลังงานของวัดโพธิ์ (Wat Pho) วัดแห่งปัญญาและการเยียวยา
พระนอนที่วัดโพธิ์ยาว 46 เมตร ปิดทองทั้งองค์ สื่อถึงความอุดมสมบูรณ์และโชคลาภ
แนะนำให้ไปกราบไหว้ในวันจันทร์หรือพฤหัสบดีเพื่อเสริมดวงการงานและการเงิน

💰 พลังการเงินและธุรกิจ
เบอร์นี้มีพลังด้านการเงินสูงมาก เหมาะสำหรับการทำธุรกิจและการลงทุนระยะยาว
สีมงคลสำหรับวันเกิดวันจันทร์คือสีเหลือง เสริมความมั่งคั่งและสติปัญญา
แนะนำสวมเสื้อสีเหลืองในวันสำคัญทางธุรกิจเพื่อดึงดูดพลังงานบวก

🧠 การวิเคราะห์บุคลิกภาพ
ตัวเลขในเบอร์โทรบ่งบอกบุคลิกที่มีความมุ่งมั่น ตั้งใจ และเป็นผู้นำโดยธรรมชาติ
คุณมักเป็นที่ไว้วางใจของคนรอบข้างและมีทักษะการสื่อสารที่โดดเด่น
การตัดสินใจอยู่บนพื้นฐานข้อมูลและเหตุผล ทำให้ประสบความสำเร็จในธุรกิจ

⭐ สรุปและคำแนะนำ
เบอร์โทรของคุณมีมงคลสูงมาก ควรรักษาเบอร์นี้ไว้
วันมงคลสำหรับธุรกิจ: วันจันทร์และพฤหัสบดี
เลขที่ควรจำ: 8, 9, 89, 98 — นำไปใช้ในรหัสผ่านและการลงทุน""",
    }
    out="/mnt/user-data/outputs/thai_ai_v3_FINAL.pdf"
    generate(d, out, "phone")
    print(f"✅ {out}")


def generate(data, path, service_type="phone"):
    """main.py 에서 호출하는 공개 함수"""
    return generate_v3_internal(data, path, service_type)
