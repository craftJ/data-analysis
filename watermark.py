from PIL import Image, ImageDraw, ImageFont
import os

def add_watermark(input_folder, output_folder, watermark_text):
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入目录
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            image = Image.open(image_path)

            # 创建一个可以在其上绘图的图像
            txt = Image.new('RGBA', image.size, (255, 255, 255, 0))

            # 设置字体和大小
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except IOError:
                print("Arial font not found. Using default font.")
                font = ImageFont.load_default()

            draw = ImageDraw.Draw(txt)

            # 水印位置和内容
            width, height = image.size
            text_width, text_height = draw.textsize(watermark_text, font=font)
            position = (width - text_width - 10, height - text_height - 10)

            # 添加水印
            draw.text(position, watermark_text, fill=(255, 255, 255, 128), font=font)

            # 合并原图和水印
            watermarked = Image.alpha_composite(image.convert('RGBA'), txt)

            # 保存到输出文件夹
            output_path = os.path.join(output_folder, filename)
            watermarked.save(output_path, 'PNG')

# 设置输入和输出文件夹路径
input_folder = './result/raw'  # 替换为你的输入文件夹路径
output_folder = './result'  # 替换为你的输出文件夹路径
watermark_text = 'ByteForge Certification'  # 替换为你的水印文本

# 调用函数
add_watermark(input_folder, output_folder, watermark_text)






