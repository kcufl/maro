#!/usr/bin/env python3
"""
maro 채널 시스템 테스트 스크립트
각 모듈의 기능을 개별적으로 테스트할 수 있습니다.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """모든 모듈 import 테스트"""
    print("🔍 모듈 import 테스트 중...")
    
    try:
        from config import CHANNEL_NAME, CHANNEL_SLOGAN
        print(f"✅ config.py: {CHANNEL_NAME} - {CHANNEL_SLOGAN}")
    except Exception as e:
        print(f"❌ config.py import 실패: {e}")
        return False
    
    try:
        from comfort_generator import ComfortContentGenerator
        print("✅ comfort_generator.py import 성공")
    except Exception as e:
        print(f"❌ comfort_generator.py import 실패: {e}")
        return False
    
    try:
        from video_maker import make_healing_video
        print("✅ video_maker.py import 성공")
    except Exception as e:
        print(f"❌ video_maker.py import 실패: {e}")
        return False
    
    try:
        from thumbnail_gen import generate_healing_thumbnail
        print("✅ thumbnail_gen.py import 성공")
    except Exception as e:
        print(f"❌ thumbnail_gen.py import 실패: {e}")
        return False
    
    try:
        from tts_openai import synthesize_segments
        print("✅ tts_openai.py import 성공")
    except Exception as e:
        print(f"❌ tts_openai.py import 실패: {e}")
        return False
    
    return True

def test_comfort_generator():
    """위로 콘텐츠 생성기 테스트"""
    print("\n🎯 위로 콘텐츠 생성기 테스트 중...")
    
    try:
        from comfort_generator import ComfortContentGenerator
        
        generator = ComfortContentGenerator()
        
        # 오늘의 위로 테스트
        comfort = generator.generate_daily_comfort("일상의 작은 기쁨")
        print(f"✅ 오늘의 위로 생성: {comfort['title']}")
        print(f"   내용 길이: {len(comfort['content'])}자")
        
        # 힐링 사운드 스크립트 테스트
        healing = generator.generate_healing_sound_script("빗소리")
        print(f"✅ 힐링 사운드 스크립트 생성: {healing['title']}")
        
        # 극복 스토리 테스트
        story = generator.generate_overcome_story("취업 실패 후 성공")
        print(f"✅ 극복 스토리 생성: {story['title']}")
        
        # 맞춤형 위로 테스트
        custom = generator.generate_custom_comfort("퇴근 후 무기력할 때")
        print(f"✅ 맞춤형 위로 생성: {custom['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 위로 콘텐츠 생성기 테스트 실패: {e}")
        return False

def test_thumbnail_generation():
    """썸네일 생성 테스트"""
    print("\n🖼️ 썸네일 생성 테스트 중...")
    
    try:
        from thumbnail_gen import generate_healing_thumbnail
        
        # 테스트용 출력 디렉토리 생성
        test_dir = Path("test_output")
        test_dir.mkdir(exist_ok=True)
        
        # 각 콘텐츠 타입별 썸네일 생성 테스트
        content_types = ["daily_comfort", "healing_sound", "overcome_story", "custom_comfort"]
        
        for content_type in content_types:
            thumb_path = test_dir / f"test_thumbnail_{content_type}.jpg"
            generate_healing_thumbnail(
                str(thumb_path), 
                f"테스트 제목 - {content_type}", 
                content_type, 
                ["테스트", "키워드", "maro", "마음위로"]
            )
            
            if thumb_path.exists():
                print(f"✅ {content_type} 썸네일 생성: {thumb_path}")
            else:
                print(f"❌ {content_type} 썸네일 생성 실패")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 썸네일 생성 테스트 실패: {e}")
        return False

def test_video_maker():
    """비디오 메이커 테스트"""
    print("\n🎬 비디오 메이커 테스트 중...")
    
    try:
        from video_maker import create_healing_background, parse_resolution
        
        # 해상도 파싱 테스트
        w, h = parse_resolution("1920x1080")
        print(f"✅ 해상도 파싱: {w}x{h}")
        
        # 배경 생성 테스트
        bg = create_healing_background(w, h, 10.0, "calm")
        print(f"✅ 힐링 배경 생성: {bg.size}")
        
        return True
        
    except Exception as e:
        print(f"❌ 비디오 메이커 테스트 실패: {e}")
        return False

def test_config():
    """설정 파일 테스트"""
    print("\n⚙️ 설정 파일 테스트 중...")
    
    try:
        from config import (
            CHANNEL_NAME, CHANNEL_SLOGAN, CONTENT_TYPES,
            VIDEO_RESOLUTION, OUTPUT_DIR
        )
        
        print(f"✅ 채널명: {CHANNEL_NAME}")
        print(f"✅ 슬로건: {CHANNEL_SLOGAN}")
        print(f"✅ 비디오 해상도: {VIDEO_RESOLUTION}")
        print(f"✅ 출력 디렉토리: {OUTPUT_DIR}")
        
        print("✅ 콘텐츠 타입:")
        for content_type, config in CONTENT_TYPES.items():
            print(f"   - {content_type}: {config['duration']} ({config['upload_frequency']})")
        
        return True
        
    except Exception as e:
        print(f"❌ 설정 파일 테스트 실패: {e}")
        return False

def test_environment():
    """환경 설정 테스트"""
    print("\n🌍 환경 설정 테스트 중...")
    
    # OpenAI API 키 확인
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print(f"✅ OpenAI API 키: {openai_key[:10]}...")
    else:
        print("⚠️ OpenAI API 키가 설정되지 않음")
    
    # YouTube API 설정 파일 확인
    youtube_config = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "./client_secret.json")
    if Path(youtube_config).exists():
        print(f"✅ YouTube API 설정 파일: {youtube_config}")
    else:
        print(f"⚠️ YouTube API 설정 파일 없음: {youtube_config}")
    
    # 출력 디렉토리 생성 테스트
    from config import OUTPUT_DIR
    try:
        Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        print(f"✅ 출력 디렉토리 생성/확인: {OUTPUT_DIR}")
    except Exception as e:
        print(f"❌ 출력 디렉토리 생성 실패: {e}")
        return False
    
    return True

def run_all_tests():
    """모든 테스트 실행"""
    print("🚀 maro 채널 시스템 테스트 시작\n")
    
    tests = [
        ("모듈 Import", test_imports),
        ("환경 설정", test_environment),
        ("설정 파일", test_config),
        ("위로 콘텐츠 생성기", test_comfort_generator),
        ("썸네일 생성", test_thumbnail_generation),
        ("비디오 메이커", test_video_maker),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"📋 {test_name} 테스트")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 테스트 통과\n")
            else:
                print(f"❌ {test_name} 테스트 실패\n")
        except Exception as e:
            print(f"❌ {test_name} 테스트 오류: {e}\n")
    
    print(f"🎯 테스트 결과: {passed}/{total} 통과")
    
    if passed == total:
        print("🎉 모든 테스트가 통과했습니다! 시스템이 정상적으로 작동합니다.")
        return True
    else:
        print("⚠️ 일부 테스트가 실패했습니다. 설정을 확인해주세요.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
