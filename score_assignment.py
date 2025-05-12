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
    code_blocks = list(filter(None, re.split(r'#.+\n', file.read())))

pyta_messages = []

for block in code_blocks:
    temp = tempfile.NamedTemporaryFile()

    with open(temp.name, 'w') as f:
        f.write(block)
    
    # print(block)
    with contextlib.redirect_stdout(io.StringIO()) as g:
        python_ta.check_errors(temp.name, config={"output-format": "pyta-plain", "disable": "E9992, W0104"})
        pyta_messages.append(g.getvalue().split('\n'))
    # try:
    #     with contextlib.redirect_stdout(open('/dev/null', 'w')) as g:
    #         exec(block)
    #     clean_blocks.append(block)
    # except (SyntaxError, TypeError, NameError) as e:
    #     # print(block.strip())
    #     # print(e)
    #     # print("________________________________________________")
    #     continue

for idmessage, message in enumerate(pyta_messages):
    if message == ['']:
        pyta_messages[idmessage] = ["err"]
    elif message[3] == "No problems detected, good job!":
        pyta_messages[idmessage] = []
    else:
        pyta_messages[idmessage] = message[4]

clean_blocks = []

if any(pyta_messages):
    print("Your code has an error in the following location(s):")

for x, y in zip(pyta_messages, code_blocks):
    if not x:
        clean_blocks.append(y)
    elif x != ["err"]:
        print(x)
        print(y)
        print("________________________________________________")
    else:
        try:
            with contextlib.redirect_stdout(open('/dev/null', 'w')) as g:
                exec(y)
        except SyntaxError as e:
            print(e)
            print(y)
        print("________________________________________________")

with open("ASSIGNMENT.py", 'w') as file:
    for block in clean_blocks:
        file.write(block)

print('_________________________________________________________________________________')
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
