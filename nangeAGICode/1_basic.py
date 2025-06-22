import asyncio
from metagpt.context import Context
from metagpt.roles.product_manager import ProductManager
from metagpt.logs import logger

async def main():
    # 定义初始消息
    msg = "写一个基本的俄罗斯方块游戏，尽量简单"
    # 提供环境 即创建上下文
    context = Context()
    # 实例化角色
    role = ProductManager(context=context) #产品经理只写prd
    while msg:
        # 运行角色
        msg = await role.run(msg)
        logger.info(str(msg))

if __name__ == '__main__':
    asyncio.run(main())