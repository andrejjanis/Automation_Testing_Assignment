# Automation Testing Assignment

Rudimentary Pytest framework implementation for the purposes of functional testing of CeitSolver sample app's output file in JSON format.

## Description

This is a very basic implementation of a testing framework based on Pytest library. For example, logging is using the built-in logging library with just a basic configuration in the 'pyproject.toml' file. In a robust testing framework, there would be a complete custom logger with custom log levels, formatting, command line options, etc. There is not even an implementation for specifying a path to input and output data files using CLI.

The implementation of the classes for input and output JSON data manipulation can also be further improved for efficiency and further functionality like delivery and order comparison, etc.. The validity or structure of the JSON files is assumed to be correct.

The test cases are created to check for any functionality that can be expected or implied for the output JSON file. Aspects of the tested data that are a concern of optimizing the transport orders for better performance are considered out of scope for these tests.

One big thing that will be obvious from the test cases is the lack of optimization for the performance of the test case execution. Test cases loop through the data even multiple times in some cases. Some of the basic and nested loops can be reused for multiple test cases. Either by separating them into individual functions, using some advanced design methods, or ideally after some serious redesign utilizing parallel execution looping through the potentially enormous output file just once and calculating what is necessary using only fixtures called by test cases that are selected for execution.

Something that will perhaps be of consideration when a proper version of Python where GIL can be disabled is available (version 3.14 perhaps).

Since that would take a considerable time and effort, these optimizations can be delivered if requested. Current implementation at least conserves the independency of each test case and clearly demonstrates the algorithm of each one.  

As stated in the beginning, this framework can use a lot more features and optimization. If necessary, anything can be added or changed after a consultation of what else is expected for the purpose of this framework to be considered satifactory.

## Getting Started

### Dependencies

* Python version 3.10

### Installing

* Install required packages
```
pip install -r requirements.txt
```

### Executing test cases

* To execute test cases, valid 'in.json' and 'out.json' files have to be present in framework root directory. If 'out.json' is not present in this directory or a new input file is to be tested, make sure the desired and valid 'in.json' file is placed in the framework root directory and run CeitSolver.exe. New 'out.json' file should be created.
* Execute all test cases:
```
pytest .
```
* Execute all test cases in a module:
```
pytest .\test_cases\functional\test_agv.py
```
* Execute all test cases in a test class:
```
pytest .\test_cases\functional\test_agv.py::TestAgv
```
* Execute a single test case:
```
pytest .\test_cases\functional\test_agv.py::TestAgv::test_minimal_agv_count
```


## Author

Andrej Janis

## Version History

* 0.1
    * Initial Release
