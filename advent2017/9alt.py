f = open("9.in","r")
s=f.read()
f.close()

def answer(stream, day2):
    score = 0
    should_ignore = False
    open_braces = 0
    open_angle = False
    garbage_count = 0
    for char in stream:
        if open_angle:
            if should_ignore:
                should_ignore = False
            elif char == '!':
                should_ignore = True
            elif char == '>':
                open_angle = False
            else:
                garbage_count += 1
        else:
            #if should_ignore: #added
            #    should_ignore = False
            #elif char == "!": # added
            #    should_ignore = True
            if char == '{':
                open_braces += 1
                score += open_braces
            elif char == '}':
                open_braces -= 1
            elif char == '<':
                open_angle = True
    return garbage_count if day2 else score


print answer(s, 0) 

