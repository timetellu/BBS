"""
求一个0~255的随机数
"""

# import random
# ret = random.randint(0, 255)
# print(ret)


# 如何生成五位数的字母和数字随机组合的验证码, "A3bv7"
import random
tmp_list = []
for i in range(6):
    u = chr(random.randint(65, 90))  # 生成大写字母
    l = chr(random.randint(97, 122))  # 生成小写字母
    n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

    # random.choice(): 可以从任何序列，比如list列表中，选取一个随机的元素返回，可以用于字符串、列表、元组等
    tmp = random.choice([u, l, n])
    tmp_list.append(tmp)
    print(tmp_list)

print("".join(tmp_list))
