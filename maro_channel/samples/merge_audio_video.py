#!/usr/bin/env python3
"""
maro 채널 오디오와 비디오 합치기
"""

import os
import subprocess
import sys

def merge_audio_video():
    """오디오와 비디오를 합쳐서 최종 영상 생성"""
    
    # 파일 경로
    video_path = "maro_sample_content/maro_comfort_video.mp4"
    audio_path = "maro_sample_content/comfort_narration.mp3"
    output_path = "maro_sample_content/maro_final_comfort_video.mp4"
    
    print("🎬 maro 채널 최종 영상 제작 시작")
    print("=" * 50)
    
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
    
    # FFmpeg 명령어
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",  # 비디오 코덱 복사 (재인코딩 없음)
        "-c:a", "aac",   # 오디오를 AAC로 인코딩
        "-shortest",     # 짧은 쪽에 맞춤
        "-y",            # 덮어쓰기
        output_path
    ]
    
    try:
        print("🔄 오디오와 비디오 합치는 중...")
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 오디오와 비디오 합치기 완료!")
            
            # 파일 정보 출력
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024 / 1024
                print(f"📁 최종 파일 크기: {file_size:.2f} MB")
                print(f"📁 최종 파일 위치: {output_path}")
                
                # 비디오 정보 확인
                info_cmd = [
                    "ffprobe",
                    "-v", "quiet",
                    "-print_format", "json",
                    "-show_format",
                    "-show_streams",
                    output_path
                ]
                
                info_result = subprocess.run(info_cmd, capture_output=True, text=True)
                if info_result.returncode == 0:
                    import json
                    info = json.loads(info_result.stdout)
                    duration = float(info['format']['duration'])
                    print(f"⏱️ 영상 길이: {duration:.1f}초 ({duration/60:.1f}분)")
                
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
    success = merge_audio_video()
    
    if success:
        print("\n🎉 maro 채널 '오늘의 위로' 최종 영상 제작 완료!")
        print("📺 YouTube 업로드 준비 완료!")
    else:
        print("\n❌ 영상 제작 실패")

if __name__ == "__main__":
    main()
