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
    1: "easy",
    2: "medium",
    3: "hard"
}


def create(message: List[dict], top_p: float = 0.7, temperature: float = 0.9, max_tokens: int = 2000):
    res = client.chat.completions.create(
        model="glm-4",
        messages=message,
        stream=True,
        top_p=top_p,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return res


def generate_ideas(content: str, courseName: str, chapterName: str):
    messages = [
        {"role": "system", "content": "你是一名计算机专业的大学教授。"},
        {
            "role": "user",
            "content": reference_msg % (content, courseName, chapterName)
        }
    ]
    res = create(messages)
    print(res)


def generate_eval(content: str, studentAnswer: str, answer):
    messages = [
        {"role": "system", "content": "你是一名计算机专业的大学教授。"},
        {
            "role": "user",
            "content": eval_msg % (content, studentAnswer, answer)
        }
    ]
    res = create(messages)
    print(res)


def generate_question(courseName: str, chapterName: str, difficulty: int, number: int):
    messages = [
        {"role": "system", "content": "你是一名计算机专业的大学教授。"},
        {
            "role": "user",
            "content": question_msg % (number, courseName, chapterName, difficulty_map[difficulty])
        }
    ]
    res = create(messages)
    if res:
        for chunk in res:
            content = chunk.choices[0].delta.content
            print_with_typewriter_effect(content)


generate_question("计算机网络", "物理层", 2, 3)
