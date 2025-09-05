#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 영상 생성기 - 대안적 방법
PIL 폰트 문제를 완전히 우회하는 방법
"""

import os
import json
import cv2
import numpy as np
import subprocess
import sys

def create_video_with_cv2_only():
    """OpenCV만 사용한 영상 생성 (PIL 없이)"""
    print("🎬 OpenCV만 사용한 영상 생성...")
    
    try:
        # 샘플 콘텐츠 로드
        content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 비디오 설정
        width, height = 1920, 1080
        fps = 24
        
        # 비디오 라이터 생성
        output_file = "maro_sample_content/maro_cv2_only.mp4"
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
        
        # 제목 텍스트 (영문으로)
        title_text = "Today's Comfort: Self-Esteem"
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
            "You are not alone.",
            "You are doing great.",
            "Take care of yourself.",
            "Tomorrow will be better."
        ]
        
        print(f"📝 콘텐츠 프레임 생성 ({len(content_texts)}개)...")
        
        for idx, text in enumerate(content_texts):
            print(f"  - 프레임 {idx+1}: {text}")
            line_img = np.full((height, width, 3), bg_color, dtype=np.uint8)
            
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            x = (width - text_size[0]) // 2
            y = height // 2
            
            cv2.putText(line_img, text, (x, y), font, font_scale, color, thickness)
            
            for i in range(4 * fps):
                out.write(line_img)
        
        # 마무리 프레임
        print("📝 마무리 프레임 생성...")
        outro_img = np.full((height, width, 3), bg_color, dtype=np.uint8)
        outro_text = "You are not alone."
        
        text_size = cv2.getTextSize(outro_text, font, font_scale, thickness)[0]
        x = (width - text_size[0]) // 2
        y = height // 2
        
        cv2.putText(outro_img, outro_text, (x, y), font, font_scale, color, thickness)
        
        for i in range(3 * fps):
            out.write(outro_img)
        
        out.release()
        
        print(f"✅ OpenCV만 사용한 영상 생성 완료: {output_file}")
        
        # 오디오 추가
        audio_file = "maro_sample_content/narration.mp3"
        if os.path.exists(audio_file):
            add_audio_to_video(output_file, audio_file)
        
        return True
        
    except Exception as e:
        print(f"❌ OpenCV만 사용한 영상 생성 실패: {e}")
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

def create_video_with_ffmpeg_text():
    """FFmpeg의 drawtext 필터를 사용한 영상 생성"""
    print("🎬 FFmpeg drawtext를 사용한 영상 생성...")
    
    try:
        # 샘플 콘텐츠 로드
        content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
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
        output_file = "maro_sample_content/maro_ffmpeg_text.mp4"
        
        # FFmpeg 명령어로 텍스트가 포함된 영상 생성
        cmd = [
            ffmpeg_path, '-y',
            '-f', 'lavfi', '-i', 'color=c=0xFFF8F0:size=1920x1080:duration=35',
            '-i', audio_file,
            '-vf', 'drawtext=text="Today\'s Comfort: Self-Esteem":fontsize=60:fontcolor=0x2C3E50:x=(w-text_w)/2:y=(h-text_h)/2:enable=\'between(t,0,3)\'',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-shortest',
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ FFmpeg 텍스트 영상 생성 완료: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ FFmpeg 텍스트 영상 생성 실패: {e}")
            return False
        
    except Exception as e:
        print(f"❌ FFmpeg 텍스트 영상 생성 실패: {e}")
        return False

def create_video_with_subtitles_only():
    """자막만 사용한 영상 생성"""
    print("🎬 자막만 사용한 영상 생성...")
    
    try:
        # 샘플 콘텐츠 로드
        content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 자막 파일 생성
        subtitle_file = "maro_sample_content/subtitles_english.srt"
        with open(subtitle_file, 'w', encoding='utf-8') as f:
            f.write("1\n")
            f.write("00:00:00,000 --> 00:00:03,000\n")
            f.write("Today's Comfort: Self-Esteem\n\n")
            
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
            
            start_time = 3
            for i, text in enumerate(content_texts):
                end_time = start_time + 4
                f.write(f"{i+2}\n")
                f.write(f"00:00:{start_time:02d},000 --> 00:00:{end_time:02d},000\n")
                f.write(f"{text}\n\n")
                start_time = end_time
            
            # 마무리 자막
            f.write(f"{len(content_texts)+2}\n")
            f.write(f"00:00:{start_time:02d},000 --> 00:00:{start_time+3:02d},000\n")
            f.write("You are not alone.\n\n")
        
        print(f"✅ 영문 자막 파일 생성: {subtitle_file}")
        
        # FFmpeg로 자막이 포함된 영상 생성
        ffmpeg_path = "ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
        if not os.path.exists(ffmpeg_path):
            print("❌ FFmpeg를 찾을 수 없음")
            return False
        
        # 단색 배경 영상 생성
        output_file = "maro_sample_content/maro_subtitles_only.mp4"
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
            print(f"✅ 자막만 사용한 영상 생성 완료: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 자막만 사용한 영상 생성 실패: {e}")
            return False
        
    except Exception as e:
        print(f"❌ 자막만 사용한 영상 생성 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("🚀 maro 채널 영상 생성기 (대안적 방법)")
    print("=" * 60)
    
    # 방법 1: OpenCV만 사용
    print("\n🎬 OpenCV만 사용한 영상 생성 시도...")
    if create_video_with_cv2_only():
        print("✅ OpenCV만 사용한 영상 생성 완료!")
        return
    
    # 방법 2: FFmpeg drawtext 사용
    print("\n🎬 FFmpeg drawtext로 영상 생성 시도...")
    if create_video_with_ffmpeg_text():
        print("✅ FFmpeg drawtext 영상 생성 완료!")
        return
    
    # 방법 3: 자막만 사용
    print("\n🎬 자막만 사용한 영상 생성 시도...")
    if create_video_with_subtitles_only():
        print("✅ 자막만 사용한 영상 생성 완료!")
        return
    
    print("❌ 모든 영상 생성 방법 실패")

if __name__ == "__main__":
    main()
