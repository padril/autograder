from setuptools import setup

setup(
    name='autograder',
    version='0.1.0',    
    description='For use in automatically grading and providing feedback for problems in Jupyter notebooks.',
    url='https://github.com/michaelong7/autograder',
    packages=['autograder'],
    entry_points={
        'console_scripts': ['score=autograder.score_assignment:main'],
    },
    install_requires=['nbconvert',
                      'python-ta @ git+https://github.com/pyta-uoft/pyta.git',
                      ],
)
