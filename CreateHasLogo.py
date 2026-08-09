from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# Paths
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
has_dir = os.path.join(desktop, 'HAS')
os.makedirs(has_dir, exist_ok=True)
ico_path = os.path.join(has_dir, 'HasTimerIcon.ico')

# Sizes
base_size = 512
img = Image.new('RGBA', (base_size, base_size), (0,0,0,0))
d = ImageDraw.Draw(img)

# Leave background transparent so icon appears like a PNG (no black vignette)
# (canvas already created with transparent background)

# Clock face
cx = cy = base_size // 2
radius = int(base_size * 0.36)
face_box = [cx-radius, cy-radius, cx+radius, cy+radius]
# outer ring
d.ellipse(face_box, fill=(20,20,20,255), outline=(70,70,70,255), width=6)
# inner slightly lighter circle
inner_r = int(radius*0.88)
d.ellipse([cx-inner_r, cy-inner_r, cx+inner_r, cy+inner_r], fill=(28,28,28,255))

# ticks
for i in range(12):
    angle = i * (360/12)
    import math
    a = math.radians(angle - 90)
    outer = (cx + math.cos(a)* (inner_r-6), cy + math.sin(a)* (inner_r-6))
    inner = (cx + math.cos(a)* (inner_r-28), cy + math.sin(a)* (inner_r-28))
    d.line([outer, inner], fill=(140,140,140,255) if i%3==0 else (90,90,90,255), width=3 if i%3==0 else 2)

# hands (pointing to 10:10 for nice symmetry)
import math
def hand(angle_deg, length, width, color):
    a = math.radians(angle_deg - 90)
    end = (cx + math.cos(a)*length, cy + math.sin(a)*length)
    d.line([(cx,cy), end], fill=color, width=width)

hand(300, inner_r*0.6, 10, (220,180,70,255))  # hour - warm gold
hand(300, inner_r*0.85, 6, (255,255,255,200))  # minute - light
# center cap
d.ellipse([cx-10, cy-10, cx+10, cy+10], fill=(255,255,255,220))

# Overlay letters 'HAS' centered, blend softly
try:
    font_path = 'C:/Windows/Fonts/seguisb.ttf'  # Segoe UI Semibold
    font = ImageFont.truetype(font_path, int(base_size*0.24))
except Exception:
    try:
        font = ImageFont.truetype('arialbd.ttf', int(base_size*0.24))
    except Exception:
        font = ImageFont.load_default()

text = 'HAS'
w, h = d.textbbox((0,0), text, font=font)[2:]
text_xy = ((base_size - w)//2, (base_size - h)//2 + int(base_size*0.04))
# shadow
shadow = Image.new('RGBA', img.size, (0,0,0,0))
sd = ImageDraw.Draw(shadow)
sd.text((text_xy[0]+6, text_xy[1]+6), text, font=font, fill=(0,0,0,140))
shadow = shadow.filter(ImageFilter.GaussianBlur(4))
img = Image.alpha_composite(img.convert('RGBA'), shadow)
# main text with subtle gradient
txt = Image.new('RGBA', img.size, (0,0,0,0))
td = ImageDraw.Draw(txt)
# gradient fill for text: light gray to warm gold
for i, ch in enumerate(text):
    ch_w, ch_h = td.textbbox((0,0), ch, font=font)[2:]
# draw full text
td.text(text_xy, text, font=font, fill=(245,245,245,255))
img = Image.alpha_composite(img, txt)

# No vignette: keep outer area transparent. Ensure image has alpha.
img = img.convert('RGBA')

# Save as ico in multiple sizes
sizes = [(256,256),(128,128),(64,64),(48,48),(32,32),(16,16)]
img.save(ico_path, format='ICO', sizes=sizes)
print('Created icon at:', ico_path)
