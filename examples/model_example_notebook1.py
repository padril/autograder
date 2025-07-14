from autograder.model_problem import ModelProblem
import re
from pathlib import Path

def threshold(score: float):
    cutoff = 0.9
    if score >= cutoff:
        return "You passed! The password is: password"
    else:
        return f"Try again. You need to get at least {cutoff * 100:.0f}% of the questions correct to get the password."

# model notebook needs:
# solution functions
# prep functions (which create lists of arguments for the solution + student functions)
# model functions (which instantiate the ModelProblem class and run the tests)

# solutions
# same format as student functions, but return the correct answer
def sentence_segment(text, eos_punctuation, abbreviations):
    sentences = []
    start_sent = 0
    for end_sent in range(len(text)):
        last_space = next((i+1 for i in range(end_sent-1,-1,-1) if text[i] == ' '),0)
        next_space = next((i for i in range(end_sent, len(text),1) if text[i] == ' '),len(text))
        third_space = next((i for i in range(next_space+1,len(text),1) if text[i] == ' '),len(text))
        token = text[last_space:next_space]
        next_token = text[next_space+1:third_space]
        is_boundary = True if text[end_sent] in eos_punctuation and (not (token in abbreviations and next_token.lower()[:1] == next_token[:1]) and end_sent + 1 == next_space) or end_sent + 1 == len(text) else False
        if is_boundary:
            sentences.append(re.sub(r'[\n\s]+', ' ', text[start_sent: end_sent+1]))
            start_sent = end_sent+2
    return sentences

def punctuation_stripping(sentence, punct):
    word_tokenized = sentence.split(' ')
    clean_word_tokenized = []
    for word in word_tokenized:
        pre = []
        post = []
        while len(word) > 0 and word[0] in punct:
            initial_char = word[0]
            word = word[1:]
            pre.append(initial_char)
        while len(word) > 0 and word[-1] in punct:
            final_char = word[-1]
            word = word[:-1]
            post = [final_char] + post
        new_segment = pre + [word] + post
        clean_word_tokenized.extend(new_segment)
    return clean_word_tokenized

def clitic_compound_splitting(tokenized_sentence, characters):
    new_tokenized_sentence = []
    for word in tokenized_sentence:
        new_tokenized_sentence.extend(re.split('[' + characters + ']', word))
    return new_tokenized_sentence

def longest_match_tokenize(sentence, all_words):
    words = []
    start = 0
    for i in range(len(sentence)):
        if sentence[start:i+1] not in all_words:
            words.append(sentence[start:i])
            start = i
    words.append(sentence[-1])
    return words

# prep
# return format is list of tuples with the first element being the list of args (can be partial)
# and the second element being the visibility of the tests connected to that list of args
# (if the list of args in the prep fuunction is only partial, the remaining arguments need to be specified
# in extra_sfunc_args and extra_model_args when initializing the ModelProblem class)

def model_sentence_segment_prep():
    eos = '.?!'
    abbreviations = ['U.S.', 'pm.']
    s1 = 'He came over at 4 pm. Then he watched the game, at 5 pm. between Canada and the U.S. Finally, he ordered take-out.'
    s2 = "The quick brown fox jumped over the lazy dog. The quick brown fox went to the U.S. at 3 pm."
    args_list = [([s1, eos, abbreviations], True), ([s2, eos, abbreviations], False)]
    return args_list

def model_cleaner_tokenized_check_prep():
    eos = '.?!'
    abbreviations = ['U.S.', 'pm.']
    punct = '.?!,[]()"\';:'
    args_list = []

    fh = open("/home/michael/faetar/autograder/examples/lowry.txt")
    for l in fh.readlines():
        sentences = sentence_segment(l, eos, abbreviations)
        for sentence in sentences:
            args_list.append(([punctuation_stripping(sentence, punct)], True))
    return args_list

def model_longest_match_tokenize_prep():
    txt = open("/home/michael/faetar/autograder/examples/lowry_zh.txt").read()
    all_words = open("examples/words_zh.txt").read().split('\n')
    sentences = [x + '。' for x in txt.split('。') if x]
    args_list = []
    visible = True
    for sentence in sentences:
        args_list.append(([sentence, (all_words)], visible))
        # only the first sentence is visibly tested
        if visible:
            visible = False
    return args_list

# tests
def model_sentence_segment(student_func):
    model = ModelProblem(model_sentence_segment_prep, sentence_segment, student_func)

    return model.run_basic_tests(err_num=False,
                                 len_err_message="incorrect. Your function split test string 1 into {sfunc_len} sentence(s) instead of {model_len} sentences.\n",
                                 hidden_len_err_message="incorrect. Your function split test string 2 into the wrong number of sentences.\n",
                                 hidden_elems_err_message="incorrect. Your function did not split the sentences in test string 2 correctly.\n")


def model_cleaner_tokenized_check(student_var):
    clitic_compound = "-–'"
    model = ModelProblem(model_cleaner_tokenized_check_prep,
                        clitic_compound_splitting,
                        student_var,
                        extra_sfunc_args=[student_var()],
                        extra_model_args=[clitic_compound])

    return model.run_basic_tests(list_len=False,
                                 list_elems=False,
                                 one_err_message="incorrect. There is still 1 sentence with incorrect tokenization.\n",
                                 multi_err_message="incorrect. There are still {err_num} sentences with incorrect tokenization.\n")

def model_longest_match_tokenize(student_func):
    model = ModelProblem(model_longest_match_tokenize_prep, longest_match_tokenize, student_func)
    return model.run_basic_tests(err_num=True,
                                 hidden=True,
                                 list_len=False,
                                 list_elems=True,
                                 hidden_elems_err_message="incorrect. The hidden sentences were not tokenized correctly.\n",
                                 one_err_message="incorrect. There is still 1 sentence with incorrect tokenization.\n",
                                 multi_err_message="incorrect. There are still {err_num} sentences with incorrect tokenization.\n")