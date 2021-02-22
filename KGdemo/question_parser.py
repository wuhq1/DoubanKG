#CODE:"UTF-8"
#AUTHOR:"WUHEQING"

class QuestionParser:

    #构造实体节点
    def build_entitydict(self, args):
        entity_dict ={}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] =[arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict


    #解析主函数
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args) #{'moviename':'山楂树之恋'}
        question_types = res_classify['question_types']
        sqls=[] #[{'question_type':'name2english', 'sql':'match 语句'}]
        for question_type in question_types:
            sql_={}
            sql_['question_type'] = question_type # {'question_type':'name2english'}
            sql=[]
            if question_type =='name2english':
                sql = self.sql_transfer(question_type, entity_dict.get('moviename'))

            elif question_type == "movie2ID":
                sql = self.sql_transfer(question_type, entity_dict.get('moviename'))

            elif question_type == "movierank":
                sql = self.sql_transfer(question_type, entity_dict.get('moviename'))

            elif question_type == "link2":
                sql = self.sql_transfer(question_type, entity_dict.get('moviename'))

            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)
        return sqls



    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []
        # 查询语句
        sql = []
        # 查询电影的英文名字
        if question_type == 'name2english':
            sql =[ " MATCH p = (m:moviename) - [r:name2english]->(n:englishname) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]
        # 查询电影的评分
        elif question_type == 'movierank':

            sql = ["MATCH p=(m:moviename) -[r:movierank]->(n:ranknumber) where m.name='{0}' return m.name, n.name".format(i) for i in entities]
         # 查询电影的链接
        elif question_type == 'link2':
            sql = ["MATCH p=(m:moviename) -[r:link2]->(n:link1) where m.name='{0}' return m.name, n.name".format(i) for i in entities]

         # 查询电影的排名
        elif question_type == 'movie2ID':
            sql = ["MATCH p=(m:moviename) -[r:movie2ID]->(n:ID) where m.name='{0}' return m.name, n.name".format(i) for i in entities]

        return sql


if __name__ == '__main__':
        handler = QuestionParser()
