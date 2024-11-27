from flask import current_app as app

# Code snippet for logging a message
# app.logger.critical("message")

def sanitize(input: str) -> str:
    to_replace = ["<", ">", ";"]
    replacements = ["%3C", "%3E", "%3B"]
    char_list = list(input)
    for i in range(len(char_list)):
        if char_list[i] in to_replace:
            index = to_replace.index(char_list[i])
            char_list[i] = replacements[index]
    input = "".join(char_list)
    return input

def validate(input: str) -> bool:
    sum_num = 0
    sum_alpha = 0
    for i in input:
        if i.isnumeric():
            sum_num += 1
        elif i.isalpha():
            sum_alpha += 1
        else:
            return False
    if len(input) < 8 or len(input) > 12:
        return False
    elif sum_alpha < 4:
        return False
    elif sum_num < 3:
        return False
    return True