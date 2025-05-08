# Autograder

For use in automatically grading and providing feedback for problems in Jupyter notebooks.

## Scoring

To score a student notebook, create a model notebook (see below for format + naming), then use the scoring script:

```python score_assignment.py [student-notebook.ipynb]```

(When calling this script, provide the local path to the student notebook.)

## Student Notebooks

All cells in student notebooks that are not necessary for problems should be marked with the tag "remove".

## Model Notebooks

Model notebooks should have the name of the corresponding student notebook prefixed with "model_".

Model notebooks consist of 4 sections:

Threshold function:
- takes in the percentage of correct questions as a float and returns the password if the score is above the threshold

Solution functions:
- same format as the code given in the student notebooks, but with the solution code filled in

Prep functions:
- creates lists of arguments for the solution function + corresponding student function
- return format is list of 2 element tuples 
- the first element of each tuple is the list of args provided to the solution / student functions (can be partial)
- the second element of each tuple is the visibility of the tests connected to that list of args
(if the list of args in the prep fuunction is only partial, the remaining arguments need to be specified in extra_sfunc_args and extra_model_args when initializing the ModelProblem class)


Model functions (one per problem in the student notebook):
- model functions should have the name of the corresponding student function prefixed with "model_"
- inside the model function, instantiate the ModelProblem class and run the tests

```
model = ModelProblem(prep_func, soln_func, stud_func, [extra_sfunc_args], [extra_model_args])
return model.run_basic_tests(err_num=True,
                                 hidden=True,
                                 list_len=True,
                                 list_elems=True)
```

- different error messages can be created by setting [one_err_message, multi_err_message, len_err_message, elems_err_message, hidden_len_err_message, hidden_elems_err_message] in run_basic_tests
- err messages can use f-strings (for custom f strings, change the .format() in the ModelProblem check functions)
- if the student needs to return a value, put the return value of the function in a list and pass it to extra_sfunc_args (and use extra_model_args).
