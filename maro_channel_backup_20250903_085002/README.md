# maro 채널 - 파일 구조 가이드

마음위로(maro) 채널의 모든 파일들이 기능별로 정리되어 있습니다.

## 📁 폴더 구조

| 폴더명 | 설명 | 파일 수 |
|--------|------|--------|
| **core** | 핵심 콘텐츠 생성 모듈 | 7개 |
| **media** | 미디어 제작 관련 모듈 | 4개 |
| **upload** | 유튜브 업로드 및 관리 | 2개 |
| **config** | 설정 및 유틸리티 | 3개 |
| **scheduling** | 스케줄링 및 자동화 | 2개 |
| **testing** | 테스트 및 검증 | 10개 |
| **samples** | 샘플 콘텐츠 및 생성기 | 1개 |
| **docs** | 문서 및 가이드 | 2개 |
| **assets** | 미디어 자산 | 8개 |
| **legacy** | 기존 뉴스 관련 파일 (참고용) | 9개 |

## 🚀 빠른 시작

### 1. 기본 설정
```bash
cd config/
# env_example.txt를 .env로 복사하고 API 키 설정
```

### 2. 콘텐츠 생성
```bash
cd core/
python comfort_generator_main.py
```

### 3. 샘플 콘텐츠 생성
```bash
cd samples/
python create_sample_content.py
```

### 4. 테스트 실행
```bash
cd testing/
python test_comfort_system.py
```

## 📋 폴더별 상세 설명

### 📁 CORE
핵심 콘텐츠 생성 모듈

**주요 파일:**
- `comfort_generator_base.py`
- `comfort_generator_main.py`
- `comfort_generator_daily.py`
- `comfort_generator_healing.py`
- `comfort_generator_story.py`
- `comfort_generator_custom.py`
- `comfort_generator_challenge.py`

### 📁 MEDIA
미디어 제작 관련 모듈

**주요 파일:**
- `video_maker.py`
- `thumbnail_gen.py`
- `tts_openai.py`
- `tts_openai_fixed.py`

### 📁 UPLOAD
유튜브 업로드 및 관리

**주요 파일:**
- `uploader_youtube.py`
- `youtube_setup_guide.md`

### 📁 CONFIG
설정 및 유틸리티

**주요 파일:**
- `config.py`
- `utils.py`
- `env_example.txt`

### 📁 SCHEDULING
스케줄링 및 자동화

**주요 파일:**
- `schedule_comfort.py`
- `main.py`

### 📁 TESTING
테스트 및 검증

**주요 파일:**
- `test_comfort_system.py`
- `test_core_functions.py`
- `test_complete_system.py`
- `test_simple_video.py`
- `test_video_only.py`
- `test_youtube_auth.py`
- `test_youtube_auth_headless.py`
- `test_youtube_quick.py`
- `test_youtube_upload.py`
- `test_system_without_youtube.py`

### 📁 SAMPLES
샘플 콘텐츠 및 생성기

**주요 파일:**
- `create_sample_content.py`

### 📁 DOCS
문서 및 가이드

**주요 파일:**
- `README.md`
- `google_cloud_setup_detailed.md`

### 📁 ASSETS
미디어 자산

**주요 파일:**
- `background.jpg`
- `better_news_briefing.mp4`
- `final_news_briefing.mp4`
- `fixed_news_briefing.mp4`
- `pil_news_briefing.mp4`
- `test_complete_system.py`
- `test_narration.mp3`
- `test_simple_news.mp4`

### 📁 LEGACY
기존 뉴스 관련 파일 (참고용)

**주요 파일:**
- `check_account.py`
- `create_better_news_video.py`
- `create_final_news_video.py`
- `create_fixed_news_video.py`
- `create_korean_news_video.py`
- `create_pil_news_video.py`
- `news_fetcher.py`
- `summarizer_openai.py`
- `setup_assistant.py`

## 🔧 개발 환경 설정

```bash
pip install -r requirements.txt
```

## 📚 주요 기능

- **콘텐츠 생성**: AI 기반 위로 콘텐츠 자동 생성
- **비디오 제작**: MoviePy를 활용한 자동 비디오 제작
- **유튜브 업로드**: 자동 업로드 및 플레이리스트 관리
- **스케줄링**: 정기적인 콘텐츠 생성 및 업로드
- **테스트**: 모든 기능에 대한 종합 테스트

## 🎯 3분 위로 콘텐츠 구성안

모든 콘텐츠는 다음 구조를 따릅니다:

- **인트로 (10-15초)**: 채널 로고 + 제목 카드 + 주제 소개
- **본문 (120-130초)**: 6-8개 단락으로 이어지는 위로 글귀
- **아웃로 (20-30초)**: 요약 + 다음 영상 안내

---
**정리일**: 2025년 09월 03일
**maro 채널 파일 정리 스크립트**로 자동 생성되었습니다.
