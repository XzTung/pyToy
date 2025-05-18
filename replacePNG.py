import os
import re

# 示例用法
md_file_path = "d:/09_Project/replaceLocalpic/Origin.md"  # 输入的 Markdown 文件路径
image_folder_path = "d:/09_Project/replaceLocalpic/images"  # 图片文件夹路径
output_md_file_path = "d:/09_Project/replaceLocalpic/convertDone.md"  # 输出的 Markdown 文件路径

def replace_md_image_links(md_file_path, image_folder_path, output_md_file_path):
    # 检查文件和文件夹是否存在
    if not os.path.exists(md_file_path):
        print(f"Markdown 文件 {md_file_path} 不存在！")
        return
    if not os.path.exists(image_folder_path):
        print(f"图片文件夹 {image_folder_path} 不存在！")
        return

    # 获取图片文件名列表（仅限 .png 文件）
    image_files = [f for f in os.listdir(image_folder_path) if f.lower().endswith('.png')]
    if not image_files:
        print("图片文件夹中没有找到 .png 图片！")
        return

    # 读取 Markdown 文件内容
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # 找到所有 ![]() 格式的字段
    image_pattern = r'!\[.*?\]\((.*?)\)'
    matches = re.findall(image_pattern, md_content)

    # 替换括号中的内容
    updated_content = md_content
    for i, match in enumerate(matches):
        if i < len(image_files):
            image_name = os.path.splitext(image_files[i])[0]  # 获取图片文件名（不包括扩展名）
            new_image_path = f"./img/{image_name}.png"
            updated_content = updated_content.replace(f"({match})", f"({new_image_path})", 1)

    # 扫描并替换类似 "5. ####" 的字段
    header_pattern = r'(\d+\.\s+)(#+)'
    updated_content = re.sub(header_pattern, lambda m: f"{m.group(2)} {m.group(1).strip()}", updated_content)

    # 将更新后的内容写入新的 Markdown 文件
    with open(output_md_file_path, 'w', encoding='utf-8') as output_md_file:
        output_md_file.write(updated_content)

    print(f"Markdown 文件已更新并保存到 {output_md_file_path}")


replace_md_image_links(md_file_path, image_folder_path, output_md_file_path)