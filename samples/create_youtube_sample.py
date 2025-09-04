#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 유튜브 샘플 영상 생성기
실제 영상과 나레이션을 만들어서 유튜브에 올릴 수 있는 샘플 생성
"""

import os
import sys
import json
from datetime import datetime

def create_sample_content():
    """샘플 콘텐츠 생성"""
    sample_content = {
        "type": "daily_comfort",
        "theme": "자존감을 높이는 방법",
        "title": "오늘의 위로: 자존감을 높이는 방법",
        "content": """오늘도 지치셨죠. 

때로는 결과가 없어도 의미가 있습니다. 

잠시 멈춰도 괜찮습니다. 

당신이 지금까지 걸어온 길은 이미 충분히 의미가 있어요. 

작은 성취 하나하나가 당신을 만든 것입니다. 

자신의 장점을 하나씩 적어보세요. 

당신은 생각보다 훨씬 훌륭한 사람입니다. 

내일도 당신을 기다리는 빛이 있습니다.""",
        "duration": "3분",
        "tags": ["위로", "힐링", "일상위로", "maro", "마음위로", "자존감", "자기계발", "루틴"],
        "structure": {
            "intro": "10-15초 - 채널 로고 + '오늘의 위로' 타이틀 + 주제 소개",
            "main_message": "120-130초 - 이어지는 위로 글귀 낭독 (6-8개 단락)",
            "outro": "20-30초 - 요약 + '당신은 혼자가 아닙니다' + 다음 영상 안내"
        },
        "timing": {
            "0:00-0:15": "인트로 - 로고 + 제목 카드 + 주제 소개",
            "0:15-2:25": "본문 위로글 - 6-8개 단락으로 이어지는 글귀 낭독",
            "2:25-3:00": "아웃로 - 요약 + 구독/다음 영상 안내"
        },
        "visual_elements": [
            "따뜻한 노을빛 하늘",
            "평화로운 숲길", 
            "부드러운 파스텔 톤"
        ],
        "audio_elements": [
            "잔잔한 피아노 멜로디",
            "따뜻하고 차분한 내레이션"
        ]
    }
    return sample_content

def create_tts_script():
    """TTS용 스크립트 생성"""
    script = """안녕하세요, maro입니다.

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
    
    return script

def create_video_script():
    """비디오 제작용 스크립트 생성"""
    video_script = {
        "title": "오늘의 위로: 자존감을 높이는 방법 | maro",
        "description": """오늘도 지치셨죠. 때로는 결과가 없어도 의미가 있습니다.

이 영상은 당신의 자존감을 높이는 방법에 대해 이야기합니다.

💝 maro 채널 구독하기: https://youtube.com/@maro
📱 더 많은 위로 콘텐츠: #maro #마음위로

🎵 오늘의 메시지:
- 잠시 멈춰도 괜찮습니다
- 당신이 지금까지 걸어온 길은 이미 충분히 의미가 있어요
- 작은 성취 하나하나가 당신을 만든 것입니다
- 자신의 장점을 하나씩 적어보세요
- 당신은 생각보다 훨씬 훌륭한 사람입니다

#위로 #힐링 #일상위로 #maro #마음위로 #자존감 #자기계발 #루틴 #마음치유 #자기사랑""",
        "tags": [
            "위로", "힐링", "일상위로", "maro", "마음위로", 
            "자존감", "자기계발", "루틴", "마음치유", "자기사랑",
            "위로영상", "힐링영상", "자존감향상", "마음위로", "일상힐링"
        ],
        "category": "22",  # People & Blogs
        "privacy": "public"
    }
    return video_script

def create_production_guide():
    """제작 가이드 생성"""
    guide = {
        "video_specs": {
            "duration": "3분 (180초)",
            "resolution": "1920x1080 (Full HD)",
            "frame_rate": "30fps",
            "aspect_ratio": "16:9"
        },
        "audio_specs": {
            "sample_rate": "44100 Hz",
            "bitrate": "128 kbps",
            "format": "MP3"
        },
        "timing_breakdown": {
            "0:00-0:15": {
                "content": "인트로",
                "visual": "채널 로고 + '오늘의 위로' 타이틀 + 주제 소개",
                "audio": "따뜻한 인사말 + BGM 시작"
            },
            "0:15-2:25": {
                "content": "본문 위로글",
                "visual": "자연스러운 배경 + 자막 표시",
                "audio": "차분한 내레이션 + 잔잔한 BGM"
            },
            "2:25-3:00": {
                "content": "아웃로",
                "visual": "요약 메시지 + 구독 안내",
                "audio": "마무리 멘트 + BGM 페이드아웃"
            }
        },
        "visual_style": {
            "background": "따뜻한 노을빛 하늘, 평화로운 숲길",
            "color_palette": "부드러운 파스텔 톤 (크림, 베이지, 연한 오렌지)",
            "font": "둥근고딕 또는 산세리프 계열",
            "animation": "미니멀한 페이드 인/아웃 효과"
        },
        "audio_style": {
            "bgm": "잔잔한 피아노/스트링 중심",
            "narration": "따뜻하고 차분한 톤",
            "pacing": "문장 끝마다 1-2초 멈춤으로 여운 강조"
        }
    }
    return guide

def save_sample_files():
    """샘플 파일들 저장"""
    # 출력 디렉토리 생성
    output_dir = "./youtube_sample"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 1. 콘텐츠 파일
    content = create_sample_content()
    with open(f"{output_dir}/sample_content.json", 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    # 2. TTS 스크립트
    tts_script = create_tts_script()
    with open(f"{output_dir}/tts_script.txt", 'w', encoding='utf-8') as f:
        f.write(tts_script)
    
    # 3. 비디오 업로드 스크립트
    video_script = create_video_script()
    with open(f"{output_dir}/video_upload_script.json", 'w', encoding='utf-8') as f:
        json.dump(video_script, f, ensure_ascii=False, indent=2)
    
    # 4. 제작 가이드
    guide = create_production_guide()
    with open(f"{output_dir}/production_guide.json", 'w', encoding='utf-8') as f:
        json.dump(guide, f, ensure_ascii=False, indent=2)
    
    # 5. 실행 스크립트
    execution_script = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
maro 채널 유튜브 샘플 영상 제작 실행 스크립트
\"\"\"

import os
import sys
from datetime import datetime

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, '..'))

def main():
    print("🚀 maro 채널 유튜브 샘플 영상 제작 시작")
    print("=" * 60)
    
    try:
        # 1. TTS 생성
        print("🎤 TTS 나레이션 생성 중...")
        from media.tts_openai import create_tts
        tts_file = create_tts(
            text=open("tts_script.txt", "r", encoding="utf-8").read(),
            output_file="narration.mp3"
        )
        print(f"✅ TTS 생성 완료: {{tts_file}}")
        
        # 2. 비디오 생성
        print("🎬 비디오 제작 중...")
        from media.video_maker import make_healing_video
        video_file = make_healing_video(
            content_file="sample_content.json",
            audio_file="narration.mp3",
            output_file="maro_sample_video.mp4"
        )
        print(f"✅ 비디오 생성 완료: {{video_file}}")
        
        # 3. 썸네일 생성
        print("🖼️ 썸네일 생성 중...")
        from media.thumbnail_gen import generate_healing_thumbnail
        thumbnail_file = generate_healing_thumbnail(
            title="오늘의 위로: 자존감을 높이는 방법",
            content_type="daily_comfort",
            output_file="maro_sample_thumbnail.jpg"
        )
        print(f"✅ 썸네일 생성 완료: {{thumbnail_file}}")
        
        # 4. 유튜브 업로드 (선택사항)
        print("📤 유튜브 업로드 준비 완료")
        print("업로드를 원하시면 다음 명령어를 실행하세요:")
        print("python upload_to_youtube.py")
        
        print("\\n" + "=" * 60)
        print("🎉 모든 샘플 파일 생성 완료!")
        print(f"📁 생성 위치: {{os.getcwd()}}")
        print("\\n생성된 파일들:")
        print("- narration.mp3 (나레이션)")
        print("- maro_sample_video.mp4 (비디오)")
        print("- maro_sample_thumbnail.jpg (썸네일)")
        
    except Exception as e:
        print(f"❌ 오류 발생: {{e}}")
        return False
    
    return True

if __name__ == "__main__":
    main()
"""
    
    with open(f"{output_dir}/create_sample_video.py", 'w', encoding='utf-8') as f:
        f.write(execution_script)
    
    # 6. README 파일
    readme_content = f"""# maro 채널 유튜브 샘플 영상 제작 가이드

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
pip install -r ../requirements.txt

# 환경 변수 설정 (.env 파일 생성)
OPENAI_API_KEY=your_openai_api_key
YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
```

### 2. 샘플 영상 제작
```bash
python create_sample_video.py
```

### 3. 유튜브 업로드 (선택사항)
```bash
python upload_to_youtube.py
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

---
**생성일**: {datetime.now().strftime("%Y년 %m월 %d일")}
**maro 채널 샘플 영상 제작기**로 자동 생성되었습니다.
"""
    
    with open(f"{output_dir}/README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    return output_dir

def main():
    """메인 실행 함수"""
    print("🚀 maro 채널 유튜브 샘플 영상 제작 파일 생성 시작")
    print("=" * 70)
    
    try:
        # 샘플 파일들 생성
        print("📝 샘플 파일들 생성 중...")
        output_dir = save_sample_files()
        
        print(f"✅ 샘플 파일들 생성 완료!")
        print(f"📁 생성 위치: {output_dir}")
        print("\n생성된 파일들:")
        print("- sample_content.json (샘플 콘텐츠)")
        print("- tts_script.txt (TTS 스크립트)")
        print("- video_upload_script.json (업로드 설정)")
        print("- production_guide.json (제작 가이드)")
        print("- create_sample_video.py (실행 스크립트)")
        print("- README.md (사용 가이드)")
        
        print("\n" + "=" * 70)
        print("🎉 유튜브 샘플 영상 제작 준비 완료!")
        print(f"\n다음 단계:")
        print(f"1. cd {output_dir}")
        print(f"2. python create_sample_video.py")
        print(f"3. 유튜브에 업로드!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
