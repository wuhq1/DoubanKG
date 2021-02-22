#CODE:"UTF-8"
#AUTHOR:"WUHEQING"
#首先要进行分步骤：1、问题分类 2、问题解析 3、问题搜索

from question_classifier import *
from answer_searcher import *
from question_parser import *
#问答部分
class chatbotmoviegraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionParser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = "您好，我是小清助理，希望能够帮助到你了解电影相关知识"
        res_classify = self.classifier.classify(sent)
        # {'args': {'山楂树之恋': ['moviename']}, 'question_types': ['name2english']}
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)


if __name__ == '__main__':
    handler = chatbotmoviegraph()
    while 1:
        question = input("用户：")
        answer = handler.chat_main(question)
        print("小清（问答小能手）", answer)
