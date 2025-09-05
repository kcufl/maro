#!/usr/bin/env python3
"""
API 키 제거 스크립트
- 모든 Python 파일에서 하드코딩된 API 키를 제거
- 환경변수 사용으로 변경
"""

import os
import re
import glob

def remove_api_keys_from_file(file_path):
    """파일에서 API 키 제거"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # API 키 패턴 찾기
        api_key_pattern = r'api_key = "sk-proj-[^"]*"'
        
        if re.search(api_key_pattern, content):
            print(f"🔧 API 키 제거 중: {file_path}")
            
            # API 키를 환경변수 사용으로 변경
            new_content = re.sub(
                api_key_pattern,
                'api_key = os.getenv("OPENAI_API_KEY")',
                content
            )
            
            # 파일에 다시 쓰기
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ API 키 제거 완료: {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생 {file_path}: {e}")
        return False

def main():
    print("🔧 API 키 제거 시작")
    print("=" * 50)
    
    # maro_channel/samples 폴더의 모든 Python 파일 찾기
    python_files = glob.glob("maro_channel/samples/*.py")
    
    modified_files = 0
    
    for file_path in python_files:
        if remove_api_keys_from_file(file_path):
            modified_files += 1
    
    print(f"\n🎉 API 키 제거 완료!")
    print(f"수정된 파일 수: {modified_files}")
    print(f"총 검사한 파일 수: {len(python_files)}")

if __name__ == "__main__":
    main()
