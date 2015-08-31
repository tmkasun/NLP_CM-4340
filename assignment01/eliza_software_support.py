__author__ = 'tmkasun'
import re
from random import randint

solutions = [

    ["Hello (.*)",
     ["Hello %1 I'm willing to help you.",
      "Hi %1... how are you today?",
      "Hello %1, how are you feeling today?"]],

    ["I can't run (.*)",
     ["How do you know you can't %1 ?",
      "Perhaps you could %1 if you tried.",
      "Did you try running %1 in safe-mode"]],

    ["My (.*) operating system went (.*) when I try to (.*)",
     ["Is %1 booting properly?",
      "When your %1 last time went %2 ?",
      "Is your %1 support to do %3 without %2 the system."]],

    ["My (.*) server not (.*)",
     ["Did you retry %1 server before %2 it for second time",
      "Have you properly installed your %1",
      "Can you re-try %2 again after restarting your computer"
      ]],

    ["I want to install (.*)",
     ["First, you have to download %1.",
      "Do you have %1 file with you?",
      "Have you tried to install %1 before?",
      "Why you need to install %1?"]],

    ["quit",
     ["Thank you for talking with me.",
      "Good-bye.",
      "Thank you, Have a good day!"]],
]

patterns = map(lambda x: re.compile(x[0], re.IGNORECASE), solutions)
answers = map(lambda x: x[1], solutions)


def make_answer(matched_pattern, answer_template):
    matched_groups = matched_pattern.groups()
    match_count = len(matched_groups)
    answer = answer_template
    for match in range(match_count):
        replace_number = '%{}'.format(match + 1)
        answer = answer.replace(replace_number, matched_groups[match])
    return answer


def respond(input_string):
    for pattern_index in range(len(patterns)):
        pattern = patterns[pattern_index]
        pattern_matched = pattern.match(input_string)
        if pattern_matched:
            answers_for_pattern = answers[pattern_index]
            random_answer_index = randint(0, len(answers_for_pattern) - 1)
            answer_template = answers_for_pattern[random_answer_index]
            return_answer = make_answer(pattern_matched, answer_template)
            break
        else:
            return_answer = "Sorry I didn't understand what you said."
    return return_answer


print 'Welcome to Software system help Agent.'
print 'Enter "quit" when you want to exit.'
print '=' * 72
print "Hello. How are you feeling today?"
user_input = ""
while user_input != "quit":
    try:
        user_input = raw_input(">")
    except EOFError:
        user_input = "quit"
        print user_input
    print respond(user_input)