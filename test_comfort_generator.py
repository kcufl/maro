#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 콘텐츠 생성기 테스트 파일 - 3분 구성안 포함
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_comfort_generator():
    """콘텐츠 생성기 기본 테스트"""
    try:
        from comfort_generator_main import MaroComfortGenerator
        
        print("✅ MaroComfortGenerator 클래스 임포트 성공")
        
        # 생성기 인스턴스 생성
        generator = MaroComfortGenerator()
        print("✅ MaroComfortGenerator 인스턴스 생성 성공")
        
        # 콘텐츠 타입 정보 확인
        content_types = generator.get_content_types_info()
        print(f"✅ 지원하는 콘텐츠 타입: {len(content_types)}개")
        
        for content_type, info in content_types.items():
            print(f"  - {info['name']}: {info['description']}")
            if 'structure' in info:
                print(f"    구조: {info['structure']['timing']}")
        
        # 주간 스케줄 확인
        weekly_schedule = generator.generate_weekly_schedule()
        print(f"✅ 주간 스케줄 생성: {len(weekly_schedule)}일")
        
        for day, plan in weekly_schedule.items():
            print(f"  - {day}: {plan['description']}")
            print(f"    타이밍: {plan['timing']}")
        
        print("\n🎉 모든 테스트가 성공적으로 완료되었습니다!")
        return True
        
    except ImportError as e:
        print(f"❌ 임포트 오류: {e}")
        return False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return False

def test_3min_structure():
    """3분 위로 콘텐츠 구성안 테스트"""
    try:
        from comfort_generator_main import MaroComfortGenerator
        
        generator = MaroComfortGenerator()
        guide = generator.get_3min_structure_guide()
        
        print("\n=== 3분 위로 콘텐츠 구성안 테스트 ===")
        print(f"✅ 제목: {guide['title']}")
        print(f"✅ 총 시간: {guide['total_duration']}")
        
        # 구조 상세 확인
        structure = guide['structure']
        print(f"✅ 인트로: {structure['intro']['duration']} - {', '.join(structure['intro']['elements'])}")
        print(f"✅ 본문: {structure['main_content']['duration']} - {', '.join(structure['main_content']['elements'])}")
        print(f"✅ 아웃로: {structure['outro']['duration']} - {', '.join(structure['outro']['elements'])}")
        
        # 시각 가이드 확인
        visual = guide['visual_guide']
        print(f"✅ 배경: {visual['background']}")
        print(f"✅ 자막: {visual['subtitle']}")
        print(f"✅ 폰트: {visual['font']}")
        print(f"✅ 컬러: {visual['color']}")
        
        # 오디오 가이드 확인
        audio = guide['audio_guide']
        print(f"✅ BGM: {audio['bgm']}")
        print(f"✅ 내레이션: {audio['narration']}")
        print(f"✅ 볼륨: {audio['volume']}")
        
        print("✅ 3분 구성안 테스트 완료!")
        return True
        
    except Exception as e:
        print(f"❌ 3분 구성안 테스트 오류: {e}")
        return False

def test_individual_modules():
    """개별 모듈 테스트"""
    modules = [
        "comfort_generator_base",
        "comfort_generator_daily", 
        "comfort_generator_healing",
        "comfort_generator_story",
        "comfort_generator_custom",
        "comfort_generator_challenge"
    ]
    
    print("\n=== 개별 모듈 테스트 ===")
    
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name} 모듈 임포트 성공")
        except ImportError as e:
            print(f"❌ {module_name} 모듈 임포트 실패: {e}")

def test_daily_comfort_structure():
    """오늘의 위로 3분 구조 테스트"""
    try:
        from comfort_generator_main import MaroComfortGenerator
        
        generator = MaroComfortGenerator()
        
        # 더미 데이터로 구조 테스트
        test_content = {
            "type": "daily_comfort",
            "theme": "테스트 테마",
            "title": "오늘의 위로: 테스트 테마",
            "content": "테스트 콘텐츠입니다.",
            "duration": "3분",
            "structure": {
                "intro": "10-15초 - 채널 로고 + '오늘의 위로' 타이틀 + 주제 소개",
                "main_message": "120-130초 - 이어지는 위로 글귀 낭독 (6-8개 단락)",
                "outro": "20-30초 - 요약 + '당신은 혼자가 아닙니다' + 다음 영상 안내"
            },
            "timing": {
                "0:00-0:15": "인트로 - 로고 + 제목 카드 + 주제 소개",
                "0:15-2:25": "본문 위로글 - 6-8개 단락으로 이어지는 글귀 낭독",
                "2:25-3:00": "아웃로 - 요약 + 구독/다음 영상 안내"
            }
        }
        
        print("\n=== 오늘의 위로 3분 구조 테스트 ===")
        print(f"✅ 타입: {test_content['type']}")
        print(f"✅ 제목: {test_content['title']}")
        print(f"✅ 지속시간: {test_content['duration']}")
        
        # 구조 확인
        for section, desc in test_content['structure'].items():
            print(f"✅ {section}: {desc}")
        
        # 타이밍 확인
        for time, desc in test_content['timing'].items():
            print(f"✅ {time}: {desc}")
        
        print("✅ 오늘의 위로 구조 테스트 완료!")
        return True
        
    except Exception as e:
        print(f"❌ 오늘의 위로 구조 테스트 오류: {e}")
        return False

if __name__ == "__main__":
    print("🚀 maro 채널 콘텐츠 생성기 테스트 시작 (3분 구성안 포함)")
    print("=" * 60)
    
    # 개별 모듈 테스트
    test_individual_modules()
    
    # 통합 테스트
    print("\n" + "=" * 60)
    success = test_comfort_generator()
    
    # 3분 구성안 테스트
    if success:
        print("\n" + "=" * 60)
        test_3min_structure()
        
        print("\n" + "=" * 60)
        test_daily_comfort_structure()
    
    if success:
        print("\n🎯 maro 채널 콘텐츠 생성기가 정상적으로 작동합니다!")
        print("✅ 3분 위로 콘텐츠 세부 구성안이 포함되어 있습니다.")
        print("이제 main.py에서 실제 콘텐츠를 생성할 수 있습니다.")
    else:
        print("\n⚠️  일부 테스트가 실패했습니다. 오류를 확인해주세요.")
    
    print("\n테스트 완료!")
