#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 비디오 생성 스크립트 (MoviePy 없이)
"""

import os
import json
from datetime import datetime

def create_simple_video():
    """간단한 비디오 정보 파일 생성"""
    print("🎬 간단한 비디오 정보 생성")
    
    try:
        # 비디오 정보 로드
        with open("video_info.json", "r", encoding="utf-8") as f:
            video_info = json.load(f)
        
        # 나레이션 파일 확인
        if os.path.exists("narration.mp3"):
            print(f"✅ 나레이션 파일 확인: narration.mp3 ({os.path.getsize('narration.mp3')} bytes)")
        else:
            print("❌ 나레이션 파일이 없습니다.")
            return False
        
        # 비디오 제작 정보 생성
        video_production_info = {
            "title": video_info["title"],
            "theme": video_info["theme"],
            "duration": video_info["duration"],
            "narration_file": "narration.mp3",
            "narration_size": os.path.getsize("narration.mp3"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "TTS 완료, 비디오 제작 대기",
            "next_steps": [
                "1. 배경 이미지 준비",
                "2. MoviePy로 비디오 제작",
                "3. 썸네일 생성",
                "4. 유튜브 업로드"
            ]
        }
        
        # 비디오 제작 정보 저장
        with open("video_production_info.json", "w", encoding="utf-8") as f:
            json.dump(video_production_info, f, ensure_ascii=False, indent=2)
        
        print("✅ 비디오 제작 정보 생성: video_production_info.json")
        
        # 간단한 비디오 스크립트 생성
        video_script = f"""# maro 채널 비디오 제작 스크립트

## 📁 현재 상태
- ✅ TTS 나레이션 생성 완료: narration.mp3
- ⏳ 비디오 제작 대기 중

## 🎬 비디오 정보
- 제목: {video_info['title']}
- 테마: {video_info['theme']}
- 지속시간: {video_info['duration']}
- 나레이션: {os.path.getsize('narration.mp3')} bytes

## 📋 다음 단계
1. 배경 이미지 준비 (1920x1080)
2. MoviePy 설치 및 비디오 제작
3. 썸네일 생성
4. 유튜브 업로드

## 🎯 최종 결과물
- maro_video.mp4 (완성된 비디오)
- thumbnail.jpg (썸네일)

---
생성일: {datetime.now().strftime("%Y년 %m월 %d일")}
"""
        
        with open("video_script.md", "w", encoding="utf-8") as f:
            f.write(video_script)
        
        print("✅ 비디오 스크립트 생성: video_script.md")
        
        print("\n" + "=" * 50)
        print("🎉 비디오 제작 준비 완료!")
        print("\n📁 생성된 파일들:")
        print("- narration.mp3 (TTS 나레이션)")
        print("- video_production_info.json (제작 정보)")
        print("- video_script.md (제작 스크립트)")
        
        print("\n📋 현재 상태:")
        print("✅ TTS 나레이션 생성 완료")
        print("⏳ 비디오 제작 대기 중 (MoviePy 필요)")
        
        print("\n🎯 다음 단계:")
        print("1. MoviePy 재설치 또는 다른 비디오 제작 도구 사용")
        print("2. 배경 이미지 준비")
        print("3. 비디오 제작")
        print("4. 썸네일 생성")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

if __name__ == "__main__":
    create_simple_video()
