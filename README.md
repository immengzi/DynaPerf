# DynaPerf

DynaPerf is a code performance optimization tool based on [DynaPyt](https://github.com/sola-st/DynaPyt).

## Getting Started

### 1. Install DynaPyt
Before using DynaPerf, ensure you have installed DynaPyt by following the [installation guide](https://github.com/sola-st/DynaPyt?tab=readme-ov-file#installation).

### 2. Learn the Basics of DynaPyt
DynaPyt provides dynamic instrumentation and runtime analysis. Familiarize yourself with its basic usage before proceeding.

### 3. Instrument and Analyze Code
To instrument and analyze Python code using DynaPyt, use the following commands:

```sh
# Instrument the code
python3 -m dynapyt.instrument.instrument --files <path_to_python_file> <analysis_class_full_dotted_path>

# Run the analysis
python -m dynapyt.run_analysis --entry <entry_file_python> --analysis <analysis_class_full_dotted_path>
```

## Custom Performance Analyses
DynaPerf includes several predefined analyses to detect common performance bottlenecks in Python code.

| Issue ID | Issue Title | Analysis Class |
|----------|---------------|----------------|
| R1-1     | Inefficient API Usage | [CallGraph](https://github.com/sola-st/DynaPyt/blob/main/src/dynapyt/analyses/CallGraph.py) |
| R1-2     | Excessive Recursion | [RecursionAnalysis](../code/my_analysis/RecursionAnalysis.py) |
| R2-1     | String Concatenation in Loops | [SlowStringConcatAnalysis](../code/my_analysis/SlowStringConcatAnalysis.py) |
| R2-2     | Nested Looping | [NestedLoopingAnalysis](../code/my_analysis/NestedLoopingAnalysis.py) |
| R2-3     | Object Creation in Loops | [ObjectCreationInLoopAnalysis](../code/my_analysis/ObjectCreationInLoopAnalysis.py) |
| R4-2     | Unused Variables | [UnusedVarAnalysis](../code/my_analysis/UnusedVarAnalysis.py) |

Each analysis module targets specific inefficiencies, helping developers optimize their Python applications efficiently.
