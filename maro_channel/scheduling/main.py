import os, datetime
from pathlib import Path
from config import (CHANNEL_NAME, CHANNEL_SLOGAN, CHANNEL_TITLE_PREFIX,
                    OUTPUT_DIR, BACKGROUND_IMAGE, VIDEO_RESOLUTION,
                    YOUTUBE_CLIENT_SECRETS_FILE, CONTENT_TYPES)
from comfort_generator import ComfortContentGenerator
from tts_openai import synthesize_segments, concat_audio
from video_maker import make_healing_video
from thumbnail_gen import generate_healing_thumbnail
from uploader_youtube import get_service, upload_video, get_or_create_playlist, add_video_to_playlist
from utils import ensure_dir

def create_daily_comfort():
    """오늘의 위로 콘텐츠 생성 (매일)"""
    print("🌅 오늘의 위로 콘텐츠 생성 중...")
    
    generator = ComfortContentGenerator()
    content = generator.generate_daily_comfort()
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(OUTPUT_DIR) / today / "daily_comfort"
    ensure_dir(out_dir)
    
    # TTS 생성
    segments = [content["content"]]
    parts = synthesize_segments(segments, out_dir / "audio")
    concat_audio(parts, out_dir / "narration.mp3")
    
    # 콘텐츠에 지속시간 정보 추가
    content["duration_seconds"] = parts[0]["duration"] + 3.0  # 3초 제목 시간 추가
    
    # 썸네일 생성
    thumb_path = str(out_dir / "thumbnail.jpg")
    generate_healing_thumbnail(thumb_path, content["title"], content["type"], content["tags"])
    
    # 비디오 생성
    video_path = str(out_dir / "daily_comfort.mp4")
    make_healing_video(str(out_dir / "narration.mp3"), content, BACKGROUND_IMAGE, VIDEO_RESOLUTION, video_path)
    
    return content, video_path, thumb_path

def create_healing_sound():
    """힐링 사운드 콘텐츠 생성 (화,토)"""
    print("🌿 힐링 사운드 콘텐츠 생성 중...")
    
    generator = ComfortContentGenerator()
    content = generator.generate_healing_sound_script()
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(OUTPUT_DIR) / today / "healing_sound"
    ensure_dir(out_dir)
    
    # TTS 생성
    segments = [content["content"]]
    parts = synthesize_segments(segments, out_dir / "audio")
    concat_audio(parts, out_dir / "narration.mp3")
    
    # 콘텐츠에 지속시간 정보 추가
    content["duration_seconds"] = parts[0]["duration"] + 3.0
    
    # 썸네일 생성
    thumb_path = str(out_dir / "thumbnail.jpg")
    generate_healing_thumbnail(thumb_path, content["title"], content["type"], content["tags"])
    
    # 비디오 생성
    video_path = str(out_dir / "healing_sound.mp4")
    make_healing_video(str(out_dir / "narration.mp3"), content, BACKGROUND_IMAGE, VIDEO_RESOLUTION, video_path)
    
    return content, video_path, thumb_path

def create_overcome_story():
    """극복 스토리 콘텐츠 생성 (수요일)"""
    print("💪 극복 스토리 콘텐츠 생성 중...")
    
    generator = ComfortContentGenerator()
    content = generator.generate_overcome_story()
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(OUTPUT_DIR) / today / "overcome_story"
    ensure_dir(out_dir)
    
    # TTS 생성
    segments = [content["content"]]
    parts = synthesize_segments(segments, out_dir / "audio")
    concat_audio(parts, out_dir / "narration.mp3")
    
    # 콘텐츠에 지속시간 정보 추가
    content["duration_seconds"] = parts[0]["duration"] + 3.0
    
    # 썸네일 생성
    thumb_path = str(out_dir / "thumbnail.jpg")
    generate_healing_thumbnail(thumb_path, content["title"], content["type"], content["tags"])
    
    # 비디오 생성
    video_path = str(out_dir / "overcome_story.mp4")
    make_healing_video(str(out_dir / "narration.mp3"), content, BACKGROUND_IMAGE, VIDEO_RESOLUTION, video_path)
    
    return content, video_path, thumb_path

def create_custom_comfort():
    """맞춤형 위로 콘텐츠 생성 (금요일)"""
    print("🎯 맞춤형 위로 콘텐츠 생성 중...")
    
    generator = ComfortContentGenerator()
    content = generator.generate_custom_comfort()
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    out_dir = Path(OUTPUT_DIR) / today / "custom_comfort"
    ensure_dir(out_dir)
    
    # TTS 생성
    segments = [content["content"]]
    parts = synthesize_segments(segments, out_dir / "audio")
    concat_audio(parts, out_dir / "narration.mp3")
    
    # 콘텐츠에 지속시간 정보 추가
    content["duration_seconds"] = parts[0]["duration"] + 3.0
    
    # 썸네일 생성
    thumb_path = str(out_dir / "thumbnail.jpg")
    generate_healing_thumbnail(thumb_path, content["title"], content["type"], content["tags"])
    
    # 비디오 생성
    video_path = str(out_dir / "custom_comfort.mp4")
    make_healing_video(str(out_dir / "narration.mp3"), content, BACKGROUND_IMAGE, VIDEO_RESOLUTION, video_path)
    
    return content, video_path, thumb_path

def upload_to_youtube(content: dict, video_path: str, thumb_path: str):
    """YouTube에 업로드"""
    try:
        youtube = get_service(str(YOUTUBE_CLIENT_SECRETS_FILE))
        
        # 설명 생성
        description = f"""
{content['title']}

{content['content'][:200]}...

#maro #마음위로 #위로 #힐링 #일상위로

구독과 좋아요 부탁드립니다 💙
        """.strip()
        
        # 업로드
        video_id = upload_video(
            youtube, video_path, content["title"], description, 
            tags=content["tags"], privacy_status="public", thumbnail_path=thumb_path
        )
        
        # 재생목록에 추가
        content_type = content["type"]
        playlist_name = CONTENT_TYPES[content_type]["upload_frequency"]
        pl_id = get_or_create_playlist(youtube, f"maro - {playlist_name}", 
                                     f"maro {playlist_name} 콘텐츠")
        add_video_to_playlist(youtube, pl_id, video_id)
        
        print(f"✅ YouTube 업로드 완료: {video_id}")
        return video_id
        
    except Exception as e:
        print(f"❌ YouTube 업로드 실패: {e}")
        return None

def run_weekly_schedule():
    """주간 콘텐츠 스케줄 실행"""
    today = datetime.datetime.now()
    weekday = today.weekday()  # 0=월요일, 1=화요일, ...
    
    print(f"📅 {today.strftime('%Y-%m-%d')} ({['월', '화', '수', '목', '금', '토', '일'][weekday]}요일) 콘텐츠 생성 시작")
    
    if weekday in [0, 2, 6]:  # 월, 수, 일 - 오늘의 위로
        content, video_path, thumb_path = create_daily_comfort()
        print(f"✅ 오늘의 위로 생성 완료: {content['title']}")
        
    elif weekday in [1, 5]:  # 화, 토 - 힐링 사운드
        content, video_path, thumb_path = create_healing_sound()
        print(f"✅ 힐링 사운드 생성 완료: {content['title']}")
        
    elif weekday == 3:  # 수요일 - 극복 스토리
        content, video_path, thumb_path = create_overcome_story()
        print(f"✅ 극복 스토리 생성 완료: {content['title']}")
        
    elif weekday == 4:  # 금요일 - 맞춤형 위로
        content, video_path, thumb_path = create_custom_comfort()
        print(f"✅ 맞춤형 위로 생성 완료: {content['title']}")
    
    # YouTube 업로드
    video_id = upload_to_youtube(content, video_path, thumb_path)
    
    # 결과 저장
    today_str = today.strftime("%Y-%m-%d")
    out_dir = Path(OUTPUT_DIR) / today_str
    (out_dir / "upload_result.txt").write_text(
        f"콘텐츠 타입: {content['type']}\n"
        f"제목: {content['title']}\n"
        f"YouTube ID: {video_id or '업로드 실패'}\n"
        f"생성 시간: {datetime.datetime.now()}\n",
        encoding="utf-8"
    )
    
    print(f"🎉 {today_str} 콘텐츠 생성 및 업로드 완료!")

def run_once():
    """단일 콘텐츠 생성 (테스트용)"""
    print("🧪 단일 콘텐츠 생성 (테스트 모드)")
    content, video_path, thumb_path = create_daily_comfort()
    print(f"✅ 테스트 콘텐츠 생성 완료: {content['title']}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_once()
    else:
        run_weekly_schedule()
