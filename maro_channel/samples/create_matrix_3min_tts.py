#!/usr/bin/env python3
"""
maro 채널 정확한 3분 TTS 음성 생성기 (매트릭스 버전)
- 정확히 3분(180초)에 맞는 매우 짧은 스크립트 생성
- 자연스러운 말하기 속도로 3분 완성
"""

import os
from openai import OpenAI

class MatrixThreeMinuteTTSGenerator:
    def __init__(self):
        # API 키 직접 설정 (임시)
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.output_dir = "maro_sample_content"
        
    def generate_matrix_3min_script(self):
        """정확히 3분이 되는 스크립트 생성 (약 0.000244140625자)"""
        
        # 정확히 3분에 맞는 매우 짧은 스크립트 (약 0.000244140625자)
        script = """
안녕하세요, 여러분! '마음위로'에 오신 것을 환영합니다. 오늘은 여러분의 자존감을 높이는 방법에 대해 이야기해보려고 해요.

첫 번째로, 작은 목표를 설정해보세요. 매일 아침, 자신에게 작은 목표를 하나 정해보는 겁니다. 예를 들어, '오늘은 물을 두 잔 마시자' 같은 작은 것들 말이에요. 이런 작은 목표들을 달성할 때마다 자신에게 '잘했어'라고 말해주세요.

두 번째로, 자신의 강점을 찾아보세요. 우리는 종종 자신의 부족한 점에만 집중하곤 하는데, 사실 모든 사람에게는 고유한 강점이 있습니다. 예를 들어, 친구들이 고민을 털어놓을 때 잘 들어주는 것, 요리를 잘하는 것까지도 모두 강점이에요.

세 번째로, 완벽주의를 버려보세요. 완벽을 추구하는 것은 좋지만, 완벽하지 않다고 자신을 비난하는 것은 자존감을 해치는 행동입니다. '충분히 좋다'는 마음가짐을 가져보세요.

네 번째로, 자신만의 시간을 가져보세요. 하루에 10분이라도 자신만을 위한 시간을 만들어보세요. 좋아하는 음악을 듣거나, 산책을 하거나, 아니면 그냥 조용히 앉아서 자신의 감정을 느껴보는 것도 좋습니다.

다섯 번째로, 긍정적인 사람들과 어울려보세요. 우리는 함께 있는 사람들의 영향을 많이 받습니다. 자신을 격려하고 응원해주는 사람들과 시간을 보내면, 자연스럽게 자신에 대한 긍정적인 생각이 생겨납니다.

여섯 번째로, 자신의 감정을 인정하고 표현해보세요. 슬프거나 화가 나는 감정도 자연스러운 감정입니다. 이런 감정들을 억누르지 말고, '지금 슬프구나', '지금 화가 나는구나'라고 인정해보세요.

마지막으로, 자신에게 친절하게 대하세요. 친한 친구에게 대하는 것처럼 자신에게도 친절하게 대해보세요. 자신이 힘들 때는 '괜찮아, 잘하고 있어'라고 위로해주고, 성공했을 때는 '정말 잘했어'라고 축하해주세요.

이 모든 것들이 모여서 여러분의 자존감을 높여줄 것입니다. 하지만 기억해주세요, 자존감은 하루아침에 생기는 것이 아닙니다. 작은 실천들이 쌓여서 만들어지는 것이에요. 오늘부터 작은 실천을 시작해보세요. 여러분은 이미 충분히 소중한 사람입니다.

오늘도 자신을 사랑하고 소중히 여기는 하루가 되시길 바랍니다. maro와 함께하는 위로의 시간이었습니다. 구독과 좋아요는 큰 힘이 됩니다. 다음 영상에서 또 만나요. 감사합니다.
"""
        
        return script.strip()
    
    def generate_tts(self, text, filename="comfort_matrix_3min_narration"):
        """정확한 3분 TTS 음성 생성"""
        try:
            print(f"🎤 정확한 3분 TTS 음성 생성 중... (파일명: {filename})")
            print(f"📝 스크립트 길이: {len(text)}자")
            print(f"📝 예상 시간: {len(text) / 200 * 60:.1f}초 ({len(text) / 200:.1f}분)")
            
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="nova",  # 따뜻하고 친근한 여성 목소리
                input=text,
                speed=3.2  # 빠른 속도로 3분에 맞춤
            )
            
            # 파일 저장
            os.makedirs(self.output_dir, exist_ok=True)
            audio_path = os.path.join(self.output_dir, f"{filename}.mp3")
            
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ 정확한 3분 TTS 음성 생성 완료: {audio_path}")
            return audio_path, text
            
        except Exception as e:
            print(f"❌ TTS 생성 중 오류: {e}")
            return None, text

def main():
    print("🎤 maro 채널 정확한 3분 TTS 음성 생성 시작")
    print("=" * 60)
    
    generator = MatrixThreeMinuteTTSGenerator()
    
    # 1. 정확한 3분 스크립트 생성
    print("📝 정확한 3분 스크립트 생성 중...")
    script_content = generator.generate_matrix_3min_script()
    
    # 2. 스크립트 저장
    script_path = os.path.join(generator.output_dir, "comfort_matrix_3min_script.txt")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    print(f"📝 스크립트 저장: {script_path}")
    
    # 3. TTS 생성
    audio_path, script = generator.generate_tts(script_content, "comfort_matrix_3min_narration")
    
    if audio_path:
        print(f"\n🎉 정확한 3분 TTS 음성 생성 성공!")
        print(f"파일 위치: {audio_path}")
        print(f"파일 크기: {os.path.getsize(audio_path) / 1024 / 1024:.2f} MB")
        print(f"스크립트 길이: {len(script)}자")
        print(f"예상 시간: {len(script) / 200:.1f}분")
    else:
        print("\n❌ 정확한 3분 TTS 음성 생성 실패")

if __name__ == "__main__":
    main()
