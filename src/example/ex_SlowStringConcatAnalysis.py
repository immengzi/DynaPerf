s = ''
for i in range(10):
    s += str(i) + ' '
print(s)

"""
immengzi@Meng-PC:~/test_dynapyt/example$ python3 -m dynapyt.instrument.instrument --files ex_SlowStringConcatAnalysis.py --analysis my_analysis.SlowStringConcatAnalysis.SlowStringConcatAnalysis
Done with ex_SlowStringConcatAnalysis.py
immengzi@Meng-PC:~/test_dynapyt/example$ python3 -m dynapyt.run_analysis --entry ex_SlowStringConcatAnalysis --analysis my_analysis.SlowStringConcatAnalysis.SlowStringConcatAnalysis
Setting coverage for None
Possible slow string concatenation in /home/immengzi/test_dynapyt/example/ex_SlowStringConcatAnalysis.py.orig at 1
Possible slow string concatenation in /home/immengzi/test_dynapyt/example/ex_SlowStringConcatAnalysis.py.orig at 1
Possible slow string concatenation in /home/immengzi/test_dynapyt/example/ex_SlowStringConcatAnalysis.py.orig at 1
Possible slow string concatenation in /home/immengzi/test_dynapyt/example/ex_SlowStringConcatAnalysis.py.orig at 1
Possible slow string concatenation in /home/immengzi/test_dynapyt/example/ex_SlowStringConcatAnalysis.py.orig at 1
Possible slow string concatenation in /home/immengzi/test_dynapyt/example/ex_SlowStringConcatAnalysis.py.orig at 1
0 1 2 3 4 5 6 7 8 9
"""
