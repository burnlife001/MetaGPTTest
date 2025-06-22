## 3.2 目配置虚拟python环境                                            
## 3.4 安装项目依赖       
pip install metagpt==0.8.1 asyncio==3.4.3                                            
## 4.1配置LLM                            
metagpt --init-config    
## 编辑: `C:\Users\Administrator\.metagpt\config2.yaml`

## 4.2 运行脚本测试         
脚本均放置在nangeAGICode目录内                
**(1)运行脚本后报错解决**                      
打开命令行终端运行脚本，可能会出现如下报错信息                  
TypeError: AsyncClient.__init__() got an unexpected keyword argument 'proxies'                            
原因为httpx的版本问题，执行如下命令更换版本                                         
pip install --upgrade httpx==0.27.2                            

**(2)脚本测试**            
打开命令行终端运行脚本进行功能测试             
