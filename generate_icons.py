#!/usr/bin/env python3
"""
Simple script to generate basic PWA icons for MoodTunes
Run this script to create placeholder icons until you design custom ones
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

import os

def create_simple_icon(size, color="#667eea", text="🎵"):
    """Create a simple colored icon with emoji"""
    if PIL_AVAILABLE:
        # Create with PIL if available
        img = Image.new('RGB', (size, size), color)
        draw = ImageDraw.Draw(img)
        
        try:
            # Try to use a system font
            font_size = size // 2
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size and center it
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), text, fill="white", font=font)
        return img
    else:
        print(f"PIL not available. Creating placeholder for {size}x{size}")
        return None

def generate_icons():
    """Generate all required PWA icons"""
    icons_dir = "static/icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    print("Generating PWA icons for MoodTunes...")
    
    for size in sizes:
        filename = f"icon-{size}x{size}.png"
        filepath = os.path.join(icons_dir, filename)
        
        if PIL_AVAILABLE:
            icon = create_simple_icon(size)
            if icon:
                icon.save(filepath, "PNG")
                print(f"✅ Created {filename}")
        else:
            # Create empty file as placeholder
            with open(filepath, 'w') as f:
                f.write(f"# Placeholder for {size}x{size} icon")
            print(f"📝 Created placeholder {filename}")
    
    print("\n🎉 Icon generation complete!")
    
    if not PIL_AVAILABLE:
        print("\n📋 Next steps:")
        print("1. Install Pillow for better icon generation: pip install Pillow")
        print("2. Or create custom icons using online tools:")
        print("   - https://realfavicongenerator.net/")
        print("   - https://www.favicon-generator.org/")
        print("3. Replace placeholder files in static/icons/ with actual PNG icons")

if __name__ == "__main__":
    generate_icons()