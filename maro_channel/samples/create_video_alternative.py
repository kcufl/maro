#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MoviePy 대신 다른 방법으로 비디오 생성
"""

import os
import json
import subprocess
from datetime import datetime

def create_video_with_ffmpeg():
    """FFmpeg를 사용해서 간단한 비디오 생성"""
    print("🎬 FFmpeg를 사용한 비디오 생성 시작")
    
    try:
        # 1. 나레이션 파일 확인
        if not os.path.exists("narration.mp3"):
            print("❌ narration.mp3 파일이 없습니다.")
            return False
        
        print(f"✅ 나레이션 파일 확인: {os.path.getsize('narration.mp3')} bytes")
        
        # 2. 간단한 배경 이미지 생성 (PIL 사용)
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # 1920x1080 배경 이미지 생성
            width, height = 1920, 1080
            img = Image.new('RGB', (width, height), color='#FFE4E1')  # 연한 핑크색
            
            # 텍스트 추가
            draw = ImageDraw.Draw(img)
            
            # 제목 텍스트
            title = "오늘의 위로: 자존감을 높이는 방법"
            subtitle = "maro (마음위로)"
            
            try:
                # 폰트 설정 (시스템 폰트 사용)
                title_font = ImageFont.truetype("arial.ttf", 60)
                subtitle_font = ImageFont.truetype("arial.ttf", 40)
            except:
                # 기본 폰트 사용
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
            
            # 텍스트 그리기
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_height = title_bbox[3] - title_bbox[1]
            
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            
            # 중앙 정렬
            title_x = (width - title_width) // 2
            title_y = (height - title_height) // 2 - 50
            
            subtitle_x = (width - subtitle_width) // 2
            subtitle_y = title_y + title_height + 20
            
            # 텍스트 그리기
            draw.text((title_x, title_y), title, fill='#8B4513', font=title_font)
            draw.text((subtitle_x, subtitle_y), subtitle, fill='#A0522D', font=subtitle_font)
            
            # 이미지 저장
            background_img = "background.png"
            img.save(background_img)
            print(f"✅ 배경 이미지 생성: {background_img}")
            
        except ImportError:
            print("⚠️ PIL이 없어서 단색 배경을 사용합니다.")
            background_img = None
        
        # 3. FFmpeg 명령어 생성
        if background_img and os.path.exists(background_img):
            # 이미지 + 오디오로 비디오 생성
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", background_img,
                "-i", "narration.mp3",
                "-c:v", "libx264", "-tune", "stillimage",
                "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest",
                "maro_video.mp4"
            ]
        else:
            # 오디오만으로 비디오 생성 (검은 화면)
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", "color=c=black:s=1920x1080:d=180",
                "-i", "narration.mp3",
                "-c:v", "libx264",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                "maro_video.mp4"
            ]
        
        print("🎬 FFmpeg로 비디오 생성 중...")
        print(f"명령어: {' '.join(cmd)}")
        
        # FFmpeg 실행
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 비디오 생성 완료!")
            if os.path.exists("maro_video.mp4"):
                size = os.path.getsize("maro_video.mp4")
                print(f"📁 파일 크기: {size} bytes")
                return True
            else:
                print("❌ 비디오 파일이 생성되지 않았습니다.")
                return False
        else:
            print(f"❌ FFmpeg 오류: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ FFmpeg가 설치되지 않았습니다.")
        print("FFmpeg 설치 방법:")
        print("1. https://ffmpeg.org/download.html 에서 다운로드")
        print("2. 또는 chocolatey: choco install ffmpeg")
        print("3. 또는 winget: winget install ffmpeg")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def create_simple_video_info():
    """간단한 비디오 정보 생성"""
    print("📝 비디오 정보 생성")
    
    video_info = {
        "title": "오늘의 위로: 자존감을 높이는 방법",
        "theme": "자존감 향상",
        "duration": "3분",
        "narration_file": "narration.mp3",
        "video_file": "maro_video.mp4",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "비디오 생성 완료",
        "files": {
            "narration": "narration.mp3",
            "video": "maro_video.mp4",
            "background": "background.png"
        }
    }
    
    with open("final_video_info.json", "w", encoding="utf-8") as f:
        json.dump(video_info, f, ensure_ascii=False, indent=2)
    
    print("✅ 최종 비디오 정보 생성: final_video_info.json")
    return video_info

def main():
    """메인 실행 함수"""
    print("🚀 maro 채널 비디오 생성 시작")
    print("=" * 60)
    
    # 1. FFmpeg로 비디오 생성 시도
    success = create_video_with_ffmpeg()
    
    if success:
        print("\n🎉 비디오 생성 성공!")
        
        # 2. 비디오 정보 생성
        video_info = create_simple_video_info()
        
        print("\n📁 생성된 파일들:")
        for key, filename in video_info["files"].items():
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                print(f"- {filename} ({size} bytes)")
            else:
                print(f"- {filename} (없음)")
        
        print("\n🎯 다음 단계:")
        print("1. 썸네일 생성")
        print("2. 유튜브 업로드")
        
    else:
        print("\n❌ 비디오 생성 실패")
        print("\n대안:")
        print("1. FFmpeg 설치 후 재시도")
        print("2. 온라인 비디오 편집 도구 사용")
        print("3. 다른 비디오 제작 소프트웨어 사용")

if __name__ == "__main__":
    main()
