import os
import time
import hashlib
from typing import Tuple, Optional
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class SignLanguageService:
    """
    Service for generating sign language videos from text.

    NOTE: This is a placeholder implementation that generates demo videos.
    For production, you would integrate with:
    - Pre-recorded ASL video datasets (e.g., WLASL dataset)
    - 3D avatar animation systems
    - Machine learning models for sign language generation
    """

    def __init__(self, output_dir: str = "./output/videos"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_video(self, text: str, format: str = "mp4") -> Tuple[str, float]:
        """
        Generate a sign language video from text.

        Args:
            text: Input text to convert to sign language
            format: Output format (mp4 or gif)

        Returns:
            Tuple of (video_path, duration)
        """
        # Create unique filename based on text hash and timestamp
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        timestamp = int(time.time())
        filename = f"sign_{text_hash}_{timestamp}.{format}"
        filepath = os.path.join(self.output_dir, filename)

        # Generate the video (placeholder implementation)
        duration = self._create_demo_video(text, filepath, format)

        return filepath, duration

    def _create_demo_video(self, text: str, output_path: str, format: str) -> float:
        """
        Creates a demo video with text animation.

        In production, replace this with:
        - Real ASL video stitching from a dataset
        - 3D avatar animation rendering
        - ML-generated sign language videos
        """
        # Video parameters
        width, height = 640, 480
        fps = 30

        # Calculate duration based on text length (roughly 0.5s per word)
        words = text.split()
        duration = max(2.0, len(words) * 0.5)
        total_frames = int(duration * fps)

        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_video = output_path.replace(f'.{format}', '_temp.mp4')
        video_writer = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))

        try:
            # Generate frames
            for frame_num in range(total_frames):
                # Create frame with gradient background
                frame = self._create_frame_background(width, height, frame_num, total_frames)

                # Add animated text
                progress = frame_num / total_frames
                current_word_idx = int(progress * len(words))
                if current_word_idx < len(words):
                    current_word = words[current_word_idx]
                    frame = self._add_text_to_frame(frame, current_word, frame_num)

                # Add "signing" hand animation placeholder
                frame = self._add_hand_animation(frame, frame_num, total_frames)

                video_writer.write(frame)

        finally:
            video_writer.release()

        # Convert to GIF if requested
        if format == "gif":
            self._convert_to_gif(temp_video, output_path)
            os.remove(temp_video)
        else:
            os.rename(temp_video, output_path)

        return duration

    def _create_frame_background(self, width: int, height: int, frame_num: int, total_frames: int) -> np.ndarray:
        """Create an animated gradient background"""
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Animated gradient
        phase = (frame_num / total_frames) * 2 * np.pi
        for y in range(height):
            color_value = int(100 + 50 * np.sin(phase + y / height * np.pi))
            frame[y, :] = [color_value, 150, 200]

        return frame

    def _add_text_to_frame(self, frame: np.ndarray, text: str, frame_num: int) -> np.ndarray:
        """Add text overlay to frame"""
        # Convert to PIL for better text rendering
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)

        # Try to use a nice font, fall back to default if not available
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except:
            font = ImageFont.load_default()

        # Calculate text position (centered)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        x = (pil_image.width - text_width) // 2
        y = pil_image.height - 100

        # Draw text with shadow
        draw.text((x + 2, y + 2), text, fill=(0, 0, 0), font=font)
        draw.text((x, y), text, fill=(255, 255, 255), font=font)

        # Convert back to OpenCV format
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    def _add_hand_animation(self, frame: np.ndarray, frame_num: int, total_frames: int) -> np.ndarray:
        """Add placeholder hand animation"""
        height, width = frame.shape[:2]

        # Animated circle representing hand position
        phase = (frame_num / total_frames) * 4 * np.pi
        center_x = int(width // 2 + 100 * np.sin(phase))
        center_y = int(height // 2 + 50 * np.cos(phase * 1.5))

        # Draw hand placeholder (circle)
        cv2.circle(frame, (center_x, center_y), 30, (255, 200, 100), -1)
        cv2.circle(frame, (center_x, center_y), 30, (0, 0, 0), 2)

        # Add text label
        cv2.putText(frame, "ASL Sign", (center_x - 40, center_y - 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        return frame

    def _convert_to_gif(self, video_path: str, gif_path: str):
        """Convert MP4 video to GIF"""
        cap = cv2.VideoCapture(video_path)
        frames = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Convert BGR to RGB and reduce size for GIF
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            # Resize to reduce file size
            pil_image = pil_image.resize((320, 240), Image.Resampling.LANCZOS)
            frames.append(pil_image)

        cap.release()

        if frames:
            # Save as GIF
            frames[0].save(
                gif_path,
                save_all=True,
                append_images=frames[1:],
                duration=33,  # ~30fps
                loop=0,
                optimize=True
            )

    def get_video_info(self, video_path: str) -> Optional[dict]:
        """Get information about a video file"""
        if not os.path.exists(video_path):
            return None

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None

        info = {
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "duration": cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS) if cap.get(cv2.CAP_PROP_FPS) > 0 else 0,
        }

        cap.release()
        return info
