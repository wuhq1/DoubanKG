#CODE:"UTF-8"
#AUTHOR:"WUHEQING"
from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="123456")
        self.num_limit = 10

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql'] #查询语句
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'name2english':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的英文版本有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'movie2ID':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '这部电影{0}所在的排名是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'movierank':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}这部电影的豆瓣评分为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'link2':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}这部电影的链接是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))


        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
