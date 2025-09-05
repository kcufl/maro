#!/usr/bin/env python3
"""
maro 채널 배경음악 추가기 (간단 버전)
- 더 간단한 FFmpeg 명령어 사용
"""

import os
import subprocess

class SimpleBGMusicAdder:
    def __init__(self):
        self.output_dir = "maro_sample_content"
        
    def create_background_music(self):
        """배경음악 생성"""
        print("🎵 배경음악 생성 중...")
        
        bg_music_path = os.path.join(self.output_dir, "bg_music.mp3")
        
        # 간단한 톤 생성
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "sine=frequency=220:duration=180",
            "-af", "volume=0.1",
            bg_music_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 배경음악 생성 완료: {bg_music_path}")
            return bg_music_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 배경음악 생성 실패: {e}")
            return None
    
    def merge_audio_simple(self, tts_path, bg_music_path):
        """간단한 오디오 합성"""
        print("🔊 오디오 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "final_audio_with_bg.mp3")
        
        # 간단한 amix 사용
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", bg_music_path,
            "-filter_complex", "amix=inputs=2:duration=first:weights=1 0.2",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 오디오 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 오디오 합성 실패: {e}")
            return None
    
    def create_final_video(self, video_path, audio_path):
        """최종 영상 생성"""
        print("🎬 최종 영상 생성 중...")
        
        output_path = os.path.join(self.output_dir, "maro_final_comfort_video_with_music.mp4")
        
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
    print("🎵 maro 채널 배경음악 추가 시작 (간단 버전)")
    print("=" * 60)
    
    adder = SimpleBGMusicAdder()
    
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
    
    # 1. 배경음악 생성
    bg_music_path = adder.create_background_music()
    if not bg_music_path:
        print("❌ 배경음악 생성 실패")
        return
    
    # 2. 오디오 합성
    final_audio_path = adder.merge_audio_simple(tts_path, bg_music_path)
    if not final_audio_path:
        print("❌ 오디오 합성 실패")
        return
    
    # 3. 최종 영상 생성
    final_video_path = adder.create_final_video(video_path, final_audio_path)
    
    if final_video_path:
        print(f"\n🎉 배경음악이 포함된 최종 영상 생성 성공!")
        print(f"파일 위치: {final_video_path}")
        print(f"파일 크기: {os.path.getsize(final_video_path) / 1024 / 1024:.2f} MB")
        print("\n🎵 배경음악 특징:")
        print("- A3 톤 (220Hz) - 잔잔하고 편안한 소리")
        print("- 낮은 볼륨으로 TTS 음성을 방해하지 않음")
        print("- 3분간 지속되는 부드러운 배경음악")
    else:
        print("\n❌ 최종 영상 생성 실패")

if __name__ == "__main__":
    main()
