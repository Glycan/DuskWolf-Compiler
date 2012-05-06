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
    from langdef import cmd_trans, cmds
    params = {"encoding": "dict", "parens": True}
    def __init__(self, name, auto=True, **params):
        self.params.update(params)
        self.encoding=self.params["encoding"]
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
                    actions = []
                    try:
                        container["actions"] = actions
                    except TypeError:
                        container.append(actions)
                    block_stack.append(actions)
                else:
                    block_stack[-1].append(self.compile_line(lineno, line))

    def compile_line(self, lineno, line):
        line = shlex.split(line)
        cmd, *args = line
        if cmd in self.cmd_trans:
            cmd = self.cmd_trans[cmd]
            #this handles neater aliases
        if cmd in self.cmds:
            argnames = self.cmds[cmd]
            action = self.encodings[self.encoding](cmd, args, argnames)
            return action
        else:
            raise Exception("No such cmd")

    def check_indent(self, line):
        new_indent_level = 0
        for char in line:
            if char is " ":
                indent += 0.25
        if int(new_indent_level) != new_indent_level:
            #if it's not a whole number
            raise Exception("Bad indent in source at line " + str(lineno))
        return new_indent_level

    def write(self, f=None, pretty=True):
        if not f:
            name = self.name.split(".")[0] + ".json"
            f = open(name, "w")
        if pretty:
            json.dump(self.output, f, indent=4)
        else:
            json.dump(self.output, f)

    def dict_encoding(cmd, args, argnames):
        action = dict(zip(argnames, args))
        action["a"] = cmd
        return action

    def list_encoding(cmd, args, argnames):
        action = [cmd] + args
        return action

    encodings = {"dict": dict_encoding, "list": list_encoding}

if len(sys.argv) > 1:
    Compiler(sys.argv[1])
else:
    c = Compiler("hello.dw", auto=False)
    c.compile()
    c.write(pretty=False)
