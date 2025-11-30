#!/usr/bin/env python3
"""
简单的 Python 测试文件
用于测试 Git push 功能
"""


def hello_world():
    """打印 Hello World"""
    print("Hello, World!")
    print("这是一个测试文件，用于验证 Git push 功能")


def add_numbers(a, b):
    """简单的加法函数"""
    return a + b


if __name__ == "__main__":
    hello_world()
    result = add_numbers(5, 3)
    print(f"5 + 3 = {result}")
