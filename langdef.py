cmd_trans = {
    "on": "listen",
    "echo": "print"
}
cannon_cmds = {
    "listen": ["event"],
    "comment": ["text"],
    "var": ["name", "value"],
    "print": ["text"]
}

alt_cmds = {
    "set": ["name", "value"],
    "get": ["name"],
    "sum": ["x", "y"],
    "print": ["text"]
}

cmds = alt_cmds
