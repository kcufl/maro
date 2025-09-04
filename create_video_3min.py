#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 영상 생성기 - 3분 정확한 시간 맞춤
3분 구성안에 맞춰서 정확한 시간으로 영상 생성
"""

import os
import json
import cv2
import numpy as np
import subprocess
import sys

def create_3min_video():
    """3분 정확한 시간으로 영상 생성"""
    print("🎬 3분 정확한 시간으로 영상 생성...")
    
    try:
        # 샘플 콘텐츠 로드
        content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 비디오 설정
        width, height = 1920, 1080
        fps = 24
        
        # 비디오 라이터 생성
        output_file = "maro_sample_content/maro_3min_video.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
        
        # 배경 색상
        bg_color = (240, 248, 255)  # BGR 형식
        
        # OpenCV putText 설정
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2.0
        color = (80, 62, 44)  # BGR 형식
        thickness = 3
        
        # 1. 인트로 (15초) - 0:00-0:15
        print("📝 인트로 프레임 생성 (15초)...")
        intro_img = np.full((height, width, 3), bg_color, dtype=np.uint8)
        
        # 제목 텍스트
        title_text = "Today's Comfort: Self-Esteem"
        text_size = cv2.getTextSize(title_text, font, font_scale, thickness)[0]
        x = (width - text_size[0]) // 2
        y = height // 2
        
        cv2.putText(intro_img, title_text, (x, y), font, font_scale, color, thickness)
        
        # 15초 = 15 * 24 = 360 프레임
        for i in range(15 * fps):
            out.write(intro_img)
        
        # 2. 본문 (130초) - 0:15-2:25
        print("📝 본문 프레임 생성 (130초)...")
        
        # 본문 텍스트들 (8개)
        content_texts = [
            "You did well today.",
            "It's okay to take a break.",
            "You are stronger than you think.",
            "Small steps matter.",
            "You are not alone.",
            "You are doing great.",
            "Take care of yourself.",
            "Tomorrow will be better."
        ]
        
        # 각 텍스트당 130초 / 8개 = 16.25초씩
        frames_per_text = int(130 * fps / len(content_texts))
        
        for idx, text in enumerate(content_texts):
            print(f"  - 프레임 {idx+1}: {text} ({frames_per_text/fps:.1f}초)")
            line_img = np.full((height, width, 3), bg_color, dtype=np.uint8)
            
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            x = (width - text_size[0]) // 2
            y = height // 2
            
            cv2.putText(line_img, text, (x, y), font, font_scale, color, thickness)
            
            for i in range(frames_per_text):
                out.write(line_img)
        
        # 3. 아웃로 (35초) - 2:25-3:00
        print("📝 아웃로 프레임 생성 (35초)...")
        outro_img = np.full((height, width, 3), bg_color, dtype=np.uint8)
        
        # 아웃로 텍스트
        outro_text = "You are not alone."
        text_size = cv2.getTextSize(outro_text, font, font_scale, thickness)[0]
        x = (width - text_size[0]) // 2
        y = height // 2
        
        cv2.putText(outro_img, outro_text, (x, y), font, font_scale, color, thickness)
        
        # 35초 = 35 * 24 = 840 프레임
        for i in range(35 * fps):
            out.write(outro_img)
        
        out.release()
        
        print(f"✅ 3분 영상 생성 완료: {output_file}")
        print(f"📊 총 시간: {15 + 130 + 35}초 = 3분")
        
        # 오디오 추가
        audio_file = "maro_sample_content/narration.mp3"
        if os.path.exists(audio_file):
            add_audio_to_video(output_file, audio_file)
        
        return True
        
    except Exception as e:
        print(f"❌ 3분 영상 생성 실패: {e}")
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

def create_3min_video_with_ffmpeg():
    """FFmpeg로 3분 영상 생성"""
    print("🎬 FFmpeg로 3분 영상 생성...")
    
    try:
        # FFmpeg 경로
        ffmpeg_path = "ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
        if not os.path.exists(ffmpeg_path):
            print("❌ FFmpeg를 찾을 수 없음")
            return False
        
        # 오디오 파일
        audio_file = "maro_sample_content/narration.mp3"
        if not os.path.exists(audio_file):
            print("❌ 오디오 파일을 찾을 수 없음")
            return False
        
        # 출력 파일
        output_file = "maro_sample_content/maro_3min_ffmpeg.mp4"
        
        # FFmpeg 명령어로 3분 영상 생성
        cmd = [
            ffmpeg_path, '-y',
            '-f', 'lavfi', '-i', 'color=c=0xFFF8F0:size=1920x1080:duration=180',  # 3분 = 180초
            '-i', audio_file,
            '-vf', 'drawtext=text="Today\'s Comfort: Self-Esteem":fontsize=60:fontcolor=0x2C3E50:x=(w-text_w)/2:y=(h-text_h)/2:enable=\'between(t,0,15)\'',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-shortest',
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ FFmpeg 3분 영상 생성 완료: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ FFmpeg 3분 영상 생성 실패: {e}")
            return False
        
    except Exception as e:
        print(f"❌ FFmpeg 3분 영상 생성 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 maro 채널 3분 영상 생성기")
    print("=" * 60)
    
    # 방법 1: OpenCV로 3분 영상 생성
    print("\n🎬 OpenCV로 3분 영상 생성 시도...")
    if create_3min_video():
        print("✅ OpenCV 3분 영상 생성 완료!")
        return
    
    # 방법 2: FFmpeg로 3분 영상 생성
    print("\n🎬 FFmpeg로 3분 영상 생성 시도...")
    if create_3min_video_with_ffmpeg():
        print("✅ FFmpeg 3분 영상 생성 완료!")
        return
    
    print("❌ 모든 3분 영상 생성 방법 실패")

if __name__ == "__main__":
    main()
