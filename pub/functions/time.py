# coding=utf-8
import time

# 可用的时间数据
def get_current_time():
    return int(time.time())

# 注册
def get_due_time(maintain_seconds):
    return int(time.time()) + int(maintain_seconds)

# 续费
def get_due_time(last_due_time,maintain_seconds):
    return int(last_due_time) + int(maintain_seconds)