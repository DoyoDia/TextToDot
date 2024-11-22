from PIL import Image, ImageDraw, ImageFont
import math

def text_to_circle(text, font_path, font_size, scale_factor=4, spacing_factor=1.2):
    # 放大字体大小和图像尺寸
    scaled_font_size = font_size * scale_factor
    radius = len(text) * scaled_font_size * spacing_factor / (2 * math.pi)
    image_size = int(2 * (radius + scaled_font_size))
    
    # 创建一个放大的空白图像
    image = Image.new('RGB', (image_size, image_size), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 加载放大的字体
    font = ImageFont.truetype(font_path, scaled_font_size)
    
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
        char_image = Image.new('RGBA', (scaled_font_size * 2, scaled_font_size * 2), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_image)
        
        # 绘制加粗字符
        for offset in range(-1, 2):
            char_draw.text((scaled_font_size + offset, scaled_font_size), char, font=font, fill=(0, 0, 0), anchor="mm")
            char_draw.text((scaled_font_size, scaled_font_size + offset), char, font=font, fill=(0, 0, 0), anchor="mm")
        
        # 旋转字符图像
        char_image = char_image.rotate(-i * angle_step, resample=Image.BICUBIC, center=(scaled_font_size, scaled_font_size))
        
        # 粘贴字符图像到主图像
        image.paste(char_image, (int(x - scaled_font_size), int(y - scaled_font_size)), char_image)
    
    # 保存图像
    image.save('text_circle.png')

# 示例使用
text = "开头你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好结尾"
font_path = "SourceHanSansCN-VF.ttf"  # 替换为你的字体路径
font_size = 20

text_to_circle(text, font_path, font_size)