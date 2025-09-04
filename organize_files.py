#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maro 채널 파일 정리 및 폴더 구조 생성 스크립트
기능별로 파일들을 분류하여 체계적인 폴더 구조 생성
"""

import os
import shutil
from datetime import datetime

def create_folder_structure():
    """maro 채널 폴더 구조 생성"""
    
    # 메인 폴더 구조 정의
    folders = {
        "core": {
            "description": "핵심 콘텐츠 생성 모듈",
            "files": [
                "comfort_generator_base.py",
                "comfort_generator_main.py",
                "comfort_generator_daily.py", 
                "comfort_generator_healing.py",
                "comfort_generator_story.py",
                "comfort_generator_custom.py",
                "comfort_generator_challenge.py"
            ]
        },
        "media": {
            "description": "미디어 제작 관련 모듈",
            "files": [
                "video_maker.py",
                "thumbnail_gen.py",
                "tts_openai.py",
                "tts_openai_fixed.py"
            ]
        },
        "upload": {
            "description": "유튜브 업로드 및 관리",
            "files": [
                "uploader_youtube.py",
                "youtube_setup_guide.md"
            ]
        },
        "config": {
            "description": "설정 및 유틸리티",
            "files": [
                "config.py",
                "utils.py",
                "env_example.txt"
            ]
        },
        "scheduling": {
            "description": "스케줄링 및 자동화",
            "files": [
                "schedule_comfort.py",
                "main.py"
            ]
        },
        "testing": {
            "description": "테스트 및 검증",
            "files": [
                "test_comfort_system.py",
                "test_core_functions.py",
                "test_complete_system.py",
                "test_simple_video.py",
                "test_video_only.py",
                "test_youtube_auth.py",
                "test_youtube_auth_headless.py",
                "test_youtube_quick.py",
                "test_youtube_upload.py",
                "test_system_without_youtube.py"
            ]
        },
        "samples": {
            "description": "샘플 콘텐츠 및 생성기",
            "files": [
                "create_sample_content.py"
            ]
        },
        "docs": {
            "description": "문서 및 가이드",
            "files": [
                "README.md",
                "google_cloud_setup_detailed.md"
            ]
        },
        "assets": {
            "description": "미디어 자산",
            "files": [
                "background.jpg",
                "better_news_briefing.mp4",
                "final_news_briefing.mp4",
                "fixed_news_briefing.mp4",
                "pil_news_briefing.mp4",
                "test_complete_system.py",
                "test_narration.mp3",
                "test_simple_news.mp4"
            ]
        },
        "legacy": {
            "description": "기존 뉴스 관련 파일 (참고용)",
            "files": [
                "check_account.py",
                "create_better_news_video.py",
                "create_final_news_video.py",
                "create_fixed_news_video.py",
                "create_korean_news_video.py",
                "create_pil_news_video.py",
                "news_fetcher.py",
                "summarizer_openai.py",
                "setup_assistant.py"
            ]
        }
    }
    
    return folders

def create_directories(base_dir, folders):
    """디렉토리 생성"""
    created_dirs = []
    
    for folder_name, folder_info in folders.items():
        folder_path = os.path.join(base_dir, folder_name)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            created_dirs.append(folder_path)
        
        # README 파일 생성
        readme_path = os.path.join(folder_path, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"# {folder_name.upper()}\n\n")
            f.write(f"## 📋 설명\n\n")
            f.write(f"{folder_info['description']}\n\n")
            f.write(f"## 📁 포함 파일\n\n")
            for file_name in folder_info['files']:
                f.write(f"- `{file_name}`\n")
            f.write(f"\n---\n")
            f.write(f"**생성일**: {datetime.now().strftime('%Y년 %m월 %d일')}\n")
            f.write(f"**maro 채널 파일 정리**로 자동 생성되었습니다.\n")
    
    return created_dirs

def move_files_to_folders(base_dir, folders):
    """파일들을 해당 폴더로 이동"""
    moved_files = []
    not_found_files = []
    
    for folder_name, folder_info in folders.items():
        folder_path = os.path.join(base_dir, folder_name)
        
        for file_name in folder_info['files']:
            source_path = os.path.join(base_dir, file_name)
            target_path = os.path.join(folder_path, file_name)
            
            if os.path.exists(source_path):
                try:
                    shutil.move(source_path, target_path)
                    moved_files.append({
                        "file": file_name,
                        "from": base_dir,
                        "to": folder_path
                    })
                    print(f"✅ {file_name} → {folder_name}/")
                except Exception as e:
                    print(f"❌ {file_name} 이동 실패: {e}")
            else:
                not_found_files.append(file_name)
    
    return moved_files, not_found_files

def create_main_readme(base_dir, folders):
    """메인 README 파일 생성"""
    readme_path = os.path.join(base_dir, "README.md")
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# maro 채널 - 파일 구조 가이드\n\n")
        f.write("마음위로(maro) 채널의 모든 파일들이 기능별로 정리되어 있습니다.\n\n")
        
        f.write("## 📁 폴더 구조\n\n")
        f.write("| 폴더명 | 설명 | 파일 수 |\n")
        f.write("|--------|------|--------|\n")
        
        for folder_name, folder_info in folders.items():
            file_count = len(folder_info['files'])
            f.write(f"| **{folder_name}** | {folder_info['description']} | {file_count}개 |\n")
        
        f.write("\n## 🚀 빠른 시작\n\n")
        f.write("### 1. 기본 설정\n")
        f.write("```bash\n")
        f.write("cd config/\n")
        f.write("# env_example.txt를 .env로 복사하고 API 키 설정\n")
        f.write("```\n\n")
        
        f.write("### 2. 콘텐츠 생성\n")
        f.write("```bash\n")
        f.write("cd core/\n")
        f.write("python comfort_generator_main.py\n")
        f.write("```\n\n")
        
        f.write("### 3. 샘플 콘텐츠 생성\n")
        f.write("```bash\n")
        f.write("cd samples/\n")
        f.write("python create_sample_content.py\n")
        f.write("```\n\n")
        
        f.write("### 4. 테스트 실행\n")
        f.write("```bash\n")
        f.write("cd testing/\n")
        f.write("python test_comfort_system.py\n")
        f.write("```\n\n")
        
        f.write("## 📋 폴더별 상세 설명\n\n")
        
        for folder_name, folder_info in folders.items():
            f.write(f"### 📁 {folder_name.upper()}\n")
            f.write(f"{folder_info['description']}\n\n")
            f.write("**주요 파일:**\n")
            for file_name in folder_info['files']:
                f.write(f"- `{file_name}`\n")
            f.write("\n")
        
        f.write("## 🔧 개발 환경 설정\n\n")
        f.write("```bash\n")
        f.write("pip install -r requirements.txt\n")
        f.write("```\n\n")
        
        f.write("## 📚 주요 기능\n\n")
        f.write("- **콘텐츠 생성**: AI 기반 위로 콘텐츠 자동 생성\n")
        f.write("- **비디오 제작**: MoviePy를 활용한 자동 비디오 제작\n")
        f.write("- **유튜브 업로드**: 자동 업로드 및 플레이리스트 관리\n")
        f.write("- **스케줄링**: 정기적인 콘텐츠 생성 및 업로드\n")
        f.write("- **테스트**: 모든 기능에 대한 종합 테스트\n\n")
        
        f.write("## 🎯 3분 위로 콘텐츠 구성안\n\n")
        f.write("모든 콘텐츠는 다음 구조를 따릅니다:\n\n")
        f.write("- **인트로 (10-15초)**: 채널 로고 + 제목 카드 + 주제 소개\n")
        f.write("- **본문 (120-130초)**: 6-8개 단락으로 이어지는 위로 글귀\n")
        f.write("- **아웃로 (20-30초)**: 요약 + 다음 영상 안내\n\n")
        
        f.write("---\n")
        f.write("**정리일**: " + datetime.now().strftime("%Y년 %m월 %d일") + "\n")
        f.write("**maro 채널 파일 정리 스크립트**로 자동 생성되었습니다.\n")
    
    print(f"✅ 메인 README 생성 완료: {readme_path}")

def create_requirements_file(base_dir):
    """requirements.txt 파일 생성"""
    requirements_path = os.path.join(base_dir, "requirements.txt")
    
    requirements = [
        "# maro 채널 필수 패키지",
        "# 핵심 기능",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "",
        "# 비디오 제작",
        "moviepy>=1.0.3",
        "Pillow>=10.0.0",
        "numpy>=1.24.0",
        "",
        "# 오디오 처리",
        "pydub>=0.25.1",
        "srt>=3.5.2",
        "",
        "# 유튜브 API",
        "google-api-python-client>=2.0.0",
        "google-auth-oauthlib>=1.0.0",
        "google-auth-httplib2>=0.1.0",
        "",
        "# 스케줄링",
        "schedule>=1.2.0",
        "",
        "# 유틸리티",
        "requests>=2.31.0",
        "tqdm>=4.65.0"
    ]
    
    with open(requirements_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(requirements))
    
    print(f"✅ requirements.txt 생성 완료: {requirements_path}")

def create_project_structure(base_dir):
    """프로젝트 구조 시각화 파일 생성"""
    structure_path = os.path.join(base_dir, "PROJECT_STRUCTURE.txt")
    
    structure = """maro 채널 프로젝트 구조
=======================

📁 maro_channel/
├── 📁 core/                    # 핵심 콘텐츠 생성 모듈
│   ├── comfort_generator_base.py
│   ├── comfort_generator_main.py
│   ├── comfort_generator_daily.py
│   ├── comfort_generator_healing.py
│   ├── comfort_generator_story.py
│   ├── comfort_generator_custom.py
│   └── comfort_generator_challenge.py
│
├── 📁 media/                   # 미디어 제작 관련 모듈
│   ├── video_maker.py
│   ├── thumbnail_gen.py
│   ├── tts_openai.py
│   └── tts_openai_fixed.py
│
├── 📁 upload/                  # 유튜브 업로드 및 관리
│   ├── uploader_youtube.py
│   └── youtube_setup_guide.md
│
├── 📁 config/                  # 설정 및 유틸리티
│   ├── config.py
│   ├── utils.py
│   └── env_example.txt
│
├── 📁 scheduling/              # 스케줄링 및 자동화
│   ├── schedule_comfort.py
│   └── main.py
│
├── 📁 testing/                 # 테스트 및 검증
│   ├── test_comfort_system.py
│   ├── test_core_functions.py
│   ├── test_complete_system.py
│   └── ... (기타 테스트 파일들)
│
├── 📁 samples/                 # 샘플 콘텐츠 및 생성기
│   └── create_sample_content.py
│
├── 📁 docs/                    # 문서 및 가이드
│   ├── README.md
│   └── google_cloud_setup_detailed.md
│
├── 📁 assets/                  # 미디어 자산
│   ├── background.jpg
│   ├── *.mp4 (테스트 비디오들)
│   └── *.mp3 (테스트 오디오들)
│
├── 📁 legacy/                  # 기존 뉴스 관련 파일 (참고용)
│   ├── news_fetcher.py
│   ├── summarizer_openai.py
│   └── ... (기타 뉴스 관련 파일들)
│
├── README.md                   # 메인 프로젝트 가이드
├── requirements.txt            # 필수 패키지 목록
└── PROJECT_STRUCTURE.txt       # 이 파일

📋 주요 기능:
- AI 기반 위로 콘텐츠 자동 생성
- 3분 구성안에 맞는 구조화된 콘텐츠
- 자동 비디오 제작 및 편집
- 유튜브 자동 업로드 및 관리
- 정기적인 콘텐츠 스케줄링
- 종합적인 테스트 시스템

🎯 콘텐츠 타입:
1. 오늘의 위로 (Daily Comfort) - 3분
2. 힐링 사운드 + 멘트 (ASMR Comfort) - 10-15분
3. 극복 스토리 시리즈 (Overcome Stories) - 5-8분
4. 맞춤형 위로 시리즈 (Target Healing) - 3-5분
5. 한 줄 위로 챌린지 (One-Line Comfort Challenge) - 3-5분
"""
    
    with open(structure_path, 'w', encoding='utf-8') as f:
        f.write(structure)
    
    print(f"✅ 프로젝트 구조 파일 생성 완료: {structure_path}")

def main():
    """메인 실행 함수"""
    print("🚀 maro 채널 파일 정리 및 폴더 구조 생성 시작")
    print("=" * 70)
    
    try:
        # 기본 디렉토리 설정
        base_dir = "./maro_channel"
        
        # 기존 디렉토리가 있으면 백업
        if os.path.exists(base_dir):
            backup_dir = f"{base_dir}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.move(base_dir, backup_dir)
            print(f"📦 기존 폴더를 백업했습니다: {backup_dir}")
        
        # 새 디렉토리 생성
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        
        # 폴더 구조 정의
        folders = create_folder_structure()
        print(f"📋 {len(folders)}개 폴더 구조 정의 완료")
        
        # 디렉토리 생성
        print("\n📁 디렉토리 생성 중...")
        created_dirs = create_directories(base_dir, folders)
        print(f"✅ {len(created_dirs)}개 디렉토리 생성 완료")
        
        # 파일 이동
        print("\n📄 파일 이동 중...")
        moved_files, not_found_files = move_files_to_folders(base_dir, folders)
        print(f"✅ {len(moved_files)}개 파일 이동 완료")
        
        if not_found_files:
            print(f"⚠️  찾을 수 없는 파일: {', '.join(not_found_files)}")
        
        # 메인 README 생성
        print("\n📖 메인 README 생성 중...")
        create_main_readme(base_dir, folders)
        
        # requirements.txt 생성
        print("\n📦 requirements.txt 생성 중...")
        create_requirements_file(base_dir)
        
        # 프로젝트 구조 파일 생성
        print("\n🗂️  프로젝트 구조 파일 생성 중...")
        create_project_structure(base_dir)
        
        print("\n" + "=" * 70)
        print("🎉 maro 채널 파일 정리 완료!")
        print(f"📁 정리 위치: {base_dir}")
        print(f"📊 총 폴더 수: {len(folders)}개")
        print(f"📄 이동된 파일 수: {len(moved_files)}개")
        print("\n이제 체계적으로 정리된 폴더 구조를 확인할 수 있습니다!")
        print(f"\n📖 자세한 내용은 {base_dir}/README.md를 참고하세요.")
        
        # 폴더별 요약 출력
        print("\n📁 폴더별 요약:")
        for folder_name, folder_info in folders.items():
            file_count = len(folder_info['files'])
            print(f"  📁 {folder_name}/ - {folder_info['description']} ({file_count}개 파일)")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
