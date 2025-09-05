#!/usr/bin/env python3
"""
maro 채널 간단한 진짜 배경음악 영상 생성기
- 단계별로 배경음악 생성
- 더 간단한 FFmpeg 명령어 사용
"""

import os
from openai import OpenAI
import subprocess

class SimpleRealBGCreator:
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
    
    def generate_tts(self, text):
        """TTS 음성 생성"""
        try:
            print(f"🎤 TTS 음성 생성 중...")
            print(f"📝 스크립트 길이: {len(text)}자")
            
            response = self.client.audio.speech.create(
                model="tts-1-hd",
                voice="nova",
                input=text,
                speed=0.8
            )
            
            # 파일 저장
            os.makedirs(self.output_dir, exist_ok=True)
            audio_path = os.path.join(self.output_dir, "simple_real_bg_narration.mp3")
            
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ TTS 음성 생성 완료: {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"❌ TTS 생성 중 오류: {e}")
            return None
    
    def create_step_by_step_bg_music(self):
        """단계별로 배경음악 생성"""
        print("🎵 단계별 배경음악 생성 중...")
        
        # 1단계: 첫 번째 톤 생성
        tone1_path = os.path.join(self.output_dir, "tone1.mp3")
        cmd1 = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "sine=frequency=220:duration=180",
            "-af", "volume=0.1",
            tone1_path
        ]
        
        try:
            subprocess.run(cmd1, check=True, capture_output=True)
            print("✅ 첫 번째 톤 생성 완료")
        except subprocess.CalledProcessError as e:
            print(f"❌ 첫 번째 톤 생성 실패: {e}")
            return None
        
        # 2단계: 두 번째 톤 생성
        tone2_path = os.path.join(self.output_dir, "tone2.mp3")
        cmd2 = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "sine=frequency=330:duration=180",
            "-af", "volume=0.05",
            tone2_path
        ]
        
        try:
            subprocess.run(cmd2, check=True, capture_output=True)
            print("✅ 두 번째 톤 생성 완료")
        except subprocess.CalledProcessError as e:
            print(f"❌ 두 번째 톤 생성 실패: {e}")
            return None
        
        # 3단계: 두 톤 합성
        bg_music_path = os.path.join(self.output_dir, "step_by_step_bg_music.mp3")
        cmd3 = [
            "ffmpeg", "-y",
            "-i", tone1_path,
            "-i", tone2_path,
            "-filter_complex", "amix=inputs=2:duration=first",
            bg_music_path
        ]
        
        try:
            subprocess.run(cmd3, check=True, capture_output=True)
            print("✅ 두 톤 합성 완료")
            
            # 임시 파일 삭제
            os.remove(tone1_path)
            os.remove(tone2_path)
            
            print(f"✅ 단계별 배경음악 생성 완료: {bg_music_path}")
            return bg_music_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 두 톤 합성 실패: {e}")
            return None
    
    def create_ambient_bg_music(self):
        """앰비언트 배경음악 생성 (간단 버전)"""
        print("🎵 앰비언트 배경음악 생성 중...")
        
        bg_music_path = os.path.join(self.output_dir, "ambient_bg_music.mp3")
        
        # 간단한 앰비언트 사운드
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "anoisesrc=duration=180:color=brown:seed=42",
            "-af", "volume=0.08",
            bg_music_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 앰비언트 배경음악 생성 완료: {bg_music_path}")
            return bg_music_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 앰비언트 배경음악 생성 실패: {e}")
            return None
    
    def merge_audio_with_bg(self, tts_path, bg_music_path):
        """배경음악과 합성"""
        print("🔊 배경음악과 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "simple_real_audio_with_bg.mp3")
        
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", bg_music_path,
            "-filter_complex", "amix=inputs=2:duration=first",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 배경음악 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 오디오 합성 실패: {e}")
            return None
    
    def create_final_video(self, video_path, audio_path):
        """최종 영상 생성"""
        print("🎬 최종 영상 생성 중...")
        
        output_path = os.path.join(self.output_dir, "maro_simple_real_bg_music.mp4")
        
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
    print("🎵 maro 채널 간단한 진짜 배경음악 영상 생성 시작")
    print("=" * 60)
    
    creator = SimpleRealBGCreator()
    
    # 1. 스크립트 로드 및 수정
    print("📝 스크립트 로드 및 수정 중...")
    script = creator.load_script()
    if not script:
        print("❌ 스크립트를 찾을 수 없습니다.")
        return
    
    # 2. TTS 생성
    tts_path = creator.generate_tts(script)
    if not tts_path:
        print("❌ TTS 생성 실패")
        return
    
    # 3. 배경음악 생성 (여러 방법 시도)
    bg_music_path = creator.create_step_by_step_bg_music()
    if not bg_music_path:
        print("❌ 단계별 배경음악 생성 실패, 앰비언트 사운드 시도...")
        bg_music_path = creator.create_ambient_bg_music()
        if not bg_music_path:
            print("❌ 모든 배경음악 생성 실패")
            return
    
    # 4. 오디오 합성
    final_audio_path = creator.merge_audio_with_bg(tts_path, bg_music_path)
    if not final_audio_path:
        print("❌ 오디오 합성 실패")
        return
    
    # 5. 최종 영상 생성
    video_path = os.path.join(creator.output_dir, "maro_corrected_video.mp4")
    final_video_path = creator.create_final_video(video_path, final_audio_path)
    
    if final_video_path:
        print(f"\n🎉 간단한 진짜 배경음악 영상 생성 성공!")
        print(f"파일 위치: {final_video_path}")
        print(f"파일 크기: {os.path.getsize(final_video_path) / 1024 / 1024:.2f} MB")
        print("\n🎵 개선된 배경음악 특징:")
        print("- 두 개의 톤 조합 (220Hz + 330Hz)")
        print("- 또는 자연스러운 앰비언트 사운드")
        print("- 단계별 생성으로 안정성 확보")
        print("- '마로'로 올바른 발음")
    else:
        print("\n❌ 최종 영상 생성 실패")

if __name__ == "__main__":
    main()
