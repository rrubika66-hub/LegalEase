import os
from PIL import Image, ImageDraw, ImageFont

def generate_logo(output_path: str):
    """
    Generates a high-resolution, modern scales of justice branding badge
    for LegalEase AI.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # 2x supersampling for ultra-crisp edges
    width, height = 800, 200
    img = Image.new("RGBA", (width, height), color=(15, 23, 42, 255)) # Dark navy background
    draw = ImageDraw.Draw(img)

    # Coordinates scaled for high resolution
    # Central Balance Stand
    draw.rounded_rectangle([(70, 30), (210, 170)], radius=16, fill=(30, 41, 59, 255), outline=(56, 189, 248, 255), width=2)
    
    # Stand column & base
    draw.line([(140, 55), (140, 145)], fill=(241, 245, 249, 255), width=6)
    draw.line([(110, 145), (170, 145)], fill=(56, 189, 248, 255), width=6)
    draw.ellipse([(132, 45), (148, 61)], fill=(56, 189, 248, 255))
    
    # Beam
    draw.line([(95, 75), (185, 75)], fill=(241, 245, 249, 255), width=5)
    
    # Left Scale Pan & Strings
    draw.line([(100, 75), (90, 105)], fill=(148, 163, 184, 255), width=3)
    draw.line([(100, 75), (110, 105)], fill=(148, 163, 184, 255), width=3)
    draw.polygon([(85, 105), (115, 105), (100, 122)], fill=(56, 189, 248, 255))

    # Right Scale Pan & Strings
    draw.line([(180, 75), (170, 105)], fill=(148, 163, 184, 255), width=3)
    draw.line([(180, 75), (190, 105)], fill=(148, 163, 184, 255), width=3)
    draw.polygon([(165, 105), (195, 105), (180, 122)], fill=(56, 189, 248, 255))

    # Downsample for clean anti-aliasing
    final_img = img.resize((400, 100), Image.Resampling.LANCZOS)
    draw_final = ImageDraw.Draw(final_img)

    # LegalEase Typography
    try:
        # Attempt to use standard Windows TrueType font
        font_title = ImageFont.truetype("arial.ttf", 26)
        font_sub = ImageFont.truetype("arial.ttf", 13)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw_final.text((120, 24), "LegalEase AI", fill=(255, 255, 255, 255), font=font_title)
    draw_final.text((122, 58), "PRODUCTION LEGAL DOCUMENT GENERATOR", fill=(148, 163, 184, 255), font=font_sub)

    final_img.save(output_path, "PNG")
    print(f"✅ Successfully generated logo badge at: {output_path}")

if __name__ == "__main__":
    target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
    generate_logo(target_path)
