import time
from typing import List, Optional
from zhipuai import ZhipuAI

from const.msg import refer_msg, eval_msg, question_msg, diff_map, similar_msg
from util.textProcess import process

client = ZhipuAI(api_key="7b1516a49710d181bb671927898a14b4.OCE2vCoySXStxYzx")


def print_with_typewriter_effect(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)


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
    return float(create(messages))


def generate_question(number: int,
                      courseName: str,
                      chapterName: str,
                      difficulty: int,
                      content: Optional[str] = None):
    messages = [
        {"role": "system", "content": "你是一名计算机专业的大学教授。"},
        {
            "role": "user",
            "content":
                similar_msg % (number,
                               courseName,
                               chapterName,
                               diff_map[difficulty],
                               content)
                if content else
                question_msg % (number,
                                courseName,
                                chapterName,
                                diff_map[difficulty])
        }
    ]
    print(create(messages))
    return process(create(messages))


def generate_recommend(behaviors: Optional[List[str]], number: int = 30):
    return []
