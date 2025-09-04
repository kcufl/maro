#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 영상 생성기 - 폰트 다운로드 방식
한글 폰트를 직접 다운로드해서 사용
"""

import os
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess
import sys
import platform
import urllib.request

def download_korean_font():
    """한글 폰트 다운로드"""
    print("📥 한글 폰트 다운로드 중...")
    
    # 폰트 디렉토리 생성
    font_dir = "fonts"
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)
    
    # 나눔고딕 폰트 다운로드 (무료 한글 폰트)
    font_url = "https://github.com/naver/nanumfont/releases/download/VER5.0/NanumGothic.ttf"
    font_path = os.path.join(font_dir, "NanumGothic.ttf")
    
    if not os.path.exists(font_path):
        try:
            print("📥 나눔고딕 폰트 다운로드 중...")
            urllib.request.urlretrieve(font_url, font_path)
            print(f"✅ 폰트 다운로드 완료: {font_path}")
            return font_path
        except Exception as e:
            print(f"❌ 폰트 다운로드 실패: {e}")
            return None
    else:
        print(f"✅ 폰트 이미 존재: {font_path}")
        return font_path

def create_text_image_with_downloaded_font(text, width=1920, height=200, font_size=60, bg_color=(255, 248, 240), text_color=(44, 62, 80)):
    """다운로드한 폰트로 텍스트 이미지 생성"""
    # PIL로 텍스트 이미지 생성
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 폰트 설정
    font = None
    
    # 다운로드한 폰트 사용
    font_path = download_korean_font()
    if font_path and os.path.exists(font_path):
        try:
            font = ImageFont.truetype(font_path, font_size)
            print(f"✅ 다운로드한 폰트 사용: {font_path}")
        except Exception as e:
            print(f"⚠️ 다운로드한 폰트 로드 실패: {e}")
            font = None
    
    # 시스템 폰트 사용
    if not font:
        system_fonts = [
            "C:/Windows/Fonts/malgun.ttf",
            "C:/Windows/Fonts/gulim.ttc",
            "C:/Windows/Fonts/dotum.ttc",
        ]
        
        for font_path in system_fonts:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    print(f"✅ 시스템 폰트 사용: {font_path}")
                    break
                except:
                    continue
    
    # 기본 폰트 사용
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
        
        # 텍스트 그리기
        try:
            draw.text((x, y), line, fill=text_color, font=font)
        except Exception as e:
            print(f"⚠️ 텍스트 그리기 실패: {e}")
            # 폰트 없이 그리기 시도
            draw.text((x, y), line, fill=text_color)
    
    # PIL 이미지를 OpenCV 형식으로 변환
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return cv_img

def create_video_with_downloaded_font():
    """다운로드한 폰트로 영상 생성"""
    print("🎬 다운로드한 폰트로 영상 생성...")
    
    try:
        # 샘플 콘텐츠 로드
        content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 비디오 설정
        width, height = 1920, 1080
        fps = 24
        
        # 비디오 라이터 생성
        output_file = "maro_sample_content/maro_downloaded_font.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
        
        # 제목 프레임 (3초)
        print("📝 제목 프레임 생성...")
        title_img = create_text_image_with_downloaded_font(
            content['title'], 
            width, height, 
            font_size=70, 
            bg_color=(255, 248, 240), 
            text_color=(44, 62, 80)
        )
        
        if title_img is not None:
            for i in range(3 * fps):
                out.write(title_img)
        else:
            print("❌ 제목 이미지 생성 실패")
            return False
        
        # 콘텐츠 프레임들
        content_lines = content['content'].split('\n\n')
        print(f"📝 콘텐츠 프레임 생성 ({len(content_lines)}개)...")
        
        for idx, line in enumerate(content_lines):
            if line.strip():
                print(f"  - 프레임 {idx+1}: {line.strip()[:30]}...")
                line_img = create_text_image_with_downloaded_font(
                    line.strip(),
                    width, height,
                    font_size=50,
                    bg_color=(255, 248, 240),
                    text_color=(52, 73, 94)
                )
                
                if line_img is not None:
                    for i in range(4 * fps):
                        out.write(line_img)
                else:
                    print(f"❌ 프레임 {idx+1} 이미지 생성 실패")
        
        # 마무리 프레임
        print("📝 마무리 프레임 생성...")
        outro_text = "당신은 혼자가 아닙니다.\n\n구독과 좋아요 부탁드려요!"
        outro_img = create_text_image_with_downloaded_font(
            outro_text,
            width, height,
            font_size=60,
            bg_color=(255, 248, 240),
            text_color=(44, 62, 80)
        )
        
        if outro_img is not None:
            for i in range(3 * fps):
                out.write(outro_img)
        
        out.release()
        
        print(f"✅ 다운로드한 폰트 영상 생성 완료: {output_file}")
        
        # 오디오 추가
        audio_file = "maro_sample_content/narration.mp3"
        if os.path.exists(audio_file):
            add_audio_to_video(output_file, audio_file)
        
        return True
        
    except Exception as e:
        print(f"❌ 다운로드한 폰트 영상 생성 실패: {e}")
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

def create_video_with_ffmpeg_subtitles():
    """FFmpeg 자막을 사용한 영상 생성"""
    print("🎬 FFmpeg 자막을 사용한 영상 생성...")
    
    try:
        # 샘플 콘텐츠 로드
        content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 자막 파일 생성 (UTF-8 BOM 포함)
        subtitle_file = "maro_sample_content/subtitles_utf8.srt"
        with open(subtitle_file, 'w', encoding='utf-8-sig') as f:  # BOM 포함
            f.write("1\n")
            f.write("00:00:00,000 --> 00:00:03,000\n")
            f.write(f"{content['title']}\n\n")
            
            content_lines = content['content'].split('\n\n')
            start_time = 3
            for i, line in enumerate(content_lines):
                if line.strip():
                    end_time = start_time + 4
                    f.write(f"{i+2}\n")
                    f.write(f"00:00:{start_time:02d},000 --> 00:00:{end_time:02d},000\n")
                    f.write(f"{line.strip()}\n\n")
                    start_time = end_time
            
            # 마무리 자막
            f.write(f"{len(content_lines)+2}\n")
            f.write(f"00:00:{start_time:02d},000 --> 00:00:{start_time+3:02d},000\n")
            f.write("당신은 혼자가 아닙니다.\n\n")
        
        print(f"✅ UTF-8 자막 파일 생성: {subtitle_file}")
        
        # FFmpeg로 자막이 포함된 영상 생성
        ffmpeg_path = "ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
        if not os.path.exists(ffmpeg_path):
            print("❌ FFmpeg를 찾을 수 없음")
            return False
        
        # 단색 배경 영상 생성
        output_file = "maro_sample_content/maro_ffmpeg_subtitle.mp4"
        audio_file = "maro_sample_content/narration.mp3"
        
        cmd = [
            ffmpeg_path, '-y',
            '-f', 'lavfi', '-i', 'color=c=0xFFF8F0:size=1920x1080:duration=35',
            '-i', audio_file,
            '-vf', f'subtitles={subtitle_file}:force_style=\'FontSize=40,PrimaryColour=&H000000FF,OutlineColour=&HFFFFFF00,Outline=2\'',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-shortest',
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ FFmpeg 자막 영상 생성 완료: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ FFmpeg 자막 영상 생성 실패: {e}")
            return False
        
    except Exception as e:
        print(f"❌ FFmpeg 자막 영상 생성 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 maro 채널 영상 생성기 (폰트 다운로드 방식)")
    print("=" * 60)
    
    # 방법 1: 다운로드한 폰트 사용
    print("\n🎬 다운로드한 폰트로 영상 생성 시도...")
    if create_video_with_downloaded_font():
        print("✅ 다운로드한 폰트 영상 생성 완료!")
        return
    
    # 방법 2: FFmpeg 자막 사용
    print("\n🎬 FFmpeg 자막으로 영상 생성 시도...")
    if create_video_with_ffmpeg_subtitles():
        print("✅ FFmpeg 자막 영상 생성 완료!")
        return
    
    print("❌ 모든 영상 생성 방법 실패")

if __name__ == "__main__":
    main()
