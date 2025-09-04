#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 실제 영상 생성 스크립트
"""

import os
import sys
import json
from datetime import datetime

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'maro_channel'))

def create_simple_video():
    """간단한 테스트 영상 생성"""
    print("🚀 maro 채널 실제 영상 생성 시작")
    print("=" * 60)
    
    try:
        # 1. 샘플 콘텐츠 로드
        print("📝 샘플 콘텐츠 로드 중...")
        with open("maro_channel/samples/youtube_sample/sample_content.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        print(f"✅ 콘텐츠 로드 완료: {content['title']}")
        
        # 2. TTS 스크립트 로드
        print("🎤 TTS 스크립트 로드 중...")
        with open("maro_channel/samples/youtube_sample/tts_script.txt", "r", encoding="utf-8") as f:
            tts_script = f.read()
        print(f"✅ TTS 스크립트 로드 완료 ({len(tts_script)}자)")
        
        # 3. 간단한 텍스트 파일로 나레이션 생성 (TTS 없이)
        print("📝 나레이션 텍스트 파일 생성 중...")
        narration_file = "narration.txt"
        with open(narration_file, 'w', encoding='utf-8') as f:
            f.write(tts_script)
        print(f"✅ 나레이션 파일 생성 완료: {narration_file}")
        
        # 4. 간단한 비디오 정보 파일 생성
        print("📹 비디오 정보 파일 생성 중...")
        video_info = {
            "title": content['title'],
            "content": content['content'],
            "duration": content['duration'],
            "narration_file": narration_file,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open("video_info.json", 'w', encoding='utf-8') as f:
            json.dump(video_info, f, ensure_ascii=False, indent=2)
        print(f"✅ 비디오 정보 파일 생성 완료: video_info.json")
        
        # 5. 제작 가이드 생성
        print("📋 제작 가이드 생성 중...")
        guide = {
            "steps": [
                "1. OpenAI API 키 설정",
                "2. TTS 생성: python -c \"from maro_channel.media.tts_openai import create_tts; create_tts(open('narration.txt', 'r', encoding='utf-8').read(), 'narration.mp3')\"",
                "3. 비디오 제작: python -c \"from maro_channel.media.video_maker import make_healing_video; make_healing_video('video_info.json', 'narration.mp3', 'maro_sample_video.mp4')\"",
                "4. 썸네일 생성: python -c \"from maro_channel.media.thumbnail_gen import generate_healing_thumbnail; generate_healing_thumbnail('오늘의 위로: 자존감을 높이는 방법', 'daily_comfort', 'maro_sample_thumbnail.jpg')\""
            ],
            "requirements": [
                "OpenAI API 키",
                "MoviePy 라이브러리",
                "Pillow 라이브러리",
                "배경 이미지 파일"
            ]
        }
        
        with open("production_guide.json", 'w', encoding='utf-8') as f:
            json.dump(guide, f, ensure_ascii=False, indent=2)
        print(f"✅ 제작 가이드 생성 완료: production_guide.json")
        
        print("\n" + "=" * 60)
        print("🎉 영상 제작 준비 완료!")
        print(f"📁 현재 위치: {os.getcwd()}")
        print("\n생성된 파일들:")
        print(f"- {narration_file} (나레이션 텍스트)")
        print("- video_info.json (비디오 정보)")
        print("- production_guide.json (제작 가이드)")
        
        print("\n📋 다음 단계:")
        print("1. OpenAI API 키 설정")
        print("2. 필요한 라이브러리 설치: pip install openai moviepy pillow")
        print("3. 위의 제작 가이드에 따라 실제 영상 생성")
        
        print("\n🎯 최종 결과물:")
        print("- narration.mp3 (TTS 나레이션)")
        print("- maro_sample_video.mp4 (완성된 비디오)")
        print("- maro_sample_thumbnail.jpg (썸네일)")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False
    
    return True

if __name__ == "__main__":
    create_simple_video()
