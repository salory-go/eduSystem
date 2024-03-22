import time
from typing import List

from fastapi.responses import StreamingResponse
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="7b1516a49710d181bb671927898a14b4.OCE2vCoySXStxYzx")

difficulty_map = {
    1: "easy",
    2: "medium",
    3: "hard"
}


def create(message: List[dict], top_p: float = 0.7, temperature: float = 0.9, max_tokens: int = 2000):
    response = client.chat.completions.create(
        model="glm-4",
        messages=message,
        top_p=top_p,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response


def print_with_typewriter_effect(text, delay=0.05):
    for char in text:
        print(char, end='')
        time.sleep(delay)


def generate_ideas(content: str, courseName: str, chapterName: str):
    messages = [
                   {"role": "system", "content": "你是一名计算机专业的大学教授。"},
                   {
                       "role": "user",
                       "content": "请根据我给出的题目内容，课程名称，章节名称，"
                                  "生成一份详细的解析，要求解析内容详细，条理清晰，语言通俗易懂。"
                                  "随后再生成这个题目所考察的知识点，要求知识点准确，全面，不重复。"
                                  "题目内容为：" +
                                  content + "，课程名称为：" + courseName + "，章节名称为：" +
                                  chapterName + "。" + "输出格式为：“解题思路：\n知识点:\n”"
                   }
               ]
    response = create(messages)



def generate_evaluate(content: str, answer: str):
    messages = [
        {"role": "system", "content": "你是一名计算机专业的大学教授。"},
        {
            "role": "user",
            "content": "请根据我给出的题目内容，对我的答案进行评分，只需给出具体分数，不需要其他内容，满分为100分。"
                       "题目为：" + content + "，我的答案为：" + answer + "。"
                                                                       "回答格式为：分数(浮点数)\n"}
    ]
    response = create(messages)



def generate_question(courseName: str, chapterName: str, difficulty: int, number: int):
    messages = [
        {"role": "system", "content": "你是一名计算机专业的大学教授。"},
        {
            "role": "user",
            "content": "请帮我生成" + str(number) + "道关于" + courseName + "课程的题目，课程章节为"
                       + chapterName + "，题目难度为" + difficulty_map[difficulty]
                       + "，题目内容为普通文本格式，并给出对应的答案" + "，题目和答案之间用---分隔。直接给出内容，题目开头不需要写出“题目：”，答案开头不需要写出“答案：”"
        }
    ]
    response = create(messages)



# response = client.chat.completions.create(
#     model="glm-4",
#     messages=[
#         {"role": "system", "content": "你是一个计算机网络的大学教授。"},
#         {"role": "user", "content": "请生成4道题目，课程是计算机网络，章节是物理层，难度为中等，并给出对应的答案。 以普通文本格式返回。"},
#     ],
#     top_p=0.7,
#     temperature=0.9,
#     stream=True,
#     max_tokens=2000,
# )
#
# # print(StreamingResponse(content=answer_text, headers=stream_response_headers, media_type="text/event-stream"))
#
# if response:
#     for chunk in response:
#         content = chunk.choices[0].delta.content
#         print_with_typewriter_effect(content)

# generate_ideas("在物理层中，以下哪种设备通常用于连接多个网络设备，并使用广播方式发送数据？\na) 路由器\nb) 交换机\nc) 集线器\nd) 网桥","计算机网络","物理层")
# generate_evaluate("在物理层中，以下哪种设备通常用于连接多个网络设备，并使用广播方式发送数据？\na) 路由器\nb) 交换机\nc) 集线器\nd) 网桥","c")
generate_question("计算机网络", "物理层", 2,2)
