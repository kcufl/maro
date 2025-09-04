#!/usr/bin/env python3
"""
maro 채널 자동 스케줄러
매일 지정된 시간에 콘텐츠를 자동으로 생성하고 업로드합니다.
"""

import schedule
import time
import datetime
import logging
from pathlib import Path
from main import run_weekly_schedule

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('maro_scheduler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def run_scheduled_content():
    """스케줄된 콘텐츠 생성 및 업로드"""
    try:
        logging.info("🚀 스케줄된 콘텐츠 생성 시작")
        run_weekly_schedule()
        logging.info("✅ 스케줄된 콘텐츠 생성 완료")
    except Exception as e:
        logging.error(f"❌ 콘텐츠 생성 중 오류 발생: {e}")

def run_backup_content():
    """백업 콘텐츠 생성 (주요 콘텐츠 실패 시)"""
    try:
        logging.info("🔄 백업 콘텐츠 생성 시작")
        from main import create_daily_comfort
        content, video_path, thumb_path = create_daily_comfort()
        logging.info(f"✅ 백업 콘텐츠 생성 완료: {content['title']}")
    except Exception as e:
        logging.error(f"❌ 백업 콘텐츠 생성 실패: {e}")

def health_check():
    """시스템 상태 확인"""
    try:
        # OpenAI API 연결 확인
        from config import OPENAI_API_KEY
        if not OPENAI_API_KEY:
            logging.warning("⚠️ OpenAI API 키가 설정되지 않았습니다")
        
        # YouTube API 설정 확인
        from config import YOUTUBE_CLIENT_SECRETS_FILE
        if Path(YOUTUBE_CLIENT_SECRETS_FILE).exists():
            logging.warning("⚠️ YouTube API 설정 파일이 없습니다")
        
        # 출력 디렉토리 확인
        from config import OUTPUT_DIR
        Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        
        logging.info("✅ 시스템 상태 정상")
        
    except Exception as e:
        logging.error(f"❌ 시스템 상태 확인 실패: {e}")

def main():
    """메인 스케줄러 실행"""
    logging.info("🎯 maro 채널 스케줄러 시작")
    
    # 시스템 상태 확인
    health_check()
    
    # 스케줄 설정
    # 매일 오전 9시에 콘텐츠 생성 (한국 시간)
    schedule.every().day.at("09:00").do(run_scheduled_content)
    
    # 매일 오후 3시에 백업 콘텐츠 생성
    schedule.every().day.at("15:00").do(run_backup_content)
    
    # 매일 자정에 시스템 상태 확인
    schedule.every().day.at("00:00").do(health_check)
    
    # 매시간 간단한 상태 확인
    schedule.every().hour.do(lambda: logging.info("⏰ 스케줄러 실행 중..."))
    
    logging.info("📅 스케줄 설정 완료:")
    logging.info("  - 매일 09:00: 정규 콘텐츠 생성")
    logging.info("  - 매일 15:00: 백업 콘텐츠 생성")
    logging.info("  - 매일 00:00: 시스템 상태 확인")
    logging.info("  - 매시간: 상태 로그")
    
    # 스케줄러 실행
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크
    except KeyboardInterrupt:
        logging.info("🛑 스케줄러 중단됨")
    except Exception as e:
        logging.error(f"❌ 스케줄러 실행 중 오류: {e}")

if __name__ == "__main__":
    main()
