import os
import re
import requests  # 用于下载图片
from PIL import Image  # 需要安装 Pillow 库
from io import BytesIO  # 用于处理网络图片的字节流

# 示例用法
md_file_path = "d:/09_Project/replaceLocalpic/Origin.md"  # 输入的 Markdown 文件路径
output_folder = "d:/09_Project/replaceLocalpic/images"  # 输出图片文件夹
prefix = "c5n"  # 图片名称前缀

def extract_and_save_images(md_file_path, output_folder, prefix):
    # 检查 Markdown 文件是否存在
    if not os.path.exists(md_file_path):
        print(f"Markdown 文件 {md_file_path} 不存在！")
        return

    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 读取 Markdown 文件内容
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # 找到所有 ![](xxx) 格式的字段
    image_pattern = r'!\[.*?\]\((.*?)\)'
    matches = re.findall(image_pattern, md_content)

    # 遍历匹配到的图片路径
    for index, image_url in enumerate(matches):
        try:
            if image_url.startswith("http"):  # 如果是网络图片
                print(f"正在下载图片: {image_url}")
                response = requests.get(image_url)
                response.raise_for_status()  # 检查请求是否成功
                img = Image.open(BytesIO(response.content))  # 从字节流中打开图片
            elif os.path.exists(image_url):  # 如果是本地图片
                print(f"正在处理本地图片: {image_url}")
                img = Image.open(image_url)
            else:
                print(f"图片路径无效: {image_url}")
                continue

            # 获取图片格式（如 PNG 或 GIF）
            image_format = img.format.lower()  # 转为小写，确保一致性
            if image_format not in ["png", "gif"]:
                print(f"不支持的图片格式: {image_format}")
                continue

            # 构造新的图片名称
            new_image_name = f"{prefix}{index + 1:02d}.{image_format}"
            new_image_path = os.path.join(output_folder, new_image_name)

            # 保存图片为对应格式
            img.save(new_image_path, image_format.upper())  # 格式需大写
            print(f"图片已保存为: {new_image_path}")
        except Exception as e:
            print(f"无法处理图片 {image_url}: {e}")

# 调用函数
extract_and_save_images(md_file_path, output_folder, prefix)