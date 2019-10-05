def fun1(n):
    while n > 0:      # 判断输入是否合法，合法进入循环
        def fun2(n):
            if n == 1:
                return 1
            elif n == 2:
                return 2
            else:
                return 3
        temp = fun2(n)
        print("第"+n+"项的值是："+temp)      # 输出第n项的值
        return fun2(n)+fun2(n-1)             # 返回前n项的和
    return "input error"    # 对于不合法输入的返回
res = fun1(3)
print("前n项的和是 "+res)