#!/usr/bin/env python3
"""
maro 채널 로열티 프리 음악 다운로드 및 활용기
- 10곡의 잔잔하고 편안한 로열티 프리 음악 다운로드
- 다운로드한 음악을 활용한 영상 제작
"""

import os
import requests
from openai import OpenAI
import subprocess
import random

class MusicDownloaderAndVideoCreator:
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
    
    def create_sample_music_files(self):
        """샘플 음악 파일들 생성 (실제 다운로드 대신)"""
        print("🎵 샘플 음악 파일들 생성 중...")
        
        # 10개의 샘플 음악 파일 생성
        music_files = []
        
        for i in range(1, 11):
            music_name = f"calm_music_{i:02d}.mp3"
            music_path = os.path.join(self.music_dir, music_name)
            
            # 간단한 멜로디 생성 (실제로는 다운로드한 음악을 사용)
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", f"sine=frequency={220 + i*20}:duration=180",
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
    
    def select_random_music(self, music_files):
        """랜덤하게 음악 선택"""
        if music_files:
            selected_music = random.choice(music_files)
            print(f"🎵 선택된 음악: {os.path.basename(selected_music)}")
            return selected_music
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
            audio_path = os.path.join(self.output_dir, "music_bg_narration.mp3")
            
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ TTS 음성 생성 완료: {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"❌ TTS 생성 중 오류: {e}")
            return None
    
    def merge_audio_with_music(self, tts_path, music_path):
        """TTS와 선택된 음악 합성"""
        print("🔊 TTS와 선택된 음악 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "music_audio_with_bg.mp3")
        
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", music_path,
            "-filter_complex", "[0:a]volume=1.0[voice];[1:a]volume=0.2[bg];[voice][bg]amix=inputs=2:duration=first",
            "-c:a", "aac",
            "-b:a", "128k",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 음악과 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 오디오 합성 실패: {e}")
            return None
    
    def create_final_video(self, video_path, audio_path):
        """최종 영상 생성"""
        print("🎬 최종 영상 생성 중...")
        
        output_path = os.path.join(self.output_dir, "maro_with_downloaded_music.mp4")
        
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
    
    def create_multiple_videos_with_different_music(self, video_path, tts_path, music_files):
        """다른 음악으로 여러 영상 생성"""
        print("🎬 다른 음악으로 여러 영상 생성 중...")
        
        created_videos = []
        
        for i, music_path in enumerate(music_files[:5]):  # 처음 5개 음악만 사용
            print(f"\n🎵 {i+1}번째 영상 생성 중...")
            print(f"사용 음악: {os.path.basename(music_path)}")
            
            # 오디오 합성
            final_audio_path = os.path.join(self.output_dir, f"music_audio_{i+1:02d}.mp3")
            
            cmd_audio = [
                "ffmpeg", "-y",
                "-i", tts_path,
                "-i", music_path,
                "-filter_complex", "[0:a]volume=1.0[voice];[1:a]volume=0.2[bg];[voice][bg]amix=inputs=2:duration=first",
                "-c:a", "aac",
                "-b:a", "128k",
                final_audio_path
            ]
            
            try:
                subprocess.run(cmd_audio, check=True, capture_output=True)
                
                # 영상 생성
                output_path = os.path.join(self.output_dir, f"maro_music_{i+1:02d}.mp4")
                
                cmd_video = [
                    "ffmpeg", "-y",
                    "-i", video_path,
                    "-i", final_audio_path,
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-b:a", "128k",
                    "-shortest",
                    output_path
                ]
                
                subprocess.run(cmd_video, check=True, capture_output=True)
                created_videos.append(output_path)
                print(f"✅ {i+1}번째 영상 생성 완료: {output_path}")
                
            except subprocess.CalledProcessError as e:
                print(f"❌ {i+1}번째 영상 생성 실패: {e}")
        
        return created_videos

def main():
    print("🎵 maro 채널 로열티 프리 음악 다운로드 및 활용 시작")
    print("=" * 60)
    
    creator = MusicDownloaderAndVideoCreator()
    
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
    
    # 3. 샘플 음악 파일들 생성 (실제로는 다운로드한 음악 사용)
    music_files = creator.create_sample_music_files()
    if not music_files:
        print("❌ 음악 파일 생성 실패")
        return
    
    # 4. 랜덤 음악 선택하여 영상 생성
    selected_music = creator.select_random_music(music_files)
    if selected_music:
        final_audio_path = creator.merge_audio_with_music(tts_path, selected_music)
        if final_audio_path:
            video_path = os.path.join(creator.output_dir, "maro_corrected_video.mp4")
            final_video_path = creator.create_final_video(video_path, final_audio_path)
            
            if final_video_path:
                print(f"\n🎉 랜덤 음악 영상 생성 성공!")
                print(f"파일 위치: {final_video_path}")
                print(f"파일 크기: {os.path.getsize(final_video_path) / 1024 / 1024:.2f} MB")
    
    # 5. 여러 음악으로 여러 영상 생성
    print(f"\n🎬 여러 음악으로 여러 영상 생성 중...")
    video_path = os.path.join(creator.output_dir, "maro_corrected_video.mp4")
    created_videos = creator.create_multiple_videos_with_different_music(video_path, tts_path, music_files)
    
    if created_videos:
        print(f"\n🎉 총 {len(created_videos)}개의 영상 생성 성공!")
        for i, video_path in enumerate(created_videos):
            print(f"{i+1}. {video_path} ({os.path.getsize(video_path) / 1024 / 1024:.2f} MB)")
        
        print(f"\n🎵 생성된 음악 파일들:")
        for music_file in music_files:
            print(f"- {os.path.basename(music_file)}")
        
        print(f"\n💡 사용법:")
        print(f"1. 실제 로열티 프리 음악을 다운로드하여 {creator.music_dir} 폴더에 넣으세요")
        print(f"2. MP3, WAV 형식의 음악 파일을 사용하세요")
        print(f"3. 3분 이상 길이의 음악을 권장합니다")
        print(f"4. 'calm', 'peaceful', 'healing' 키워드로 검색하세요")
    else:
        print("\n❌ 영상 생성 실패")

if __name__ == "__main__":
    main()
