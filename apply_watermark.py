import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

def get_fitted_font(draw, text, max_width, initial_font_size):
    """
    Decreases font size until the text fits within max_width.
    """
    current_size = initial_font_size
    font = ImageFont.truetype("Inter-Bold.ttf", current_size)
    
    # Calculate width of text
    text_width = draw.textbbox((0, 0), text, font=font)[2]
    
    while text_width > max_width and current_size > 10:
        current_size -= 2
        font = ImageFont.truetype("Inter-Bold.ttf", current_size)
        text_width = draw.textbbox((0, 0), text, font=font)[2]
        
    return font, current_size

def apply_watermark(image_path, watermark_path, output_path, session_name, scale_factor=0.15):
    with Image.open(image_path) as base_image:
        base_image = ImageOps.exif_transpose(base_image)
        if base_image.mode != 'RGBA':
            base_image = base_image.convert('RGBA')
        
        width, height = base_image.size
        is_portrait = height > width
        
        # 1. THE GRADIENT
        gradient_height = int(height * 0.45)
        gradient = Image.new('L', (1, gradient_height), color=0)
        for y in range(gradient_height):
            progress = y / gradient_height
            alpha = int(230 * (progress ** 1.2)) 
            gradient.putpixel((0, y), alpha)
        
        gradient = gradient.resize((width, gradient_height))
        black_layer = Image.new('RGBA', (width, gradient_height), (0, 0, 0, 0))
        black_layer.putalpha(gradient)
        
        overlay = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
        overlay.paste(black_layer, (0, height - gradient_height))
        
        # 2. DIMENSIONS & TEXT SCALING
        padding = int(min(width, height) * 0.05)
        # We start with a smaller base size as requested (3.5% of shorter side)
        initial_font_size = int(min(width, height) * 0.035)
        
        draw = ImageDraw.Draw(overlay)
        
        # Determine maximum available width for text (leave room for logo)
        # We give text roughly 60% of the width to prevent overlap
        max_text_width = width * 0.6
        
        try:
            font, final_font_size = get_fitted_font(draw, session_name, max_text_width, initial_font_size)
        except:
            font = ImageFont.load_default()
            final_font_size = 15

        # 3. "NATURAL" TEXT (Off-white with 85% opacity)
        # fill=(R, G, B, Alpha) -> (235, 235, 235, 215)
        text_color = (235, 235, 235, 215)
        draw.text((padding, height - final_font_size - padding), session_name, font=font, fill=text_color)

        # 4. LOGO
        with Image.open(watermark_path) as wm:
            wm_scale = scale_factor * 0.6 if is_portrait else scale_factor
            wm_w = int(width * wm_scale)
            wm_h = int(wm_w * wm.height / wm.width)
            wm_resized = wm.resize((wm_w, wm_h), Image.Resampling.LANCZOS)
            overlay.paste(wm_resized, (width - wm_w - padding, height - wm_h - padding), wm_resized)

        # 5. SAVE
        final_output = os.path.splitext(output_path)[0] + ".jpg"
        os.makedirs(os.path.dirname(final_output), exist_ok=True)
        final = Image.new('RGB', output_image.size, (255, 255, 255)) if 'output_image' in locals() else Image.new('RGB', base_image.size)
        
        output_image = Image.alpha_composite(base_image, overlay)
        final = Image.new('RGB', output_image.size, (255, 255, 255))
        final.paste(output_image, mask=output_image.split()[3])
        final.save(final_output, "JPEG", quality=95, subsampling=0)

def process_images(input_folder, output_folder, watermark_path, session_name):
    valid_extensions = ('.jpg', '.jpeg', '.png', '.heic', '.heif')
    
    # Use os.walk for better reliability over glob
    count = 0
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(valid_extensions):
                image_path = os.path.join(root, file)
                rel_path = os.path.relpath(image_path, input_folder)
                output_path = os.path.join(output_folder, rel_path)
                
                try:
                    apply_watermark(image_path, watermark_path, output_path, session_name)
                    print(f"✅ Processed: {file}")
                    count += 1
                except Exception as e:
                    print(f"❌ Error {file}: {e}")
    
    print(f"\nFinished! Total images processed: {count}")

if __name__ == "__main__":
    process_images(
        input_folder="input", 
        output_folder="output",
        watermark_path="watermark.png",
        session_name="Session on Game Development"
    )