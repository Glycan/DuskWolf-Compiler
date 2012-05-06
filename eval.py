from pdb import pm


class Code:
    def __init__(self, code):
        self.ns = {}
        for expr in code:
            Expr(self, expr)


class Expr:
    def __init__(self, code, expr, auto=True):
        self.expr = expr
        self.code = code
        if auto:
            self.eval(expr)

    def eval(self, obj):
        cmd = obj.pop("a")
        for key, arg in obj.items():
            if type(arg) not in (int, str, bool):
                obj[key] = self.eval(arg)
        cmd_func = getattr(self, "cmd_" + cmd)
        return cmd_func(**obj)

    def cmd_set(self, name, value):
        self.code.ns[name] = value

    def cmd_get(self, name):
        return self.code.ns[name]

    def cmd_sum(self, x, y):
        return x + y

    def cmd_diff(self, x, y):
        return x - y

    def cmd_print(self, text):
        return print(text)

code = [
    {"a": "set", "name": "a", "value": 10},
    {"a": "set", "name": "b", "value": 7},
    {"a": "set", "name": "z", "value": {
        "a":"sum",
        "x": {"a": "get", "name": "a"},
        "y": {
            "a": "diff",
            "x": {"a":"get", "name":"b"},
            "y": 5
            }
        }},
    {"a": "print", "text": {"a": "get", "name": "z"}},
]

Code(code)
