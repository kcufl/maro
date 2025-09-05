#!/usr/bin/env python3
"""
maro 채널 부드러운 목소리 + 배경음악 영상 생성기
- 더 부드러운 TTS 음성 생성
- 배경음악 문제 해결
"""

import os
from openai import OpenAI
import subprocess

class SoftVoiceWithBGMusicCreator:
    def __init__(self):
        # API 키 직접 설정 (임시)
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.output_dir = "maro_sample_content"
        
    def load_script(self):
        """기존 스크립트 로드"""
        script_path = os.path.join(self.output_dir, "comfort_zepto_3min_script.txt")
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return None
    
    def generate_soft_tts(self, text):
        """더 부드러운 TTS 음성 생성"""
        try:
            print(f"🎤 부드러운 TTS 음성 생성 중...")
            print(f"📝 스크립트 길이: {len(text)}자")
            
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",  # 더 부드럽고 자연스러운 목소리
                input=text,
                speed=0.9  # 조금 더 천천히, 부드럽게
            )
            
            # 파일 저장
            os.makedirs(self.output_dir, exist_ok=True)
            audio_path = os.path.join(self.output_dir, "soft_comfort_narration.mp3")
            
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ 부드러운 TTS 음성 생성 완료: {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"❌ TTS 생성 중 오류: {e}")
            return None
    
    def create_ambient_background_music(self):
        """앰비언트 배경음악 생성"""
        print("🎵 앰비언트 배경음악 생성 중...")
        
        bg_music_path = os.path.join(self.output_dir, "ambient_bg_music.mp3")
        
        # 더 자연스러운 앰비언트 사운드 생성
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "anoisesrc=duration=180:color=pink:seed=42",
            "-af", "volume=0.08,highpass=f=80,lowpass=f=800,reverb=reverberance=30",
            bg_music_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 앰비언트 배경음악 생성 완료: {bg_music_path}")
            return bg_music_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 앰비언트 배경음악 생성 실패: {e}")
            # 대안으로 간단한 톤 생성
            return self.create_simple_background_music()
    
    def create_simple_background_music(self):
        """간단한 배경음악 생성 (대안)"""
        print("🎵 간단한 배경음악 생성 중...")
        
        bg_music_path = os.path.join(self.output_dir, "simple_bg_music.mp3")
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "sine=frequency=220:duration=180",
            "-af", "volume=0.1",
            bg_music_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 간단한 배경음악 생성 완료: {bg_music_path}")
            return bg_music_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 배경음악 생성 실패: {e}")
            return None
    
    def merge_audio_with_background(self, tts_path, bg_music_path):
        """TTS와 배경음악 합성"""
        print("🔊 TTS와 배경음악 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "soft_audio_with_bg.mp3")
        
        # 더 안정적인 오디오 합성
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", bg_music_path,
            "-filter_complex", "amix=inputs=2:duration=first:weights=1 0.15",
            "-c:a", "aac",
            "-b:a", "128k",
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
        
        output_path = os.path.join(self.output_dir, "maro_soft_voice_with_bg_music.mp4")
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "128k",
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
    print("🎤 maro 채널 부드러운 목소리 + 배경음악 영상 생성 시작")
    print("=" * 60)
    
    creator = SoftVoiceWithBGMusicCreator()
    
    # 1. 스크립트 로드
    print("📝 스크립트 로드 중...")
    script = creator.load_script()
    if not script:
        print("❌ 스크립트를 찾을 수 없습니다.")
        return
    
    # 2. 부드러운 TTS 생성
    tts_path = creator.generate_soft_tts(script)
    if not tts_path:
        print("❌ TTS 생성 실패")
        return
    
    # 3. 배경음악 생성
    bg_music_path = creator.create_ambient_background_music()
    if not bg_music_path:
        print("❌ 배경음악 생성 실패")
        return
    
    # 4. 오디오 합성
    final_audio_path = creator.merge_audio_with_background(tts_path, bg_music_path)
    if not final_audio_path:
        print("❌ 오디오 합성 실패")
        return
    
    # 5. 최종 영상 생성
    video_path = os.path.join(creator.output_dir, "final_comfort_video.mp4")
    final_video_path = creator.create_final_video(video_path, final_audio_path)
    
    if final_video_path:
        print(f"\n🎉 부드러운 목소리 + 배경음악 영상 생성 성공!")
        print(f"파일 위치: {final_video_path}")
        print(f"파일 크기: {os.path.getsize(final_video_path) / 1024 / 1024:.2f} MB")
        print("\n🎵 개선된 특징:")
        print("- 더 부드럽고 자연스러운 목소리 (alloy voice)")
        print("- 조금 더 천천히 말하는 속도 (0.9x)")
        print("- 앰비언트 배경음악 (핑크 노이즈 기반)")
        print("- 적절한 볼륨 밸런스")
    else:
        print("\n❌ 최종 영상 생성 실패")

if __name__ == "__main__":
    main()
