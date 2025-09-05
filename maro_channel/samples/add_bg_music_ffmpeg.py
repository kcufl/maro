#!/usr/bin/env python3
"""
maro 채널 배경음악 추가기 (FFmpeg 버전)
- FFmpeg만 사용해서 배경음악 추가
- 잔잔하고 편안한 배경음악 생성
"""

import os
import subprocess
import numpy as np

class FFmpegBackgroundMusicAdder:
    def __init__(self):
        self.output_dir = "maro_sample_content"
        
    def create_background_music_with_ffmpeg(self):
        """FFmpeg로 배경음악 생성"""
        print("🎵 FFmpeg로 배경음악 생성 중...")
        
        bg_music_path = os.path.join(self.output_dir, "background_music.mp3")
        
        # FFmpeg 명령어로 간단한 배경음악 생성
        # 실제로는 더 복잡한 멜로디를 만들 수 있음
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "sine=frequency=440:duration=180",  # 3분간 A4 톤
            "-af", "volume=0.1,highpass=f=200,lowpass=f=800",  # 볼륨 낮춤, 필터 적용
            bg_music_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 배경음악 생성 완료: {bg_music_path}")
            return bg_music_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 배경음악 생성 실패: {e}")
            return None
    
    def create_ambient_background_music(self):
        """앰비언트 배경음악 생성"""
        print("🎵 앰비언트 배경음악 생성 중...")
        
        bg_music_path = os.path.join(self.output_dir, "ambient_bg_music.mp3")
        
        # 더 복잡한 앰비언트 사운드 생성
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "anoisesrc=duration=180:color=white:seed=1",
            "-af", "volume=0.05,highpass=f=100,lowpass=f=1000,reverb=reverberance=50",
            bg_music_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 앰비언트 배경음악 생성 완료: {bg_music_path}")
            return bg_music_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 앰비언트 배경음악 생성 실패: {e}")
            return None
    
    def merge_audio_with_background(self, tts_path, bg_music_path):
        """TTS와 배경음악 합성"""
        print("🔊 TTS와 배경음악 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "final_audio_with_bg.mp3")
        
        # FFmpeg로 오디오 합성
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,  # TTS 음성
            "-i", bg_music_path,  # 배경음악
            "-filter_complex", "[0:a]volume=1.0[voice];[1:a]volume=0.3[bg];[voice][bg]amix=inputs=2:duration=first",
            "-c:a", "aac",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 오디오 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 오디오 합성 실패: {e}")
            return None
    
    def create_final_video_with_music(self, video_path, audio_path):
        """최종 영상 생성 (배경음악 포함)"""
        print("🎬 최종 영상 생성 중...")
        
        output_path = os.path.join(self.output_dir, "maro_final_comfort_video_with_music.mp4")
        
        # FFmpeg 명령어
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 최종 영상 생성 완료: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 최종 영상 생성 실패: {e}")
            return None

def main():
    print("🎵 maro 채널 배경음악 추가 시작 (FFmpeg 버전)")
    print("=" * 60)
    
    adder = FFmpegBackgroundMusicAdder()
    
    # 파일 경로 설정
    tts_path = os.path.join(adder.output_dir, "final_comfort_narration.mp3")
    video_path = os.path.join(adder.output_dir, "final_comfort_video.mp4")
    
    # 파일 존재 확인
    if not os.path.exists(tts_path):
        print(f"❌ TTS 파일을 찾을 수 없습니다: {tts_path}")
        return
    
    if not os.path.exists(video_path):
        print(f"❌ 비디오 파일을 찾을 수 없습니다: {video_path}")
        return
    
    # 1. 앰비언트 배경음악 생성 (더 자연스러운 소리)
    bg_music_path = adder.create_ambient_background_music()
    if not bg_music_path:
        print("❌ 배경음악 생성 실패")
        return
    
    # 2. TTS와 배경음악 합성
    final_audio_path = adder.merge_audio_with_background(tts_path, bg_music_path)
    if not final_audio_path:
        print("❌ 오디오 합성 실패")
        return
    
    # 3. 최종 영상 생성
    final_video_path = adder.create_final_video_with_music(video_path, final_audio_path)
    
    if final_video_path:
        print(f"\n🎉 배경음악이 포함된 최종 영상 생성 성공!")
        print(f"파일 위치: {final_video_path}")
        print(f"파일 크기: {os.path.getsize(final_video_path) / 1024 / 1024:.2f} MB")
        print("\n🎵 배경음악 특징:")
        print("- 앰비언트 화이트 노이즈 기반")
        print("- 저주파 필터링으로 부드러운 소리")
        print("- 리버브 효과로 공간감 추가")
        print("- TTS 음성과 적절한 볼륨 밸런스")
    else:
        print("\n❌ 최종 영상 생성 실패")

if __name__ == "__main__":
    main()
