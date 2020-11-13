from pptree import *
import os
import sys
import io


def get_first_word(line):
    if line == "":
        return
    words = line.split()
    if len(words) > 0:
        first_word = words[0]
        return first_word

def add_node(current, line):
    if current is None:
        return Node("head" + line, None)
    else:
        return Node(line, current)


with open(r"trace.txt", 'r') as trace_file:
    current = None
    call_tree = None

    while True:
        line = trace_file.readline()
        if line.strip() == "":  # run till it face an empty string.
            break
        first_word = get_first_word(line)

        if line[0] != " " and line[0] != "\t":
            continue
        elif current is None:
            call_tree = add_node(current, line)
            current = call_tree
        elif first_word == "Call:":
            current = add_node(current, line)
        elif first_word == "Exit:":
            add_node(current, line)  # get_assignment(line))
            current = current.parent
        elif first_word == "Fail:":
            add_node(current, line)
            current = current.parent
        elif first_word == "Redo:":
            current = add_node(current, line)
        elif first_word == "Unify:":
            current = add_node(current, line)

original_stdout = sys.stdout

with io.open("tmp.txt", "w", encoding="utf-8") as f:
    sys.stdout = f
    print_tree(call_tree)
    sys.stdout = original_stdout


with io.open("tmp.txt", "r", encoding="utf-8") as tmp:
    lines = tmp.readlines()
    with io.open("out.txt", "w", encoding="utf-8") as f:
        sys.stdout = f

        n = len(lines)
        i = 0
        while i < n:
            if i < n-1 and lines[i+1][0] != '\n':
                last_char = lines[i+1][0]
            else:
                last_char = " "
            m = len(lines[i])-1
            print(lines[i][0:m]+" "+last_char)
            i += 2

        sys.stdout = original_stdout
                
os.remove("tmp.txt")
