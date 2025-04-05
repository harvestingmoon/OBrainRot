import os
from PIL import Image

def resize_png_images(folder_path, output_size=(512, 512)):
    """
    Resizes all PNG images in a specified folder to a given size.

    Args:
        folder_path (str): The path to the folder containing PNG images.
        output_size (tuple): The desired output size (width, height). Defaults to (512, 512).
    """

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            filepath = os.path.join(folder_path, filename)
            try:
                img = Image.open(filepath)
                img = img.resize(output_size, Image.Resampling.LANCZOS) # Use LANCZOS for best quality.
                img.save(filepath) # Overwrites the original image. If you want to save to a new folder, change this line.
                print(f"Resized: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing PNG images: ")
    resize_png_images(folder_path)
    print("Resizing complete.")