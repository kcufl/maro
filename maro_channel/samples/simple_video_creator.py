#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 maro 채널 영상 생성기
"""

import os
import json
from datetime import datetime

def create_video_files():
    """영상 제작용 파일들 생성"""
    print("🚀 maro 채널 영상 제작 파일 생성")
    print("=" * 50)
    
    # 1. 나레이션 텍스트 생성
    narration_text = """안녕하세요, maro입니다.

오늘의 위로 시간입니다.

자존감을 높이는 방법에 대해 이야기해볼게요.

오늘도 지치셨죠. 

때로는 결과가 없어도 의미가 있습니다. 

잠시 멈춰도 괜찮습니다. 

당신이 지금까지 걸어온 길은 이미 충분히 의미가 있어요. 

작은 성취 하나하나가 당신을 만든 것입니다. 

자신의 장점을 하나씩 적어보세요. 

당신은 생각보다 훨씬 훌륭한 사람입니다. 

내일도 당신을 기다리는 빛이 있습니다.

당신은 혼자가 아닙니다.

구독과 좋아요 부탁드려요.

다음 영상에서 또 만나요."""
    
    with open("narration.txt", "w", encoding="utf-8") as f:
        f.write(narration_text)
    print("✅ 나레이션 텍스트 생성: narration.txt")
    
    # 2. 비디오 정보 생성
    video_info = {
        "title": "오늘의 위로: 자존감을 높이는 방법",
        "theme": "자존감 향상",
        "duration": "3분",
        "content": "오늘도 지치셨죠. 때로는 결과가 없어도 의미가 있습니다. 잠시 멈춰도 괜찮습니다.",
        "tags": ["위로", "힐링", "maro", "자존감"],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open("video_info.json", "w", encoding="utf-8") as f:
        json.dump(video_info, f, ensure_ascii=False, indent=2)
    print("✅ 비디오 정보 생성: video_info.json")
    
    # 3. 제작 가이드 생성
    guide = {
        "title": "maro 채널 영상 제작 가이드",
        "steps": [
            {
                "step": 1,
                "title": "TTS 나레이션 생성",
                "command": "python -c \"from maro_channel.media.tts_openai import create_tts; create_tts(open('narration.txt', 'r', encoding='utf-8').read(), 'narration.mp3')\"",
                "result": "narration.mp3 파일 생성"
            },
            {
                "step": 2,
                "title": "비디오 제작",
                "command": "python -c \"from maro_channel.media.video_maker import make_healing_video; make_healing_video('video_info.json', 'narration.mp3', 'maro_video.mp4')\"",
                "result": "maro_video.mp4 파일 생성"
            },
            {
                "step": 3,
                "title": "썸네일 생성",
                "command": "python -c \"from maro_channel.media.thumbnail_gen import generate_healing_thumbnail; generate_healing_thumbnail('오늘의 위로: 자존감을 높이는 방법', 'daily_comfort', 'thumbnail.jpg')\"",
                "result": "thumbnail.jpg 파일 생성"
            }
        ],
        "requirements": [
            "OpenAI API 키 (TTS용)",
            "MoviePy 라이브러리 (비디오 제작용)",
            "Pillow 라이브러리 (썸네일용)",
            "배경 이미지 파일"
        ]
    }
    
    with open("production_guide.json", "w", encoding="utf-8") as f:
        json.dump(guide, f, ensure_ascii=False, indent=2)
    print("✅ 제작 가이드 생성: production_guide.json")
    
    # 4. README 파일 생성
    readme_content = f"""# maro 채널 영상 제작

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
생성일: {datetime.now().strftime("%Y년 %m월 %d일")}
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✅ README 파일 생성: README.md")
    
    print("\n" + "=" * 50)
    print("🎉 영상 제작 파일 생성 완료!")
    print("\n📁 생성된 파일들:")
    print("- narration.txt (나레이션 텍스트)")
    print("- video_info.json (비디오 정보)")
    print("- production_guide.json (제작 가이드)")
    print("- README.md (사용 가이드)")
    
    print("\n📋 다음 단계:")
    print("1. OpenAI API 키 설정")
    print("2. 필요한 라이브러리 설치")
    print("3. README.md의 가이드에 따라 영상 제작")
    
    print("\n🎯 최종 결과물:")
    print("- narration.mp3 (TTS 나레이션)")
    print("- maro_video.mp4 (완성된 비디오)")
    print("- thumbnail.jpg (썸네일)")

if __name__ == "__main__":
    create_video_files()
