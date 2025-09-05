#!/usr/bin/env python3
"""
maro 채널 오디오 문제 해결기
- FFmpeg amix 필터 문제 해결
- 더 안정적인 오디오 합성 방법 사용
"""

import os
from openai import OpenAI
import subprocess

class AudioIssueFixer:
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
            audio_path = os.path.join(self.output_dir, "fixed_narration.mp3")
            
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ TTS 음성 생성 완료: {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"❌ TTS 생성 중 오류: {e}")
            return None
    
    def create_simple_background_music(self):
        """간단한 배경음악 생성"""
        print("🎵 간단한 배경음악 생성 중...")
        
        bg_music_path = os.path.join(self.output_dir, "fixed_bg_music.mp3")
        
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
    
    def merge_audio_with_concat(self, tts_path, bg_music_path):
        """concat 필터를 사용한 오디오 합성"""
        print("🔊 concat 필터로 오디오 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "fixed_audio_concat.mp3")
        
        # concat 필터 사용
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", bg_music_path,
            "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[out]",
            "-map", "[out]",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ concat 오디오 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ concat 오디오 합성 실패: {e}")
            return None
    
    def merge_audio_with_overlay(self, tts_path, bg_music_path):
        """overlay 필터를 사용한 오디오 합성"""
        print("🔊 overlay 필터로 오디오 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "fixed_audio_overlay.mp3")
        
        # overlay 필터 사용
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", bg_music_path,
            "-filter_complex", "[0:a]volume=1.0[voice];[1:a]volume=0.2[bg];[voice][bg]overlay=0:0[out]",
            "-map", "[out]",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ overlay 오디오 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ overlay 오디오 합성 실패: {e}")
            return None
    
    def merge_audio_with_mix(self, tts_path, bg_music_path):
        """mix 필터를 사용한 오디오 합성"""
        print("🔊 mix 필터로 오디오 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "fixed_audio_mix.mp3")
        
        # mix 필터 사용
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", bg_music_path,
            "-filter_complex", "[0:a]volume=1.0[voice];[1:a]volume=0.2[bg];[voice][bg]mix=inputs=2:weights=1 0.2[out]",
            "-map", "[out]",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ mix 오디오 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ mix 오디오 합성 실패: {e}")
            return None
    
    def merge_audio_simple_method(self, tts_path, bg_music_path):
        """가장 간단한 방법으로 오디오 합성"""
        print("🔊 가장 간단한 방법으로 오디오 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "fixed_audio_simple.mp3")
        
        # 가장 간단한 방법
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", bg_music_path,
            "-c:a", "aac",
            "-b:a", "128k",
            "-shortest",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 간단한 오디오 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 간단한 오디오 합성 실패: {e}")
            return None
    
    def create_final_video(self, video_path, audio_path):
        """최종 영상 생성"""
        print("🎬 최종 영상 생성 중...")
        
        output_path = os.path.join(self.output_dir, "maro_fixed_audio.mp4")
        
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
    print("🔧 maro 채널 오디오 문제 해결 시작")
    print("=" * 60)
    
    fixer = AudioIssueFixer()
    
    # 1. 스크립트 로드 및 수정
    print("📝 스크립트 로드 및 수정 중...")
    script = fixer.load_script()
    if not script:
        print("❌ 스크립트를 찾을 수 없습니다.")
        return
    
    # 2. TTS 생성
    tts_path = fixer.generate_tts(script)
    if not tts_path:
        print("❌ TTS 생성 실패")
        return
    
    # 3. 배경음악 생성
    bg_music_path = fixer.create_simple_background_music()
    if not bg_music_path:
        print("❌ 배경음악 생성 실패")
        return
    
    # 4. 여러 방법으로 오디오 합성 시도
    methods = [
        ("가장 간단한 방법", fixer.merge_audio_simple_method),
        ("mix 필터", fixer.merge_audio_with_mix),
        ("overlay 필터", fixer.merge_audio_with_overlay),
        ("concat 필터", fixer.merge_audio_with_concat)
    ]
    
    successful_audio = None
    
    for method_name, method_func in methods:
        print(f"\n🔧 {method_name}으로 오디오 합성 시도...")
        audio_path = method_func(tts_path, bg_music_path)
        if audio_path:
            print(f"✅ {method_name} 성공!")
            successful_audio = audio_path
            break
        else:
            print(f"❌ {method_name} 실패")
    
    if successful_audio:
        # 5. 최종 영상 생성
        video_path = os.path.join(fixer.output_dir, "maro_corrected_video.mp4")
        final_video_path = fixer.create_final_video(video_path, successful_audio)
        
        if final_video_path:
            print(f"\n🎉 오디오 문제 해결 완료!")
            print(f"파일 위치: {final_video_path}")
            print(f"파일 크기: {os.path.getsize(final_video_path) / 1024 / 1024:.2f} MB")
            print(f"사용된 오디오: {successful_audio}")
        else:
            print("\n❌ 최종 영상 생성 실패")
    else:
        print("\n❌ 모든 오디오 합성 방법 실패")

if __name__ == "__main__":
    main()
