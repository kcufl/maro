from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import List

def generate_healing_thumbnail(out_path: str, title: str, content_type: str, keywords: List[str] = None):
    """maro 채널용 힐링 썸네일 생성"""
    W, H = 1280, 720
    
    # 콘텐츠 타입별 색상 테마
    color_themes = {
        "daily_comfort": {"bg": (45, 55, 75), "accent": (120, 180, 255), "text": (255, 255, 255)},
        "healing_sound": {"bg": (35, 65, 55), "accent": (100, 200, 150), "text": (255, 255, 255)},
        "overcome_story": {"bg": (65, 45, 65), "accent": (200, 120, 200), "text": (255, 255, 255)},
        "custom_comfort": {"bg": (55, 65, 45), "accent": (180, 200, 120), "text": (255, 255, 255)}
    }
    
    theme = color_themes.get(content_type, color_themes["daily_comfort"])
    
    # 배경 이미지 생성
    img = Image.new("RGB", (W, H), theme["bg"])
    d = ImageDraw.Draw(img)
    
    # 그라데이션 효과 (상단에서 하단으로)
    for y in range(H):
        alpha = int(255 * (y / H) * 0.3)
        color = tuple(int(c * (1 - alpha/255)) for c in theme["bg"])
        d.line([(0, y), (W, y)], fill=color)
    
    # 중앙 원형 그라데이션
    center_x, center_y = W // 2, H // 2
    radius = min(W, H) // 4
    for r in range(radius, 0, -5):
        alpha = int(255 * (1 - r / radius) * 0.2)
        color = tuple(int(c * (1 - alpha/255)) for c in theme["accent"])
        d.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=color)
    
    # 폰트 설정
    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 72)
        font_subtitle = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
        font_keywords = ImageFont.truetype("DejaVuSans.ttf", 36)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_keywords = ImageFont.load_default()
    
    # 채널명 (상단)
    channel_name = "maro"
    d.text((60, 40), channel_name, fill=theme["accent"], font=font_subtitle)
    
    # 제목 (중앙)
    # 제목이 너무 길면 줄바꿈
    title_lines = []
    current_line = ""
    words = title.split()
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if len(test_line) * 36 < W - 120:  # 폰트 크기 고려
            current_line = test_line
        else:
            if current_line:
                title_lines.append(current_line)
            current_line = word
    
    if current_line:
        title_lines.append(current_line)
    
    # 제목 그리기
    title_y = H // 2 - (len(title_lines) * 60) // 2
    for i, line in enumerate(title_lines):
        y_pos = title_y + i * 60
        d.text((W//2, y_pos), line, fill=theme["text"], font=font_title, anchor="mm")
    
    # 하단 장식선
    line_y = H - 120
    d.rectangle([60, line_y, W-60, line_y+3], fill=theme["accent"])
    
    # 키워드 (하단)
    if keywords:
        kw_text = " · ".join(keywords[:3])
        d.text((60, H-80), kw_text, fill=theme["text"], font=font_keywords)
    
    # 콘텐츠 타입 표시 (우상단)
    type_labels = {
        "daily_comfort": "일일 위로",
        "healing_sound": "힐링 사운드",
        "overcome_story": "극복 스토리",
        "custom_comfort": "맞춤 위로"
    }
    
    type_label = type_labels.get(content_type, "위로 콘텐츠")
    
    # 타입 라벨 배경
    label_width = len(type_label) * 30 + 20
    label_height = 40
    label_x = W - label_width - 20
    label_y = 20
    
    d.rectangle([label_x, label_y, label_x + label_width, label_y + label_height], 
                fill=theme["accent"], outline=theme["text"], width=2)
    
    # 타입 라벨 텍스트
    d.text((label_x + label_width//2, label_y + label_height//2), type_label, 
            fill=theme["text"], font=font_keywords, anchor="mm")
    
    img.save(out_path)
    print(f"✅ 힐링 썸네일 생성 완료: {out_path}")

def generate_thumbnail(out_path: str, date_str: str, keywords: List[str]):
    """기존 호환성을 위한 함수 (deprecated)"""
    print("⚠️ 이 함수는 deprecated되었습니다. generate_healing_thumbnail을 사용하세요.")
    generate_healing_thumbnail(out_path, f"maro - {date_str}", "daily_comfort", keywords)
