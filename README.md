# maro 채널 유튜브 샘플 영상 제작 가이드

## 📁 생성된 파일들

- `sample_content.json` - 샘플 콘텐츠 데이터
- `tts_script.txt` - TTS용 나레이션 스크립트
- `video_upload_script.json` - 유튜브 업로드 설정
- `production_guide.json` - 제작 가이드
- `create_sample_video.py` - 실행 스크립트

## 🚀 사용 방법

### 1. 환경 설정
```bash
# 필요한 패키지 설치
pip install -r ../../requirements.txt

# 환경 변수 설정 (.env 파일 생성)
OPENAI_API_KEY=your_openai_api_key
YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
```

### 2. 샘플 영상 제작
```bash
python create_sample_video.py
```

### 3. 실제 영상 제작 (API 키 필요)
```bash
# TTS 생성
python -c "from media.tts_openai import create_tts; create_tts(open('tts_script.txt', 'r', encoding='utf-8').read(), 'narration.mp3')"

# 비디오 제작
python -c "from media.video_maker import make_healing_video; make_healing_video('sample_content.json', 'narration.mp3', 'maro_sample_video.mp4')"

# 썸네일 생성
python -c "from media.thumbnail_gen import generate_healing_thumbnail; generate_healing_thumbnail('오늘의 위로: 자존감을 높이는 방법', 'daily_comfort', 'maro_sample_thumbnail.jpg')"
```

### 4. 유튜브 업로드 (선택사항)
```bash
python -c "from upload.uploader_youtube import upload_video; upload_video('maro_sample_video.mp4', 'video_upload_script.json')"
```

## 📋 제작 과정

1. **TTS 생성**: OpenAI TTS API로 나레이션 생성
2. **비디오 제작**: MoviePy로 영상 편집
3. **썸네일 생성**: Pillow로 썸네일 제작
4. **유튜브 업로드**: YouTube Data API로 업로드

## 🎯 3분 구성안

- **인트로 (10-15초)**: 채널 로고 + 제목 카드 + 주제 소개
- **본문 (120-130초)**: 6-8개 단락으로 이어지는 위로 글귀
- **아웃로 (20-30초)**: 요약 + 구독/다음 영상 안내

## 📝 제작 노트

- **BGM**: 잔잔한 피아노/스트링 중심
- **내레이션**: 따뜻하고 차분한 톤, 문장 끝마다 1-2초 멈춤
- **시각 스타일**: 자연스럽고 따뜻한 파스텔 톤, 부드러운 전환
- **자막 폰트**: 둥근고딕 또는 산세리프 계열, 가독성 중심

## 🎬 샘플 콘텐츠

**제목**: 오늘의 위로: 자존감을 높이는 방법

**내용**: 
- 오늘도 지치셨죠
- 때로는 결과가 없어도 의미가 있습니다
- 잠시 멈춰도 괜찮습니다
- 당신이 지금까지 걸어온 길은 이미 충분히 의미가 있어요
- 작은 성취 하나하나가 당신을 만든 것입니다
- 자신의 장점을 하나씩 적어보세요
- 당신은 생각보다 훨씬 훌륭한 사람입니다
- 내일도 당신을 기다리는 빛이 있습니다

---
**생성일**: 2025년 09월 04일
**maro 채널 샘플 영상 제작기**로 자동 생성되었습니다.