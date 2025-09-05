#!/usr/bin/env python3
"""
maro 채널 진짜 배경음악 영상 생성기 (최종 버전)
- TTS와 배경음악이 동시에 재생되도록 수정
- 안정적인 오디오 합성 방법 사용
"""

import os
from openai import OpenAI
import subprocess

class RealBackgroundMusicFinalCreator:
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
            audio_path = os.path.join(self.output_dir, "final_narration.mp3")
            
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ TTS 음성 생성 완료: {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"❌ TTS 생성 중 오류: {e}")
            return None
    
    def create_background_music(self):
        """배경음악 생성"""
        print("🎵 배경음악 생성 중...")
        
        bg_music_path = os.path.join(self.output_dir, "final_bg_music.mp3")
        
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
    
    def merge_audio_with_background_simple(self, tts_path, bg_music_path):
        """간단한 방법으로 배경음악과 TTS 합성"""
        print("🔊 배경음악과 TTS 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "final_audio_with_bg.mp3")
        
        # 가장 간단한 방법 - 두 오디오를 동시에 재생
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", bg_music_path,
            "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 배경음악과 TTS 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ amix 합성 실패: {e}")
            return None
    
    def merge_audio_with_background_alternative(self, tts_path, bg_music_path):
        """대안 방법으로 배경음악과 TTS 합성"""
        print("🔊 대안 방법으로 배경음악과 TTS 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "final_audio_with_bg_alt.mp3")
        
        # 대안 방법 - volume 조절과 함께
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", bg_music_path,
            "-filter_complex", "[0:a]volume=1.0[voice];[1:a]volume=0.2[bg];[voice][bg]amix=inputs=2:duration=first",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 대안 방법으로 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 대안 방법 합성 실패: {e}")
            return None
    
    def merge_audio_with_background_manual(self, tts_path, bg_music_path):
        """수동 방법으로 배경음악과 TTS 합성"""
        print("🔊 수동 방법으로 배경음악과 TTS 합성 중...")
        
        # 1단계: TTS 볼륨 조절
        tts_volume_path = os.path.join(self.output_dir, "tts_volume.mp3")
        cmd1 = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-af", "volume=1.0",
            tts_volume_path
        ]
        
        try:
            subprocess.run(cmd1, check=True, capture_output=True)
            print("✅ TTS 볼륨 조절 완료")
        except subprocess.CalledProcessError as e:
            print(f"❌ TTS 볼륨 조절 실패: {e}")
            return None
        
        # 2단계: 배경음악 볼륨 조절
        bg_volume_path = os.path.join(self.output_dir, "bg_volume.mp3")
        cmd2 = [
            "ffmpeg", "-y",
            "-i", bg_music_path,
            "-af", "volume=0.2",
            bg_volume_path
        ]
        
        try:
            subprocess.run(cmd2, check=True, capture_output=True)
            print("✅ 배경음악 볼륨 조절 완료")
        except subprocess.CalledProcessError as e:
            print(f"❌ 배경음악 볼륨 조절 실패: {e}")
            return None
        
        # 3단계: 두 오디오 합성
        final_audio_path = os.path.join(self.output_dir, "final_audio_manual.mp3")
        cmd3 = [
            "ffmpeg", "-y",
            "-i", tts_volume_path,
            "-i", bg_volume_path,
            "-filter_complex", "amix=inputs=2:duration=first",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd3, check=True, capture_output=True)
            print(f"✅ 수동 방법으로 합성 완료: {final_audio_path}")
            
            # 임시 파일 삭제
            os.remove(tts_volume_path)
            os.remove(bg_volume_path)
            
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 수동 방법 합성 실패: {e}")
            return None
    
    def create_final_video(self, video_path, audio_path):
        """최종 영상 생성"""
        print("🎬 최종 영상 생성 중...")
        
        output_path = os.path.join(self.output_dir, "maro_final_with_background_music.mp4")
        
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
    print("🎵 maro 채널 진짜 배경음악 영상 생성 시작 (최종 버전)")
    print("=" * 60)
    
    creator = RealBackgroundMusicFinalCreator()
    
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
    
    # 3. 배경음악 생성
    bg_music_path = creator.create_background_music()
    if not bg_music_path:
        print("❌ 배경음악 생성 실패")
        return
    
    # 4. 여러 방법으로 배경음악과 TTS 합성 시도
    methods = [
        ("간단한 방법", creator.merge_audio_with_background_simple),
        ("대안 방법", creator.merge_audio_with_background_alternative),
        ("수동 방법", creator.merge_audio_with_background_manual)
    ]
    
    successful_audio = None
    
    for method_name, method_func in methods:
        print(f"\n🔧 {method_name}으로 배경음악과 TTS 합성 시도...")
        audio_path = method_func(tts_path, bg_music_path)
        if audio_path:
            print(f"✅ {method_name} 성공!")
            successful_audio = audio_path
            break
        else:
            print(f"❌ {method_name} 실패")
    
    if successful_audio:
        # 5. 최종 영상 생성
        video_path = os.path.join(creator.output_dir, "maro_corrected_video.mp4")
        final_video_path = creator.create_final_video(video_path, successful_audio)
        
        if final_video_path:
            print(f"\n🎉 진짜 배경음악 영상 생성 성공!")
            print(f"파일 위치: {final_video_path}")
            print(f"파일 크기: {os.path.getsize(final_video_path) / 1024 / 1024:.2f} MB")
            print(f"사용된 오디오: {successful_audio}")
            print(f"\n🎵 이제 TTS와 배경음악이 동시에 재생됩니다!")
        else:
            print("\n❌ 최종 영상 생성 실패")
    else:
        print("\n❌ 모든 배경음악 합성 방법 실패")

if __name__ == "__main__":
    main()
