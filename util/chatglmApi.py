import time
from typing import List
from zhipuai import ZhipuAI

from const.msg import reference_msg, eval_msg, question_msg

client = ZhipuAI(api_key="7b1516a49710d181bb671927898a14b4.OCE2vCoySXStxYzx")


def print_with_typewriter_effect(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)


# if response:
#     for chunk in response:
#         content = chunk.choices[0].delta.content
#         print_with_typewriter_effect(content)

difficulty_map = {
    1: "简单",
    2: "中等",
    3: "困难"
}


def create(message: List[dict], top_p: float = 0.7, temperature: float = 0.5, max_tokens: int = 2000):
    res = client.chat.completions.create(
        model="glm-4",
        messages=message,
        top_p=top_p,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return res.choices[0].message.content


def generate_ideas(content: str, courseName: str, chapterName: str):
    messages = [
        {"role": "system", "content": "你是一名计算机专业的大学教授。"},
        {
            "role": "user",
            "content": reference_msg % (content, courseName, chapterName)
        }
    ]
    res = create(messages)
    return res


def generate_eval(content: str, studentAnswer: str, answer):
    messages = [
        {"role": "system", "content": "你是一名计算机专业的大学教授。"},
        {
            "role": "user",
            "content": eval_msg % (content, studentAnswer, answer)
        }
    ]
    res = create(messages)
    return res


def generate_question(number: int, courseName: str, chapterName: str, difficulty: int):
    messages = [
        {"role": "system", "content": "你是一名计算机专业的大学教授。"},
        {
            "role": "user",
            "content": question_msg % (number, courseName, chapterName, difficulty_map[difficulty])
        }
    ]
    res = create(messages)
    return res


# generate_ideas("在数据链路层中，什么是帧？请简述帧的主要作用。", "计算机网络", "数据链路层")
generate_question(2, "计算机网络", "数据链路层", 2)
