from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import os
from datetime import datetime

def overlay_images_on_video(video_path, image_folder, output_path, text_path, timing_info):
    """
    Overlays a sequence of images onto a video at specified time intervals.

    Args:
        video_path (str): Path to the input video file.
        image_folder (str): Path to the folder containing the images.
        output_path (str): Path to save the output video.
    """
    try:
        video_clip = VideoFileClip(video_path)
        video_duration = video_clip.duration
        image_files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        num_images = len(image_files)
        video_width, video_height = video_clip.size

        if not image_files:
            print(f"No image files found in: {image_folder}")
            video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            return




        with open(text_path, 'r') as file: 
            lines = [line.strip() for line in file]

        with open(timing_info, 'r') as file: 
            timing_line = [line.strip() for line in file]


        print(lines)
        print(timing_line)

        clips = [video_clip]
      


        finalised_timing = []
        # for i in range(zip(lines, timing_line)):
        #     return

        # we will need to develop the algoirhtm from here... (keepm this closed for now)
        format_str = "%H:%M:%S.%f"

        cur_sentence = lines[0]
        i = 0
        while i < len(lines):
            cur_sentence = lines[i]
            first_timing_info = None
            last_timing_info = None

            # Find the first and last timing for the current sentence
            j = i
            while j < len(lines) and lines[j] == cur_sentence and j < len(timing_line):
                timing_parts = timing_line[j].split()
                if len(timing_parts) >= 3:
                    if first_timing_info is None:
                        try:
                            first_timing_info = (timing_parts[0], datetime.strptime(timing_parts[1], format_str), datetime.strptime(timing_parts[2], format_str))
                        except ValueError as e:
                            print(f"Error parsing time in timing_line[{j}]: {e}")
                            first_timing_info = None
                    try:
                        last_timing_info = (timing_parts[0], datetime.strptime(timing_parts[1], format_str), datetime.strptime(timing_parts[2], format_str))
                    except ValueError as e:
                        print(f"Error parsing time in timing_line[{j}]: {e}")
                j += 1

            # If we found timing information for the sentence
            if first_timing_info and last_timing_info:
                start_time = first_timing_info[1]
                end_time = last_timing_info[2]
                finalised_timing.append([start_time.strftime(format_str), end_time.strftime(format_str)])
            elif cur_sentence:
                print(f"Warning: No valid timing information found for sentence: '{cur_sentence}'")

            # Move the index 'i' to the next different sentence
            while i < len(lines) and lines[i] == cur_sentence:
                i += 1


        for i, timing in enumerate(finalised_timing):
            image_path = os.path.join(image_folder, image_files[i])
            image_clip = ImageClip(image_path)
            start, end = timing
            start_time_dt = datetime.strptime(start, format_str)
            end_time_dt = datetime.strptime(end, format_str)
            duration = (end_time_dt - start_time_dt).total_seconds()
            start_time_seconds = (start_time_dt - datetime.strptime("0:00:00.00", format_str)).total_seconds()
            image_clip = image_clip.set_duration(duration)
            image_clip = image_clip.set_start(start_time_seconds)

                        # Get image size
            image_width, image_height = image_clip.size

            # Position the image at the bottom left
            margin = 10  # Optional margin from the edges
            position = (margin, video_height - image_height - margin)
            image_clip = image_clip.set_pos(position)

            clips.append(image_clip)

            
        final_clip = CompositeVideoClip(clips)
        final_clip = final_clip.subclip(0, video_duration) # Trim the final clip
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        final_clip.close()
        video_clip.close()

        print(f"Video with image overlays saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_filepath = "final.mp4"  
    image_directory = "../assets/griffin"  
    output_filepath = "output_with_overlays.mp4"
    text_path = "../texts/test.txt"
    timing_path = "../texts/testing.txt"

    # Create a dummy video and image folder for testing if you don't have them
    if not os.path.exists(video_filepath):
        from moviepy.editor import ColorClip
        clip = ColorClip((640, 480), color=(255, 0, 0), duration=10)
        clip.write_videofile(video_filepath, fps=24)
        clip.close()
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
        from PIL import Image, ImageDraw
        for i in range(5):
            img = Image.new('RGB', (100, 100), color = (0, 255, 0))
            d = ImageDraw.Draw(img)
            d.text((20,20), str(i+1), fill=(255,255,0))
            img.save(os.path.join(image_directory, f"image_{i+1}.png"))

    overlay_images_on_video(video_filepath, image_directory, output_filepath,text_path, timing_path )