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

for fn_a, fx_a in ASSIGNMENT.__dict__.items():
    fn_m = 'model_' + fn_a
    try: 
        fx_m = MODEL.__dict__[fn_m]
    except: continue
    a = fx_m(fx_a)
    print('exercise %s: %s' % (fn_a.upper(), a))

os.remove('MODEL.py')
