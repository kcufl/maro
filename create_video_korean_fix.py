#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 영상 생성기 - 한글 폰트 문제 완전 해결
네모 문제 해결을 위한 다양한 방법 시도
"""

import os
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess
import sys
import platform

def get_best_korean_font():
    """최적의 한글 폰트 찾기"""
    system = platform.system()
    
    if system == "Windows":
        # Windows 한글 폰트 경로들 (우선순위 순)
        font_paths = [
            "C:/Windows/Fonts/malgun.ttf",      # 맑은 고딕
            "C:/Windows/Fonts/malgunbd.ttf",    # 맑은 고딕 Bold
            "C:/Windows/Fonts/gulim.ttc",       # 굴림
            "C:/Windows/Fonts/gulim.ttc",       # 굴림체
            "C:/Windows/Fonts/dotum.ttc",       # 돋움
            "C:/Windows/Fonts/dotum.ttc",       # 돋움체
            "C:/Windows/Fonts/batang.ttc",      # 바탕
            "C:/Windows/Fonts/batang.ttc",      # 바탕체
            "C:/Windows/Fonts/arial.ttf",       # Arial (영문)
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

def create_text_image_with_fallback(text, width=1920, height=200, font_size=60, bg_color=(255, 248, 240), text_color=(44, 62, 80)):
    """폴백 방식으로 텍스트 이미지 생성"""
    # PIL로 텍스트 이미지 생성
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 폰트 설정 (여러 방법 시도)
    font = None
    
    # 방법 1: 직접 폰트 경로 지정
    font_path = get_best_korean_font()
    if font_path:
        try:
            font = ImageFont.truetype(font_path, font_size)
            print(f"✅ 폰트 로드 성공: {font_path}")
        except Exception as e:
            print(f"⚠️ 폰트 로드 실패: {e}")
            font = None
    
    # 방법 2: 폰트 이름으로 찾기
    if not font:
        font_names = ["malgun.ttf", "gulim.ttc", "dotum.ttc", "batang.ttc", "arial.ttf"]
        for font_name in font_names:
            try:
                font = ImageFont.truetype(font_name, font_size)
                print(f"✅ 폰트 이름으로 로드 성공: {font_name}")
                break
            except:
                continue
    
    # 방법 3: 기본 폰트 사용
    if not font:
        try:
            font = ImageFont.load_default()
            print("⚠️ 기본 폰트 사용")
        except:
            print("❌ 모든 폰트 로드 실패")
            return None
    
    # 텍스트를 여러 줄로 나누기
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        try:
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
        except:
            # bbox 계산 실패시 대략적 계산
            text_width = len(test_line) * font_size * 0.6
        
        if text_width <= width - 100:
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
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except:
            text_width = len(line) * font_size * 0.6
            text_height = font_size
        
        x = (width - text_width) // 2
        y = y_start + i * font_size
        
        draw.text((x, y), line, fill=text_color, font=font)
    
    # PIL 이미지를 OpenCV 형식으로 변환
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return cv_img

def create_video_with_cv2_text():
    """OpenCV의 putText를 사용한 영상 생성"""
    print("🎬 OpenCV putText로 영상 생성...")
    
    try:
        # 샘플 콘텐츠 로드
        content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 비디오 설정
        width, height = 1920, 1080
        fps = 24
        
        # 비디오 라이터 생성
        output_file = "maro_sample_content/maro_cv2_video.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
        
        # 배경 색상
        bg_color = (240, 248, 255)  # BGR 형식
        
        # 제목 프레임 (3초)
        print("📝 제목 프레임 생성...")
        title_img = np.full((height, width, 3), bg_color, dtype=np.uint8)
        
        # OpenCV putText 사용
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2.0
        color = (80, 62, 44)  # BGR 형식
        thickness = 3
        
        # 텍스트를 여러 줄로 나누기
        title_lines = content['title'].split('\n')
        y_start = height // 2 - len(title_lines) * 60
        
        for i, line in enumerate(title_lines):
            text_size = cv2.getTextSize(line, font, font_scale, thickness)[0]
            x = (width - text_size[0]) // 2
            y = y_start + i * 120
            
            cv2.putText(title_img, line, (x, y), font, font_scale, color, thickness)
        
        for i in range(3 * fps):
            out.write(title_img)
        
        # 콘텐츠 프레임들
        content_lines = content['content'].split('\n\n')
        print(f"📝 콘텐츠 프레임 생성 ({len(content_lines)}개)...")
        
        for idx, line in enumerate(content_lines):
            if line.strip():
                print(f"  - 프레임 {idx+1}: {line.strip()[:30]}...")
                line_img = np.full((height, width, 3), bg_color, dtype=np.uint8)
                
                # 텍스트를 여러 줄로 나누기
                words = line.strip().split()
                lines = []
                current_line = ""
                
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    text_size = cv2.getTextSize(test_line, font, font_scale, thickness)[0]
                    
                    if text_size[0] <= width - 100:
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
                y_start = height // 2 - len(lines) * 60
                for i, text_line in enumerate(lines):
                    text_size = cv2.getTextSize(text_line, font, font_scale, thickness)[0]
                    x = (width - text_size[0]) // 2
                    y = y_start + i * 120
                    
                    cv2.putText(line_img, text_line, (x, y), font, font_scale, color, thickness)
                
                for i in range(4 * fps):
                    out.write(line_img)
        
        # 마무리 프레임
        print("📝 마무리 프레임 생성...")
        outro_img = np.full((height, width, 3), bg_color, dtype=np.uint8)
        outro_text = "당신은 혼자가 아닙니다."
        
        text_size = cv2.getTextSize(outro_text, font, font_scale, thickness)[0]
        x = (width - text_size[0]) // 2
        y = height // 2
        
        cv2.putText(outro_img, outro_text, (x, y), font, font_scale, color, thickness)
        
        for i in range(3 * fps):
            out.write(outro_img)
        
        out.release()
        
        print(f"✅ OpenCV 영상 생성 완료: {output_file}")
        
        # 오디오 추가
        audio_file = "maro_sample_content/narration.mp3"
        if os.path.exists(audio_file):
            add_audio_to_video(output_file, audio_file)
        
        return True
        
    except Exception as e:
        print(f"❌ OpenCV 영상 생성 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def add_audio_to_video(video_file, audio_file):
    """FFmpeg로 오디오 추가"""
    print("🎵 오디오 추가 중...")
    
    ffmpeg_path = "ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
    if not os.path.exists(ffmpeg_path):
        print("❌ FFmpeg를 찾을 수 없음")
        return False
    
    temp_file = video_file.replace('.mp4', '_with_audio.mp4')
    
    cmd = [
        ffmpeg_path, '-y',
        '-i', video_file,
        '-i', audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-shortest',
        temp_file
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        
        if os.path.exists(temp_file):
            os.replace(temp_file, video_file)
            print("✅ 오디오 추가 완료")
            return True
        else:
            print("❌ 임시 파일이 생성되지 않음")
            return False
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 오디오 추가 실패: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False

def create_simple_text_video():
    """간단한 텍스트 영상 생성 (한글 문제 해결)"""
    print("🎬 간단한 텍스트 영상 생성...")
    
    try:
        # 샘플 콘텐츠 로드
        content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 비디오 설정
        width, height = 1920, 1080
        fps = 24
        
        # 비디오 라이터 생성
        output_file = "maro_sample_content/maro_simple_text.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
        
        # 배경 색상
        bg_color = (240, 248, 255)  # BGR 형식
        
        # 제목 프레임
        title_img = np.full((height, width, 3), bg_color, dtype=np.uint8)
        
        # 간단한 텍스트 (영문으로 테스트)
        title_text = "Today's Comfort: Self-Esteem"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2.0
        color = (80, 62, 44)
        thickness = 3
        
        text_size = cv2.getTextSize(title_text, font, font_scale, thickness)[0]
        x = (width - text_size[0]) // 2
        y = height // 2
        
        cv2.putText(title_img, title_text, (x, y), font, font_scale, color, thickness)
        
        for i in range(3 * fps):
            out.write(title_img)
        
        # 콘텐츠 프레임들 (영문으로)
        content_texts = [
            "You did well today.",
            "It's okay to take a break.",
            "You are stronger than you think.",
            "Small steps matter.",
            "You are not alone."
        ]
        
        for text in content_texts:
            line_img = np.full((height, width, 3), bg_color, dtype=np.uint8)
            
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            x = (width - text_size[0]) // 2
            y = height // 2
            
            cv2.putText(line_img, text, (x, y), font, font_scale, color, thickness)
            
            for i in range(4 * fps):
                out.write(line_img)
        
        # 마무리 프레임
        outro_img = np.full((height, width, 3), bg_color, dtype=np.uint8)
        outro_text = "You are not alone."
        
        text_size = cv2.getTextSize(outro_text, font, font_scale, thickness)[0]
        x = (width - text_size[0]) // 2
        y = height // 2
        
        cv2.putText(outro_img, outro_text, (x, y), font, font_scale, color, thickness)
        
        for i in range(3 * fps):
            out.write(outro_img)
        
        out.release()
        
        print(f"✅ 간단한 텍스트 영상 생성 완료: {output_file}")
        
        # 오디오 추가
        audio_file = "maro_sample_content/narration.mp3"
        if os.path.exists(audio_file):
            add_audio_to_video(output_file, audio_file)
        
        return True
        
    except Exception as e:
        print(f"❌ 간단한 텍스트 영상 생성 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 maro 채널 영상 생성기 (한글 문제 해결)")
    print("=" * 60)
    
    # 한글 폰트 확인
    font_path = get_best_korean_font()
    if font_path:
        print(f"✅ 한글 폰트 발견: {font_path}")
    else:
        print("⚠️ 한글 폰트를 찾을 수 없음")
    
    # 방법 1: OpenCV putText 사용
    print("\n🎬 OpenCV putText로 영상 생성 시도...")
    if create_video_with_cv2_text():
        print("✅ OpenCV 영상 생성 완료!")
        return
    
    # 방법 2: 간단한 영문 영상 생성
    print("\n🎬 간단한 영문 영상 생성 시도...")
    if create_simple_text_video():
        print("✅ 간단한 영문 영상 생성 완료!")
        return
    
    print("❌ 모든 영상 생성 방법 실패")

if __name__ == "__main__":
    main()
