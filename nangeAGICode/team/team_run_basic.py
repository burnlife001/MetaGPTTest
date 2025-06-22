from metagpt.software_company import generate_repo  
  
# 使用generate_repo确保生成代码  
repo_path = generate_repo(  
    "写一个基本的python冒泡排序，尽量简单",  
    investment=5.0,  
    n_round=8,  
    code_review=True,  
    implement=True  # 明确启用代码实现  
)  
print(f"项目已生成到: {repo_path}")