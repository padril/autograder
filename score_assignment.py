import sys
import shutil
import os
import subprocess

filename = sys.argv[1]
subprocess.run(['jupyter','nbconvert','--TagRemovePreprocessor.enabled=True','--TagRemovePreprocessor.remove_cell_tags','remove','--log-level','ERROR','--to','python',filename]) 
conv_filename = filename[:-6] + '.py'
modelname = 'model_' + conv_filename
shutil.copy(modelname, 'MODEL.py')
shutil.copy(conv_filename, 'ASSIGNMENT.py')

print('_________________________________________________________________________________')
print('Results:\n')

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

print(f"You got {correct_num} exercise(s) correct out of {total} total exercises.")
print(f"Your score is: {correct_num * 100 / total:.0f}%")
print(MODEL.threshold(correct_num / total))

os.remove('MODEL.py')
