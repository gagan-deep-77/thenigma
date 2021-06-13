import requests

from bs4 import BeautifulSoup
# from . import options
from .import options


def ques_dict(url):
    URL = url

    form_page = requests.get(URL)

    soup = BeautifulSoup(form_page.content, "html.parser")

    results = soup.find_all(
        class_="freebirdFormviewerComponentsQuestionBaseTitle")

    question_list = []
    for question in results:
        question_list.append(question.text)

    optionss = options.get_options(URL)

    # print(optionss)


# i = 1
# j = 0
# for item in range(no_op_per_ques):
#     question_list.append(all_option_list[j:no_question * i])
#     j += 4
#     i += 1

    ques_ans_dict = {}
    no_op_ques = int(len(optionss)) / int(len(question_list))
    # print(no_op_ques)
    start_count = 0
    j = int(no_op_ques)
    for item in question_list:
        # for i in option_list[start_count:j]:
        #     ques_ans_dict[item].append(i)
        ques_ans_dict[item] = optionss[start_count:j]
        start_count += int(no_op_ques)
        j += int(no_op_ques)
    # print(ques_ans_dict)
    return ques_ans_dict
