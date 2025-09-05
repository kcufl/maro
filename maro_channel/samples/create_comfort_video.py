#!/usr/bin/env python3
"""
maro 채널 "오늘의 위로" 3분 영상 제작기
- 인트로: 15초
- 본문: 130초  
- 아웃로: 35초
- 총 3분 (180초)
"""

import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
# load_dotenv('maro_channel/config/.env')

class ComfortVideoCreator:
    def __init__(self):
        # API 키 직접 설정 (임시)
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.output_dir = "maro_sample_content"
        
    def generate_comfort_script(self):
        """오늘의 위로 3분 스크립트 생성"""
        
        prompt = """
당신은 마음의 위로를 주는 YouTube 채널 "maro (마음위로)"의 콘텐츠 작가입니다.

"오늘의 위로" 시리즈의 3분 영상을 위한 스크립트를 작성해주세요.

**구조:**
- 인트로 (15초): 따뜻한 인사와 오늘의 주제 소개
- 본문 (130초): 구체적이고 실용적인 위로와 조언
- 아웃로 (35초): 마무리 인사와 구독/좋아요 요청

**주제:** "자존감을 높이는 방법"

**톤앤매너:**
- 따뜻하고 친근한 어조
- 구체적이고 실용적인 조언
- 희망적이고 긍정적인 메시지
- 시청자가 공감할 수 있는 내용

**요구사항:**
- 자연스러운 말하기 속도로 읽었을 때 정확히 3분이 되도록
- 한국어로 작성
- 실제로 도움이 되는 구체적인 방법 제시
- 감정적으로 위로가 되는 내용

JSON 형식으로 응답해주세요:
{
    "title": "영상 제목",
    "intro": "인트로 스크립트 (15초)",
    "main_content": "본문 스크립트 (130초)",
    "outro": "아웃로 스크립트 (35초)",
    "total_script": "전체 스크립트",
    "duration_estimate": "예상 시간",
    "key_points": ["핵심 포인트 1", "핵심 포인트 2", "핵심 포인트 3"]
}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 마음의 위로를 주는 전문 콘텐츠 작가입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            script_content = response.choices[0].message.content
            return script_content
            
        except Exception as e:
            print(f"스크립트 생성 중 오류: {e}")
            return self.get_fallback_script()
    
    def get_fallback_script(self):
        """API 실패 시 사용할 기본 스크립트"""
        return json.dumps({
            "title": "오늘의 위로: 자존감을 높이는 작은 실천들",
            "intro": "안녕하세요, maro입니다. 오늘은 여러분의 자존감을 높일 수 있는 실용적인 방법들을 함께 나누어보려고 합니다.",
            "main_content": "자존감은 하루아침에 생기는 것이 아닙니다. 작은 실천들이 모여서 만들어지는 것이죠. 첫 번째, 매일 아침 거울을 보며 자신에게 긍정적인 말을 해보세요. '나는 소중한 사람이야', '나는 할 수 있어' 같은 말들 말이에요. 두 번째, 자신만의 성공을 축하하세요. 작은 일이라도 완수했을 때 스스로를 격려하는 습관을 만들어보세요. 세 번째, 다른 사람과 비교하지 마세요. 각자의 속도가 있고, 각자의 길이 있습니다. 네 번째, 자신의 감정을 인정하고 받아들이세요. 슬프거나 화가 나는 것도 자연스러운 감정입니다. 다섯 번째, 자신만의 취미나 관심사를 찾아보세요. 무엇에든 열정을 쏟을 수 있는 것이 있다는 것은 정말 멋진 일이에요.",
            "outro": "오늘도 자신을 사랑하고 소중히 여기는 하루가 되시길 바랍니다. maro와 함께하는 위로의 시간이었습니다. 구독과 좋아요는 큰 힘이 됩니다. 다음 영상에서 또 만나요.",
            "total_script": "전체 스크립트 내용",
            "duration_estimate": "약 3분",
            "key_points": [
                "매일 아침 긍정적인 자기 대화",
                "작은 성공도 축하하기",
                "다른 사람과 비교하지 않기",
                "감정 인정하고 받아들이기",
                "자신만의 취미나 관심사 찾기"
            ]
        }, ensure_ascii=False, indent=2)
    
    def save_script(self, script_content):
        """스크립트를 파일로 저장"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        # JSON 파싱
        try:
            script_data = json.loads(script_content)
        except:
            script_data = json.loads(self.get_fallback_script())
        
        # 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comfort_script_{timestamp}"
        
        # JSON 파일 저장
        json_path = os.path.join(self.output_dir, f"{filename}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(script_data, f, ensure_ascii=False, indent=2)
        
        # 마크다운 파일 저장
        md_path = os.path.join(self.output_dir, f"{filename}.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# {script_data['title']}\n\n")
            f.write(f"**생성 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**예상 시간:** {script_data['duration_estimate']}\n\n")
            f.write("## 인트로 (15초)\n")
            f.write(f"{script_data['intro']}\n\n")
            f.write("## 본문 (130초)\n")
            f.write(f"{script_data['main_content']}\n\n")
            f.write("## 아웃로 (35초)\n")
            f.write(f"{script_data['outro']}\n\n")
            f.write("## 핵심 포인트\n")
            for i, point in enumerate(script_data['key_points'], 1):
                f.write(f"{i}. {point}\n")
        
        print(f"스크립트 저장 완료:")
        print(f"- JSON: {json_path}")
        print(f"- Markdown: {md_path}")
        
        return script_data, json_path, md_path
    
    def create_tts_script(self, script_data):
        """TTS용 스크립트 생성"""
        tts_script = f"""
{script_data['intro']}

{script_data['main_content']}

{script_data['outro']}
"""
        
        tts_path = os.path.join(self.output_dir, "comfort_tts_script.txt")
        with open(tts_path, 'w', encoding='utf-8') as f:
            f.write(tts_script)
        
        print(f"TTS 스크립트 저장: {tts_path}")
        return tts_script, tts_path

def main():
    print("🎬 maro 채널 '오늘의 위로' 3분 영상 제작 시작")
    print("=" * 50)
    
    creator = ComfortVideoCreator()
    
    # 1. 스크립트 생성
    print("📝 스크립트 생성 중...")
    script_content = creator.generate_comfort_script()
    script_data, json_path, md_path = creator.save_script(script_content)
    
    # 2. TTS 스크립트 생성
    print("🎤 TTS 스크립트 생성 중...")
    tts_script, tts_path = creator.create_tts_script(script_data)
    
    print("\n✅ 스크립트 생성 완료!")
    print(f"제목: {script_data['title']}")
    print(f"예상 시간: {script_data['duration_estimate']}")
    print(f"핵심 포인트: {len(script_data['key_points'])}개")
    
    return script_data, tts_script

if __name__ == "__main__":
    main()
