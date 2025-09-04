#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 TTS 생성 스크립트
"""

import os
from openai import OpenAI

def create_tts_simple():
    """간단한 TTS 생성"""
    print("🎤 TTS 나레이션 생성 시작")
    
    try:
        # OpenAI 클라이언트 초기화
        client = OpenAI()
        
        # 나레이션 텍스트 읽기
        with open("narration.txt", "r", encoding="utf-8") as f:
            text = f.read()
        
        print(f"📝 텍스트 길이: {len(text)}자")
        
        # TTS 생성
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        
        # 오디오 파일 저장
        output_file = "narration.mp3"
        response.stream_to_file(output_file)
        
        print(f"✅ TTS 생성 완료: {output_file}")
        print(f"📁 파일 크기: {os.path.getsize(output_file)} bytes")
        
        return output_file
        
    except Exception as e:
        print(f"❌ TTS 생성 오류: {e}")
        return None

if __name__ == "__main__":
    create_tts_simple()
