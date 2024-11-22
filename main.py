from PIL import Image, ImageDraw, ImageFont
import math

def text_to_circle(text, font_path, font_size):
    # 计算圆的半径
    radius = len(text) * font_size / (2 * math.pi)
    image_size = int(2 * (radius + font_size))
    
    # 创建一个空白图像
    image = Image.new('RGB', (image_size, image_size), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 加载字体
    font = ImageFont.truetype(font_path, font_size)
    
    # 计算圆的中心点
    center_x, center_y = image_size // 2, image_size // 2
    
    # 计算每个字符的角度
    angle_step = 360 / len(text)
    
    for i, char in enumerate(text):
        # 计算字符的位置
        angle = math.radians(i * angle_step - 90)  # 调整起始角度，使顶部为起始点
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        # 创建一个单字符图像
        char_image = Image.new('RGBA', (font_size * 2, font_size * 2), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_image)
        char_draw.text((font_size, font_size), char, font=font, fill=(0, 0, 0), anchor="mm")
        
        # 旋转字符图像
        char_image = char_image.rotate(-i * angle_step, resample=Image.BICUBIC, center=(font_size, font_size))
        
        # 粘贴字符图像到主图像
        image.paste(char_image, (int(x - font_size), int(y - font_size)), char_image)
    
    # 保存图像
    image.save('text_circle.png')

# 示例使用
text = "这是一个测试文本"
font_path = "SourceHanSansCN-VF.ttf"  # 替换为你的字体路径
font_size = 20

text_to_circle(text, font_path, font_size)