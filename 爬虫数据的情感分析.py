import re
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
import json
import time
from collections import Counter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# 设置matplotlib的字体，以便可以显示中文
plt.rcParams['font.sans-serif'] = ['SimHei', 'Songti SC', 'STFangsong']
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 读取停用词文件
stopwords_file = 'stopwords.txt'
with open(stopwords_file, "r", encoding='utf-8') as words:
    stopwords = [i.strip() for i in words]

# 定义一个函数，用于对文本进行分词
def segment_text(texts):
    segmented_texts = []
    for text in texts:
        if len(text) == 0:
            continue
        seg_list = ' '.join(jieba.lcut(text, cut_all=True))
        segmented_texts.append(seg_list)
    return segmented_texts

# 定义一个函数，用于生成词云
def generate_wordcloud(text):
    wordcloud = WordCloud(width=1000,
                          height=700,
                          background_color='white',
                          font_path='simhei.ttf',
                          scale=15,
                          contour_width=5,
                          contour_color='red',
                          ).generate(text)
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# 定义一个函数，用于清理文本，包括删除URLs、特殊字符等
def clean_text(text):
    text = str(text)
    text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", text)  # 删除回复和@
    text = re.sub(r"\[\S+]", "", text)  # 删除[]
    URL_REGEX = re.compile(
        r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s('
        r')<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
        re.IGNORECASE)
    text = re.sub(URL_REGEX, "", text)  # 删除URLs
    for word in stopwords:
        text = text.replace(word, '')  # 删除停用词
    text = re.sub(r"\s+", " ", text)  # 删除多余的空格
    text = text.strip().replace(' ', '')  # 删除首尾空格和中间空格
    return text.strip()

# 定义一个函数，用于绘制词频图
def plot_word_frequency(text):
    word_list = jieba.cut(text)
    word_list = [word for word in word_list if word.strip()]
    word_counter = Counter(word_list)
    word_freq = word_counter.most_common(20)
    words, freqs = zip(*word_freq)

    plt.figure(figsize=(10, 8))
    plt.bar(words, freqs)
    plt.xticks(rotation=45)
    plt.xlabel('词语')
    plt.ylabel('频次')
    plt.title('笔记内容词语频次图')
    plt.show()

# 定义一个函数，用于获取百度API的token
def get_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': 'VuzeNQgoVOCFvuWECRqdIhqf',  # API Key
        'client_secret': 'X6I852BGpZZwe50QY9Mvtr3kHVPdbbBD'  # Secret Key
    }
    response = requests.post(url, data=data)
    return response.json()['access_token']

# 定义一个函数，用于获取文本的情感
def get_emotion(data, token):
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token={}'.format(token)
    headers = {'Content-Type': 'application/json'}
    data = {'text': data}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        print(f"Response for text: {data['text']}\n{json.dumps(result, ensure_ascii=False, indent=2)}")
        if result is not None and 'items' in result:
            item = result['items'][0]
            sentiment = item['sentiment']
            confidence = item.get('confidence', None)
            negative_prob = item.get('negative_prob', None)
            positive_prob = item.get('positive_prob', None)
            return sentiment, confidence, negative_prob, positive_prob
        else:
            print("No items in result")
            return None, None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None, None, None, None

# 定义一个函数，用于分析CSV文件中的数据
def analyze_csv(data, token, extra_column, keywords_column):
    sentiments = {0: 0, 1: 0, 2: 0}
    results = []
    for i, text in enumerate(data):
        print(f"Analyzing text: {text[:30]}...")  # 打印前30个字符以了解处理进度
        time.sleep(2)
        sentiment, confidence, negative_prob, positive_prob = get_emotion(text, token)
        if sentiment is not None:
            sentiments[sentiment] += 1
            results.append({
                '笔记内容': text,  # 这里将键改为中文
                '情感倾向': sentiment,
                '置信度': confidence,
                '负面概率': negative_prob,
                '正面概率': positive_prob,
                '笔记链接': extra_column[i],  # 添加第2列内容到结果中
                '关键词': keywords_column[i]  # 添加第13列内容到结果中
            })
        else:
            print(f"Failed to analyze text: {text[:30]}...")
    results_df = pd.DataFrame(results)
    results_df.to_csv('情感分析结果.csv', index=False, encoding='utf-8-sig')
    return sentiments

# 定义一个函数，用于绘制饼图
def plot_pie(sentiments):
    labels = ['Negative', 'Neutral', 'Positive']
    sizes = [sentiments[0], sentiments[1], sentiments[2]]
    colors = ['#FF9999', '#99CC99', '#66B3FF']
    explode = (0.1, 0, 0)

    plt.figure(figsize=(8, 8))  # 增加图像大小的设置
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Sentiment Analysis Results')
    plt.show()

# 定义一个函数，用于绘制条形图
def plot_bar(sentiments):
    labels = ['Negative', 'Neutral', 'Positive']
    sizes = [sentiments[0], sentiments[1], sentiments[2]]
    colors = ['#FF9999', '#99CC99', '#66B3FF']
    y_pos = range(len(labels))
    fig, ax = plt.subplots()
    ax.barh(y_pos, sizes, color=colors)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel('Amount')
    ax.set_title('Sentiment Analysis Results')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.show()

# 新增函数，用于保存负面信息
def save_negative_info():
    results_df = pd.read_csv('情感分析结果.csv')
    negative_info_df = results_df[results_df['情感倾向'] == 0]  # 判断情感列的内容是否为0
    negative_info_df.to_csv('负面信息收集.csv', index=False, encoding='utf-8-sig')


# 新增函数，用于发送邮件
def send_email(subject, body, to, attachment):
    from_addr = "450971619@qq.com"
    password = "fvxtvjfzufkebjaf"
    smtp_server = "smtp.qq.com"
    smtp_port = 465

    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to
    msg['Subject'] = subject

    # 邮件正文
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # 添加附件
    attachment_name = '负面信息收集.csv'
    with open(attachment, 'rb') as attach_file:
        mime = MIMEBase('text', 'csv', charset='utf-8')
        mime.set_payload(attach_file.read())
        encoders.encode_base64(mime)
        mime.add_header('Content-Disposition', f'attachment; filename="{attachment_name}"')
        msg.attach(mime)

    # 发送邮件
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # 使用SMTP_SSL
        server.login(from_addr, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# 主程序
if __name__ == "__main__":
    data = pd.read_csv('话题笔记数据.csv')  # 读取CSV文件
    xhs_content = data['笔记内容']  # 获取笔记内容
    xhs_content = xhs_content.drop_duplicates()  # 删除重复的笔记
    cleaned_content = xhs_content.apply(clean_text)  # 清理笔记内容
    segment_content = segment_text(cleaned_content)  # 对清理后的笔记内容进行分词
    content_text = ' '.join(segment_content)  # 将分词后的笔记内容连接成一个字符串
    generate_wordcloud(content_text)  # 生成词云
    total_text = ' '.join(cleaned_content)  # 将清理后的笔记内容连接成一个字符串
    plot_word_frequency(total_text)  # 绘制词频图
    ip_location = data['IP属地']  # 获取IP地址
    pie_labels = ip_location.value_counts()[:10].index  # 获取IP地址的前10个值
    plt.pie(ip_location.value_counts()[:10].values, labels=pie_labels, autopct='%1.2f%%', shadow=True)  # 绘制饼图
    plt.title("话题中IP属地的占比")
    plt.show()
    count = data[['笔记收藏数量', '笔记评论数量', '笔记点赞数量']]  # 获取笔记的收藏数量、评论数量和点赞数量
    count.sum(axis=0).plot(kind='bar')  # 绘制条形图

    # 情感分析
    token = get_token()
    extra_column = data.iloc[:, 1].tolist()  # 获取第二列内容
    keywords_column = data.iloc[:, 12].tolist()  # 获取第十三列内容
    sentiments = analyze_csv(cleaned_content, token, extra_column, keywords_column)
    plot_pie(sentiments)
    plot_bar(sentiments)

    # 保存负面信息
    save_negative_info()

    # 发送邮件
    subject = "负面信息收集报告"
    body = "附件是最新的负面信息收集报告，请查收。"
    to = "juwubafff@163.com"
    attachment = '负面信息收集.csv'
    send_email(subject, body, to, attachment)

