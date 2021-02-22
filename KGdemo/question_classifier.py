#CODE:"UTF-8"
#AUTHOR:"WUHEQING"

import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #特征词路径
        self.movienamepath = os.path.join(cur_dir, 'Data/moviename.txt')
        self.englishnamepath = os.path.join(cur_dir, 'Data/englishname.txt')
        self.ranknumberpath = os.path.join(cur_dir, 'Data/ranknumber.txt')
        self.IDpath = os.path.join(cur_dir, 'Data/ID.txt')
        self.linkpath = os.path.join(cur_dir, 'Data/link.txt')
        self.denypath  = os.path.join(cur_dir,'Data/deny.txt')
        #加载特征词
        #i.strip()默认删除i的头和尾的空白字符
        self.moviename_wds = [i.strip() for i in open(self.movienamepath, encoding = "utf-8" ) if i.strip()]
        self.englishname_wds = [i.strip() for i in open(self.englishnamepath, encoding="utf-8") if i.strip()]
        self.ranknumber_wds = [i.strip() for i in open(self.ranknumberpath, encoding="utf-8") if i.strip()]
        self.link_wds = [i.strip() for i in open(self.linkpath, encoding="utf-8") if i.strip()]
        self.ID_wds = [i.strip() for i in open(self.IDpath, encoding="utf-8") if i.strip()]
        self.regin_words = set(self.moviename_wds + self.englishname_wds + self.ranknumber_wds+self.ID_wds + self.link_wds)
        self.deny_words = [i.strip() for i in open(self.denypath, encoding="utf-8")if i.strip() ]
         #构建领域树actree
        self.regin_tree = self.build_actree(list(self.regin_words))
        #构建词典
        self.wdstype_dict = self.build_wdstype_dict()
        #问句疑问词
        self.moviename_wds=['影片', '电影', '排片', '院线']
        self.englishname_wds = ['英译本', '英文名字', '别名']
        self.ID_wds=['排名', '排号']
        self.ranknumber_wds = ['评分', '评价分数']
        self.link_wds= ['链接', '外部资源']
        print("model init finished...")

        return

    #分类主函数
    def classify(self, question):
        data={}

        movie_dict = self.check_movie(question) # {'山楂树之恋':['moviename']}
        if not movie_dict:
            if 'movie_dict' in globals():  # 判断是否是首次提问，若首次提问，则diseases_dict无值
                movie_dict = movie_dict
            else:
                return {}

        data['args'] = movie_dict #是个dict， {'args':{'山楂树之恋':['moviename']}}
        #收集问句当中涉及到的实体类型
        types =[] # ['moviename']
        for type_ in movie_dict.values():
            types += type_
        question_type = 'others'

        question_types = []
        #说明电影名字的英文
        if self.check_words(self.englishname_wds, question) and ('moviename' in types):
            question_type='name2english'
            question_types.append(question_type) #question_types为['name2english']

        #电影名字与评分
        if self.check_words(self.ranknumber_wds, question) and ('moviename' in types):
            question_type='movierank'
            question_types.append(question_type)

        #电影名字与排名
        if self.check_words(self.ID_wds, question) and ('moviename'in types):
            question_type = 'movie2ID'
            question_types.append(question_type)

        #电影名字与链接
        if self.check_words(self.link_wds, question) and ('moviename' in types):
            question_type = 'link2'
            question_types.append(question_type)

        #如果没找到相关的外部查询信息，那么将该电影的描述信息返回
        if question_type==[] and 'moviename' in types:
            question_types = ['moviename']
        data['question_types'] = question_types

#{'args':{'山楂树之恋':['moviename']},'question_types':['name2english'] }
        return data

    #构造词对应的类型
    def build_wdstype_dict(self):
        wd_dict = dict()
        for wd in self.regin_words:
            wd_dict[wd] = []
            if wd in self.moviename_wds:
                wd_dict[wd].append('moviename')
            if wd in self.englishname_wds:
                wd_dict[wd].append('englishname')
            if wd in self.ID_wds:
                wd_dict[wd].append('ID')
            if wd in self.link_wds:
                wd_dict[wd].append('link1')
            if wd in self.ranknumber_wds:
                wd_dict[wd].append('ranknumber')
        return wd_dict

    #构造actree, 加速过滤
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        #字典树上加上失配边，构成AC自动机
        for index , word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree




    #问句过滤
    def check_movie(self, question):
        global movie_dict

        region_wds = []
        for i in self.regin_tree.iter(question):
            wd =i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds ]
        final_dict ={i: self.wdstype_dict.get(i) for i in final_wds}
        if final_dict:
            movie_dict = final_dict

        return final_dict


    #基于特征词进行分类
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False

if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question =input("input an question:")
        data = handler.classify(question)
        print(data)


