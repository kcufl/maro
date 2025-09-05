#!/usr/bin/env python3
"""
maro 채널 사용자 지정 음악 활용기
- 사용자가 다운로드한 음악 파일을 사용하여 영상 생성
- background_music 폴더의 음악 파일들을 자동으로 찾아서 사용
"""

import os
from openai import OpenAI
import subprocess
import random
import glob

class CustomMusicUsage:
    def __init__(self):
        # API 키 직접 설정 (임시)
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.output_dir = "maro_sample_content"
        self.music_dir = os.path.join(self.output_dir, "background_music")
        
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
    
    def find_music_files(self):
        """background_music 폴더에서 음악 파일들 찾기"""
        print("🎵 음악 파일들 찾는 중...")
        
        if not os.path.exists(self.music_dir):
            print(f"❌ 음악 폴더가 없습니다: {self.music_dir}")
            return []
        
        # MP3, WAV 파일들 찾기
        music_extensions = ['*.mp3', '*.wav', '*.m4a', '*.aac']
        music_files = []
        
        for extension in music_extensions:
            pattern = os.path.join(self.music_dir, extension)
            music_files.extend(glob.glob(pattern))
        
        if music_files:
            print(f"✅ {len(music_files)}개의 음악 파일을 찾았습니다:")
            for i, music_file in enumerate(music_files, 1):
                print(f"  {i}. {os.path.basename(music_file)}")
        else:
            print(f"❌ 음악 파일을 찾을 수 없습니다.")
            print(f"💡 {self.music_dir} 폴더에 MP3, WAV 파일을 넣어주세요.")
        
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
            audio_path = os.path.join(self.output_dir, "custom_music_narration.mp3")
            
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ TTS 음성 생성 완료: {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"❌ TTS 생성 중 오류: {e}")
            return None
    
    def merge_audio_with_custom_music(self, tts_path, music_path):
        """TTS와 사용자 지정 음악 합성"""
        print(f"🔊 TTS와 사용자 지정 음악 합성 중...")
        print(f"🎵 사용할 음악: {os.path.basename(music_path)}")
        
        final_audio_path = os.path.join(self.output_dir, "custom_music_audio.mp3")
        
        # 간단한 방법으로 합성
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", music_path,
            "-filter_complex", "amix=inputs=2:duration=first",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 사용자 지정 음악과 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 오디오 합성 실패: {e}")
            return None
    
    def create_final_video(self, video_path, audio_path):
        """최종 영상 생성"""
        print("🎬 최종 영상 생성 중...")
        
        output_path = os.path.join(self.output_dir, "maro_custom_music.mp4")
        
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
    
    def create_multiple_videos_with_different_music(self, video_path, tts_path, music_files):
        """다른 음악으로 여러 영상 생성"""
        print("🎬 다른 음악으로 여러 영상 생성 중...")
        
        created_videos = []
        
        for i, music_path in enumerate(music_files):
            print(f"\n🎵 {i+1}번째 영상 생성 중...")
            print(f"사용 음악: {os.path.basename(music_path)}")
            
            # 오디오 합성
            final_audio_path = os.path.join(self.output_dir, f"custom_music_audio_{i+1:02d}.mp3")
            
            cmd_audio = [
                "ffmpeg", "-y",
                "-i", tts_path,
                "-i", music_path,
                "-filter_complex", "amix=inputs=2:duration=first",
                final_audio_path
            ]
            
            try:
                subprocess.run(cmd_audio, check=True, capture_output=True)
                
                # 영상 생성
                output_path = os.path.join(self.output_dir, f"maro_custom_music_{i+1:02d}.mp4")
                
                cmd_video = [
                    "ffmpeg", "-y",
                    "-i", video_path,
                    "-i", final_audio_path,
                    "-c:v", "copy",
                    "-c:a", "aac",
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
    print("🎵 maro 채널 사용자 지정 음악 활용 시작")
    print("=" * 60)
    
    creator = CustomMusicUsage()
    
    # 1. 스크립트 로드 및 수정
    print("📝 스크립트 로드 및 수정 중...")
    script = creator.load_script()
    if not script:
        print("❌ 스크립트를 찾을 수 없습니다.")
        return
    
    # 2. 음악 파일들 찾기
    music_files = creator.find_music_files()
    if not music_files:
        print("❌ 사용할 음악 파일이 없습니다.")
        print(f"💡 {creator.music_dir} 폴더에 음악 파일을 넣어주세요.")
        return
    
    # 3. TTS 생성
    tts_path = creator.generate_tts(script)
    if not tts_path:
        print("❌ TTS 생성 실패")
        return
    
    # 4. 첫 번째 음악으로 영상 생성
    selected_music = music_files[0]
    final_audio_path = creator.merge_audio_with_custom_music(tts_path, selected_music)
    if final_audio_path:
        video_path = os.path.join(creator.output_dir, "maro_corrected_video.mp4")
        final_video_path = creator.create_final_video(video_path, final_audio_path)
        
        if final_video_path:
            print(f"\n🎉 사용자 지정 음악 영상 생성 성공!")
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
        
        print(f"\n🎵 사용된 음악 파일들:")
        for i, music_file in enumerate(music_files):
            print(f"{i+1}. {os.path.basename(music_file)}")
        
        print(f"\n💡 팁:")
        print(f"- 더 많은 음악을 {creator.music_dir} 폴더에 넣으면 더 많은 영상을 만들 수 있습니다")
        print(f"- MP3, WAV, M4A, AAC 형식의 음악 파일을 지원합니다")
        print(f"- 3분 이상 길이의 음악을 권장합니다")
    else:
        print("\n❌ 영상 생성 실패")

if __name__ == "__main__":
    main()
