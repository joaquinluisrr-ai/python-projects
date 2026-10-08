# Image Metadata Cleaner

A lightweight Python tool designed to strip sensitive metadata (EXIF, GPS, camera details, timestamps) from image files by regenerating clean pixel data.

## Features

- **Privacy Protection:** Completely removes EXIF, GPS locations, device details, and creation dates.
- **Clean Pixel Reconstruction:** Rebuilds images directly from raw pixel matrices to guarantee zero leftover metadata headers.
- **Command Line Support:** Easily run the script against any image directly from your terminal.

## Prerequisites

- **Python 3.8+**
- **Pillow** library

Install dependencies:
```bash
pip install Pillow
```

## Usage

### Command Line Interface

Pass the path of the image you want to clean as an argument:

```bash
python metadata_remover.py path/to/your_image.jpg
```

This generates a cleaned version named `your_image_clean.jpg` in the same directory.

### Python Import

You can also import and use the function in your own Python projects:

```python
from metadata_remover import remove_metadata

remove_metadata("my_photo.png", "cleaned_photo.png")
```

## Verification

To verify that metadata has been removed, you can inspect file properties in your OS or run Python's Pillow library to check `img.getexif()` — it will return an empty set.

## License

MIT License. Free to use and modify.