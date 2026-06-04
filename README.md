# Thai AI Spiritual Platform — PDF Server v3.0

## Railway 배포 순서 (10분)

### 1단계: GitHub 업로드
1. github.com 접속 → "New repository" 클릭
2. 이름: `thai-ai-pdf-server` → "Create repository"
3. 이 폴더의 파일들을 전부 업로드 (Upload files 클릭)
4. "Commit changes" 클릭

### 2단계: Railway 연결
1. railway.app 접속 → "Start a New Project"
2. "Deploy from GitHub repo" 선택
3. `thai-ai-pdf-server` 선택
4. 자동 배포 시작 (약 3-5분)

### 3단계: 환경변수 설정
Railway 대시보드 → Variables 탭:
```
ANTHROPIC_API_KEY = sk-ant-api03-...여기에붙여넣기...
```

### 4단계: URL 확인
배포 완료 후 Railway가 URL 제공:
`https://thai-ai-pdf-server-xxxx.railway.app`

헬스체크: `GET /health` → {"status":"ok"}

### 5단계: Make.com 연결
Make.com HTTP 모듈:
- URL: `https://[your-url].railway.app/generate-pdf`
- Method: POST
- Body (JSON):
```json
{
  "name": "{{1.name}}",
  "phone": "{{1.phone}}",
  "birthdate": "{{1.birthdate}}",
  "focus": "{{1.focus}}",
  "service_type": "phone",
  "report_date": "{{formatDate(now; 'DD/MM/YYYY')}}"
}
```

## API 명세

### POST /generate-pdf
PDF 파일을 생성하여 반환합니다.

**Request Body:**
| 필드 | 타입 | 설명 |
|------|------|------|
| name | string | 고객 이름 (태국어) |
| phone | string | 전화번호/번호판/꿈 내용 |
| birthdate | string | 생년월일 DD/MM/YYYY |
| focus | string | 관심 분야 (การเงิน/ความรัก 등) |
| service_type | string | phone / plate / dream |
| report_date | string | 리포트 날짜 |

**Response:** `application/pdf` 파일

### GET /health
서버 상태 확인. `{"status":"ok","version":"3.0"}`
