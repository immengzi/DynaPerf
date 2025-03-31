def test_nested_loops():
    # 矩阵数据
    matrix_2x3 = [[1, 2, 3], [4, 5, 6]]
    matrix_3x2 = [[1, 2], [3, 4], [5, 6]]

    # 双重循环 - 矩阵转置
    rows = len(matrix_2x3)
    cols = len(matrix_2x3[0])
    result = [[0 for _ in range(rows)] for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix_2x3[i][j]

    # 三重循环 - 矩阵乘法
    rows_A = len(matrix_2x3)
    cols_A = len(matrix_2x3[0])
    cols_B = len(matrix_3x2[0])

    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += matrix_2x3[i][k] * matrix_3x2[k][j]

    # 单循环+while组合
    found = False
    for row in matrix_2x3:
        i = 0
        while i < len(row):
            if row[i] == 5:
                found = True
                break
            i += 1
        if found:
            break

# 直接调用函数
test_nested_loops()

"""
===== Nested Looping Analysis Report =====
Warning: Possible performance issue - maximum nesting depth is 3
Detected 5 unique nested loop structures

For /home/immengzi/test_dynapyt/example/example.py.orig: for loop (iid: 245):
  Maximum nesting depth: 2
  Nested loop structures:
  Structure #1:
    Level 1: for loop at /home/immengzi/test_dynapyt/example/example.py.orig (iid: 244)
  Performance suggestion: Monitor the performance of this double loop for large datasets

For /home/immengzi/test_dynapyt/example/example.py.orig: for loop (iid: 246):
  Maximum nesting depth: 2
  Nested loop structures:
  Structure #1:
    Level 1: for loop at /home/immengzi/test_dynapyt/example/example.py.orig (iid: 247)
  Performance suggestion: Monitor the performance of this double loop for large datasets

For /home/immengzi/test_dynapyt/example/example.py.orig: for loop (iid: 249):
  Maximum nesting depth: 2
  Nested loop structures:
  Structure #1:
    Level 1: for loop at /home/immengzi/test_dynapyt/example/example.py.orig (iid: 248)
  Performance suggestion: Monitor the performance of this double loop for large datasets

For /home/immengzi/test_dynapyt/example/example.py.orig: for loop (iid: 250):
  Maximum nesting depth: 3
  Nested loop structures:
  Structure #1:
    Level 1: for loop at /home/immengzi/test_dynapyt/example/example.py.orig (iid: 251)
  Structure #2:
    Level 1: for loop at /home/immengzi/test_dynapyt/example/example.py.orig (iid: 251)
    Level 2: for loop at /home/immengzi/test_dynapyt/example/example.py.orig (iid: 252)
  Performance suggestion: Consider refactoring code to reduce nesting depth, or use vectorization

===== Analysis Complete ====="
"""
