import asyncio
import json
from metagpt.context import Context
from metagpt.roles.product_manager import ProductManager
from metagpt.logs import logger

async def main():
    # 定义初始消息
    msg = "写一个俄罗斯方块游戏的PRD文档"
    # 提供环境 即创建上下文
    context = Context()
    # 实例化角色
    role = ProductManager(context=context)
    while msg:
        # 运行角色
        msg = await role.run(msg)
        # 优化信息显示
        if msg:
            print("\n" + "🤖 " + "="*60)
            print(f"   角色: {role.name}")
            print("   " + "-"*58)
            
            # 处理消息内容
            if hasattr(msg, 'content') and msg.content:
                content = str(msg.content)
            else:
                content = str(msg)
            
            # 格式化输出内容 - 优化JSON转文本显示
            json_data = None
            
            # 尝试解析JSON数据
            if content.startswith('{') and content.endswith('}'):
                try:
                    # 首先尝试直接解析
                    parsed_json = json.loads(content)
                    
                    # 检查是否包含docs字段（MetaGPT的ProductManager角色返回格式）
                    if 'docs' in parsed_json and isinstance(parsed_json['docs'], dict):
                        # 遍历docs中的所有文件
                        for filename, file_obj in parsed_json['docs'].items():
                            if 'content' in file_obj and isinstance(file_obj['content'], str):
                                try:
                                    # 尝试解析文件内容中的JSON
                                    json_data = json.loads(file_obj['content'])
                                    # 找到第一个有效的JSON就退出循环
                                    break
                                except json.JSONDecodeError:
                                    continue
                    
                    # 如果没有从docs中找到有效的JSON，尝试其他解析方式
                    if json_data is None:
                        # 检查是否直接包含content字段
                        if 'content' in parsed_json and isinstance(parsed_json['content'], str):
                            if parsed_json['content'].startswith('{') and parsed_json['content'].endswith('}'):
                                try:
                                    json_data = json.loads(parsed_json['content'])
                                except json.JSONDecodeError:
                                    pass
                        else:
                            # 直接使用解析后的JSON
                            json_data = parsed_json
                except json.JSONDecodeError:
                    json_data = None
            
            if json_data:
                print("   📋 生成的文档内容:")
                print("   " + "-"*58)
                
                # 定义字段显示映射
                field_mapping = {
                    'Project Name': ('🎯', '项目名称'),
                    'Language': ('🌐', '语言'),
                    'Programming Language': ('💻', '编程语言'),
                    'Product Goals': ('🎯', '产品目标'),
                    'User Stories': ('👤', '用户故事'),
                    'Competitive Analysis': ('📊', '竞品分析'),
                    'Requirement Analysis': ('📋', '需求分析'),
                    'Requirement Pool': ('💡', '需求池'),
                    'UI Design draft': ('🎨', 'UI设计草图'),
                    'Anything UNCLEAR': ('❓', '待明确事项')
                }
                
                # 按优先级显示字段
                priority_fields = ['Project Name', 'Language', 'Programming Language']
                list_fields = ['Product Goals', 'User Stories', 'Competitive Analysis', 'Requirement Analysis', 'Requirement Pool']
                
                # 显示优先级字段
                for field in priority_fields:
                    if field in json_data:
                        icon, label = field_mapping.get(field, ('📌', field))
                        print(f"   {icon} {label}: {json_data[field]}")
                
                print()
                
                # 显示列表类型字段
                for field in list_fields:
                    if field in json_data:
                        icon, label = field_mapping.get(field, ('📌', field))
                        print(f"   {icon} {label}:")
                        value = json_data[field]
                        if isinstance(value, list):
                            for i, item in enumerate(value, 1):
                                # 处理嵌套对象
                                if isinstance(item, dict):
                                    print(f"      {i}. {json.dumps(item, ensure_ascii=False, indent=8)[1:-1].strip()}")
                                # 处理嵌套列表（如Requirement Pool）
                                elif isinstance(item, list):
                                    if len(item) == 2:  # 假设是[优先级, 描述]格式
                                        print(f"      {i}. [{item[0]}] {item[1]}")
                                    else:
                                        print(f"      {i}. {item}")
                                else:
                                    print(f"      {i}. {item}")
                        elif isinstance(value, dict):
                            for k, v in value.items():
                                print(f"      • {k}: {v}")
                        else:
                            print(f"      {value}")
                        print()
                
                # 显示其他字段
                displayed_fields = set(priority_fields + list_fields)
                for key, value in json_data.items():
                    if key not in displayed_fields:
                        icon, label = field_mapping.get(key, ('📌', key))
                        print(f"   {icon} {label}:")
                        if isinstance(value, (list, dict)):
                            print(f"      {json.dumps(value, ensure_ascii=False, indent=6)}")
                        else:
                            print(f"      {value}")
                        print()
            else:
                print(f"   📄 消息: {content[:500]}..." if len(content) > 500 else f"   📄 消息: {content}")
            
            print("   " + "="*60 + "\n")
        else:
            print("\n🎉 任务完成！所有文档已生成完毕。\n")

if __name__ == '__main__':
    asyncio.run(main())