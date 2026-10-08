import os
import sys
from PIL import Image

def remove_metadata(input_path: str, output_path: str = None) -> None:
    """
    Removes all metadata (EXIF, GPS, camera details, etc.) from an image file.

    :param input_path: Path to the original image file.
    :param output_path: Path where the cleaned image will be saved.
                        If not provided, '_clean' will be appended to the filename.
    """
    if not os.path.exists(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        return

    # Determine default output path if not specified
    if not output_path:
        filename, ext = os.path.splitext(input_path)
        output_path = f"{filename}_clean{ext}"

    try:
        # Open source image
        with Image.open(input_path) as img:
            # Re-create image solely from raw pixel data to guarantee zero metadata payload
            pixel_data = list(img.getdata())
            clean_img = Image.new(img.mode, img.size)
            clean_img.putdata(pixel_data)

            # Save the clean image
            clean_img.save(output_path)
            print(f"Metadata successfully stripped!\nSaved clean image to: {output_path}")

    except Exception as e:
        print(f"Failed to process image. Error: {e}")

if __name__ == "__main__":
    # Example usage via command line argument or manual run
    if len(sys.argv) > 1:
        file_to_process = sys.argv[1]
        remove_metadata(file_to_process)
    else:
        print("Usage: python metadata_remover.py <path_to_image>")