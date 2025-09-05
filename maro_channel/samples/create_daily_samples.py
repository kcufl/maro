#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 날짜별 샘플 콘텐츠 생성기
maro_sample_content 폴더에 날짜별로 샘플 생성
"""

import os
import json
from datetime import datetime, timedelta

def create_daily_samples():
    """날짜별 샘플 콘텐츠 생성"""
    print("🚀 maro 채널 날짜별 샘플 콘텐츠 생성 시작")
    print("=" * 60)
    
    # 샘플 테마들
    themes = [
        "자존감을 높이는 방법",
        "힘든 순간을 이겨내는 법",
        "일상의 작은 기쁨",
        "자신을 사랑하는 방법",
        "마음의 평화를 찾는 법",
        "새로운 시작의 용기",
        "스트레스 해소법",
        "감사함을 느끼는 법",
        "외로움을 극복하는 법",
        "자신감을 키우는 방법",
        "실패 후 다시 일어서는 법",
        "변화에 적응하는 법",
        "불안감을 다루는 법",
        "우울한 기분을 이겨내는 법",
        "새로운 환경에서 견뎌내는 법"
    ]
    
    # 샘플 콘텐츠 템플릿
    content_templates = {
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
        }
    }
    
    # 기본 템플릿 (테마가 없을 때)
    default_template = {
        "content": """오늘 하루도 수고했어요. 

때로는 모든 것이 힘들어 보일 수 있어요. 

하지만 당신은 이미 충분히 잘하고 있습니다. 

작은 것 하나하나가 의미가 있어요. 

자신을 너무 몰아세우지 마세요. 

잠시 쉬어도 괜찮습니다. 

내일은 오늘보다 나아질 거예요. 

당신은 혼자가 아닙니다.""",
        "visual_elements": ["따뜻한 배경", "평화로운 풍경", "부드러운 톤"],
        "audio_elements": ["잔잔한 음악", "따뜻한 내레이션"]
    }
    
    # 7일간의 샘플 생성
    base_dir = "./maro_sample_content"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    created_folders = []
    
    for i in range(7):
        # 날짜 계산
        date = datetime.now() + timedelta(days=i)
        folder_name = date.strftime("%Y%m%d")
        folder_path = os.path.join(base_dir, folder_name)
        
        # 폴더 생성
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # 테마 선택
        theme = themes[i % len(themes)]
        content_data = content_templates.get(theme, default_template)
        
        # 샘플 콘텐츠 생성
        sample_content = {
            "type": "daily_comfort",
            "theme": theme,
            "title": f"오늘의 위로: {theme}",
            "date": date.strftime("%Y년 %m월 %d일"),
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
        
        # 마크다운 파일로도 저장
        md_file = os.path.join(folder_path, f"daily_comfort_{theme.replace(' ', '_')}.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# {sample_content['title']}\n\n")
            f.write(f"**날짜**: {date.strftime('%Y년 %m월 %d일')}\n")
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
        
        created_folders.append({
            "date": date.strftime("%Y년 %m월 %d일"),
            "folder": folder_name,
            "theme": theme,
            "files": [os.path.basename(json_file), os.path.basename(md_file)]
        })
        
        print(f"✅ {date.strftime('%Y년 %m월 %d일')}: {theme} 샘플 생성 완료")
        print(f"   📁 폴더: {folder_path}")
        print(f"   📄 파일: {os.path.basename(json_file)}, {os.path.basename(md_file)}")
        print()
    
    # README 파일 생성
    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# maro 채널 날짜별 샘플 콘텐츠\n\n")
        f.write("## 📁 폴더 구조\n\n")
        f.write("각 날짜별로 오늘의 위로 샘플 콘텐츠가 생성됩니다.\n\n")
        
        f.write("| 날짜 | 폴더명 | 테마 | 파일 형식 |\n")
        f.write("|------|--------|------|-----------|\n")
        
        for folder_info in created_folders:
            f.write(f"| {folder_info['date']} | {folder_info['folder']} | {folder_info['theme']} | JSON, MD |\n")
        
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
    
    print("\n" + "=" * 60)
    print("🎉 모든 날짜별 샘플 콘텐츠 생성 완료!")
    print(f"📁 생성 위치: {base_dir}")
    print(f"📅 생성 기간: {created_folders[0]['date']} ~ {created_folders[-1]['date']}")
    print(f"📊 총 파일 수: {len(created_folders) * 2}개 (JSON + MD)")
    print("\n이제 각 폴더에서 샘플 콘텐츠를 확인할 수 있습니다!")
    
    return created_folders

if __name__ == "__main__":
    create_daily_samples()
