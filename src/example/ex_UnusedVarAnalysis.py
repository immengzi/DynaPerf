def test_unused_vars():
    # 情况1：变量被覆盖前未使用
    num1 = 5
    num1 = 10  # num1=5 将被检测为未使用
    print(num1)

    # 情况2：变量声明后到程序结束都未使用
    never_used = "这个变量永远不会被使用"

    # 情况3：循环中的变量被覆盖
    for i in range(3):
        temp = i  # 每次循环都会覆盖前一次的值
        # 注意不使用temp

    # 情况4：使用过的变量
    used_var = 42
    print(used_var)  # 使用了变量

    return "Test completed"

test_unused_vars()

"""
UNUSED VARIABLE: var_at_iid_46 was written at IID 46 with value 0 but never read before being written again at IID 46
UNUSED VARIABLE: var_at_iid_46 was written at IID 46 with value 1 but never read before being written again at IID 46
===== Analysis Complete =====
NEVER USED: var_at_iid_40 was written at IID 40 with value 5 but never read until program end
NEVER USED: var_at_iid_43 was written at IID 43 with value 这个变量永远不会被使用 but never read until program end
NEVER USED: var_at_iid_46 was written at IID 46 with value 2 but never read until program end
Found 3 unused variables in total:
  Variables never used until program end: 3
  - var_at_iid_40 written at IID 40 with value 5 but never read
  - var_at_iid_43 written at IID 43 with value 这个变量永远不会被使用 but never read
  - var_at_iid_46 written at IID 46 with value 2 but never read
Total write operations tracked: 5
Total read operations tracked: 2
"""
