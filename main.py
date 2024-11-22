import gradio as gr
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
    
    return image

def generate_image(text, font_size, use_custom_font, font_file=None):
    if not text.strip():
        raise gr.Error("警告：文本输入不能为空！")
    
    if use_custom_font and font_file is not None:
        font_path = font_file.name
    else:
        font_path = "SourceHanSansCN-VF.ttf"
    
    image = text_to_circle(text, font_path, font_size)
    return image

def update_visibility(use_custom_font):
    return gr.update(visible=use_custom_font)

with gr.Blocks() as iface:
    text_input = gr.Textbox(lines=2, placeholder="输入文本...")
    font_size_slider = gr.Slider(minimum=6, maximum=100, value=15, step=1, label="字体大小")  # step=1 字号必须是整数
    use_custom_font_checkbox = gr.Checkbox(label="使用自定义字体")
    font_file_input = gr.File(label="上传字体文件", visible=False)
    
    use_custom_font_checkbox.change(
        fn=update_visibility,
        inputs=use_custom_font_checkbox,
        outputs=font_file_input
    )
    
    generate_button = gr.Button("生成图像")
    output_image = gr.Image()
    
    generate_button.click(
        fn=generate_image,
        inputs=[text_input, font_size_slider, use_custom_font_checkbox, font_file_input],
        outputs=output_image
    )

iface.launch()