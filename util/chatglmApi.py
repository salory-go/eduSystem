import time
from typing import List
from zhipuai import ZhipuAI

from const.msg import refer_msg, eval_msg, question_msg, diff_map
from util.textProcess import process

client = ZhipuAI(api_key="7b1516a49710d181bb671927898a14b4.OCE2vCoySXStxYzx")


def print_with_typewriter_effect(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)


# if response:
#     for chunk in response:
#         content = chunk.choices[0].delta.content
#         print_with_typewriter_effect(content)


def create(message: List[dict],
           top_p: float = 0.7,
           temperature: float = 0.9,
           max_tokens: int = 2000):
    res = client.chat.completions.create(
        model="glm-4",
        messages=message,
        top_p=top_p,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return res.choices[0].message.content


def generate_refer(content: str,
                   courseName: str,
                   chapterName: str):
    messages = [
        {"role": "system", "content": "你是一名计算机专业的大学教授。"},
        {
            "role": "user",
            "content": refer_msg % (content, courseName, chapterName)
        }
    ]
    return process(create(messages))


def generate_eval(content: str,
                  studentAnswer: str,
                  answer: str):
    messages = [
        {"role": "system", "content": "你是一名计算机专业的大学教授。"},
        {
            "role": "user",
            "content": eval_msg % (content, studentAnswer, answer)
        }
    ]
    return create(messages)


def generate_question(number: int,
                      courseName: str,
                      chapterName: str,
                      difficulty: int):
    messages = [
        {"role": "system", "content": "你是一名计算机专业的大学教授。"},
        {
            "role": "user",
            "content": question_msg % (number, courseName, chapterName, diff_map[difficulty])
        }
    ]
    return process(create(messages))

# print_with_typewriter_effect(generate_ideas("在数据链路层中，什么是帧？请简述帧的主要作用。", "计算机网络", "数据链路层"))
