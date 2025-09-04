# maro 채널 영상 제작

## 📁 생성된 파일들

- `narration.txt` - 나레이션 텍스트
- `video_info.json` - 비디오 정보
- `production_guide.json` - 제작 가이드

## 🚀 영상 제작 방법

### 1. 환경 설정
```bash
pip install openai moviepy pillow
```

### 2. API 키 설정
```bash
# .env 파일 생성
OPENAI_API_KEY=your_api_key_here
```

### 3. 영상 제작
```bash
# TTS 생성
python -c "from maro_channel.media.tts_openai import create_tts; create_tts(open('narration.txt', 'r', encoding='utf-8').read(), 'narration.mp3')"

# 비디오 제작
python -c "from maro_channel.media.video_maker import make_healing_video; make_healing_video('video_info.json', 'narration.mp3', 'maro_video.mp4')"

# 썸네일 생성
python -c "from maro_channel.media.thumbnail_gen import generate_healing_thumbnail; generate_healing_thumbnail('오늘의 위로: 자존감을 높이는 방법', 'daily_comfort', 'thumbnail.jpg')"
```

## 📋 최종 결과물

- `narration.mp3` - TTS 나레이션
- `maro_video.mp4` - 완성된 비디오
- `thumbnail.jpg` - 썸네일

---
생성일: 2025년 09월 04일
