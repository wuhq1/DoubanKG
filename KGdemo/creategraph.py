#CODE:"UTF-8"
#AUTHOR:"WUHEQING"
#CODE:"UTF-8"
#AUTHOR:"WUHEQING"
import os
import json
from py2neo import Graph, Node

class Moviegraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path=os.path.join(cur_dir, 'data/Option.json')
        self.g= Graph(
            host="127.0.0.1",
            http_port= 7474,
            user = "neo4j",
            password= "123456"
        )
    '读取文件'
    def read_nodes(self):
        #共有5个节点
        ID=[]
        moviename =[]
        englishname =[]
        ranknumber =[]
        movie_info = []
        link1 =[]
        #构建节点实体关系

        rels_name2english = [] #中文名字与英文名字的对应
        rels_movierank =[] #电影与排名得分的对应
        rels_movie2ID =[] #电影与top250的对应
        rels_link2=[] #电影与连接的对应
        count =0
        for data in open(self.data_path, encoding = "utf-8"):
            movie_dict = {}
            count+=1
            print(count)
            data_json = json.loads(data)
           # print(data_json)
            movie = data_json["moviename"]
            movie_dict["moviename"] =movie
            moviename.append(movie)

            movie_dict['englishname'] = ""
            movie_dict['ranknumber'] =""
            movie_dict['link1'] = ""
            movie_dict['ID'] = ""


            if 'englishname' in data_json:
                englishname+=data_json['englishname'] #此时英文名字返回是个列表
                for engna in data_json['englishname']:
                    rels_name2english.append([movie, engna])
                # movie_dict['englishname'] = englishname
            if 'ranknumber' in data_json:
                ranknumber+=data_json['ranknumber']
                # print(ranknumber)
                for rank in data_json['ranknumber']:
                    rels_movierank.append([movie, rank])

            if 'link1' in data_json:
                link1 += data_json['link1']
                for link in data_json['link1']:
                    rels_link2.append([movie, link])
            if 'ID' in data_json:
                ID += data_json['ID']
                for ID1 in data_json['ID']:
                    rels_movie2ID.append([movie, ID1])
            if 'ID'in data_json:
                movie_dict['ID'] = data_json['ID']
            if 'moviename' in data_json:
                movie_dict['moviename'] = data_json['moviename']
            if 'ranknumber' in data_json:
                movie_dict['ranknumber'] = data_json['ranknumber']
            if 'link1' in data_json:
                movie_dict['link1'] = data_json['link1']
            if 'englishname' in data_json:
                movie_dict['englishname'] = data_json['englishname']
            movie_info.append(movie_dict)
        return set(ID),set(moviename),set(englishname), set(ranknumber), set(link1),  movie_info, rels_movie2ID, rels_name2english, rels_movierank,rels_link2


    #建立节点
    def creat_nodes(self, label, nodes):
        count =0
        for node_name in nodes:
            node =Node(label, name = node_name)
            self.g.create(node)
            count+=1
            print(count, len(nodes))
        return

    # 创建知识图谱中心结点
    def create_movie_nodes(self, movie_info):
        count =0
        for movie_dict in movie_info:
            node = Node("Movie", moviename=movie_dict['moviename'], englishname = movie_dict['englishname'],
                        ranknumber=movie_dict['ranknumber'], ID=movie_dict['ID'], link1 = movie_dict['link1'])
            self.g.create(node)
            count+=1
            print(count)
        return

    # 创建知识图谱实体节点类型schema
    def creat_graphnodes(self):
        ID, moviename, englishname, ranknumber,link1, movie_info, rels_movie2ID ,rels_name2english,rels_movierank, rels_link2= self.read_nodes()
        self.create_movie_nodes(movie_info)
        # print(moviename, englishname, ranknumber)
        # self.create_movie_nodes()
        self.creat_nodes('ID', ID)
        print(len(ID))
        self.creat_nodes('moviename', moviename)
        print(len(moviename))
        self.creat_nodes('englishname', englishname)
        print(len(englishname))
        self.creat_nodes('ranknumber', ranknumber)
        print(len(ranknumber))
        self.creat_nodes('link1', link1)
        print(len(link1))
        return


    #创建实体关联边
    def creat_relationship(self, start, end, edges, rel_type, rel_name):
        count = 0
        #去重处理
        set_edges =[]
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set_edges:
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query ="match(p:%s) , (q:%s) where p.name = '%s' and q.name = '%s' create (p) -[rel:%s{name :'%s'}] ->(q)" %(start, end, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count+=1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return


    #创建实体关系边
    def create_graphrel(self):
        ID, moviename, englishname, ranknumber,link1, movie_info,rels_movie2ID, rels_name2english,rels_movie2rank, rels_link= self.read_nodes()
        self.creat_relationship('moviename', 'ID', rels_movie2ID, 'movie2ID', '电影排名')
        self.creat_relationship('moviename', 'englishname', rels_name2english, 'name2english', '中英对照')
        self.creat_relationship('moviename', 'ranknumber', rels_movie2rank, 'movierank', '电影评分')
        self.creat_relationship('moviename', 'link1', rels_link, 'link2','电影链接' )

    #导出数据
    def export_data(self):
        ID,moviename,englishname, ranknumber, link1, movie_info, rels_movie2ID, rels_name2english, rels_movie2rank,rels_link= self.read_nodes()
        f_ID = open('ID.txt', 'w+', encoding = "utf_8")
        f_moviename = open('moviename.txt', 'w+', encoding = "utf_8")
        f_englishname = open('englishname.txt', 'w+', encoding = "utf_8")
        f_ranknumber = open('ranknumber.txt', 'w+', encoding = "utf_8")
        f_link = open('link.txt', 'w+', encoding = "utf_8")

        f_ID.write('\n'.join(list(ID)))
        f_moviename.write('\n'.join(list(moviename)))
        f_englishname.write('\n'.join(list(englishname)))
        f_ranknumber.write('\n'.join(list(ranknumber)))
        f_link.write('\n'.join(list(link1)))

        f_ID.close()
        f_moviename.close()
        f_englishname.close()
        f_ranknumber.close()
        f_link.close()

        return


if __name__ == '__main__':
        handler = Moviegraph()
        print('step1:导入节点进neo4j')
        handler.creat_graphnodes()
        print("step2:导入关系进neo4j")
        handler.create_graphrel()
        # handler.export_data()




