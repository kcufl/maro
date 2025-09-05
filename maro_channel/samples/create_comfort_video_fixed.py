#!/usr/bin/env python3
"""
maro 채널 "오늘의 위로" 3분 영상 제작기 (한글 폰트 + 정확한 타이밍 수정)
- PIL/Pillow로 한글 텍스트 렌더링
- 정확한 3분(180초) 타이밍
- 힐링 스타일의 배경
"""

import cv2
import numpy as np
import os
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import tempfile

class ComfortVideoCreatorFixed:
    def __init__(self):
        self.output_dir = "maro_sample_content"
        self.width = 1920
        self.height = 1080
        self.fps = 30
        
        # 정확한 3분 타이밍
        self.intro_duration = 15  # 15초
        self.main_duration = 130  # 130초
        self.outro_duration = 35  # 35초
        self.total_duration = 180  # 3분
        
        # 힐링 색상 팔레트
        self.colors = {
            'background': (240, 248, 255),  # 앨리스 블루
            'primary': (70, 130, 180),      # 스틸 블루
            'secondary': (135, 206, 235),   # 스카이 블루
            'accent': (255, 182, 193),      # 라이트 핑크
            'text': (25, 25, 112),          # 미드나이트 블루
            'text_light': (72, 61, 139)     # 다크 슬레이트 블루
        }
        
        # 한글 폰트 설정
        self.setup_korean_font()
        
    def setup_korean_font(self):
        """한글 폰트 설정"""
        try:
            # Windows 시스템 폰트 경로들
            font_paths = [
                "C:/Windows/Fonts/malgun.ttf",  # 맑은 고딕
                "C:/Windows/Fonts/gulim.ttc",   # 굴림
                "C:/Windows/Fonts/batang.ttc",  # 바탕
                "C:/Windows/Fonts/arial.ttf",   # Arial (영문)
            ]
            
            self.fonts = {}
            for size in [40, 60, 80, 100, 120]:
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        try:
                            self.fonts[size] = ImageFont.truetype(font_path, size)
                            print(f"✅ 폰트 로드 성공: {font_path} (크기: {size})")
                            break
                        except:
                            continue
                else:
                    # 폰트를 찾지 못한 경우 기본 폰트 사용
                    self.fonts[size] = ImageFont.load_default()
                    print(f"⚠️ 기본 폰트 사용 (크기: {size})")
            
            if not self.fonts:
                raise Exception("사용 가능한 폰트가 없습니다.")
                
        except Exception as e:
            print(f"❌ 폰트 설정 오류: {e}")
            # 기본 폰트로 폴백
            self.fonts = {size: ImageFont.load_default() for size in [40, 60, 80, 100, 120]}
    
    def create_healing_background(self, frame_type="main"):
        """힐링 스타일의 배경 생성"""
        if frame_type == "intro":
            # 인트로: 그라데이션 배경
            bg = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            for y in range(self.height):
                ratio = y / self.height
                color = (
                    int(self.colors['background'][0] * (1 - ratio) + self.colors['primary'][0] * ratio),
                    int(self.colors['background'][1] * (1 - ratio) + self.colors['primary'][1] * ratio),
                    int(self.colors['background'][2] * (1 - ratio) + self.colors['primary'][2] * ratio)
                )
                bg[y, :] = color
        elif frame_type == "outro":
            # 아웃로: 따뜻한 그라데이션
            bg = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            for y in range(self.height):
                ratio = y / self.height
                color = (
                    int(self.colors['primary'][0] * (1 - ratio) + self.colors['accent'][0] * ratio),
                    int(self.colors['primary'][1] * (1 - ratio) + self.colors['accent'][1] * ratio),
                    int(self.colors['primary'][2] * (1 - ratio) + self.colors['accent'][2] * ratio)
                )
                bg[y, :] = color
        else:
            # 메인: 부드러운 단색
            bg = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        return bg
    
    def add_korean_text(self, frame, text, position, font_size=80, color=None):
        """한글 텍스트를 PIL로 렌더링하여 OpenCV 프레임에 추가"""
        if color is None:
            color = self.colors['text']
        
        # OpenCV BGR을 PIL RGB로 변환
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)
        draw = ImageDraw.Draw(pil_image)
        
        # 폰트 선택
        font = self.fonts.get(font_size, self.fonts[80])
        
        # 텍스트 크기 계산
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 텍스트 위치 조정 (중앙 정렬)
        x = position[0] - text_width // 2
        y = position[1] - text_height // 2
        
        # 그림자 효과
        shadow_offset = 3
        draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 128))
        
        # 메인 텍스트
        draw.text((x, y), text, font=font, fill=color)
        
        # PIL 이미지를 OpenCV로 변환
        frame_bgr = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return frame_bgr
    
    def create_intro_frames(self):
        """인트로 프레임 생성 (정확히 15초)"""
        frames = []
        total_frames = int(self.intro_duration * self.fps)  # 450 프레임
        
        intro_texts = [
            ("maro", 100),
            ("마음위로", 80),
            ("오늘의 위로", 70),
            ("자존감을 높이는 방법", 60)
        ]
        
        frames_per_text = total_frames // len(intro_texts)
        
        for i, (text, font_size) in enumerate(intro_texts):
            for j in range(frames_per_text):
                frame = self.create_healing_background("intro")
                
                # 페이드 인 효과
                alpha = min(1.0, j / (frames_per_text * 0.3))  # 30% 구간에서 페이드 인
                
                # 텍스트 추가
                center_x = self.width // 2
                center_y = self.height // 2
                
                frame = self.add_korean_text(frame, text, (center_x, center_y), font_size)
                
                # 알파 블렌딩 (페이드 인 효과)
                if alpha < 1.0:
                    overlay = frame.copy()
                    frame = cv2.addWeighted(frame, alpha, overlay, 1 - alpha, 0)
                
                frames.append(frame)
        
        # 남은 프레임 채우기
        while len(frames) < total_frames:
            frames.append(frames[-1] if frames else self.create_healing_background("intro"))
        
        return frames[:total_frames]
    
    def create_main_frames(self):
        """메인 콘텐츠 프레임 생성 (정확히 130초)"""
        frames = []
        total_frames = int(self.main_duration * self.fps)  # 3900 프레임
        
        # 메인 메시지들 (더 많은 내용으로 130초 채우기)
        main_messages = [
            ("자존감은 하루아침에 생기는 것이 아닙니다", 60),
            ("작은 실천들이 모여서 만들어지는 것이죠", 60),
            ("", 0),  # 빈 화면
            ("첫 번째, 매일 아침 거울을 보며", 60),
            ("자신에게 긍정적인 말을 해보세요", 60),
            ("", 0),
            ("'나는 소중한 사람이야'", 70),
            ("'나는 할 수 있어'", 70),
            ("'나는 충분히 좋은 사람이야'", 60),
            ("", 0),
            ("두 번째, 자신만의 성공을 축하하세요", 60),
            ("작은 일이라도 완수했을 때", 60),
            ("스스로를 격려하는 습관을 만들어보세요", 60),
            ("", 0),
            ("세 번째, 다른 사람과 비교하지 마세요", 60),
            ("각자의 속도가 있고", 70),
            ("각자의 길이 있습니다", 70),
            ("", 0),
            ("네 번째, 자신의 감정을 인정하고", 60),
            ("받아들이세요", 80),
            ("슬프거나 화가 나는 것도", 60),
            ("자연스러운 감정입니다", 60),
            ("", 0),
            ("다섯 번째, 자신만의 취미나", 60),
            ("관심사를 찾아보세요", 70),
            ("무엇에든 열정을 쏟을 수 있는", 60),
            ("것이 있다는 것은 정말 멋진 일이에요", 60),
            ("", 0),
            ("이 모든 것들이 모여서", 70),
            ("여러분의 자존감을 높여줄 것입니다", 60),
            ("", 0),
            ("오늘부터 작은 실천을 시작해보세요", 60),
            ("여러분은 이미 충분히 소중한 사람입니다", 60)
        ]
        
        frames_per_message = total_frames // len(main_messages)
        
        for i, (message, font_size) in enumerate(main_messages):
            for j in range(frames_per_message):
                frame = self.create_healing_background("main")
                
                if message:  # 빈 메시지가 아닌 경우
                    center_x = self.width // 2
                    center_y = self.height // 2
                    
                    # 색상 선택
                    if "'" in message:  # 인용구
                        color = self.colors['primary']
                    else:
                        color = self.colors['text']
                    
                    frame = self.add_korean_text(frame, message, (center_x, center_y), font_size, color)
                
                frames.append(frame)
        
        # 남은 프레임 채우기
        while len(frames) < total_frames:
            frames.append(frames[-1] if frames else self.create_healing_background("main"))
        
        return frames[:total_frames]
    
    def create_outro_frames(self):
        """아웃로 프레임 생성 (정확히 35초)"""
        frames = []
        total_frames = int(self.outro_duration * self.fps)  # 1050 프레임
        
        outro_texts = [
            ("오늘도 자신을 사랑하고", 70),
            ("소중히 여기는 하루가 되시길 바랍니다", 60),
            ("", 0),
            ("maro와 함께하는 위로의 시간이었습니다", 60),
            ("", 0),
            ("구독과 좋아요는 큰 힘이 됩니다", 60),
            ("다음 영상에서 또 만나요", 70),
            ("", 0),
            ("감사합니다", 80)
        ]
        
        frames_per_text = total_frames // len(outro_texts)
        
        for i, (text, font_size) in enumerate(outro_texts):
            for j in range(frames_per_text):
                frame = self.create_healing_background("outro")
                
                if text:  # 빈 텍스트가 아닌 경우
                    center_x = self.width // 2
                    center_y = self.height // 2
                    
                    color = self.colors['text_light']
                    frame = self.add_korean_text(frame, text, (center_x, center_y), font_size, color)
                
                frames.append(frame)
        
        # 남은 프레임 채우기
        while len(frames) < total_frames:
            frames.append(frames[-1] if frames else self.create_healing_background("outro"))
        
        return frames[:total_frames]
    
    def create_video(self, output_filename="maro_comfort_video_fixed"):
        """전체 영상 생성 (정확히 3분)"""
        print("🎬 maro 채널 3분 영상 제작 시작 (한글 폰트 + 정확한 타이밍)")
        print("=" * 60)
        
        # 프레임 생성
        print(f"📝 인트로 프레임 생성 중... ({self.intro_duration}초)")
        intro_frames = self.create_intro_frames()
        
        print(f"📝 메인 콘텐츠 프레임 생성 중... ({self.main_duration}초)")
        main_frames = self.create_main_frames()
        
        print(f"📝 아웃로 프레임 생성 중... ({self.outro_duration}초)")
        outro_frames = self.create_outro_frames()
        
        # 모든 프레임 합치기
        all_frames = intro_frames + main_frames + outro_frames
        
        print(f"📊 총 프레임 수: {len(all_frames)}")
        print(f"📊 예상 시간: {len(all_frames) / self.fps:.1f}초 ({len(all_frames) / self.fps / 60:.1f}분)")
        print(f"📊 목표 시간: {self.total_duration}초 (3분)")
        
        # 비디오 저장
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, f"{output_filename}.mp4")
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        print("💾 비디오 저장 중...")
        for i, frame in enumerate(all_frames):
            out.write(frame)
            if (i + 1) % 500 == 0:
                print(f"진행률: {i + 1}/{len(all_frames)} ({(i + 1) / len(all_frames) * 100:.1f}%)")
        
        out.release()
        
        print(f"✅ 영상 생성 완료: {output_path}")
        print(f"📁 파일 크기: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
        
        return output_path

def main():
    creator = ComfortVideoCreatorFixed()
    video_path = creator.create_video("maro_comfort_video_fixed")
    
    print("\n🎉 maro 채널 '오늘의 위로' 영상 제작 완료!")
    print(f"영상 파일: {video_path}")
    print("📺 한글 텍스트와 정확한 3분 타이밍이 적용되었습니다!")

if __name__ == "__main__":
    main()
