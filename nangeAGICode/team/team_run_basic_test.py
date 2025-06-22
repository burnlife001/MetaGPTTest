from metagpt.software_company import generate_repo    
    
repo_path = generate_repo(    
    "写一个基本的python快速排序，尽量简单",  
    investment=5.0,    
    n_round=8,    
    code_review=True,    
    run_tests=True,  # 启用测试  
    implement=True    
)    
print(f"项目已生成到: {repo_path}")