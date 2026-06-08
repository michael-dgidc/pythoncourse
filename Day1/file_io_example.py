#!/usr/bin/env python3
def write_text(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

def append_lines(path, lines):
    with open(path, 'a', encoding='utf-8') as f:
        for line in lines:
            f.write(line if line.endswith('\n') else line + '\n')

def read_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    path = 'sample.txt'
    text = "Line one\nLine two\nLine three\n"
    write_text(path, text)
    append_lines(path, ['Appended line 1', 'Appended line 2\n'])
    print('File content:')
    print(read_text(path))

if __name__ == '__main__':
    main()
