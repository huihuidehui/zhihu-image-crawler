## 爬取知乎某个问题下所有回答的图片
使用的python模块包括，grequest、click.

## 使用

1. clone到你的电脑 `git clone https://github.com/laodiaoyadashu/zhihu-image-crawler.git`
2. 切换目录 `cd zhihu-image-crawler`
3. 安装依赖 `pip install -r requirements.txt`
4. 命令说明 `python main.py`接受两个参数,你也可以使用`python main.py --help`获取帮助。
### 参数说明
1. `question`: 你想要爬取的问题id,例如在这个问题中`question`就是`299205851` `https://www.zhihu.com/question/299205851`
2. `votenum`: 将会过滤掉点赞数小于该值的回答.
	例如：`python main.py --question 299205851 --votenum 800`
