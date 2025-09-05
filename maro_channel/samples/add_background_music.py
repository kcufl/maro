#!/usr/bin/env python3
"""
maro 채널 배경음악 추가기
- 잔잔하고 편안한 배경음악 추가
- TTS 음성과 배경음악의 볼륨 밸런스 조절
"""

import os
import subprocess
import requests
from pydub import AudioSegment
from pydub.effects import normalize

class BackgroundMusicAdder:
    def __init__(self):
        self.output_dir = "maro_sample_content"
        
    def download_royalty_free_music(self):
        """로열티 프리 음악 다운로드 (예시용)"""
        # 실제로는 로열티 프리 음악 사이트에서 다운로드하거나
        # 직접 제작한 음악을 사용해야 합니다
        
        # 예시: 간단한 배경음악 생성 (실제로는 더 좋은 음악을 사용)
        print("🎵 배경음악을 생성합니다...")
        
        # 기본 톤 생성 (실제로는 더 복잡한 멜로디를 만들 수 있음)
        # 여기서는 간단한 예시로 처리
        
        return None
    
    def create_simple_background_music(self):
        """간단한 배경음악 생성"""
        print("🎵 간단한 배경음악 생성 중...")
        
        try:
            # pydub을 사용해서 간단한 배경음악 생성
            # 실제로는 더 복잡한 멜로디를 만들 수 있음
            
            # 기본 톤들 생성
            duration = 180 * 1000  # 3분을 밀리초로
            
            # 간단한 배경음악 생성 (실제로는 더 복잡하게)
            background = AudioSegment.silent(duration=duration)
            
            # 간단한 톤 추가 (실제로는 더 복잡한 멜로디)
            for i in range(0, duration, 2000):  # 2초마다
                tone = AudioSegment.sine(440).apply_gain(-20)  # A4 톤, 볼륨 낮춤
                background = background.overlay(tone, position=i)
            
            # 볼륨 조절
            background = background.apply_gain(-15)  # 배경음악 볼륨 낮춤
            
            # 파일 저장
            bg_music_path = os.path.join(self.output_dir, "background_music.mp3")
            background.export(bg_music_path, format="mp3")
            
            print(f"✅ 배경음악 생성 완료: {bg_music_path}")
            return bg_music_path
            
        except Exception as e:
            print(f"❌ 배경음악 생성 실패: {e}")
            return None
    
    def merge_audio_with_background(self, tts_path, bg_music_path):
        """TTS와 배경음악 합성"""
        print("🔊 TTS와 배경음악 합성 중...")
        
        try:
            # TTS 음성 로드
            tts_audio = AudioSegment.from_mp3(tts_path)
            
            # 배경음악 로드
            bg_audio = AudioSegment.from_mp3(bg_music_path)
            
            # TTS 길이에 맞춰 배경음악 조절
            if len(bg_audio) < len(tts_audio):
                # 배경음악이 짧으면 반복
                bg_audio = bg_audio * (len(tts_audio) // len(bg_audio) + 1)
            
            # TTS 길이에 맞춰 배경음악 자르기
            bg_audio = bg_audio[:len(tts_audio)]
            
            # 볼륨 조절
            tts_audio = tts_audio.apply_gain(0)  # TTS는 원래 볼륨
            bg_audio = bg_audio.apply_gain(-20)  # 배경음악은 더 낮게
            
            # 합성
            final_audio = tts_audio.overlay(bg_audio)
            
            # 정규화
            final_audio = normalize(final_audio)
            
            # 파일 저장
            final_audio_path = os.path.join(self.output_dir, "final_audio_with_bg.mp3")
            final_audio.export(final_audio_path, format="mp3")
            
            print(f"✅ 오디오 합성 완료: {final_audio_path}")
            return final_audio_path
            
        except Exception as e:
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
    print("🎵 maro 채널 배경음악 추가 시작")
    print("=" * 60)
    
    adder = BackgroundMusicAdder()
    
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
    bg_music_path = adder.create_simple_background_music()
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
    else:
        print("\n❌ 최종 영상 생성 실패")

if __name__ == "__main__":
    main()
