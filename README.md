## 爬取知乎某个问题下所有回答的图片
使用的python模块包括，grequest、click.[参考文章](https://www.huihuidehui.com/posts/4fcb5fd7.html)

## 使用

1. clone到你的电脑 `git clone https://github.com/laodiaoyadashu/zhihu-image-crawler.git`
2. 切换目录 `cd zhihu-image-crawler`
3. 安装依赖 `pip install -r requirements.txt`
4. 命令说明 `python main.py`接受两个参数,你也可以使用`python main.py --help`获取帮助。
### 参数说明
1. `question`: 你想要爬取的问题id,例如在这个问题中`question`就是`296631231` `https://www.zhihu.com/question/296631231`
2. `votenum`: 将会过滤掉点赞数小于该值的回答.
	例如：`python main.py --question 296631231 --votenum 1000`

### 注意
代码中加入了`sleep`用来减小爬虫的频率。不管怎么爬，一定要保证知乎正常的服务。

### 运行截图

<img src="https://www.huihuidehui.com/postimg/20200330184235.png" style="zoom: 25%;" />

