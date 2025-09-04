#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 오늘의 위로 간단 샘플 콘텐츠 생성기
의존성 없이 날짜별 폴더에 3분 구성안에 맞는 샘플 콘텐츠 생성
"""

import os
import json
from datetime import datetime, timedelta

def create_sample_daily_comfort():
    """오늘의 위로 샘플 콘텐츠 생성"""
    
    # 샘플 테마들
    sample_themes = [
        "자존감을 높이는 방법",
        "힘든 순간을 이겨내는 법", 
        "일상의 작은 기쁨",
        "자신을 사랑하는 방법",
        "마음의 평화를 찾는 법",
        "새로운 시작의 용기",
        "스트레스 해소법",
        "감사함을 느끼는 법"
    ]
    
    # 샘플 콘텐츠 (3분 구성안에 맞춤)
    sample_contents = {
        "자존감을 높이는 방법": {
            "content": """오늘도 지치셨죠. 

때로는 결과가 없어도 의미가 있습니다. 

잠시 멈춰도 괜찮습니다. 

당신이 지금까지 걸어온 길은 이미 충분히 의미가 있어요. 

작은 성취 하나하나가 당신을 만든 것입니다. 

자신의 장점을 하나씩 적어보세요. 

당신은 생각보다 훨씬 훌륭한 사람입니다. 

내일도 당신을 기다리는 빛이 있습니다.""",
            "visual_elements": ["따뜻한 노을빛 하늘", "평화로운 숲길", "부드러운 파스텔 톤"],
            "audio_elements": ["잔잔한 피아노 멜로디", "따뜻하고 차분한 내레이션"]
        },
        "힘든 순간을 이겨내는 법": {
            "content": """힘든 순간은 누구에게나 찾아옵니다. 

그 순간에는 모든 것이 어려워 보여요. 

하지만 그 순간도 지나갑니다. 

당신은 이미 충분히 강합니다. 

작은 변화부터 시작해보세요. 

하루에 한 걸음씩만 나아가도 충분해요. 

힘들 때는 잠시 쉬어도 됩니다. 

내일은 오늘보다 나아질 거예요. 

당신은 혼자가 아닙니다.""",
            "visual_elements": ["차분한 파도 소리", "안정적인 산 풍경", "따뜻한 크림색 톤"],
            "audio_elements": ["편안한 스트링 음악", "공감되는 내레이션"]
        },
        "일상의 작은 기쁨": {
            "content": """오늘 하루도 잘 버텨줘서 고마워요. 

아침에 마시는 따뜻한 차 한 잔. 

창밖을 바라보며 느끼는 바람. 

지나가는 사람들의 미소. 

이 모든 것이 기적입니다. 

작은 것 하나라도 감사함을 느껴보세요. 

당신의 일상은 이미 아름다워요. 

내일도 이런 작은 기쁨들이 기다리고 있을 거예요. 

오늘 하루도 수고했어요.""",
            "visual_elements": ["아침 햇살", "꽃이 핀 정원", "밝은 노란색 톤"],
            "audio_elements": ["경쾌한 어쿠스틱 기타", "밝고 따뜻한 내레이션"]
        },
        "자신을 사랑하는 방법": {
            "content": """완벽하지 않아도 괜찮아요. 

당신은 그 자체로 소중합니다. 

자신의 감정을 인정해주세요. 

슬플 때는 슬퍼도 됩니다. 

화날 때는 화내도 됩니다. 

그 모든 감정이 당신의 일부예요. 

자신을 용서해주세요. 

실수해도 괜찮습니다. 

당신은 이미 충분히 사랑받을 만한 사람입니다. 

오늘부터 자신을 더 사랑해주세요.""",
            "visual_elements": ["부드러운 구름", "평화로운 호수", "따뜻한 파스텔 톤"],
            "audio_elements": ["감성적인 피아노", "따뜻하고 부드러운 내레이션"]
        },
        "마음의 평화를 찾는 법": {
            "content": """마음이 복잡할 때는 잠시 쉬어보세요. 

깊게 숨을 들이마시고 내쉬세요. 

지금 이 순간에 집중해보세요. 

과거의 상처는 과거에 두세요. 

미래에 대한 걱정은 미래에 맡기세요. 

지금 이 순간만 생각해보세요. 

마음의 소리에 귀 기울여보세요. 

당신이 진짜 원하는 것이 무엇인지. 

마음의 평화는 이미 당신 안에 있어요. 

조용히 마음을 들여다보세요.""",
            "visual_elements": ["고요한 밤하늘", "평온한 숲속", "차분한 푸른색 톤"],
            "audio_elements": ["명상적인 앰비언트", "차분하고 평온한 내레이션"]
        },
        "새로운 시작의 용기": {
            "content": """새로운 시작은 항상 두렵습니다. 

하지만 그 두려움은 성장의 신호예요. 

변화를 두려워하지 마세요. 

당신은 이미 충분히 준비되어 있어요. 

작은 변화부터 시작해보세요. 

한 걸음씩 나아가면 됩니다. 

실패해도 괜찮아요. 

실패는 성공의 어머니입니다. 

새로운 도전을 응원합니다. 

당신은 할 수 있어요.""",
            "visual_elements": ["새벽 하늘", "새싹이 돋는 땅", "희망적인 초록색 톤"],
            "audio_elements": ["희망적인 오케스트라", "격려하는 내레이션"]
        },
        "스트레스 해소법": {
            "content": """스트레스는 현대인의 일상입니다. 

하지만 스트레스는 관리할 수 있어요. 

깊게 숨을 들이마시고 내쉬세요. 

몸을 움직여보세요. 

산책도 좋고, 요가도 좋아요. 

좋아하는 음악을 들어보세요. 

친구와 대화해보세요. 

혼자만의 시간도 가져보세요. 

스트레스는 당신을 성장시킵니다. 

오늘 하루도 잘 버텨주세요.""",
            "visual_elements": ["편안한 카페 분위기", "자연 속 산책로", "편안한 베이지 톤"],
            "audio_elements": ["편안한 재즈", "편안하고 안정적인 내레이션"]
        },
        "감사함을 느끼는 법": {
            "content": """감사함은 마음의 비타민입니다. 

오늘 하루를 살아낼 수 있어서 감사해요. 

숨을 쉴 수 있어서 감사해요. 

먹을 수 있어서 감사해요. 

잘 수 있어서 감사해요. 

사랑하는 사람들이 있어서 감사해요. 

작은 것 하나하나가 기적입니다. 

감사함을 느낄 때 마음이 가벼워져요. 

내일도 감사한 하루가 될 거예요. 

오늘 하루도 감사해요.""",
            "visual_elements": ["따뜻한 노을", "평화로운 마을", "따뜻한 오렌지 톤"],
            "audio_elements": ["따뜻한 포크 음악", "감사함이 담긴 내레이션"]
        }
    }
    
    return sample_themes, sample_contents

def create_folder_structure():
    """날짜별 폴더 구조 생성"""
    base_dir = "./maro_sample_content"
    
    # 기본 폴더 생성
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # 오늘부터 7일간의 폴더 생성
    folders = []
    for i in range(7):
        date = datetime.now() + timedelta(days=i)
        folder_name = date.strftime("%Y%m%d")
        folder_path = os.path.join(base_dir, folder_name)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        folders.append({
            "date": date.strftime("%Y년 %m월 %d일"),
            "folder": folder_name,
            "path": folder_path
        })
    
    return folders

def create_sample_files(folders, themes, contents):
    """각 폴더에 샘플 파일 생성"""
    
    for i, folder_info in enumerate(folders):
        folder_path = folder_info["path"]
        date_str = folder_info["date"]
        
        # 해당 날짜의 테마 선택 (순환)
        theme = themes[i % len(themes)]
        content_data = contents[theme]
        
        # 3분 구성안에 맞는 구조화된 콘텐츠 생성
        sample_content = {
            "type": "daily_comfort",
            "theme": theme,
            "title": f"오늘의 위로: {theme}",
            "date": date_str,
            "duration": "3분",
            "content": content_data["content"],
            "structure": {
                "intro": "10-15초 - 채널 로고 + '오늘의 위로' 타이틀 + 주제 소개",
                "main_message": "120-130초 - 이어지는 위로 글귀 낭독 (6-8개 단락)",
                "outro": "20-30초 - 요약 + '당신은 혼자가 아닙니다' + 다음 영상 안내"
            },
            "timing": {
                "0:00-0:15": "인트로 - 로고 + 제목 카드 + 주제 소개",
                "0:15-2:25": "본문 위로글 - 6-8개 단락으로 이어지는 글귀 낭독",
                "2:25-3:00": "아웃로 - 요약 + 구독/다음 영상 안내"
            },
            "visual_elements": content_data["visual_elements"],
            "audio_elements": content_data["audio_elements"],
            "tags": ["위로", "힐링", "일상위로", "maro", "마음위로", "자존감", "자기계발", "루틴"],
            "production_notes": {
                "bgm_suggestion": "따뜻하고 잔잔한 피아노/스트링 중심",
                "narration_tone": "따뜻하고 공감되는 톤, 문장 끝마다 1-2초 멈춤",
                "visual_style": "자연스럽고 따뜻한 파스텔 톤, 부드러운 전환",
                "subtitle_font": "둥근고딕 또는 산세리프 계열, 가독성 중심"
            }
        }
        
        # JSON 파일로 저장
        json_file = os.path.join(folder_path, f"daily_comfort_{theme.replace(' ', '_')}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(sample_content, f, ensure_ascii=False, indent=2)
        
        # 마크다운 파일로도 저장 (읽기 쉽게)
        md_file = os.path.join(folder_path, f"daily_comfort_{theme.replace(' ', '_')}.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# {sample_content['title']}\n\n")
            f.write(f"**날짜**: {date_str}\n")
            f.write(f"**지속시간**: {sample_content['duration']}\n\n")
            
            f.write("## 📝 콘텐츠 내용\n\n")
            f.write(sample_content['content'].replace('\n\n', '\n\n'))
            f.write("\n\n")
            
            f.write("## ⏰ 시간 배분\n\n")
            for time, desc in sample_content['timing'].items():
                f.write(f"- **{time}**: {desc}\n")
            f.write("\n")
            
            f.write("## 🎨 시각 요소\n\n")
            for element in sample_content['visual_elements']:
                f.write(f"- {element}\n")
            f.write("\n")
            
            f.write("## 🎵 오디오 요소\n\n")
            for element in sample_content['audio_elements']:
                f.write(f"- {element}\n")
            f.write("\n")
            
            f.write("## 🏷️ 태그\n\n")
            f.write(", ".join(sample_content['tags']))
            f.write("\n\n")
            
            f.write("## 📋 제작 노트\n\n")
            notes = sample_content['production_notes']
            f.write(f"- **BGM 제안**: {notes['bgm_suggestion']}\n")
            f.write(f"- **내레이션 톤**: {notes['narration_tone']}\n")
            f.write(f"- **시각 스타일**: {notes['visual_style']}\n")
            f.write(f"- **자막 폰트**: {notes['subtitle_font']}\n")
        
        print(f"✅ {date_str}: {theme} 샘플 생성 완료")
        print(f"   📁 폴더: {folder_path}")
        print(f"   📄 파일: {os.path.basename(json_file)}, {os.path.basename(md_file)}")
        print()

def create_readme_file(base_dir, folders):
    """README 파일 생성"""
    readme_path = os.path.join(base_dir, "README.md")
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# maro 채널 오늘의 위로 샘플 콘텐츠\n\n")
        f.write("## 📁 폴더 구조\n\n")
        f.write("각 날짜별로 오늘의 위로 샘플 콘텐츠가 생성됩니다.\n\n")
        
        f.write("| 날짜 | 폴더명 | 테마 | 파일 형식 |\n")
        f.write("|------|--------|------|-----------|\n")
        
        themes = ["자존감을 높이는 방법", "힘든 순간을 이겨내는 법", "일상의 작은 기쁨", 
                 "자신을 사랑하는 방법", "마음의 평화를 찾는 법", "새로운 시작의 용기", 
                 "스트레스 해소법", "감사함을 느끼는 법"]
        
        for i, folder_info in enumerate(folders):
            theme = themes[i % len(themes)]
            f.write(f"| {folder_info['date']} | {folder_info['folder']} | {theme} | JSON, MD |\n")
        
        f.write("\n## 📋 파일 설명\n\n")
        f.write("- **JSON 파일**: 프로그래밍에서 사용할 수 있는 구조화된 데이터\n")
        f.write("- **MD 파일**: 사람이 읽기 쉬운 마크다운 형식\n\n")
        
        f.write("## 🎯 3분 구성안\n\n")
        f.write("모든 샘플은 3분 위로 콘텐츠 세부 구성안을 따릅니다:\n\n")
        f.write("- **인트로 (10-15초)**: 채널 로고 + 제목 카드 + 주제 소개\n")
        f.write("- **본문 (120-130초)**: 6-8개 단락으로 이어지는 위로 글귀\n")
        f.write("- **아웃로 (20-30초)**: 요약 + 다음 영상 안내\n\n")
        
        f.write("## 🚀 사용 방법\n\n")
        f.write("```python\n")
        f.write("# 샘플 콘텐츠 확인\n")
        f.write("import json\n")
        f.write("with open('20241201/daily_comfort_자존감을_높이는_방법.json', 'r', encoding='utf-8') as f:\n")
        f.write("    content = json.load(f)\n")
        f.write("    print(content['content'])\n")
        f.write("```\n\n")
        
        f.write("## 📝 제작 가이드\n\n")
        f.write("각 샘플 파일에는 다음 정보가 포함되어 있습니다:\n\n")
        f.write("- 콘텐츠 내용 및 구조\n")
        f.write("- 정확한 시간 배분\n")
        f.write("- 시각/오디오 요소 제안\n")
        f.write("- 제작 노트 및 팁\n\n")
        
        f.write("---\n")
        f.write("**생성일**: " + datetime.now().strftime("%Y년 %m월 %d일") + "\n")
        f.write("**maro 채널 콘텐츠 생성기**로 자동 생성되었습니다.\n")
    
    print(f"✅ README 파일 생성 완료: {readme_path}")

def main():
    """메인 실행 함수"""
    print("🚀 maro 채널 오늘의 위로 샘플 콘텐츠 생성 시작")
    print("=" * 60)
    
    try:
        # 샘플 콘텐츠 준비
        print("📝 샘플 콘텐츠 준비 중...")
        themes, contents = create_sample_daily_comfort()
        print(f"✅ {len(themes)}개 테마 준비 완료")
        
        # 폴더 구조 생성
        print("\n📁 폴더 구조 생성 중...")
        folders = create_folder_structure()
        print(f"✅ {len(folders)}개 폴더 생성 완료")
        
        # 샘플 파일 생성
        print("\n📄 샘플 파일 생성 중...")
        create_sample_files(folders, themes, contents)
        
        # README 파일 생성
        print("\n📖 README 파일 생성 중...")
        create_readme_file("./maro_sample_content", folders)
        
        print("\n" + "=" * 60)
        print("🎉 모든 샘플 콘텐츠 생성 완료!")
        print(f"📁 생성 위치: ./maro_sample_content")
        print(f"📅 생성 기간: {folders[0]['date']} ~ {folders[-1]['date']}")
        print(f"📊 총 파일 수: {len(folders) * 2}개 (JSON + MD)")
        print("\n이제 각 폴더에서 샘플 콘텐츠를 확인할 수 있습니다!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
