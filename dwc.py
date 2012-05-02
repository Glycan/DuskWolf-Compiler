#!/usr/bin/python3.2
import string
import sys
import shlex
import pdb
import json


class Compiler:
    """
    Compiles DW code into JSON. Use .compile() followed by .write() if using
    auto=False.
    """
    cmd_trans = {
        "on": "listen",
        "echo": "print"
    }
    cmds = {
        "listen": ["event"],
        "comment": ["text"],
        "var": ["name", "value"],
        "print": ["text"]
    }

    def __init__(self, name, auto=True):
        self.source = open(name).read()
        self.name = name
        if auto:
            self.compile()
            self.write()

    def compile(self):
        self.output = []
        block_stack = [self.output]
        #The stack. A new block is appended at a container, and a block is
        #poped at dedents. Normal lines are appended to the last block.
        indent = 0
        for lineno, line in enumerate(self.source.split("\n")):
            if not set(line).issubset(string.whitespace):
                #if it's not blank
                new_indent = self.check_indent(line)
                if new_indent == (indent - 1):
                    #dedent
                    block_stack.pop()
                indent = new_indent
                if line.endswith(":"):
                    #if it's a container
                    line = line[:-1]
                    #strip trailling :
                    container = self.compile_line(lineno, line)
                    block_stack[-1].append(container)
                    container["actions"] = []
                    block_stack.append(container["actions"])
                else:
                    block_stack[-1].append(self.compile_line(lineno, line))

    def compile_line(self, lineno, line):
        line = shlex.split(line)
        cmd, *args = line
        if cmd in self.cmd_trans:
            cmd = self.cmd_trans[cmd]
            #this handles neater aliases
        return self.compile_action(cmd, args)

    def check_indent(self, line):
        new_indent_level = 0
        for char in line:
            if char is " ":
                indent += 0.25
        if int(new_indent_level) != new_indent_level:
            #if it's not a whole number
            raise Exception("Bad indent in source at line " + str(lineno))
        return new_indent_level

    def compile_action(self, cmd, args):
        if cmd in self.cmds:
            argnames = self.cmds[cmd]
            action = dict(zip(argnames, args))
            action["a"] = cmd
        else:
            raise Exception("No such command")
        return action

    def write(self):
        compiled_name = self.name.split(".")[0] + ".json"
        json.dump(self.output, open(compiled_name, "w"), indent=4)

if len(sys.argv) > 1:
    Compiler(sys.argv[1])
else:
    Compiler("hello.dw")
