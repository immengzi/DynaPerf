def add_K_element(test_list, K):
    res = []
    for i in test_list:
        temp = []
        for j in i:
            temp.append(j+K)
    res.append(tuple(temp))
    return (res)

add_K_element([[1, 2, 3], [4, 5, 6]], 2)

"""
immengzi@Meng-PC:~/test_dynapyt/example$ python3 -m dynapyt.instrument.instrument --files ex_ObjectCreationInLoopAnalysis.py --analysis my_analysis.ObjectCreationInLoopAnalysis.ObjectCreationInLoopAnalysis
Done with ex_ObjectCreationInLoopAnalysis.py
immengzi@Meng-PC:~/test_dynapyt/example$ python3 -m dynapyt.run_analysis --entry ex_ObjectCreationInLoopAnalysis --analysis my_analysis.ObjectCreationInLoopAnalysis.ObjectCreationInLoopAnalysis
Setting coverage for None
[DEBUG] Entering for loop with iid 3, current loop_stack: []
[DEBUG] Loop tracking reset for iid 3
[DEBUG] New for loop started. Loop depth: 1
[DEBUG] List created in loop (iid 5).
[DEBUG] Recorded creation of list (key 5:list, object id 140220946853312) in loop iid 3
[DEBUG] Memory access recorded for list (iid 6, size 56)
[DEBUG] Variable assignment in loop (iid 3): key 6:list id 140220946853312
[DEBUG] Memory access recorded for list (iid 8, size 88)
[DEBUG] Entering for loop with iid 7, current loop_stack: [('for', 3)]
[DEBUG] Loop tracking reset for iid 7
[DEBUG] New for loop started. Loop depth: 2
[DEBUG] Memory access recorded for list (iid 9, size 56)
[DEBUG] Entering for loop with iid 7, current loop_stack: [('for', 3), ('for', 7)]
[DEBUG] Loop iid 7 iteration count: 1
[DEBUG] Iteration recorded in for loop with iid 7
[DEBUG] Memory access recorded for list (iid 9, size 88)
[DEBUG] Entering for loop with iid 7, current loop_stack: [('for', 3), ('for', 7)]
[DEBUG] Loop iid 7 iteration count: 2
[DEBUG] Iteration recorded in for loop with iid 7
[DEBUG] Memory access recorded for list (iid 9, size 88)
[DEBUG] Entering for loop with iid 7, current loop_stack: [('for', 3), ('for', 7)]
[DEBUG] Loop iid 7 iteration count: 3
[DEBUG] Iteration recorded in for loop with iid 7
[DEBUG] Entering for loop with iid 3, current loop_stack: [('for', 3), ('for', 7)]
[DEBUG] Loop iid 3 iteration count: 1
[DEBUG] Iteration recorded in for loop with iid 3
[DEBUG] List created in loop (iid 5).
[DEBUG] Recorded creation of list (key 5:list, object id 140220946851776) in loop iid 7
[DEBUG] Memory access recorded for list (iid 6, size 56)
[DEBUG] Variable assignment in loop (iid 7): key 6:list id 140220946851776
[DEBUG] Memory access recorded for list (iid 8, size 88)
[DEBUG] Entering for loop with iid 7, current loop_stack: [('for', 3), ('for', 7)]
[DEBUG] Loop iid 7 iteration count: 4
[DEBUG] Iteration recorded in for loop with iid 7
[DEBUG] Memory access recorded for list (iid 9, size 56)
[DEBUG] Entering for loop with iid 7, current loop_stack: [('for', 3), ('for', 7)]
[DEBUG] Loop iid 7 iteration count: 5
[DEBUG] Iteration recorded in for loop with iid 7
[DEBUG] Memory access recorded for list (iid 9, size 88)
[DEBUG] Entering for loop with iid 7, current loop_stack: [('for', 3), ('for', 7)]
[DEBUG] Loop iid 7 iteration count: 6
[DEBUG] Iteration recorded in for loop with iid 7
[DEBUG] Memory access recorded for list (iid 9, size 88)
[DEBUG] Entering for loop with iid 7, current loop_stack: [('for', 3), ('for', 7)]
[DEBUG] Loop iid 7 iteration count: 7
[DEBUG] Iteration recorded in for loop with iid 7
[DEBUG] Entering for loop with iid 3, current loop_stack: [('for', 3), ('for', 7)]
[DEBUG] Loop iid 3 iteration count: 2
[DEBUG] Iteration recorded in for loop with iid 3
[DEBUG] Memory access recorded for list (iid 13, size 56)
[DEBUG] Memory access recorded for list (iid 15, size 88)
[DEBUG] Memory access recorded for list (iid 16, size 88)
"""
