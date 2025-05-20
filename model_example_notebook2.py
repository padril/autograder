from model_problem import ModelProblem

def threshold(score: float):
    cutoff = 1
    if score >= cutoff:
        return "You passed! The password is: password"
    else:
        return f"Try again. You need to get all of the questions correct to get the password."

def evil_laugh(var1, var2, n):
    evil_laughter = var1 + var2 * n
    return evil_laughter

def get_volume(radius):
    pi = 3.1415926535897932
    volume = (4/3) * pi * radius**3 # FILL THIS IN
    return volume

def model_evil_laugh_prep():
    args_list = ([(("mu", "ha", n), True) for n in range(1,20)] +
                 [(("ha", "mu", n), True) for n in range(1,20)])
    return args_list

def model_get_volume_prep():
    args_list = [([i], True) for i in range(1,50)]
    return args_list

def model_evil_laugh(student_func):
    model = ModelProblem(model_evil_laugh_prep, evil_laugh, student_func)
    if (value := model.run_basic_tests()) == "correct.":
        return value
    else:
        diff = [x == y for x,y in zip(model.sfunc_vals, model.model_vals)].index(False)
        diff_var1, diff_var2, diff_n = model_evil_laugh_prep()[diff][0]
        return (f"Check your code again. When var1 = {diff_var1}, " +
                f"var2 = {diff_var2}, and n = {diff_n}, " +
                f"you printed:\n{model.sfunc_vals[diff]}\ninstead of:\n{model.model_vals[diff]}")
    
def model_get_volume(student_func):
    model = ModelProblem(model_get_volume_prep, get_volume, student_func)
    if (value := model.run_basic_tests()) == "correct.":
        return value
    else:
        diff = [x == y for x,y in zip(model.sfunc_vals, model.model_vals)].index(False)
        diff_radius = model_get_volume_prep()[diff][0][0]
        return (f"Check your code again. When radius = {diff_radius}, " +
                f"you printed:\n{model.sfunc_vals[diff]}\ninstead of:\n{model.model_vals[diff]}")
    
def model_e2_q1(student_val):
    if student_val() == (42 * 60 + 42):
        return "correct."
    else:
        return "incorrect."
    
def model_e2_q2(student_val):
    if student_val() == (10 / 1.61):
        return "correct."
    else:
        return "incorrect."
    
def model_e2_q3a(student_val):
    if student_val()[0] == ((42 * 60 + 42) / (10 / 1.61) // 60):
        if student_val()[1] == ((42 * 60 + 42) / (10 / 1.61) % 60):
            return "correct."
        else:
            return "The number of minutes is correct, but the number of seconds is incorrect."
    elif student_val()[0] == (42 * 60 + 42 / 10 / 1.61 // 60) or student_val()[0] == ((42 * 60 + 42 / 10 / 1.61) // 60):
        return "The number of minutes is incorrect. Remember to use parentheses when necessary."
    else:
        return "The number of minutes is incorrect."
    
def model_e2_q3b(student_val):
    if student_val() == (10 / 1.61) / ((42 * 60 + 42) / 3600):
        return "correct."
    elif student_val() == (10 / 1.61) / ((42.42) / 60):
        return "incorrect. Remember that 42 seconds are not 0.42 minutes."
    else:
        return "incorrect."