diff_map = {
    1: "简单",
    2: "中等",
    3: "困难"
}

refer_msg = '''
请根据我给出的题目内容，课程名称，章节名称，生成详细的解题思路和知识点。
题目内容为:%s，课程名称为：%s，章节名称为：%s。

回答格式为json字符串，但一定要以普通文本格式返回，在内容需要输出换行符时，输出'\\\\n'即可，例如：
{"idea": "解题思路","topic": "知识点"}

严格按照回答格式生成内容，不要输出其他内容！
'''

eval_msg = '''
请根据我给出的题目内容、我的答案和标准答案，对我的答案进行评分。
只需给出具体分数，不需要其他内容，满分为100分。

题目为：%s，我的答案为：%s，标准答案为：%s。

回答格式为：
分数(浮点数)

'''

question_msg = '''
请根据我给出的题目数量，课程名称，章节名称，题目难度，生成相应的题目（简答题）和答案。
题目数量为：%s，课程名称为：%s，章节名称为：%s，题目难度为：%s
回答格式为json字符串，但一定要以普通文本格式返回，在内容需要输出换行符时，输出'\\\\n'即可, 例如：
[{"content": "题目内容","answer": "答案内容"},...]

不要输出其它无关内容
'''

similar_msg = '''
请根据我给出的题目数量，课程名称，章节名称，题目难度，题目内容，生成与其类似的题目。
题目数量为：%s，课程名称为：%s，章节名称为：%s，题目难度为：%s，题目内容为：%s。
回答格式为json字符串，但一定要以普通文本格式返回，在内容需要输出换行符时，输出'\\\\n'即可, 例如：
[{"content": "题目内容"},...]

不要输出其它无关内容
'''
