#!/usr/bin/env python3
"""
maro 채널 "오늘의 위로" 3분 영상 제작기
- 힐링 스타일의 배경
- 한국어 텍스트 오버레이
- 정확한 3분 타이밍
"""

import cv2
import numpy as np
import os
import json
from datetime import datetime

class ComfortVideoCreator:
    def __init__(self):
        self.output_dir = "maro_sample_content"
        self.width = 1920
        self.height = 1080
        self.fps = 30
        
        # 힐링 색상 팔레트
        self.colors = {
            'background': (240, 248, 255),  # 앨리스 블루
            'primary': (70, 130, 180),      # 스틸 블루
            'secondary': (135, 206, 235),   # 스카이 블루
            'accent': (255, 182, 193),      # 라이트 핑크
            'text': (25, 25, 112),          # 미드나이트 블루
            'text_light': (72, 61, 139)     # 다크 슬레이트 블루
        }
        
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
    
    def add_text_with_shadow(self, frame, text, position, font_scale=1.0, color=None, thickness=2):
        """그림자가 있는 텍스트 추가"""
        if color is None:
            color = self.colors['text']
        
        # 그림자 효과
        shadow_pos = (position[0] + 2, position[1] + 2)
        cv2.putText(frame, text, shadow_pos, cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale, (0, 0, 0), thickness + 1)
        
        # 메인 텍스트
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale, color, thickness)
    
    def create_intro_frames(self, duration_seconds=15):
        """인트로 프레임 생성 (15초)"""
        frames = []
        total_frames = int(duration_seconds * self.fps)
        
        intro_texts = [
            "maro",
            "마음위로",
            "오늘의 위로",
            "자존감을 높이는 방법"
        ]
        
        for i in range(total_frames):
            frame = self.create_healing_background("intro")
            
            # 페이드 인 효과
            alpha = min(1.0, i / (self.fps * 2))  # 2초에 걸쳐 페이드 인
            
            # 텍스트 표시
            if i < total_frames // 4:
                text = intro_texts[0]
                font_scale = 3.0
            elif i < total_frames // 2:
                text = intro_texts[1]
                font_scale = 2.5
            elif i < total_frames * 3 // 4:
                text = intro_texts[2]
                font_scale = 2.0
            else:
                text = intro_texts[3]
                font_scale = 1.8
            
            # 텍스트 위치 계산
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
            x = (self.width - text_size[0]) // 2
            y = (self.height + text_size[1]) // 2
            
            # 알파 블렌딩
            overlay = frame.copy()
            self.add_text_with_shadow(overlay, text, (x, y), font_scale, self.colors['text'])
            frame = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)
            
            frames.append(frame)
        
        return frames
    
    def create_main_frames(self, duration_seconds=130):
        """메인 콘텐츠 프레임 생성 (130초)"""
        frames = []
        total_frames = int(duration_seconds * self.fps)
        
        # 메인 메시지들
        main_messages = [
            "자존감은 하루아침에 생기는 것이 아닙니다",
            "작은 실천들이 모여서 만들어지는 것이죠",
            "",
            "첫 번째, 매일 아침 거울을 보며",
            "자신에게 긍정적인 말을 해보세요",
            "",
            "'나는 소중한 사람이야'",
            "'나는 할 수 있어'",
            "",
            "두 번째, 자신만의 성공을 축하하세요",
            "작은 일이라도 완수했을 때",
            "스스로를 격려하는 습관을 만들어보세요",
            "",
            "세 번째, 다른 사람과 비교하지 마세요",
            "각자의 속도가 있고",
            "각자의 길이 있습니다",
            "",
            "네 번째, 자신의 감정을 인정하고",
            "받아들이세요",
            "슬프거나 화가 나는 것도",
            "자연스러운 감정입니다",
            "",
            "다섯 번째, 자신만의 취미나",
            "관심사를 찾아보세요",
            "무엇에든 열정을 쏟을 수 있는",
            "것이 있다는 것은 정말 멋진 일이에요"
        ]
        
        frames_per_message = total_frames // len(main_messages)
        
        for i, message in enumerate(main_messages):
            for j in range(frames_per_message):
                frame = self.create_healing_background("main")
                
                if message:  # 빈 메시지가 아닌 경우
                    # 텍스트 크기 조정
                    if len(message) > 20:
                        font_scale = 1.2
                    elif len(message) > 15:
                        font_scale = 1.5
                    else:
                        font_scale = 1.8
                    
                    # 텍스트 위치 계산
                    text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
                    x = (self.width - text_size[0]) // 2
                    y = (self.height + text_size[1]) // 2
                    
                    # 색상 선택
                    if "'" in message:  # 인용구
                        color = self.colors['primary']
                    else:
                        color = self.colors['text']
                    
                    self.add_text_with_shadow(frame, message, (x, y), font_scale, color)
                
                frames.append(frame)
        
        # 남은 프레임 채우기
        while len(frames) < total_frames:
            frames.append(frames[-1] if frames else self.create_healing_background("main"))
        
        return frames[:total_frames]
    
    def create_outro_frames(self, duration_seconds=35):
        """아웃로 프레임 생성 (35초)"""
        frames = []
        total_frames = int(duration_seconds * self.fps)
        
        outro_texts = [
            "오늘도 자신을 사랑하고",
            "소중히 여기는 하루가 되시길 바랍니다",
            "",
            "maro와 함께하는 위로의 시간이었습니다",
            "",
            "구독과 좋아요는 큰 힘이 됩니다",
            "다음 영상에서 또 만나요"
        ]
        
        frames_per_text = total_frames // len(outro_texts)
        
        for i, text in enumerate(outro_texts):
            for j in range(frames_per_text):
                frame = self.create_healing_background("outro")
                
                if text:  # 빈 텍스트가 아닌 경우
                    font_scale = 1.5 if len(text) > 15 else 1.8
                    
                    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
                    x = (self.width - text_size[0]) // 2
                    y = (self.height + text_size[1]) // 2
                    
                    color = self.colors['text_light']
                    self.add_text_with_shadow(frame, text, (x, y), font_scale, color)
                
                frames.append(frame)
        
        # 남은 프레임 채우기
        while len(frames) < total_frames:
            frames.append(frames[-1] if frames else self.create_healing_background("outro"))
        
        return frames[:total_frames]
    
    def create_video(self, output_filename="maro_comfort_video"):
        """전체 영상 생성"""
        print("🎬 maro 채널 3분 영상 제작 시작")
        print("=" * 50)
        
        # 프레임 생성
        print("📝 인트로 프레임 생성 중... (15초)")
        intro_frames = self.create_intro_frames(15)
        
        print("📝 메인 콘텐츠 프레임 생성 중... (130초)")
        main_frames = self.create_main_frames(130)
        
        print("📝 아웃로 프레임 생성 중... (35초)")
        outro_frames = self.create_outro_frames(35)
        
        # 모든 프레임 합치기
        all_frames = intro_frames + main_frames + outro_frames
        
        print(f"📊 총 프레임 수: {len(all_frames)}")
        print(f"📊 예상 시간: {len(all_frames) / self.fps:.1f}초")
        
        # 비디오 저장
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, f"{output_filename}.mp4")
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        print("💾 비디오 저장 중...")
        for i, frame in enumerate(all_frames):
            out.write(frame)
            if (i + 1) % 100 == 0:
                print(f"진행률: {i + 1}/{len(all_frames)} ({(i + 1) / len(all_frames) * 100:.1f}%)")
        
        out.release()
        
        print(f"✅ 영상 생성 완료: {output_path}")
        print(f"📁 파일 크기: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
        
        return output_path

def main():
    creator = ComfortVideoCreator()
    video_path = creator.create_video("maro_comfort_video")
    
    print("\n🎉 maro 채널 '오늘의 위로' 영상 제작 완료!")
    print(f"영상 파일: {video_path}")

if __name__ == "__main__":
    main()
