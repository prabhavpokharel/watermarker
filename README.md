# Watermarker & Branding Tool

A Python-based image processor designed to apply professional branding to photography. It recursively processes images to add a dark aesthetic gradient, session typography with auto-fitting logic, and a logo watermark.

## Features

- **HEIF/HEIC Support**: Processes modern iPhone photos automatically
- **Aesthetic Gradient**: Adds a soft black "pitch" gradient at the bottom for text legibility
- **Dynamic Typography**: Adds a Session Name in Inter-Bold with "Auto-Shrink" logic to prevent text from overlapping the logo
- **Orientation Aware**: Automatically scales the logo and text differently for Portrait vs. Landscape photos
- **Structure Preserving**: Maintains your subfolder hierarchy from `input` to `output`

## Requirements

- Python 3.10 or higher
- Pillow (Image processing)
- pillow-heif (For iPhone photo support)
- Inter-Bold.ttf (Included in the root directory)

## Installation

1. **Clone the repository:**

```bash
git clone git@github.com:computerclubkec/watermarker.git
cd watermarker
```

2. **Setup Virtual Environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

## Usage

1. **Prepare Assets:**
   - Place images in the `/input` folder
   - Ensure `watermark.png` (transparent PNG) is in the root
   - Ensure `Inter-Bold.ttf` is in the root

2. **Set Session Name:**
   - Open `apply_watermark.py` and change the `session_name` in the `if __name__ == "__main__":` block

3. **Run:**

```bash
python apply_watermark.py
```

## Configuration

The script uses smart defaults, but you can tweak these in `apply_watermark.py`:

| Variable | Description | Default |
|----------|-------------|---------|
| `scale_factor` | Size of logo relative to image width | `0.15` |
| `padding_percent` | Spacing from edges based on image size | `0.05` (5%) |
| `text_color` | RGBA value for the typography | `(235, 235, 235, 215)` |