# maro - YouTube 채널 자동화 시스템

> "하루 3분, 당신은 혼자가 아닙니다"

## 📋 프로젝트 개요

**maro**는 "마음위로"의 약자로, 지친 현대인에게 짧고 진심 어린 위로를 전하는 디지털 힐링 채널입니다. 이 시스템은 AI를 활용하여 매일 자동으로 위로 콘텐츠를 생성하고 YouTube에 업로드합니다.

## 🎯 채널 목표

- **공감**: 시청자의 일상적 어려움에 공감하는 콘텐츠
- **치유**: 정서적 안정과 회복을 제공하는 힐링 콘텐츠  
- **연결**: 서로 위로하는 따뜻한 온라인 공간 형성

## 🎬 콘텐츠 구성

### 정규 콘텐츠

| 콘텐츠 타입 | 업로드 빈도 | 길이 | 특징 |
|------------|------------|------|------|
| **오늘의 위로** | 매일 (월,수,일) | 2-3분 | 따뜻한 문구 + 잔잔한 음악 |
| **힐링 사운드** | 주 2회 (화,토) | 5-10분 | 자연 소리 + 편안한 멘트 |
| **극복 스토리** | 주 1회 (수) | 5-8분 | 실패 후 회복한 이야기 |
| **맞춤형 위로** | 주 1회 (금) | 3-5분 | 상황별 맞춤 위로 |

### 주간 업로드 구조

```
월요일: 오늘의 위로
화요일: 힐링 사운드+멘트  
수요일: 극복 스토리
목요일: 오늘의 위로
금요일: 맞춤형 시리즈
토요일: 힐링 사운드+멘트
일요일: 오늘의 위로
```

## 🚀 설치 및 설정

### 1. 환경 요구사항

- Python 3.8+
- OpenAI API 키
- YouTube Data API v3 인증 정보

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
OPENAI_API_KEY=your_openai_api_key_here
YOUTUBE_CLIENT_SECRETS_FILE=./client_secret.json
OUTPUT_DIR=./maro_content
VIDEO_RESOLUTION=1920x1080
BACKGROUND_IMAGE=./background.jpg
```

### 4. YouTube API 설정

1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트 생성
2. YouTube Data API v3 활성화
3. OAuth 2.0 클라이언트 ID 생성
4. `client_secret.json` 파일 다운로드하여 프로젝트 루트에 배치

## 📖 사용법

### 기본 실행 (주간 스케줄)

```bash
python main.py
```

### 테스트 모드 (단일 콘텐츠 생성)

```bash
python main.py test
```

### 수동 콘텐츠 생성

```python
from comfort_generator import ComfortContentGenerator

generator = ComfortContentGenerator()

# 오늘의 위로 생성
comfort = generator.generate_daily_comfort()

# 힐링 사운드 스크립트 생성
healing = generator.generate_healing_sound_script("빗소리")

# 극복 스토리 생성
story = generator.generate_overcome_story("취업 실패 후 성공")

# 맞춤형 위로 생성
custom = generator.generate_custom_comfort("퇴근 후 무기력할 때")
```

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ ComfortContent  │    │   TTS OpenAI    │    │  Video Maker    │
│   Generator     │───▶│   (음성합성)     │───▶│  (비디오제작)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Thumbnail Gen   │    │  YouTube API    │    │   Output Dir    │
│  (썸네일생성)    │    │   (업로드)      │    │   (결과저장)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 주요 기능

### 1. AI 콘텐츠 생성
- OpenAI GPT 모델을 활용한 자연스러운 위로 문구 생성
- 콘텐츠 타입별 맞춤 프롬프트 시스템
- API 오류 시 기본 콘텐츠 제공

### 2. 자동 비디오 제작
- MoviePy 기반 고품질 비디오 생성
- 콘텐츠 타입별 맞춤 스타일링
- 자동 자막 및 타이밍 조정

### 3. 스마트 썸네일
- 콘텐츠 타입별 색상 테마
- 자동 텍스트 줄바꿈 및 배치
- 시각적 매력도 최적화

### 4. YouTube 자동화
- 주간 스케줄 기반 자동 업로드
- 재생목록 자동 생성 및 관리
- 태그 및 설명 자동 최적화

## 📁 프로젝트 구조

```
maro/
├── main.py                 # 메인 실행 파일
├── config.py               # 설정 파일
├── comfort_generator.py    # 위로 콘텐츠 생성기
├── video_maker.py          # 비디오 제작 엔진
├── thumbnail_gen.py        # 썸네일 생성기
├── tts_openai.py          # OpenAI TTS 연동
├── uploader_youtube.py    # YouTube 업로드
├── utils.py               # 유틸리티 함수
├── requirements.txt        # Python 의존성
├── background.jpg         # 기본 배경 이미지
└── maro_content/          # 생성된 콘텐츠 저장소
    └── YYYY-MM-DD/
        ├── daily_comfort/
        ├── healing_sound/
        ├── overcome_story/
        └── custom_comfort/
```

## 🎨 커스터마이징

### 콘텐츠 스타일 수정

`comfort_generator.py`에서 프롬프트와 테마를 수정할 수 있습니다:

```python
# 새로운 테마 추가
themes = [
    "일상의 작은 기쁨", "힘든 순간을 이겨내는 법",
    "자신을 사랑하는 방법", "새로운 시작의 용기",
    "외로움을 극복하는 법", "스트레스 해소법",
    "자신감을 키우는 방법", "감사함을 느끼는 법",
    "당신만의 테마"  # 새로 추가
]
```

### 비디오 스타일 수정

`video_maker.py`에서 배경, 폰트, 애니메이션을 커스터마이징할 수 있습니다:

```python
def create_healing_background(W: int, H: int, duration: float, style: str = "calm"):
    # 새로운 스타일 추가
    if style == "your_style":
        # 커스텀 배경 로직
        pass
```

## 📊 운영 로드맵

### 1개월차 (기초 다지기)
- [x] "오늘의 위로" 매일 업로드
- [x] 힐링 사운드·스토리 시리즈 시작
- [x] 채널 브랜딩 완성

### 2개월차 (참여 유도)
- [ ] 맞춤형 시리즈 본격 운영
- [ ] 한 줄 위로 챌린지 첫 실행
- [ ] 커뮤니티 탭 활성화

### 3개월차 (콘텐츠 다변화)
- [ ] 극복 스토리 주제 다양화
- [ ] 시청자 요청 기반 맞춤형 콘텐츠

### 4개월차 (확장 & 안정화)
- [ ] 해외 자막 지원 (영어, 일본어)
- [ ] Podcast 연동
- [ ] 재생목록으로 "위로 아카이브" 정리

## 💰 수익 구조

- **초기 (0~6개월)**: 광고 수익화 목표 (구독자 1천명, 시청시간 4천시간)
- **성장기 (6개월~1년)**: 광고 + 멤버십(전용 영상, 뱃지 제공)
- **확장기 (1년 이후)**: 위로 문구 굿즈, 에세이 출판, 심리 상담 앱 제휴

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 생성해 주세요.

---

**maro** - 당신의 마음에 쉼표를 찍어드립니다 💙
