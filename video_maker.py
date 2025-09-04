from moviepy.editor import (AudioFileClip, ImageClip, TextClip, CompositeVideoClip, ColorClip)
from typing import List, Dict, Tuple
from pathlib import Path
import srt, datetime
import PIL
import numpy as np

def parse_resolution(res: str) -> Tuple[int,int]:
    w,h = res.split("x")
    return int(w), int(h)

def create_healing_background(W: int, H: int, duration: float, style: str = "calm"):
    """힐링 스타일의 배경 생성"""
    
    if style == "calm":
        # 차분한 그라데이션 배경
        bg_base = ColorClip(size=(W, H), color=(25, 35, 45)).set_duration(duration)
        
        # 부드러운 원형 그라데이션 효과
        center_x, center_y = W // 2, H // 2
        radius = min(W, H) // 3
        
        # 중앙에서 밝아지는 효과
        for i in range(0, radius, 10):
            alpha = int(255 * (1 - i / radius) * 0.1)
            circle = ColorClip(size=(i*2, i*2), color=(100, 120, 140, alpha)).set_duration(duration)
            circle = circle.set_position((center_x - i, center_y - i))
            bg_base = CompositeVideoClip([bg_base, circle])
            
    elif style == "nature":
        # 자연스러운 그라데이션
        bg_base = ColorClip(size=(W, H), color=(30, 50, 40)).set_duration(duration)
        
        # 하단에서 위로 올라가는 그라데이션
        for y in range(0, H, 20):
            alpha = int(255 * (y / H) * 0.3)
            line = ColorClip(size=(W, 20), color=(60, 80, 60, alpha)).set_duration(duration)
            line = line.set_position((0, y))
            bg_base = CompositeVideoClip([bg_base, line])
            
    else:  # default
        bg_base = ColorClip(size=(W, H), color=(40, 50, 60)).set_duration(duration)
    
    return bg_base

def build_srt(segments: List[dict], srt_path: str):
    subs = []
    for i, seg in enumerate(segments, start=1):
        start = datetime.timedelta(seconds=float(seg["start"]))
        end = datetime.timedelta(seconds=float(seg["end"]))
        subs.append(srt.Subtitle(index=i, start=start, end=end, content=seg["text"]))
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subs))

def make_healing_video(audio_path: str, content: Dict, background_image: str, resolution: str, out_path: str, mode: str="landscape"):
    """힐링 콘텐츠용 비디오 생성"""
    W, H = parse_resolution(resolution)
    
    # 배경 이미지 사용 시도
    if background_image and Path(background_image).exists():
        try:
            bg = ImageClip(background_image).resize(newsize=(W,H)).set_duration(content.get("duration_seconds", 180))
            print(f"✅ 배경 이미지 사용: {background_image}")
        except Exception as e:
            print(f"⚠️ 배경 이미지 로드 실패, 힐링 스타일 배경 사용: {e}")
            bg = create_healing_background(W, H, content.get("duration_seconds", 180), "calm")
    else:
        print("🎨 힐링 스타일 배경 생성 중...")
        bg = create_healing_background(W, H, content.get("duration_seconds", 180), "calm")

    # 제목 (상단 중앙)
    title = content.get("title", "maro")
    title_clip = TextClip(txt=title, fontsize=64 if mode=="shorts" else 54, color="white", 
                         method="caption", size=(W-120, None), align="center")
    title_pos = ("center", 80) if mode=="landscape" else ("center", 80)
    title_clip = title_clip.set_position(title_pos).set_start(0).set_duration(3.0)

    # 콘텐츠 타입별 스타일링
    content_type = content.get("type", "daily_comfort")
    
    if content_type == "daily_comfort":
        # 짧은 위로 - 큰 글씨로 중앙 배치
        content_text = content.get("content", "")
        content_clip = TextClip(txt=content_text, fontsize=48 if mode=="shorts" else 36, color="white", 
                               method="caption", size=(W-160, None), align="center")
        content_pos = ("center", H//2)
        content_clip = content_clip.set_position(content_pos).set_start(3.0).set_duration(content.get("duration_seconds", 180) - 3.0)
        
        clips = [bg, title_clip, content_clip]
        
    elif content_type == "healing_sound":
        # 힐링 사운드 - 부드러운 텍스트 애니메이션
        content_text = content.get("content", "")
        # 텍스트를 문장 단위로 분할
        sentences = content_text.split('.')
        
        clips = [bg, title_clip]
        current_time = 3.0
        
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                sentence_clip = TextClip(txt=sentence.strip() + ".", fontsize=40 if mode=="shorts" else 32, 
                                       color="lightblue", method="caption", size=(W-160, None), align="center")
                sentence_pos = ("center", H//2)
                duration = min(8.0, max(3.0, len(sentence) * 0.5))  # 문장 길이에 따른 지속시간
                
                sentence_clip = sentence_clip.set_position(sentence_pos).set_start(current_time).set_duration(duration)
                clips.append(sentence_clip)
                current_time += duration + 1.0  # 1초 간격
                
    elif content_type == "overcome_story":
        # 극복 스토리 - 단계별 텍스트 표시
        content_text = content.get("content", "")
        paragraphs = content_text.split('\n\n')
        
        clips = [bg, title_clip]
        current_time = 3.0
        
        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():
                para_clip = TextClip(txt=paragraph.strip(), fontsize=36 if mode=="shorts" else 28, 
                                   color="white", method="caption", size=(W-160, None), align="West")
                para_pos = (80, 200 + i * 100) if mode=="landscape" else (80, 250 + i * 80)
                duration = min(10.0, max(4.0, len(paragraph) * 0.3))
                
                para_clip = para_clip.set_position(para_pos).set_start(current_time).set_duration(duration)
                clips.append(para_clip)
                current_time += duration + 0.5
                
    else:  # custom_comfort
        # 맞춤형 위로 - 깔끔한 텍스트 배치
        content_text = content.get("content", "")
        content_clip = TextClip(txt=content_text, fontsize=44 if mode=="shorts" else 32, color="white", 
                               method="caption", size=(W-160, None), align="center")
        content_pos = ("center", H//2)
        content_clip = content_clip.set_position(content_pos).set_start(3.0).set_duration(content.get("duration_seconds", 180) - 3.0)
        
        clips = [bg, title_clip, content_clip]

    # 오디오 추가
    try:
        audio = AudioFileClip(audio_path)
        final_clip = CompositeVideoClip(clips).set_audio(audio)
    except Exception as e:
        print(f"⚠️ 오디오 로드 실패: {e}")
        final_clip = CompositeVideoClip(clips)

    # 비디오 생성
    final_clip.write_videofile(out_path, fps=30, codec="libx264", audio_codec="aac", preset="medium")
    return out_path

def make_video(audio_path: str, timeline: List[dict], background_image: str, resolution: str, title: str, out_path: str, mode: str="landscape"):
    """기존 호환성을 위한 함수 (deprecated)"""
    print("⚠️ 이 함수는 deprecated되었습니다. make_healing_video를 사용하세요.")
    return make_healing_video(audio_path, {"title": title, "content": "콘텐츠"}, background_image, resolution, out_path, mode)
