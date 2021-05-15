import argparse
import sys

TAPE_LENGTH = 10000
false = False
true = True
allowed_chars = ['>', '<', '+', '-', '[', ']', ',', '.', ':']


class Interpreter:

    def __init__(self, program):
        self.dp = 0
        self.ip = 0
        self.data = [0]*TAPE_LENGTH
        self.halt = false
        self.loop = {}
        self.program = program
        self.commands = {
            '>': self.move_right,
            '<': self.move_left,
            '.': self.print_no_newline,
            ',': self.read_input,
            '+': self.increment,
            '-': self.decrement,
            '[': self.start_loop,
            ']': self.end_loop,
            ':': self.print_newline
        }

    def move_right(self):
        self.dp += 1
        self.ip += 1

    def move_left(self):
        self.dp -= 1
        self.ip += 1

    def increment(self):
        self.data[self.dp] += 1
        self.ip += 1

    def decrement(self):
        self.data[self.dp] -= 1
        self.ip += 1

    def read_input(self):
        self.data[self.dp] = int(input())
        self.ip += 1

    def print_no_newline(self):
        print(chr(self.data[self.dp]), end='')
        self.ip += 1
    
    def print_newline(self):
        print(chr(self.data[self.dp]))
        self.ip += 1

    def find_end_loop(self, start):
        count = 1
        while count > 0:
            start += 1
            if start >= len(self.program):
                raise 'Unexpected end of program: missing end of loop "]"'
            if self.program[start] == '[':
                count +=1
            if self.program[start] == ']':
                count -= 1
            
        return start

    def start_loop(self):
        if self.data[self.dp] != 0:
            self.ip += 1
        else:
            self.ip = self.loop[self.ip]
            self.ip += 1

    def end_loop(self):
        if self.data[self.dp] == 0:
            self.ip += 1
        else:
            self.ip = self.loop[self.ip]


    def precompile_loops(self):
        for index in range(len(self.program)):
            if self.program[index]=='[':
                end = self.find_end_loop(index)
                self.loop[index] = end
                self.loop[end] = index



    def execute(self):
        self.precompile_loops()
        while not self.halt: 
            command = self.program[self.ip]
            self.commands[command]()
            if (self.ip >= len(self.program)):
                 self.halt = true


def main():
    parser = argparse.ArgumentParser(description='Brainfuck interpreter')
    parser.add_argument('-i', '--input-file', type=argparse.FileType('r'), default=None if sys.stdin.isatty() else sys.stdin)
    input = parser.parse_args().input_file



    program = list(filter(lambda ch: ch in allowed_chars,
                   ''.join(input.readlines())))
    Interpreter(program).execute()


if __name__ == '__main__':
    main()
