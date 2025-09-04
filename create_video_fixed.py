#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 영상 생성기 - 수정 버전
한글 폰트 문제 해결 및 오디오 추가 기능 개선
"""

import os
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess
import sys
import platform

def get_korean_font():
    """한글 폰트 경로 찾기"""
    system = platform.system()
    
    if system == "Windows":
        # Windows 한글 폰트 경로들
        font_paths = [
            "C:/Windows/Fonts/malgun.ttf",  # 맑은 고딕
            "C:/Windows/Fonts/gulim.ttc",   # 굴림
            "C:/Windows/Fonts/batang.ttc",  # 바탕
            "C:/Windows/Fonts/dotum.ttc",   # 돋움
            "C:/Windows/Fonts/arial.ttf",   # Arial (영문)
        ]
    elif system == "Darwin":  # macOS
        font_paths = [
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    else:  # Linux
        font_paths = [
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    
    # 사용 가능한 폰트 찾기
    for font_path in font_paths:
        if os.path.exists(font_path):
            return font_path
    
    return None

def create_text_image_korean(text, width=1920, height=200, font_size=60, bg_color=(255, 248, 240), text_color=(44, 62, 80)):
    """한글 텍스트 이미지 생성 (폰트 문제 해결)"""
    # PIL로 텍스트 이미지 생성
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 한글 폰트 설정
    font_path = get_korean_font()
    if font_path:
        try:
            font = ImageFont.truetype(font_path, font_size)
            print(f"✅ 한글 폰트 사용: {font_path}")
        except Exception as e:
            print(f"⚠️ 폰트 로드 실패, 기본 폰트 사용: {e}")
            font = ImageFont.load_default()
    else:
        print("⚠️ 한글 폰트를 찾을 수 없음, 기본 폰트 사용")
        font = ImageFont.load_default()
    
    # 텍스트를 여러 줄로 나누기 (긴 텍스트 처리)
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= width - 100:  # 여백 고려
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                lines.append(word)
    
    if current_line:
        lines.append(current_line)
    
    # 각 줄을 그리기
    y_start = (height - len(lines) * font_size) // 2
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = y_start + i * font_size
        
        draw.text((x, y), line, fill=text_color, font=font)
    
    # PIL 이미지를 OpenCV 형식으로 변환
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return cv_img

def add_audio_with_ffmpeg(video_file, audio_file):
    """FFmpeg를 사용해 오디오 추가 (개선된 버전)"""
    print("🎵 오디오 추가 중...")
    
    # FFmpeg 경로 찾기
    ffmpeg_paths = [
        "ffmpeg",  # PATH에 있는 경우
        "C:/ProgramData/chocolatey/bin/ffmpeg.exe",  # Chocolatey 설치
        "C:/ffmpeg/bin/ffmpeg.exe",  # 수동 설치
    ]
    
    ffmpeg_cmd = None
    for path in ffmpeg_paths:
        try:
            result = subprocess.run([path, '-version'], capture_output=True, check=True)
            ffmpeg_cmd = path
            print(f"✅ FFmpeg 발견: {path}")
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    if not ffmpeg_cmd:
        print("❌ FFmpeg를 찾을 수 없음")
        return False
    
    # 임시 파일명
    temp_file = video_file.replace('.mp4', '_with_audio.mp4')
    
    # FFmpeg 명령어로 오디오 추가
    cmd = [
        ffmpeg_cmd, '-y',
        '-i', video_file,
        '-i', audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-shortest',
        temp_file
    ]
    
    try:
        print("🔄 FFmpeg 실행 중...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # 원본 파일을 임시 파일로 교체
        if os.path.exists(temp_file):
            os.replace(temp_file, video_file)
            print("✅ 오디오 추가 완료")
            return True
        else:
            print("❌ 임시 파일이 생성되지 않음")
            return False
        
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg 실행 실패: {e}")
        print(f"stderr: {e.stderr}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False

def create_improved_video():
    """개선된 영상 생성"""
    print("🎬 개선된 영상 생성 시작...")
    
    try:
        # 샘플 콘텐츠 로드
        content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 오디오 파일 확인
        audio_file = "maro_sample_content/narration.mp3"
        if not os.path.exists(audio_file):
            print(f"❌ 오디오 파일을 찾을 수 없습니다: {audio_file}")
            return False
        
        # 비디오 설정
        width, height = 1920, 1080
        fps = 24
        
        # 비디오 라이터 생성
        output_file = "maro_sample_content/maro_fixed_video.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
        
        # 제목 프레임 (3초)
        print("📝 제목 프레임 생성...")
        title_img = create_text_image_korean(
            content['title'], 
            width, height, 
            font_size=70, 
            bg_color=(255, 248, 240), 
            text_color=(44, 62, 80)
        )
        
        for i in range(3 * fps):  # 3초
            out.write(title_img)
        
        # 콘텐츠 프레임들 (각 4초씩)
        content_lines = content['content'].split('\n\n')
        print(f"📝 콘텐츠 프레임 생성 ({len(content_lines)}개)...")
        
        for idx, line in enumerate(content_lines):
            if line.strip():
                print(f"  - 프레임 {idx+1}: {line.strip()[:30]}...")
                line_img = create_text_image_korean(
                    line.strip(),
                    width, height,
                    font_size=50,
                    bg_color=(255, 248, 240),
                    text_color=(52, 73, 94)
                )
                
                for i in range(4 * fps):  # 4초
                    out.write(line_img)
        
        # 마무리 프레임 (3초)
        print("📝 마무리 프레임 생성...")
        outro_text = "당신은 혼자가 아닙니다.\n\n구독과 좋아요 부탁드려요!"
        outro_img = create_text_image_korean(
            outro_text,
            width, height,
            font_size=60,
            bg_color=(255, 248, 240),
            text_color=(44, 62, 80)
        )
        
        for i in range(3 * fps):  # 3초
            out.write(outro_img)
        
        out.release()
        
        print(f"✅ 영상 생성 완료: {output_file}")
        
        # 오디오 추가
        if add_audio_with_ffmpeg(output_file, audio_file):
            print("✅ 오디오 추가 완료!")
        else:
            print("⚠️ 영상은 생성되었지만 오디오 추가 실패")
        
        return True
        
    except Exception as e:
        print(f"❌ 영상 생성 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_simple_video_without_ffmpeg():
    """FFmpeg 없이 간단한 영상 생성"""
    print("🎬 FFmpeg 없이 간단한 영상 생성...")
    
    try:
        # 샘플 콘텐츠 로드
        content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 비디오 설정
        width, height = 1920, 1080
        fps = 24
        
        # 비디오 라이터 생성
        output_file = "maro_sample_content/maro_simple_video.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
        
        # 제목 프레임
        title_img = create_text_image_korean(
            content['title'], 
            width, height, 
            font_size=70, 
            bg_color=(255, 248, 240), 
            text_color=(44, 62, 80)
        )
        
        for i in range(3 * fps):
            out.write(title_img)
        
        # 콘텐츠 프레임들
        content_lines = content['content'].split('\n\n')
        for line in content_lines:
            if line.strip():
                line_img = create_text_image_korean(
                    line.strip(),
                    width, height,
                    font_size=50,
                    bg_color=(255, 248, 240),
                    text_color=(52, 73, 94)
                )
                
                for i in range(4 * fps):
                    out.write(line_img)
        
        # 마무리 프레임
        outro_img = create_text_image_korean(
            "당신은 혼자가 아닙니다.",
            width, height,
            font_size=60,
            bg_color=(255, 248, 240),
            text_color=(44, 62, 80)
        )
        
        for i in range(3 * fps):
            out.write(outro_img)
        
        out.release()
        
        print(f"✅ 간단한 영상 생성 완료: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ 간단한 영상 생성 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 maro 채널 영상 생성기 (수정 버전)")
    print("=" * 60)
    
    # 한글 폰트 확인
    font_path = get_korean_font()
    if font_path:
        print(f"✅ 한글 폰트 발견: {font_path}")
    else:
        print("⚠️ 한글 폰트를 찾을 수 없음 - 기본 폰트 사용")
    
    # 개선된 영상 생성 시도
    print("\n🎬 개선된 영상 생성 시도...")
    if create_improved_video():
        print("✅ 개선된 영상 생성 완료!")
        return
    
    # 간단한 영상 생성 시도
    print("\n🎬 간단한 영상 생성 시도...")
    if create_simple_video_without_ffmpeg():
        print("✅ 간단한 영상 생성 완료!")
        return
    
    print("❌ 모든 영상 생성 방법 실패")

if __name__ == "__main__":
    main()
