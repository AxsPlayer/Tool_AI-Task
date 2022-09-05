# -*- coding: utf-8 -*-
from rembg import remove
import matplotlib.pyplot as plt  # 数据可视化
import jieba  # 词语切割
import wordcloud  # 分词
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS  # 词云，颜色生成器，停止词
import numpy as np  # 科学计算
from PIL import Image # 处理图片
import collections  # 词频统计库
import re
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence


class WordCloudCreator(object):
    """
    根据图片和文字创建词云
    """
    def __init__(self, file_path, pic_path, pic_process=True, text_process=True):
        """
        Initialization.
        """
        self.file_path = file_path
        self.pic_path = pic_path
        self.pic_process = pic_process
        self.text_process = text_process

    def run(self):
        """
        Create word cloud result.
        """
        if self.pic_process:
            # 第一步：读取图片并去除背景
            input = Image.open(self.pic_path)
            output = remove(input)
            output_path = 'output_rm.png'
            output.save(output_path)

            # 第二步：将去除背景的图片背景转换为白色（为了词云图背景设置）
            img = Image.open(output_path).convert('RGBA')
            W, L = img.size
            white_pixel = (255, 255, 255, 255)  # 白色
            for h in range(W):
                for i in range(L):
                    if img.getpixel((h, i)) in [(0, 0, 0, 0)]:
                        img.putpixel((h, i), white_pixel)  # 设置透明
            img.save(output_path)  # 自己设置保存地址
            self.pic_path = output_path

        # 第三步：对文章内容进行处理，并提取关键词计算词频/词权重
        stopwords = [i.strip() for i in open('cn_stopwords.txt').readlines()]
        stopwords.extend(['没有', '一个', '现在', '像是'])
        if self.text_process:
            text = codecs.open('clj.txt', 'r', 'utf-8').read()
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=text, lower=True, window=2)
            frequency_dic = {}
            for item in tr4w.get_keywords(1000, word_min_len=2):
                if item.word in stopwords:
                    continue
                frequency_dic[item.word] = item.weight
            word_counts = frequency_dic
        else:
            with open(self.file_path, 'r', encoding='utf8') as f:  # 打开新的文本转码为gbk
                textfile = f.read()  # 读取文本内容
            # 文本预处理
            pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
            textfile = re.sub(pattern, '', textfile)  # 将符合模式的字符去除
            wordlist = jieba.lcut(textfile)  # 切割词语
            for i in range(len(wordlist) - 1, -1, -1):
                if wordlist[i] in stopwords or len(wordlist[i]) < 2:
                    del wordlist[i]
            word_counts = collections.Counter(wordlist)

        # 第四步：生成词云图
        backgroud = np.array(Image.open(self.pic_path))
        wc = WordCloud(width=1400, height=2200,
                       background_color='white',
                       mode='RGB',
                       mask=backgroud,  # 添加蒙版，生成指定形状的词云，并且词云图的颜色可从蒙版里提取
                       max_words=500,
                       stopwords=STOPWORDS,  # 内置的屏蔽词,并添加自己设置的词语
                       font_path='msyh.ttc',
                       max_font_size=150,
                       relative_scaling=0.6,  # 设置字体大小与词频的关联程度为0.4
                       random_state=50,
                       scale=2
                       ).generate_from_frequencies(word_counts)
        image_color = ImageColorGenerator(backgroud)  # 设置生成词云的颜色，如去掉这两行则字体为默认颜色
        wc.recolor(color_func=image_color)

        # plt.imshow(wc)  # 显示词云
        # plt.axis('off')  # 关闭x,y轴
        # plt.show()  # 显示
        wc.to_file('wordcloud.png')   # 保存词云图


