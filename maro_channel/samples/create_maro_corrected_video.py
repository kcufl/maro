#!/usr/bin/env python3
"""
maro 채널 수정된 영상 생성기
- "maro"를 "마로"로 수정
- 아웃트로를 10초로 단축
- 부드러운 목소리 + 배경음악
"""

import os
from openai import OpenAI
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess

class MaroCorrectedVideoCreator:
    def __init__(self):
        # API 키 직접 설정 (임시)
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.output_dir = "maro_sample_content"
        
    def load_script(self):
        """기존 스크립트 로드하고 "maro"를 "마로"로 수정"""
        script_path = os.path.join(self.output_dir, "comfort_zepto_3min_script.txt")
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                script = f.read().strip()
                # "maro"를 "마로"로 수정
                script = script.replace("maro", "마로")
                return script
        return None
    
    def generate_soft_tts(self, text):
        """더 부드러운 TTS 음성 생성"""
        try:
            print(f"🎤 부드러운 TTS 음성 생성 중...")
            print(f"📝 스크립트 길이: {len(text)}자")
            
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",  # 더 부드럽고 자연스러운 목소리
                input=text,
                speed=0.9  # 조금 더 천천히, 부드럽게
            )
            
            # 파일 저장
            os.makedirs(self.output_dir, exist_ok=True)
            audio_path = os.path.join(self.output_dir, "maro_corrected_narration.mp3")
            
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ 부드러운 TTS 음성 생성 완료: {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"❌ TTS 생성 중 오류: {e}")
            return None
    
    def create_video_frames_corrected(self):
        """수정된 영상 프레임 생성 (아웃트로 10초)"""
        print("🎬 수정된 영상 프레임 생성 중...")
        
        # 영상 설정
        width, height = 1920, 1080
        fps = 30
        
        # 한글 폰트 설정
        try:
            font_path = "C:/Windows/Fonts/malgun.ttf"
            font = ImageFont.truetype(font_path, 60)
            title_font = ImageFont.truetype(font_path, 80)
        except:
            print("⚠️ 한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
            font = ImageFont.load_default()
            title_font = ImageFont.load_default()
        
        # 프레임 생성
        frames = []
        
        # 1. 인트로 (15초)
        print("📹 인트로 프레임 생성...")
        for i in range(15 * fps):  # 15초
            # 배경 생성 (부드러운 그라데이션)
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            frame[:, :] = [135, 206, 235]  # 하늘색 배경
            
            # PIL 이미지로 변환
            pil_image = Image.fromarray(frame)
            draw = ImageDraw.Draw(pil_image)
            
            # 제목 텍스트 (마로로 수정)
            title = "마로"
            subtitle = "오늘의 위로 - 자존감 회복"
            
            # 텍스트 중앙 정렬
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (width - subtitle_width) // 2
            
            draw.text((title_x, height//2 - 100), title, fill=(255, 255, 255), font=title_font)
            draw.text((subtitle_x, height//2 + 50), subtitle, fill=(255, 255, 255), font=font)
            
            # OpenCV로 변환
            frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            frames.append(frame)
        
        # 2. 메인 콘텐츠 (155초) - 아웃트로가 10초로 줄어들어서 메인 콘텐츠가 늘어남
        print("📹 메인 콘텐츠 프레임 생성...")
        main_texts = [
            "작은 목표를 설정해보세요",
            "자신의 강점을 찾아보세요", 
            "완벽주의를 버려보세요",
            "자신만의 시간을 가져보세요",
            "긍정적인 사람들과 어울려보세요",
            "자신의 감정을 인정하고 표현해보세요",
            "자신에게 친절하게 대하세요"
        ]
        
        for i, text in enumerate(main_texts):
            for j in range(155 * fps // len(main_texts)):  # 각 텍스트당 동일한 시간
                # 배경 생성
                frame = np.zeros((height, width, 3), dtype=np.uint8)
                frame[:, :] = [240, 248, 255]  # 연한 파란색 배경
                
                # PIL 이미지로 변환
                pil_image = Image.fromarray(frame)
                draw = ImageDraw.Draw(pil_image)
                
                # 텍스트 중앙 정렬
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = (width - text_width) // 2
                
                draw.text((text_x, height//2), text, fill=(50, 50, 50), font=font)
                
                # OpenCV로 변환
                frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                frames.append(frame)
        
        # 3. 아웃트로 (10초) - 10초로 단축
        print("📹 아웃트로 프레임 생성...")
        for i in range(10 * fps):  # 10초
            # 배경 생성
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            frame[:, :] = [255, 228, 196]  # 연한 베이지색 배경
            
            # PIL 이미지로 변환
            pil_image = Image.fromarray(frame)
            draw = ImageDraw.Draw(pil_image)
            
            # 마무리 텍스트 (마로로 수정)
            outro_text = "여러분은 이미 충분히 소중한 사람입니다"
            thanks_text = "마로와 함께하는 위로의 시간이었습니다"
            
            # 텍스트 중앙 정렬
            outro_bbox = draw.textbbox((0, 0), outro_text, font=font)
            outro_width = outro_bbox[2] - outro_bbox[0]
            outro_x = (width - outro_width) // 2
            
            thanks_bbox = draw.textbbox((0, 0), thanks_text, font=font)
            thanks_width = thanks_bbox[2] - thanks_bbox[0]
            thanks_x = (width - thanks_width) // 2
            
            draw.text((outro_x, height//2 - 50), outro_text, fill=(50, 50, 50), font=font)
            draw.text((thanks_x, height//2 + 50), thanks_text, fill=(50, 50, 50), font=font)
            
            # OpenCV로 변환
            frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            frames.append(frame)
        
        print(f"✅ 총 {len(frames)}개 프레임 생성 완료 (총 {len(frames)/fps:.1f}초)")
        return frames, fps
    
    def save_video(self, frames, fps):
        """영상 저장"""
        print("💾 영상 저장 중...")
        
        width, height = 1920, 1080
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_path = os.path.join(self.output_dir, "maro_corrected_video.mp4")
        
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        
        for frame in frames:
            out.write(frame)
        
        out.release()
        print(f"✅ 영상 저장 완료: {video_path}")
        return video_path
    
    def create_background_music(self):
        """배경음악 생성"""
        print("🎵 배경음악 생성 중...")
        
        bg_music_path = os.path.join(self.output_dir, "maro_bg_music.mp3")
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "sine=frequency=220:duration=180",
            "-af", "volume=0.1",
            bg_music_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 배경음악 생성 완료: {bg_music_path}")
            return bg_music_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 배경음악 생성 실패: {e}")
            return None
    
    def merge_audio_simple(self, tts_path, bg_music_path):
        """간단한 오디오 합성"""
        print("🔊 오디오 합성 중...")
        
        final_audio_path = os.path.join(self.output_dir, "maro_corrected_audio_with_bg.mp3")
        
        cmd = [
            "ffmpeg", "-y",
            "-i", tts_path,
            "-i", bg_music_path,
            "-filter_complex", "amix=inputs=2:duration=first",
            final_audio_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 오디오 합성 완료: {final_audio_path}")
            return final_audio_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 오디오 합성 실패: {e}")
            return None
    
    def create_final_video(self, video_path, audio_path):
        """최종 영상 생성"""
        print("🎬 최종 영상 생성 중...")
        
        output_path = os.path.join(self.output_dir, "maro_final_corrected_video.mp4")
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 최종 영상 생성 완료: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"❌ 최종 영상 생성 실패: {e}")
            return None

def main():
    print("🎬 maro 채널 수정된 영상 생성 시작")
    print("=" * 60)
    
    creator = MaroCorrectedVideoCreator()
    
    # 1. 스크립트 로드 및 수정
    print("📝 스크립트 로드 및 수정 중...")
    script = creator.load_script()
    if not script:
        print("❌ 스크립트를 찾을 수 없습니다.")
        return
    
    # 2. 부드러운 TTS 생성
    tts_path = creator.generate_soft_tts(script)
    if not tts_path:
        print("❌ TTS 생성 실패")
        return
    
    # 3. 수정된 영상 프레임 생성
    frames, fps = creator.create_video_frames_corrected()
    
    # 4. 영상 저장
    video_path = creator.save_video(frames, fps)
    
    # 5. 배경음악 생성
    bg_music_path = creator.create_background_music()
    if not bg_music_path:
        print("❌ 배경음악 생성 실패")
        return
    
    # 6. 오디오 합성
    final_audio_path = creator.merge_audio_simple(tts_path, bg_music_path)
    if not final_audio_path:
        print("❌ 오디오 합성 실패")
        return
    
    # 7. 최종 영상 생성
    final_video_path = creator.create_final_video(video_path, final_audio_path)
    
    if final_video_path:
        print(f"\n🎉 수정된 최종 영상 생성 성공!")
        print(f"파일 위치: {final_video_path}")
        print(f"파일 크기: {os.path.getsize(final_video_path) / 1024 / 1024:.2f} MB")
        print("\n🎵 수정된 특징:")
        print("- 'maro' → '마로'로 수정")
        print("- 아웃트로 10초로 단축 (기존 35초 → 10초)")
        print("- 메인 콘텐츠 155초로 확장 (기존 130초 → 155초)")
        print("- 더 부드럽고 자연스러운 목소리 (alloy voice)")
        print("- 조금 더 천천히 말하는 속도 (0.9x)")
        print("- A3 톤 배경음악 (220Hz)")
    else:
        print("\n❌ 최종 영상 생성 실패")

if __name__ == "__main__":
    main()
