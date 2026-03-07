开工第一天，先理清楚项目是怎么回事：

用户输入 -> LongGraph(agent）   
Agent调用   
1.RAG检索增强生成  （FAISS(facebook提供的开源向量数据库）） 

2.价格查询 

3.直接回答（QWen3.5plus）   ->输出给用户

为什么选Qwen3.5plus？必须要有Funcion Calling的能力，才能让agent调用外部工具（RAG和价格查询）

今天遇到的困难：

1.人在美国，访问阿里的库又慢又不稳定，甚至访问不了，申请不了key。
解决方案：

1.用VPN访问（太贵了）

2.找国内朋友帮忙（懒得找）

3.等它加载完成，加载失败的话在URL里加上北京（https://bailian.console.aliyun.com/cn-beijing/?tab=model#/api-key）

最终选择方案3

2.明文存储密钥感觉不靠谱，弄了个.env文件，然后就跑不起来了...

解决方案：
1.把.env文件放在根目录下（并非放错目录）

2.在代码里用python-dotenv库加载.env文件（忘了加载了）

让Claude写的示例代码，居然漏写了，还好我又问了Gemini，一对账才发现问题。

今天做了什么：
验证了一下key能用，加了一个立即显示文本的小功能。