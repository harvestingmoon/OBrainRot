from moviepy.editor import VideoFileClip
import os

def trim_video(input_path, output_path, start_time, end_time):
    """
    Trims a video from a specified start time to an end time.

    Args:
        input_path (str): Path to the input video file.
        output_path (str): Path to save the trimmed video.
        start_time (int): Start time in seconds for the trimmed video.
        end_time (int): End time in seconds for the trimmed video.
    """
    try:
        video_clip = VideoFileClip(input_path)
        trimmed_clip = video_clip.subclip(start_time, end_time)
        trimmed_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        trimmed_clip.close()
        video_clip.close()
        print(f"Video trimmed and saved to: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_video = "../assets/trimed.mp4"  # Replace with the path to your 2-minute video
    output_video = "test1.mp4"
    trim_start_seconds = 0  # Start from the beginning
    trim_end_seconds = 10   # Trim to 10 seconds

    # Create a dummy 2-minute video for testing if it doesn't exist
    if not os.path.exists(input_video):
        from moviepy.editor import ColorClip
        clip = ColorClip((640, 480), color=(0, 0, 255), duration=120) # 2 minutes = 120 seconds
        clip.write_videofile(input_video, fps=24)
        clip.close()
        print(f"Created a dummy 2-minute video: {input_video}")

    trim_video(input_video, output_video, trim_start_seconds, trim_end_seconds)