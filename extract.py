import spacy
import pandas as pd
from collections import Counter
import re  # 引入正则表达式库

# 确保已安装必要的库
try:
    import spacy_transformers
except ImportError:
    print("请先安装spacy-transformers库！")
    exit()

# 加载模型
nlp = spacy.load("en_core_web_trf")

# 读取小说文件
with open("Paradise (Abdulrazak Gurnah) (z-lib.txt", "r", encoding="utf-8") as file:
    novel_text = file.read()

# 处理小说文本
doc = nlp(novel_text)  # 直接处理整个文本，无需分段

# 使用Counter来统计地名及其出现次数
location_counts = Counter()

def clean_location(location):
    # 移除可能导致问题的特殊字符
    cleaned_location = re.sub(r"[^\w\s-]", "", location)
    return cleaned_location.strip()

for ent in doc.ents:
    if ent.label_ == "GPE":
        cleaned_location = clean_location(ent.text)
        location_counts[cleaned_location] += 1

# 将地名及其出现次数转换为DataFrame
location_df = pd.DataFrame(list(location_counts.items()), columns=["Location", "Count"])

# 保存DataFrame到Excel文件
location_df.to_excel("Paradise.xlsx", index=False)

# 打印完成消息
print("地名及其出现次数已保存到'Paradise.xlsx'")
