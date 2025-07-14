from itertools import cycle

class ModelProblem:
    def __init__(self, model_func_prep, solution_func, student_func, extra_sfunc_args = [], extra_model_args = [], is_var = False):
        self.model_func_prep = model_func_prep
        self.solution_func = solution_func
        self.student_func = student_func
        self.sfunc_vals = []
        self.model_vals = []
        self.hidden_sfunc_vals = []
        self.hidden_model_vals = []
        # extra args are used for problems where the student returns a value instead of a function
        self.extra_sfunc_args = extra_sfunc_args
        self.extra_model_args = extra_model_args

        if is_var:
            self.solution_func = lambda: self.solution_func
            self.student_func = lambda: self.student_func

        self.get_vals()

    # student provided arguments must be placed at the end (can be in any order)
    # check if kwargs can be used
    # gets the value of the solution function given the arguments given by the prep function and the extra student args + extra model args
    # or gets the value of the student function + solution function on the arguments given by the prep function
    def get_vals(self):
        # uses the solution function for sfunc_vals if the student needs to provide a value
        if self.extra_model_args or self.extra_sfunc_args:
            for args, visible in self.model_func_prep():
                if visible:
                    self.sfunc_vals.append(self.solution_func(*args, *self.extra_sfunc_args))
                    self.model_vals.append(self.solution_func(*args, *self.extra_model_args))
                else:
                    self.hidden_sfunc_vals.append(self.solution_func(*args, *self.extra_sfunc_args))
                    self.hidden_model_vals.append(self.solution_func(*args, *self.extra_model_args))
        # uses the student's function for sfunc_vals if the student needs to provide a function
        else:
            for args, visible in self.model_func_prep():
                if visible:
                    self.sfunc_vals.append(self.student_func(*args, *self.extra_sfunc_args))
                    self.model_vals.append(self.solution_func(*args, *self.extra_model_args))
                else:
                    self.hidden_sfunc_vals.append(self.student_func(*args, *self.extra_sfunc_args))
                    self.hidden_model_vals.append(self.solution_func(*args, *self.extra_model_args))
    
    # check if student function returned any values
    def check_sfunc_returns(self):
        if not self.sfunc_vals and not self.hidden_sfunc_vals:
            return "incorrect. Your function did not return any values.\n"
     
    # checks for any inequalities between student values and solution values
    def check_err_num(self, one_err_message = None, multi_err_message = None):
        if one_err_message is None:
            one_err_message = "incorrect. There was 1 error.\n"
        if multi_err_message is None:
            multi_err_message = "incorrect. There were {err_num} errors.\n"
        err_num = [x != y for x, y in zip(cycle(self.sfunc_vals), self.model_vals)].count(True) + [x != y for x, y in zip(cycle(self.hidden_sfunc_vals), self.hidden_model_vals)].count(True)
        multi_err_message = multi_err_message.format(err_num=err_num)
        if err_num != 0:
            if err_num == 1:
                return one_err_message
            else:
                return multi_err_message
     
    def check_list_len(self, sfunc_list, model_list, err_message = None):
        if err_message is None:
            err_message = "incorrect. The lengths of the lists are not equal.\n"
        err_message = err_message.format(sfunc_len=len(sfunc_list), model_len=len(model_list))
        if len(sfunc_list) != len(model_list):
            return err_message
    
    # assumes list lengths are the same
    def check_list_elems(self, sfunc_list, model_list, err_message = None):
        comp_list = [x != y for x, y in zip(sfunc_list, model_list)]
        unequal_index = comp_list.index(True) if True in comp_list else None
        if unequal_index is not None:
            if err_message is None:
                err_message = f"incorrect. Your function returned \"{sfunc_list[unequal_index]}\" instead of \"{model_list[unequal_index]}\".\n"
            # add error message customization later
            # err_message = err_message.format(sfunc_len=len(sfunc_list), model_len=len(model_list))
            return err_message

    # make this more efficient
    # basic tests are:
    # checking to see if the student returned any values
    # checking for equality
    # checking list lengths
    # and checking lists elementwise
    # these run with optionally different error messages for visible and hidden tests
    def run_basic_tests(self, err_num=True, hidden=True, list_len=True, list_elems=True, **kwargs):
        if not self.hidden_model_vals:
            hidden = False
        for val in self.model_vals:
            if type(val) is not list:
                list_len = False
                list_elems = False
            break

        err_messages = ""
        one_err_message = kwargs.get('one_err_message')
        multi_err_message = kwargs.get('multi_err_message')
        len_err_message = kwargs.get('len_err_message')
        elems_err_message = kwargs.get('elems_err_message')
        hidden_len_err_message = kwargs.get('hidden_len_err_message')
        hidden_elems_err_message = kwargs.get('hidden_elems_err_message')

        # TEST
        # self.sfunc_vals = [["the quick."], ["brown fox."]]
        # self.hidden_sfunc_vals = [["the quick."], ["brown fox."]]

        self.check_sfunc_returns()
        if err_num:
            err_messages += value if (value := self.check_err_num(one_err_message=one_err_message, multi_err_message=multi_err_message)) is not None else ""
        for sfunc_elem, model_elem in zip(self.sfunc_vals, self.model_vals):
            if list_len:
                err_messages += value if (value := self.check_list_len(sfunc_elem, model_elem, err_message=len_err_message)) is not None else ""
            if list_elems:
                err_messages += value if (value := self.check_list_elems(sfunc_elem, model_elem, err_message=elems_err_message)) is not None else ""
        if hidden:
            for sfunc_elem, model_elem in zip(self.hidden_sfunc_vals, self.hidden_model_vals):
                if list_len:
                    err_messages += value if (value := self.check_list_len(sfunc_elem, model_elem, err_message=hidden_len_err_message)) is not None else ""
                if list_elems:
                    err_messages += value if (value := self.check_list_elems(sfunc_elem, model_elem, err_message=hidden_elems_err_message)) is not None else ""
                    break

        if not err_messages:
            return "correct."
        else:
            return err_messages.strip()
