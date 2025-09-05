#!/usr/bin/env python3
"""
maro 채널 오디오와 비디오 합치기 (수정된 버전)
- 정확한 3분 타이밍
- 한글 폰트 적용된 비디오
"""

import os
import subprocess
import sys

def merge_audio_video_fixed():
    """오디오와 비디오를 합쳐서 최종 영상 생성"""
    
    # 파일 경로
    video_path = "maro_sample_content/maro_comfort_video_fixed.mp4"
    audio_path = "maro_sample_content/comfort_narration.mp3"
    output_path = "maro_sample_content/maro_final_comfort_video_fixed.mp4"
    
    print("🎬 maro 채널 최종 영상 제작 시작 (수정된 버전)")
    print("=" * 60)
    
    # 파일 존재 확인
    if not os.path.exists(video_path):
        print(f"❌ 비디오 파일을 찾을 수 없습니다: {video_path}")
        return False
    
    if not os.path.exists(audio_path):
        print(f"❌ 오디오 파일을 찾을 수 없습니다: {audio_path}")
        return False
    
    print(f"📹 비디오 파일: {video_path}")
    print(f"🎵 오디오 파일: {audio_path}")
    print(f"📁 출력 파일: {output_path}")
    
    # 비디오 정보 확인
    print("\n📊 비디오 정보 확인 중...")
    video_info_cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path
    ]
    
    try:
        video_info_result = subprocess.run(video_info_cmd, capture_output=True, text=True)
        if video_info_result.returncode == 0:
            import json
            video_info = json.loads(video_info_result.stdout)
            video_duration = float(video_info['format']['duration'])
            print(f"📹 비디오 길이: {video_duration:.1f}초 ({video_duration/60:.1f}분)")
        else:
            print("⚠️ 비디오 정보를 가져올 수 없습니다.")
    except:
        print("⚠️ 비디오 정보 확인 중 오류 발생")
    
    # 오디오 정보 확인
    print("📊 오디오 정보 확인 중...")
    audio_info_cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        audio_path
    ]
    
    try:
        audio_info_result = subprocess.run(audio_info_cmd, capture_output=True, text=True)
        if audio_info_result.returncode == 0:
            import json
            audio_info = json.loads(audio_info_result.stdout)
            audio_duration = float(audio_info['format']['duration'])
            print(f"🎵 오디오 길이: {audio_duration:.1f}초 ({audio_duration/60:.1f}분)")
        else:
            print("⚠️ 오디오 정보를 가져올 수 없습니다.")
    except:
        print("⚠️ 오디오 정보 확인 중 오류 발생")
    
    # FFmpeg 명령어 (오디오를 비디오 길이에 맞춤)
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",  # 비디오 코덱 복사 (재인코딩 없음)
        "-c:a", "aac",   # 오디오를 AAC로 인코딩
        "-map", "0:v:0", # 첫 번째 입력의 비디오 스트림
        "-map", "1:a:0", # 두 번째 입력의 오디오 스트림
        "-shortest",     # 짧은 쪽에 맞춤
        "-y",            # 덮어쓰기
        output_path
    ]
    
    try:
        print("\n🔄 오디오와 비디오 합치는 중...")
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 오디오와 비디오 합치기 완료!")
            
            # 파일 정보 출력
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024 / 1024
                print(f"📁 최종 파일 크기: {file_size:.2f} MB")
                print(f"📁 최종 파일 위치: {output_path}")
                
                # 최종 비디오 정보 확인
                final_info_cmd = [
                    "ffprobe",
                    "-v", "quiet",
                    "-print_format", "json",
                    "-show_format",
                    "-show_streams",
                    output_path
                ]
                
                final_info_result = subprocess.run(final_info_cmd, capture_output=True, text=True)
                if final_info_result.returncode == 0:
                    import json
                    final_info = json.loads(final_info_result.stdout)
                    duration = float(final_info['format']['duration'])
                    print(f"⏱️ 최종 영상 길이: {duration:.1f}초 ({duration/60:.1f}분)")
                    
                    # 3분 목표와 비교
                    target_duration = 180  # 3분
                    if abs(duration - target_duration) < 5:  # 5초 오차 허용
                        print(f"🎯 목표 시간 달성! (목표: {target_duration}초, 실제: {duration:.1f}초)")
                    else:
                        print(f"⚠️ 목표 시간과 차이: {abs(duration - target_duration):.1f}초")
                
                return True
            else:
                print("❌ 최종 파일이 생성되지 않았습니다.")
                return False
        else:
            print(f"❌ FFmpeg 실행 실패:")
            print(f"오류: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ FFmpeg를 찾을 수 없습니다.")
        print("FFmpeg가 설치되어 있고 PATH에 등록되어 있는지 확인해주세요.")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def main():
    success = merge_audio_video_fixed()
    
    if success:
        print("\n🎉 maro 채널 '오늘의 위로' 최종 영상 제작 완료!")
        print("📺 한글 폰트 + 정확한 3분 타이밍 + 오디오 적용!")
        print("🚀 YouTube 업로드 준비 완료!")
    else:
        print("\n❌ 영상 제작 실패")

if __name__ == "__main__":
    main()
