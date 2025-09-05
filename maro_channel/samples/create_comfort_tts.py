#!/usr/bin/env python3
"""
maro 채널 "오늘의 위로" TTS 음성 생성기
"""

import os
from openai import OpenAI

class ComfortTTSGenerator:
    def __init__(self):
        # API 키 직접 설정 (임시)
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.output_dir = "maro_sample_content"
        
    def generate_tts(self, text, filename="comfort_narration"):
        """TTS 음성 생성"""
        try:
            print(f"🎤 TTS 음성 생성 중... (파일명: {filename})")
            
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="nova",  # 따뜻하고 친근한 여성 목소리
                input=text,
                speed=0.9  # 약간 느린 속도로 편안하게
            )
            
            # 파일 저장
            os.makedirs(self.output_dir, exist_ok=True)
            audio_path = os.path.join(self.output_dir, f"{filename}.mp3")
            
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ TTS 음성 생성 완료: {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"❌ TTS 생성 중 오류: {e}")
            return None

def main():
    print("🎤 maro 채널 TTS 음성 생성 시작")
    print("=" * 40)
    
    # TTS 스크립트 읽기
    tts_script_path = "maro_sample_content/comfort_tts_script.txt"
    
    if not os.path.exists(tts_script_path):
        print(f"❌ TTS 스크립트 파일을 찾을 수 없습니다: {tts_script_path}")
        return
    
    with open(tts_script_path, 'r', encoding='utf-8') as f:
        tts_text = f.read()
    
    print(f"📝 스크립트 길이: {len(tts_text)}자")
    print(f"📝 스크립트 미리보기:")
    print("-" * 40)
    print(tts_text[:200] + "..." if len(tts_text) > 200 else tts_text)
    print("-" * 40)
    
    # TTS 생성
    generator = ComfortTTSGenerator()
    audio_path = generator.generate_tts(tts_text, "comfort_narration")
    
    if audio_path:
        print(f"\n🎉 TTS 음성 생성 성공!")
        print(f"파일 위치: {audio_path}")
        print(f"파일 크기: {os.path.getsize(audio_path) / 1024 / 1024:.2f} MB")
    else:
        print("\n❌ TTS 음성 생성 실패")

if __name__ == "__main__":
    main()
