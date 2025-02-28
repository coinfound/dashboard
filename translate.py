import os
import json
from collections import defaultdict
from urllib.parse import quote_plus

url_prifix = "https://dianku-1251307063.file.myqcloud.com/dashboard-file/"


def process_policy_files(directory):
    # 初始化嵌套字典结构
    data = defaultdict(lambda: defaultdict(list))

    # 遍历目标目录
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # 跳过子目录，只处理文件
        if not os.path.isfile(filepath):
            continue

        # 分割文件名
        parts = filename.split('_')
        if len(parts) < 2:
            print(f"跳过不符合格式的文件: {filename}")
            continue

        # 解析组成部分
        country = parts[0]
        file_number = parts[1]
        file_name = '_'.join(parts[2:])  # 合并剩余部分作为文件名

        # 添加到数据结构
        data[country][file_number].append({
            "original_filename": filename,
            "filename": file_name,
            "url": url_prifix + quote_plus(filename)
        })

    # 转换defaultdict为普通字典（为了JSON序列化）
    result = {
        country: dict(numbers)
        for country, numbers in data.items()
    }

    return result


if __name__ == "__main__":
    target_dir = "政策文件"

    if not os.path.exists(target_dir):
        print(f"目录不存在: {target_dir}")
        exit(1)

    if not os.path.isdir(target_dir):
        print(f"路径不是目录: {target_dir}")
        exit(1)

    # 处理文件并生成结果
    output_data = process_policy_files(target_dir)

    # 写入JSON文件
    with open("policy_classification.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("文件分类完成，结果已保存到 policy_classification.json")
