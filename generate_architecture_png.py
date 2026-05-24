from PIL import Image, ImageDraw, ImageFont
import os

w, h = 1000, 600
im = Image.new('RGB', (w, h), 'white')
d = ImageDraw.Draw(im)

try:
    font_title = ImageFont.truetype('arial.ttf', 24)
    font_label = ImageFont.truetype('arial.ttf', 16)
except OSError:
    font_title = ImageFont.load_default()
    font_label = ImageFont.load_default()

boxes = [
    ((50, 50), (330, 180), 'User', ['Browser / CLI', 'Sample requests']),
    ((380, 30), (660, 180), 'Streamlit UI', ['Optional demo layer', 'REST client']),
    ((380, 230), (660, 360), 'Rasa Server', ['NLU + Core', 'Intent classification', 'Stories']),
    ((720, 50), (920, 170), 'PostgreSQL', ['faq', 'employees', 'leave_requests']),
    ((720, 230), (920, 350), 'Action Server', ['Custom actions', 'DB lookup']),
    ((50, 240), (330, 360), 'Rasa Shell', ['Direct bot testing', 'Same Rasa server'])
]
for box in boxes:
    (x1, y1), (x2, y2), title, lines = box
    d.rectangle([x1, y1, x2, y2], outline='black', width=2, fill='#f8f8f8')
    d.text((x1+15, y1+15), title, fill='black', font=font_title)
    y = y1 + 50
    for line in lines:
        d.text((x1+15, y), f'- {line}', fill='black', font=font_label)
        y += 22

arr = [
    ((330, 115), (380, 115), 'Optional demo flow'),
    ((500, 180), (500, 230), 'REST webhook'),
    ((660, 290), (720, 290), 'Action call'),
    ((500, 300), (500, 360), 'Shell requests')
]
for (x1, y1), (x2, y2), label in arr:
    d.line([(x1, y1), (x2, y2)], fill='black', width=2)
    if x2 > x1:
        d.polygon([(x2, y2), (x2-10, y2-7), (x2-10, y2+7)], fill='black')
    else:
        d.polygon([(x2, y2), (x2+10, y2-7), (x2+10, y2+7)], fill='black')
    d.text(((x1+x2)/2-60, (y1+y2)/2-15), label, fill='black', font=font_label)

subtitle = 'HR Helpdesk Architecture: User, Streamlit, Rasa, Actions, and PostgreSQL'
d.text((50, 390), subtitle, fill='black', font=font_label)

os.makedirs('screenshots', exist_ok=True)
path = os.path.join('screenshots', 'architecture.png')
im.save(path)
print(f'Created {path}')
