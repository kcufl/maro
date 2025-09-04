#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 유튜브 샘플 영상 제작 실행 스크립트
"""

import os
import sys
import json
from datetime import datetime

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, '..', '..'))

def create_sample_video():
    """샘플 비디오 제작"""
    print("🚀 maro 채널 유튜브 샘플 영상 제작 시작")
    print("=" * 60)
    
    try:
        # 1. 콘텐츠 로드
        print("📝 콘텐츠 로드 중...")
        with open("sample_content.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        print(f"✅ 콘텐츠 로드 완료: {content['title']}")
        
        # 2. TTS 스크립트 로드
        print("🎤 TTS 스크립트 로드 중...")
        with open("tts_script.txt", "r", encoding="utf-8") as f:
            tts_script = f.read()
        print(f"✅ TTS 스크립트 로드 완료 ({len(tts_script)}자)")
        
        # 3. 업로드 스크립트 로드
        print("📤 업로드 스크립트 로드 중...")
        with open("video_upload_script.json", "r", encoding="utf-8") as f:
            upload_script = json.load(f)
        print(f"✅ 업로드 스크립트 로드 완료: {upload_script['title']}")
        
        # 4. 제작 가이드 로드
        print("📋 제작 가이드 로드 중...")
        with open("production_guide.json", "r", encoding="utf-8") as f:
            guide = json.load(f)
        print(f"✅ 제작 가이드 로드 완료")
        
        print("\n" + "=" * 60)
        print("🎉 샘플 영상 제작 준비 완료!")
        print(f"📁 현재 위치: {os.getcwd()}")
        print("\n준비된 파일들:")
        print("- sample_content.json (콘텐츠 데이터)")
        print("- tts_script.txt (TTS 스크립트)")
        print("- video_upload_script.json (업로드 설정)")
        print("- production_guide.json (제작 가이드)")
        
        print("\n📋 제작 정보:")
        print(f"- 제목: {content['title']}")
        print(f"- 테마: {content['theme']}")
        print(f"- 지속시간: {content['duration']}")
        print(f"- 태그: {', '.join(content['tags'][:5])}...")
        
        print("\n🎯 3분 구성안:")
        for timing, desc in content['timing'].items():
            print(f"- {timing}: {desc}")
        
        print("\n🎨 시각 요소:")
        for element in content['visual_elements']:
            print(f"- {element}")
        
        print("\n🎵 오디오 요소:")
        for element in content['audio_elements']:
            print(f"- {element}")
        
        print("\n" + "=" * 60)
        print("📝 다음 단계:")
        print("1. OpenAI API 키 설정")
        print("2. TTS 생성: python -c \"from media.tts_openai import create_tts; create_tts(open('tts_script.txt', 'r', encoding='utf-8').read(), 'narration.mp3')\"")
        print("3. 비디오 제작: python -c \"from media.video_maker import make_healing_video; make_healing_video('sample_content.json', 'narration.mp3', 'maro_sample_video.mp4')\"")
        print("4. 썸네일 생성: python -c \"from media.thumbnail_gen import generate_healing_thumbnail; generate_healing_thumbnail('오늘의 위로: 자존감을 높이는 방법', 'daily_comfort', 'maro_sample_thumbnail.jpg')\"")
        print("5. 유튜브 업로드: python -c \"from upload.uploader_youtube import upload_video; upload_video('maro_sample_video.mp4', 'video_upload_script.json')\"")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False
    
    return True

if __name__ == "__main__":
    create_sample_video()
