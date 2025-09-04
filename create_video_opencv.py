#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 영상 생성기 - OpenCV 버전
MoviePy 대신 OpenCV와 PIL을 사용한 영상 생성
"""

import os
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess
import sys

def create_text_image(text, width=1920, height=200, font_size=60, bg_color=(255, 248, 240), text_color=(44, 62, 80)):
    """텍스트 이미지 생성"""
    # PIL로 텍스트 이미지 생성
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 폰트 설정 (시스템 기본 폰트 사용)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # 텍스트 중앙 정렬
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, fill=text_color, font=font)
    
    # PIL 이미지를 OpenCV 형식으로 변환
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return cv_img

def create_video_with_opencv():
    """OpenCV를 사용한 영상 생성"""
    print("🎬 OpenCV로 영상 생성 시작...")
    
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
        duration = 30  # 30초 영상
        
        # 비디오 라이터 생성
        output_file = "maro_sample_content/maro_sample_video.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
        
        # 배경 색상 (따뜻한 크림색)
        bg_color = (240, 248, 255)  # BGR 형식
        
        # 프레임 생성
        total_frames = duration * fps
        
        # 제목 프레임 (3초)
        title_frames = 3 * fps
        title_img = create_text_image(
            content['title'], 
            width, height, 
            font_size=60, 
            bg_color=(255, 248, 240), 
            text_color=(44, 62, 80)
        )
        
        for i in range(title_frames):
            out.write(title_img)
        
        # 콘텐츠 프레임들
        content_lines = content['content'].split('\n\n')
        frames_per_line = (total_frames - title_frames) // len(content_lines)
        
        for line in content_lines:
            if line.strip():
                line_img = create_text_image(
                    line.strip(),
                    width, height,
                    font_size=40,
                    bg_color=(255, 248, 240),
                    text_color=(52, 73, 94)
                )
                
                for i in range(frames_per_line):
                    out.write(line_img)
        
        # 비디오 라이터 해제
        out.release()
        
        print(f"✅ OpenCV 영상 생성 완료: {output_file}")
        
        # 오디오 추가 (FFmpeg 사용)
        if add_audio_to_video(output_file, audio_file):
            print("✅ 오디오 추가 완료!")
            return True
        else:
            print("⚠️ 영상은 생성되었지만 오디오 추가 실패")
            return True
            
    except Exception as e:
        print(f"❌ OpenCV 영상 생성 실패: {e}")
        return False

def add_audio_to_video(video_file, audio_file):
    """FFmpeg를 사용해 오디오 추가"""
    print("🎵 오디오 추가 중...")
    
    # FFmpeg 설치 확인
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg가 설치되지 않음 - 오디오 없이 영상만 생성됨")
        return False
    
    # 임시 파일명
    temp_file = video_file.replace('.mp4', '_temp.mp4')
    
    # FFmpeg 명령어로 오디오 추가
    cmd = [
        'ffmpeg', '-y',
        '-i', video_file,
        '-i', audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-shortest',
        temp_file
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        
        # 원본 파일을 임시 파일로 교체
        os.replace(temp_file, video_file)
        print("✅ 오디오 추가 완료")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 오디오 추가 실패: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False

def create_simple_slideshow():
    """간단한 슬라이드쇼 영상 생성"""
    print("🎬 간단한 슬라이드쇼 영상 생성...")
    
    try:
        # 샘플 콘텐츠 로드
        content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 비디오 설정
        width, height = 1920, 1080
        fps = 24
        
        # 비디오 라이터 생성
        output_file = "maro_sample_content/maro_slideshow.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
        
        # 배경 색상
        bg_color = (240, 248, 255)  # BGR 형식
        
        # 제목 슬라이드 (3초)
        title_img = create_text_image(
            content['title'], 
            width, height, 
            font_size=60, 
            bg_color=(255, 248, 240), 
            text_color=(44, 62, 80)
        )
        
        for i in range(3 * fps):  # 3초
            out.write(title_img)
        
        # 콘텐츠 슬라이드들 (각 3초씩)
        content_lines = content['content'].split('\n\n')
        for line in content_lines:
            if line.strip():
                line_img = create_text_image(
                    line.strip(),
                    width, height,
                    font_size=40,
                    bg_color=(255, 248, 240),
                    text_color=(52, 73, 94)
                )
                
                for i in range(3 * fps):  # 3초
                    out.write(line_img)
        
        # 마무리 슬라이드 (3초)
        outro_img = create_text_image(
            "당신은 혼자가 아닙니다.\n구독과 좋아요 부탁드려요!",
            width, height,
            font_size=50,
            bg_color=(255, 248, 240),
            text_color=(44, 62, 80)
        )
        
        for i in range(3 * fps):  # 3초
            out.write(outro_img)
        
        out.release()
        
        print(f"✅ 슬라이드쇼 영상 생성 완료: {output_file}")
        
        # 오디오 추가 시도
        audio_file = "maro_sample_content/narration.mp3"
        if os.path.exists(audio_file):
            add_audio_to_video(output_file, audio_file)
        
        return True
        
    except Exception as e:
        print(f"❌ 슬라이드쇼 생성 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 maro 채널 OpenCV 영상 생성기 시작")
    print("=" * 60)
    
    # OpenCV 설치 확인
    try:
        import cv2
        print(f"✅ OpenCV 설치 확인: {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV가 설치되지 않음")
        return
    
    # PIL 설치 확인
    try:
        from PIL import Image, ImageDraw, ImageFont
        print("✅ PIL 설치 확인")
    except ImportError:
        print("❌ PIL이 설치되지 않음")
        return
    
    # 영상 생성 시도
    print("\n🎬 영상 생성 시도...")
    
    # 방법 1: OpenCV로 영상 생성
    if create_video_with_opencv():
        print("✅ 영상 생성 완료!")
        return
    
    # 방법 2: 간단한 슬라이드쇼 생성
    if create_simple_slideshow():
        print("✅ 슬라이드쇼 영상 생성 완료!")
        return
    
    print("❌ 모든 영상 생성 방법 실패")

if __name__ == "__main__":
    main()
