# -*- coding: utf-8 -*-
'''      
                    $$                                                               
                  $$$                                    &&&&$$$$##$$$$$$$$$$$$$$$$$$#$$$           
                 $$$              $$$$$$$$$$$$$$$        ##$$$$$$$$$$$$$$$$$$o;       ;             
                 $$$$$$$$$$$$$$$  $$$$$$$$$$$$$$$                      *$$o           #             
                $$$    $$$        $$$         $$$          $$$         *$$o        $$$$             
               $$*     $$$        $$$         $$$           $$$$       *$$o       $$$$              
                       $$$        $$$         $$$            $$$$      *$$o     $$$$                
                       $$o        $$$         $$$              $$$     *$$o    $$$o                 
               ;$$$$$$$$$$$$$$$$  $$$         $$$                      *$$o                         
               $$$$$$$$$$$$$$$$$* $$$         $$$     ;$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$         
                      $$$         $$$         $$$                      *$$o                         
                      $$$         $$$         $$$                      *$$o                         
                     $$$$$$$      $$$         $$$                      *$$o                         
                    $$$;  $$$$    $$$         $$$                      *$$o                         
                   $$$$     $$$   $$$$$ $$$$$$$$$                      *$$o                         
                 $$$$!       $$      $$$$*                             $$$;                         
               $$$$$                  ;                        $$$$$$$$$$$                          
                                                                  $$$$$$                            
'''


from zhihu import Question
from zhihu import Answer
from zhihu import User
from zhihu import Collection

import sys,pymysql,time

reload(sys)
sys.setdefaultencoding('utf-8')

def question_test(url):
    question = Question(url)

    # 获取该问题的标题
    title = question.get_title()
    # 获取该问题的详细描述
    detail = question.get_detail()
    # 获取回答个数
    answers_num = question.get_answers_num()
    # 获取关注该问题的人数
    followers_num = question.get_followers_num()
    # 获取该问题所属话题
    topics = question.get_topics()
    # 获取该问题被浏览次数
    visit_times = question.get_visit_times()
    # 获取排名第一的回答
    top_answer = question.get_top_answer()
    # 获取排名前十的十个回答
    top_answers = question.get_top_i_answers(10)
    # 获取所有回答
    answers = question.get_all_answers()

    print title  # 输出：现实可以有多美好？
    print detail
    # 输出：
    # 本问题相对于“现实可以多残酷？传送门：现实可以有多残酷？
    # 题主：       昨天看了“现实可以有多残酷“。感觉不太好，所以我
    # 开了这个问题以相对应，希望能够“中和一下“。和那个问题题主不想
    # 把它变成“比惨大会“一样，我也不想把这个变成“鸡汤故事会“，或者
    # 是“晒幸福“比赛。所以大家从“现实，实际”的角度出发，讲述自己的
    # 美好故事，让大家看看社会的冷和暖，能更加辨证地看待世界，是此
    # 题和彼题共同的“心愿“吧。
    print answers_num  # 输出：2441
    print followers_num  # 输出：26910
    for topic in topics:
        print topic,  # 输出：情感克制 现实 社会 个人经历
    print visit_times  # 输出: 该问题当前被浏览的次数
    print top_answer  # 输出：<zhihu.Answer instance at 0x7f8b6582d0e0>(Answer类对象)
    print top_answers  # 输出：<generator object get_top_i_answers at 0x7fed676eb320>(代表前十的Answer的生成器)
    print answers  # 输出：<generator object get_all_answer at 0x7f8b66ba30a0>(代表所有Answer的生成器)


def answer_test(answer_url):
    answer = Answer(answer_url)
    # 获取该答案回答的问题
    question = answer.get_question()
    # 获取该答案的作者
    author = answer.get_author()
    # 获取该答案获得的赞同数
    upvote = answer.get_upvote()
    # 获取改该答案所属问题被浏览次数
    visit_times = answer.get_visit_times()
    # 获取所有给该答案点赞的用户信息
    voters = answer.get_voters()
    # 把答案输出为txt文件
    answer.to_txt()
    # 把答案输出为markdown文件
    answer.to_md()

    print question
    # <zhihu.Question instance at 0x7f0b25d13f80>
    # 一个Question对象
    print question.get_title()  # 输出：现实可以有多美好？
    print author
    # <zhihu.User instance at 0x7f0b25425b90>
    # 一个User对象
    print voters # <generator object get_voters at 0x7f32fbe55730>(代表所有该答案点赞的用户的生成器)
    print author.get_user_id()  # 输出：田浩
    print upvote  # 输出：9320
    print visit_times  # 输出: 改答案所属问题被浏览次数

def prepare_insert_sql(table_name, data):
    sql = 'insert into '+table_name
    key_sql = " (" + ",".join( data.keys() ) + ") "
    val_sql = " ('" + "','".join( str(i) for i in data.values() ) + "') "
    sql = sql + key_sql + 'values' + val_sql
    return sql

# 爬取用户信息
def user_spider(user_url):
    database_name = 'wjw_zhihu'
    table_name = 'user_info'

    # 设置数据库连接
    conn=pymysql.connect(host='localhost',user='root',passwd='',port=3306)
    cur=conn.cursor()
    # 选择数据库
    conn.select_db(database_name)
    # 设置编码, 否则插入数据库乱码
    cur.execute('set names utf8')

    # 获取当前用户信息
    user = User(user_url)
    user_info = user.get_user_info()
    # print user_info;
    # sys.exit()

    # 将用户数据插入数据库
    try:
        insert_sql = prepare_insert_sql(table_name, user_info)
        res=cur.execute(insert_sql)
        conn.commit()       # commit之后才能真正提交到数据库
        print(user_info['user_unique'] + '  ------  ' + str(res))
    except Exception as e:
        # 打印日志, 记录异常信息
        exceptMsg = str(e)
        print(exceptMsg)


    # 获取该用户关注的人
    followees = user.get_followees()
    # 获取关注该用户的人
    followers = user.get_followers()

    # 统计该用户关注的人
    # i = 0
    # for followee in followees:
    #     print followee.user_url
    #     print followee.get_user_id()
    #     i = i + 1
    #     if i == 41:
    #         break


    # print followers
    # <generator object get_follower at 0x7ffcac3af0f0>
    # 代表所有关注该用户的人的生成器对象
    i = 0
    for follower in followers:
        i = i + 1
        if i <= 41:
            continue
        if i % 10 == 0:
            time.sleep(0.3)
        try:
            follower_info = follower.get_user_info()
            follower_insert_sql = prepare_insert_sql(table_name, follower_info)
            res=cur.execute(follower_insert_sql)
            conn.commit()
            print(follower_info['user_unique'] + '  ------  ' + str(res))
        except Exception as e:
            # 打印日志, 记录异常信息
            exceptMsg = str(e)
            print(exceptMsg)

    # print asks
    # <generator object get_ask at 0x7ffcab9db780>
    # 代表该用户提的所有问题的生成器对象
    # print answers
    # <generator object get_answer at 0x7ffcab9db7d0>
    # 代表该用户回答的所有问题的答案的生成器对象
    # print collections
    # <generator object get_collection at 0x7ffcab9db820>
    # 代表该用户收藏夹的生成器对象


def collection_test(collection_url):
    collection = Collection(collection_url)

    # 获取该收藏夹的创建者
    creator = collection.get_creator()
    # 获取该收藏夹的名字
    name = collection.get_name()
    # 获取该收藏夹下的前十个答案
    top_answers = collection.get_top_i_answers(10)
    # 获取该收藏夹下的所有答案
    answers = collection.get_all_answers()

    print creator
    # <zhihu.User instance at 0x7fe1296f29e0>
    # 一个User对象
    print creator.get_user_id()  # 稷黍
    print name  # 给你一个不同的视角
    print top_answers
    # <generator object get_top_i_answers at 0x7f378465dc80>
    # 代表前十个答案的生成器对象
    print answers
    # <generator object get_all_answer at 0x7fe12a29b280>
    # 代表所有答案的生成器对象


def test():
    url = "http://www.zhihu.com/question/24269892"
    question = Question(url)
    # 得到排名第一的答案
    answer = question.get_top_answer()
    # 得到排名第一的答案的作者
    user = answer.get_author()
    # 得到该作者回答过的所有问题的答案
    user_answers = user.get_answers()
    # 输出该作者回答过的所有问题的标题
    for answer in user_answers:
        print answer.get_question().get_title()
    # 得到该用户的所有收藏夹
    user_collections = user.get_collections()
    for collection in user_collections:
        # 输出每一个收藏夹的名字
        print collection.get_name()
        # 得到该收藏夹下的前十个回答
        top_answers = collection.get_top_i_answers(10)
        # 把答案内容转成txt，markdown
        for answer in top_answers:
            answer.to_txt()
            answer.to_md()

def spider_user():
    pass

def main():
    # url = "http://www.zhihu.com/question/24269892"
    # question_test(url)
    # answer_url = "http://www.zhihu.com/question/24269892/answer/29960616"
    # answer_test(answer_url)
    user_url = "https://www.zhihu.com/people/zhang-jia-wei"
    # user_url = "https://www.zhihu.com/people/wujunwei928"
    user_spider(user_url)
    # collection_url = "http://www.zhihu.com/collection/36750683"
    # collection_test(collection_url)
    # test()

# 知乎话题广场: https://www.zhihu.com/topics
# 知乎发现更多: https://www.zhihu.com/explore/recommendations

if __name__ == '__main__':
    main()

