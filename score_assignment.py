import sys
import shutil
import os
import subprocess
import re
import io
import contextlib
import python_ta
import tempfile
import logging

logging.basicConfig(level='CRITICAL')

filename = sys.argv[1]
subprocess.run(['jupyter','nbconvert','--TagRemovePreprocessor.enabled=True','--TagRemovePreprocessor.remove_cell_tags','remove','--log-level','ERROR','--to','python',filename]) 
conv_filename = filename[:-6] + '.py'
modelname = 'model_' + conv_filename
shutil.copy(modelname, 'MODEL.py')
shutil.copy(conv_filename, 'ASSIGNMENT.py')

with open("ASSIGNMENT.py") as file:
    code_blocks = list(filter(None, re.split(r'# In\[[ \d]+\]:\n', file.read())))[1:]

working_blocks = []
failed_blocks = []
pyta_messages = []

for block in code_blocks:
    merged = ''.join(working_blocks) + block
    temp = tempfile.NamedTemporaryFile()

    with open(temp.name, 'w') as f:
        f.write(merged)

    with contextlib.redirect_stdout(io.StringIO()) as g:
        python_ta.check_errors(temp.name, config={"output-format": "pyta-plain", "disable": "E9992, E9999, W0104"})
        message = g.getvalue().split('\n')
        if message == ['']:
            failed_blocks.append(block)
            pyta_messages.append("err")
        elif message[3] == "No problems detected, good job!":
            working_blocks.append(block)
        else:
            failed_blocks.append(block)
            pyta_messages.append(message[4])

with open("ASSIGNMENT.py", 'w') as file:
    file.write(''.join(working_blocks))

if any(pyta_messages):
    print("Your code has an error in the following location(s):")

cleaned_pyta_messages = [re.sub(r'Parsing failed:', '', 
                         re.sub(r'[\[\(][^(]*?[Ll]ine.*?[\d]+.*?[\)\]]', '', message)).strip()
                         for message in pyta_messages]

for x, y in zip(cleaned_pyta_messages, failed_blocks):
    if x != "err":
        print(x)
        print(y)
        print("________________________________________________")
    else: # if tokenize fails at parsing
        try:
            with contextlib.redirect_stdout(open('/dev/null', 'w')) as g:
                exec(y)
        except SyntaxError as e:
            print(re.sub(r'[\[\(][^(]*?[Ll]ine.*?[\d]+.*?[\)\]]', '', str(e)).strip())
            print(y)
        print("________________________________________________")

print('Results:\n')

with contextlib.redirect_stdout(open('/dev/null', 'w')) as g:
    import ASSIGNMENT
import MODEL

total = 0
correct_num = 0

for student_func_name, student_func in ASSIGNMENT.__dict__.items():
    model_func_name = 'model_' + student_func_name
    try: 
        model_func = MODEL.__dict__[model_func_name]
    except: continue
    a = model_func(student_func)
    if a == "correct.":
        correct_num = correct_num + 1
    total = total + 1
    print(f"exercise {student_func_name.upper()}:\n{a}\n")
if total != 0:
    print(f"You got {correct_num} exercise(s) correct out of {total} total exercises.")
    print(f"Your score is: {correct_num * 100 / total:.0f}%")
    print(MODEL.threshold(correct_num / total))

os.remove('MODEL.py')
