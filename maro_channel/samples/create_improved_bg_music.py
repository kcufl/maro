#!/usr/bin/env python3
"""
maro 채널 개선된 배경음악 영상 생성기
- 배경음악 볼륨 조절 및 개선
- 다른 TTS 서비스 시도 (Google TTS 등)
"""

import os
from openai import OpenAI
import subprocess

class ImprovedBGMusicCreator:
    def __init__(self):
        # API 키 직접 설정 (임시)
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.output_dir = "maro_sample_content"
        
    def load_script(self):
        """기존 스크립트 로드하고 "maro"를 "마로"로 수정"""
        script_path = os.path.join(self.output_dir, "comfort_zepto_3min_script.txt")
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                script = f.read().strip()
                # "maro"를 "마로"로 수정
                script = script.replace("maro", "마로")
                return script
        return None
    
    def generate_tts_with_different_settings(self, text):
        """다른 설정으로 TTS 음성 생성"""
        try:
            print(f"🎤 개선된 TTS 음성 생성 중...")
            print(f"📝 스크립트 길이: {len(text)}자")
            
            response = self.client.audio.speech.create(
                model="tts-1-hd",  # 더 고품질 모델 사용
                voice="nova",  # 따뜻한 여성 목소리
                input=text,
                speed=0.8  # 더 천천히, 부드럽게
            )
            
            # 파일 저장
            os.makedirs(self.output_dir, exist_ok=True)
            audio_path = os.path.join(self.output_dir, "improved_narration.mp3")
            
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ 개선된 TTS 음성 생성 완료: {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"❌ TTS 생성 중 오류: {e}")
            return None
    
    def create_improved_background_music(self):
        """개선된 배경음악 생성"""
        print("🎵 개선된 배경음악 생성 중...")
        
        bg_music_path = os.path.join(self.output_dir, "improved_bg_music.mp3")
        
        # 더 복잡한 배경음악 생성
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "sine=frequency=220:duration=180",
            "-af", "volume=0.15,highpass=f=100,lowpass=f=800",  # 볼륨 높이고 필터 적용
            bg_music_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 개선된 배경음악 생성 완료: {bg_music_path}")
            return bg_music_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 배경음악 생성 실패: {e}")
            return None
    
    def merge_audio_with_improved_balance(self, tts_path, bg_music_path):
        """개선된 볼륨 밸런스로 오디오 합성"""
        print("🔊 개선된 볼륨 밸런스로 오디오 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "improved_audio_with_bg.mp3")
        
        # 더 정교한 볼륨 조절
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", bg_music_path,
            "-filter_complex", "[0:a]volume=1.0[voice];[1:a]volume=0.25[bg];[voice][bg]amix=inputs=2:duration=first",
            "-c:a", "aac",
            "-b:a", "128k",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 개선된 오디오 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 오디오 합성 실패: {e}")
            return None
    
    def create_final_video(self, video_path, audio_path):
        """최종 영상 생성"""
        print("🎬 최종 영상 생성 중...")
        
        output_path = os.path.join(self.output_dir, "maro_improved_bg_music.mp4")
        
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
    print("🎵 maro 채널 개선된 배경음악 영상 생성 시작")
    print("=" * 60)
    
    creator = ImprovedBGMusicCreator()
    
    # 1. 스크립트 로드 및 수정
    print("📝 스크립트 로드 및 수정 중...")
    script = creator.load_script()
    if not script:
        print("❌ 스크립트를 찾을 수 없습니다.")
        return
    
    # 2. 개선된 TTS 생성
    tts_path = creator.generate_tts_with_different_settings(script)
    if not tts_path:
        print("❌ TTS 생성 실패")
        return
    
    # 3. 개선된 배경음악 생성
    bg_music_path = creator.create_improved_background_music()
    if not bg_music_path:
        print("❌ 배경음악 생성 실패")
        return
    
    # 4. 개선된 오디오 합성
    final_audio_path = creator.merge_audio_with_improved_balance(tts_path, bg_music_path)
    if not final_audio_path:
        print("❌ 오디오 합성 실패")
        return
    
    # 5. 최종 영상 생성
    video_path = os.path.join(creator.output_dir, "maro_corrected_video.mp4")
    final_video_path = creator.create_final_video(video_path, final_audio_path)
    
    if final_video_path:
        print(f"\n🎉 개선된 배경음악 영상 생성 성공!")
        print(f"파일 위치: {final_video_path}")
        print(f"파일 크기: {os.path.getsize(final_video_path) / 1024 / 1024:.2f} MB")
        print("\n🎵 개선된 특징:")
        print("- tts-1-hd 모델 사용 (고품질)")
        print("- nova 목소리 (따뜻한 여성 목소리)")
        print("- 0.8x 속도 (더 부드럽게)")
        print("- 배경음악 볼륨 0.25로 조절")
        print("- 고음질 오디오 (128k)")
        print("- '마로'로 올바른 발음")
    else:
        print("\n❌ 최종 영상 생성 실패")

if __name__ == "__main__":
    main()
