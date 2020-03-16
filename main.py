#  -*- coding: utf-8 -*-
import json
import re
import grequests
import threading
import os
import click
# import sys

# sys.setrecursionlimit(1000000)  # 例如这里设置为一百万

BASE_URL = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&limit={}"
IMG_BASE_URL = "https://pic3.zhimg.com{}"


class ZhSpider(object):

    def __init__(self, question_id, min_voted_num):
        """
        :param question_id: 问题ID，列表形式
        :param min_voted_num: 将会过滤掉点赞数小于这个值得回答
        """
        self.min_voted_num = min_voted_num
        self.question_url = BASE_URL.format(question_id, 3)
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "en-us",
                        "Connection": "keep-alive",
                        "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7"}

    def start(self):
        """
        启动爬虫
        """
        # 创建images目录
        if not os.path.exists('images'):
            os.mkdir('images')
            print("已创建目录 'images', 所有的图片将会保存在该目录下")

        print('start')
        response = self.get(self.question_url)
        next_page_answer_url = self.parse(response)
        while next_page_answer_url is not None:
            response = self.get(next_page_answer_url)
            next_page_answer_url = self.parse(response)
        print("Done!")
    def get(self, url):
        """
        发送get请求，返回请求响应
        """
        rs = set([grequests.get(url, headers=self.headers)])
        response = grequests.map(rs)[0]

        return response

    def parse(self, response):
        print("开始新的一页")
        print("开始处理响应...")
        dic = json.loads(response.text)
        # 此相应中的回答,过滤掉点赞数小于800的回答
        answers_list = [
            answer for answer in dic.get('data')
            if answer.get('voteup_count') > self.min_voted_num
        ]
        if len(answers_list) is not 0:
            # 知乎的回答是按照点赞数来排序的，点赞数高的排在前面。所有只要爬到点赞数都不大于指定值的第一页就可以停下来了。
            for answer in answers_list:
                answer_html_content = answer.get('content')
                # 正则选出回答中的img url
                incomplete_urls = re.findall(
                    r'https:\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?',
                    answer_html_content)
                # 使用集合去除重复图片
                tmp_img_urls = set([later_url for _, later_url in incomplete_urls])
                # 过滤高清大图
                img_urls = []
                for img_url in tmp_img_urls:
                    if img_url[-5] == 'r':
                        img_urls.append(IMG_BASE_URL.format(img_url))
                print("开始下载图片:{}张.".format(len(img_urls)))
                rs = (grequests.get(u, headers=self.headers, timeout=5) for u in img_urls)
                res = grequests.map(rs)
                # 过滤掉404响应
                res = [i for i in res if i.status_code == 200]
                print("开始保存图片: {}张.".format(len(res)))
                self.save_imgs(res)
                # save_img_t = threading.Thread(target=self.save_imgs, args=(res,))
                # print("开始保存图片: {}张".format(len(res)))
                # save_img_t.start()
            else:
                # 终止爬虫
                return None

        if not dic.get('paging').get('is_end'):
            next_url = dic.get('paging').get('next')
            return next_url
        else:
            return None

    def save_imgs(self, data):
        """
        :return:
        """
        for i in data:
            with open('images/' + i.request.url[-18:], 'wb') as f:
                f.write(i.content)
        print("成功保存图片：{}张.".format(len(data)))


@click.command()
@click.option('--question', default="296631231", help="问题id", type=str)
@click.option('--votenum', default=800, help="最小点赞数,将会过滤掉点赞数小于该值得回答", type=int)
def start(question, votenum):
    """

    :param answers:
    :param votenum:
    :return:
    """
    # print(question, votenum)
    zh_spider = ZhSpider(question, votenum)
    zh_spider.start()


if __name__ == "__main__":
    start()
