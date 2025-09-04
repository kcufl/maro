#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 영상 생성기 - 최종 버전
MoviePy 문제 해결을 위한 대안적 접근
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def check_moviepy_installation():
    """MoviePy 설치 상태 확인"""
    print("🔍 MoviePy 설치 상태 확인 중...")
    
    try:
        import moviepy
        print(f"✅ MoviePy 기본 모듈: {moviepy.__version__}")
        
        # editor 모듈 확인
        try:
            from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
            print("✅ MoviePy editor 모듈 import 성공!")
            return True
        except ImportError as e:
            print(f"❌ MoviePy editor import 실패: {e}")
            return False
            
    except ImportError:
        print("❌ MoviePy가 설치되지 않음")
        return False

def install_moviepy():
    """MoviePy 재설치"""
    print("📦 MoviePy 재설치 중...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "moviepy", "-y"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "moviepy"], check=True)
        print("✅ MoviePy 재설치 완료")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ MoviePy 설치 실패: {e}")
        return False

def create_simple_video_with_moviepy():
    """MoviePy를 사용한 간단한 영상 생성"""
    print("🎬 MoviePy로 영상 생성 시작...")
    
    try:
        from moviepy.editor import (
            VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip,
            ColorClip, concatenate_videoclips
        )
        
        # 샘플 콘텐츠 로드
        content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 오디오 파일 확인
        audio_file = "maro_sample_content/narration.mp3"
        if not os.path.exists(audio_file):
            print(f"❌ 오디오 파일을 찾을 수 없습니다: {audio_file}")
            return False
        
        # 오디오 클립 생성
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration
        print(f"🎵 오디오 길이: {duration:.2f}초")
        
        # 배경 비디오 클립 생성 (단색)
        background = ColorClip(size=(1920, 1080), color=(255, 248, 240), duration=duration)
        
        # 텍스트 클립들 생성
        text_clips = []
        
        # 제목 텍스트
        title_clip = TextClip(
            content['title'],
            fontsize=60,
            color='#2C3E50',
            font='Arial-Bold',
            method='caption',
            size=(1600, 200)
        ).set_position('center').set_start(0).set_duration(3)
        
        text_clips.append(title_clip)
        
        # 콘텐츠 텍스트 (여러 부분으로 나누기)
        content_lines = content['content'].split('\n\n')
        y_position = 400
        
        for i, line in enumerate(content_lines):
            if line.strip():
                text_clip = TextClip(
                    line.strip(),
                    fontsize=40,
                    color='#34495E',
                    font='Arial',
                    method='caption',
                    size=(1600, 100)
                ).set_position(('center', y_position)).set_start(3 + i * 2).set_duration(2)
                
                text_clips.append(text_clip)
                y_position += 120
        
        # 모든 클립 합성
        final_video = CompositeVideoClip([background] + text_clips).set_audio(audio_clip)
        
        # 영상 저장
        output_file = "maro_sample_content/maro_sample_video.mp4"
        final_video.write_videofile(
            output_file,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        print(f"✅ 영상 생성 완료: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ 영상 생성 실패: {e}")
        return False

def create_video_with_ffmpeg():
    """FFmpeg를 사용한 영상 생성 (MoviePy 대안)"""
    print("🎬 FFmpeg로 영상 생성 시도...")
    
    # FFmpeg 설치 확인
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg 설치 확인됨")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg가 설치되지 않음")
        return False
    
    # 샘플 콘텐츠 로드
    content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
    with open(content_file, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    # 오디오 파일 확인
    audio_file = "maro_sample_content/narration.mp3"
    if not os.path.exists(audio_file):
        print(f"❌ 오디오 파일을 찾을 수 없습니다: {audio_file}")
        return False
    
    # 텍스트 파일 생성 (자막용)
    subtitle_file = "maro_sample_content/subtitles.srt"
    with open(subtitle_file, 'w', encoding='utf-8') as f:
        f.write("1\n")
        f.write("00:00:00,000 --> 00:00:03,000\n")
        f.write(f"{content['title']}\n\n")
        
        content_lines = content['content'].split('\n\n')
        start_time = 3
        for i, line in enumerate(content_lines):
            if line.strip():
                end_time = start_time + 2
                f.write(f"{i+2}\n")
                f.write(f"00:00:{start_time:02d},000 --> 00:00:{end_time:02d},000\n")
                f.write(f"{line.strip()}\n\n")
                start_time = end_time
    
    # FFmpeg 명령어로 영상 생성
    output_file = "maro_sample_content/maro_sample_video.mp4"
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=0xFFF8F0:size=1920x1080:duration=30',
        '-i', audio_file,
        '-vf', f'subtitles={subtitle_file}:force_style=\'FontSize=40,PrimaryColour=&H000000FF\'',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-shortest',
        output_file
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ FFmpeg 영상 생성 완료: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg 영상 생성 실패: {e}")
        return False

def create_video_preparation_files():
    """영상 제작을 위한 준비 파일들 생성"""
    print("📝 영상 제작 준비 파일들 생성...")
    
    # 샘플 콘텐츠 로드
    content_file = "maro_sample_content/20250904/daily_comfort_자존감을_높이는_방법.json"
    with open(content_file, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    # 영상 제작 가이드 생성
    production_guide = {
        "video_info": {
            "title": content['title'],
            "duration": "3분",
            "theme": content['theme'],
            "date": content['date']
        },
        "audio_files": {
            "narration": "maro_sample_content/narration.mp3",
            "bgm_suggestion": content['production_notes']['bgm_suggestion']
        },
        "visual_elements": content['visual_elements'],
        "timing_breakdown": content['timing'],
        "production_notes": content['production_notes'],
        "manual_creation_steps": [
            "1. 배경 이미지/비디오 준비 (1920x1080)",
            "2. 제목 텍스트 오버레이 (0-3초)",
            "3. 콘텐츠 텍스트 오버레이 (3초부터)",
            "4. 자막 추가",
            "5. BGM 추가 (나레이션과 믹싱)",
            "6. 최종 렌더링"
        ],
        "software_alternatives": [
            "Adobe Premiere Pro",
            "DaVinci Resolve (무료)",
            "OpenShot (무료)",
            "Shotcut (무료)",
            "FFmpeg (명령줄)"
        ]
    }
    
    # 가이드 파일 저장
    guide_file = "maro_sample_content/video_production_guide.json"
    with open(guide_file, 'w', encoding='utf-8') as f:
        json.dump(production_guide, f, ensure_ascii=False, indent=2)
    
    # 자막 파일 생성
    subtitle_file = "maro_sample_content/subtitles.srt"
    with open(subtitle_file, 'w', encoding='utf-8') as f:
        f.write("1\n")
        f.write("00:00:00,000 --> 00:00:03,000\n")
        f.write(f"{content['title']}\n\n")
        
        content_lines = content['content'].split('\n\n')
        start_time = 3
        for i, line in enumerate(content_lines):
            if line.strip():
                end_time = start_time + 2
                f.write(f"{i+2}\n")
                f.write(f"00:00:{start_time:02d},000 --> 00:00:{end_time:02d},000\n")
                f.write(f"{line.strip()}\n\n")
                start_time = end_time
    
    print(f"✅ 제작 가이드 생성: {guide_file}")
    print(f"✅ 자막 파일 생성: {subtitle_file}")
    
    return True

def main():
    """메인 실행 함수"""
    print("🚀 maro 채널 영상 생성기 시작")
    print("=" * 60)
    
    # 1. MoviePy 설치 상태 확인
    if check_moviepy_installation():
        print("🎬 MoviePy로 영상 생성 시도...")
        if create_simple_video_with_moviepy():
            print("✅ 영상 생성 완료!")
            return
    
    # 2. MoviePy 재설치 시도
    print("🔄 MoviePy 재설치 후 재시도...")
    if install_moviepy():
        if check_moviepy_installation():
            if create_simple_video_with_moviepy():
                print("✅ 영상 생성 완료!")
                return
    
    # 3. FFmpeg 대안 시도
    print("🔄 FFmpeg로 영상 생성 시도...")
    if create_video_with_ffmpeg():
        print("✅ 영상 생성 완료!")
        return
    
    # 4. 수동 제작을 위한 준비 파일 생성
    print("📝 수동 제작을 위한 준비 파일 생성...")
    create_video_preparation_files()
    
    print("\n" + "=" * 60)
    print("⚠️  자동 영상 생성 실패")
    print("📋 수동 제작을 위한 파일들이 준비되었습니다:")
    print("   - video_production_guide.json: 제작 가이드")
    print("   - subtitles.srt: 자막 파일")
    print("   - narration.mp3: 나레이션 오디오")
    print("\n💡 권장 소프트웨어:")
    print("   - DaVinci Resolve (무료, 전문적)")
    print("   - OpenShot (무료, 간단)")
    print("   - Adobe Premiere Pro (유료)")

if __name__ == "__main__":
    main()
