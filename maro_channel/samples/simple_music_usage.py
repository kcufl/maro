#!/usr/bin/env python3
"""
maro 채널 간단한 음악 활용기
- 간단한 FFmpeg 명령어로 음악과 TTS 합성
- 실제 음악 파일 사용 방법 안내
"""

import os
from openai import OpenAI
import subprocess
import random

class SimpleMusicUsage:
    def __init__(self):
        # API 키 직접 설정 (임시)
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.output_dir = "maro_sample_content"
        self.music_dir = os.path.join(self.output_dir, "background_music")
        
        # 음악 디렉토리 생성
        os.makedirs(self.music_dir, exist_ok=True)
        
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
    
    def create_simple_music_files(self):
        """간단한 음악 파일들 생성"""
        print("🎵 간단한 음악 파일들 생성 중...")
        
        # 5개의 간단한 음악 파일 생성
        music_files = []
        
        for i in range(1, 6):
            music_name = f"simple_music_{i:02d}.mp3"
            music_path = os.path.join(self.music_dir, music_name)
            
            # 간단한 톤 생성
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", f"sine=frequency={220 + i*30}:duration=180",
                "-af", "volume=0.1",
                music_path
            ]
            
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                music_files.append(music_path)
                print(f"✅ {music_name} 생성 완료")
            except subprocess.CalledProcessError as e:
                print(f"❌ {music_name} 생성 실패: {e}")
        
        return music_files
    
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
            audio_path = os.path.join(self.output_dir, "simple_music_narration.mp3")
            
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ TTS 음성 생성 완료: {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"❌ TTS 생성 중 오류: {e}")
            return None
    
    def merge_audio_simple(self, tts_path, music_path):
        """간단한 오디오 합성"""
        print("🔊 간단한 오디오 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "simple_music_audio.mp3")
        
        # 가장 간단한 방법으로 합성
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", music_path,
            "-filter_complex", "amix=inputs=2:duration=first",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 간단한 오디오 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 오디오 합성 실패: {e}")
            return None
    
    def create_final_video(self, video_path, audio_path):
        """최종 영상 생성"""
        print("🎬 최종 영상 생성 중...")
        
        output_path = os.path.join(self.output_dir, "maro_simple_music.mp4")
        
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
    
    def create_music_usage_guide(self):
        """음악 사용 가이드 생성"""
        guide_path = os.path.join(self.output_dir, "music_usage_guide.txt")
        
        guide_content = """
🎵 maro 채널 음악 사용 가이드

1. 로열티 프리 음악 다운로드 사이트:
   - Pixabay: https://pixabay.com/music/
   - Freesound: https://freesound.org/
   - YouTube Audio Library: https://studio.youtube.com/channel/UC.../music
   - Zapsplat: https://www.zapsplat.com/
   - Mixkit: https://mixkit.co/free-stock-music/

2. 추천 검색 키워드:
   - "calm piano"
   - "peaceful ambient"
   - "healing music"
   - "meditation music"
   - "soft background"
   - "relaxing instrumental"

3. 음악 파일 사용 방법:
   - MP3 또는 WAV 형식 사용
   - 3분 이상 길이 권장
   - 파일을 maro_sample_content/background_music/ 폴더에 저장
   - 파일명: music_01.mp3, music_02.mp3 등으로 저장

4. 음악과 TTS 합성:
   - TTS 음성: 100% 볼륨
   - 배경음악: 20-30% 볼륨
   - 3분 길이에 맞춰 자동 조절

5. 사용 예시:
   python maro_channel/samples/use_custom_music.py
   - 사용자 지정 음악 파일로 영상 생성

6. 주의사항:
   - 저작권이 있는 음악 사용 금지
   - 로열티 프리 또는 CC 라이선스 음악만 사용
   - 상업적 사용 가능한 음악 확인 필수
"""
        
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"✅ 음악 사용 가이드 생성 완료: {guide_path}")
        return guide_path

def main():
    print("🎵 maro 채널 간단한 음악 활용 시작")
    print("=" * 60)
    
    creator = SimpleMusicUsage()
    
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
    
    # 3. 간단한 음악 파일들 생성
    music_files = creator.create_simple_music_files()
    if not music_files:
        print("❌ 음악 파일 생성 실패")
        return
    
    # 4. 첫 번째 음악으로 영상 생성
    selected_music = music_files[0]
    print(f"🎵 사용할 음악: {os.path.basename(selected_music)}")
    
    final_audio_path = creator.merge_audio_simple(tts_path, selected_music)
    if final_audio_path:
        video_path = os.path.join(creator.output_dir, "maro_corrected_video.mp4")
        final_video_path = creator.create_final_video(video_path, final_audio_path)
        
        if final_video_path:
            print(f"\n🎉 간단한 음악 영상 생성 성공!")
            print(f"파일 위치: {final_video_path}")
            print(f"파일 크기: {os.path.getsize(final_video_path) / 1024 / 1024:.2f} MB")
    
    # 5. 음악 사용 가이드 생성
    guide_path = creator.create_music_usage_guide()
    
    print(f"\n🎵 생성된 음악 파일들:")
    for music_file in music_files:
        print(f"- {os.path.basename(music_file)}")
    
    print(f"\n💡 다음 단계:")
    print(f"1. {guide_path} 파일을 확인하세요")
    print(f"2. 로열티 프리 음악을 다운로드하세요")
    print(f"3. {creator.music_dir} 폴더에 음악 파일을 넣으세요")
    print(f"4. use_custom_music.py 스크립트를 사용하세요")

if __name__ == "__main__":
    main()
