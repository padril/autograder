import sys
import shutil
import os
import subprocess

filename = sys.argv[1]
subprocess.run(['jupyter','nbconvert','--TagRemovePreprocessor.enabled=True','--TagRemovePreprocessor.remove_cell_tags','remove','--to','python',filename]) 
conv_filename = filename[:-6] + '.py'
modelname = 'model_' + filename[:-6] + '.py'
shutil.copy(modelname, 'MODEL.py')
shutil.copy(conv_filename, 'ASSIGNMENT.py')

import ASSIGNMENT
import MODEL

for student_func_name, student_func in ASSIGNMENT.__dict__.items():
    model_func_name = 'model_' + student_func_name
    try: 
        model_func = MODEL.__dict__[model_func_name]
    except: continue
    a = model_func(student_func)
    print('exercise %s: %s' % (student_func_name.upper(), a))

os.remove('MODEL.py')
