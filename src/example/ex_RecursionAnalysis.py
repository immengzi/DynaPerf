def fib(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

fib(15)

"""
immengzi@Meng-PC:~/test_dynapyt/example$ python3 -m dynapyt.instrument.instrument --files example_RecursionAnalysis.py --analysis my_analysis.RecursionAnalysis.RecursionAnalysis
Done with example_RecursionAnalysis.py
immengzi@Meng-PC:~/test_dynapyt/example$ python3 -m dynapyt.run_analysis --entry example_RecursionAnalysis.py --analysis my_analysis.RecursionAnalysis.RecursionAnalysis
Setting coverage for None
Recursion depth exceeded for function fib at 0. Current depth: 11\"
"""
