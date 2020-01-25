import operator as op
from re import sub
from typing import List, Union, Callable, Dict, TypeVar, Any, Iterable

from project.langs.forth import wordimpl


def partial_kw(**kwargs):
    def decorator(fun):
        def inner(*args, **kwargs2):
            return fun(*args, **{**kwargs, **kwargs2})

        return inner

    return decorator


def pops(arity: int, returns=-1) -> Callable:
    """decorates a function that takes arity parameters and makes it manipulate the data stack
    popping the top arity values and passing them to the function
    if returns is -1 (default),  the return value is pushed to the data stack
    if returns is 0, the return value is ignored
    if returns is 1, the stack is extended by the return value"""

    def decorator(fun: Callable) -> Callable:
        def inner(env: ForthEnv) -> int:
            if arity:
                params = env.data[-arity:]
            else:
                params = []
            try:
                res = fun(*params)
            except TypeError as e:
                print(env.words[env.index], "missing parameters data=", env.data)  # DEBUG
                raise e
            if returns:
                if returns == -1:
                    env.data[-arity:] = [res]
                else:
                    env.data[-arity:] = res
            elif arity:
                env.data[-arity:] = []
            return 0

        return inner

    return decorator


class ForthEntry:
    def __init__(self, code: Union[List[str], Callable[['ForthEnv'], int]], special=True):
        self.code = code
        self.special = special

    def __repr__(self):
        return f'Word: {self.code}'


class VarToken:
    def __init__(self, name, val):
        self.name = name
        self.val = val


class ExecToken:
    def __init__(self, name):
        self.name = name


class Pointer:
    def __init__(self, idx: int, arr: Iterable) -> None:
        self.idx = idx
        self.arr = list(arr)

    def __add__(self, other: int) -> 'Pointer':
        return Pointer(self.idx + other, self.arr)

    def __sub__(self, other: int) -> 'Pointer':
        return Pointer(self.idx - other, self.arr)

    def resolve(self):
        return self.arr[self.idx]

    def set(self, val: Any) -> None:
        self.arr[self.idx] = val


class ForthEnv:
    def __init__(self, forth_dict: Dict[str, ForthEntry]):
        self.source = ''
        self.data: List = []
        # return stack, however, as there is no return stack used,
        # this is just a dedicated stack for R words
        self.astack: List = []
        # internal values, e.g. for loops
        self.rstack: List = []
        self.words: List[str] = []
        self.index = 0
        self.forth_dict = forth_dict
        self.var_dict: Dict[str, Any] = {}

    def call_word(self, word: ForthEntry) -> int:
        if word.special:
            return word.code(self)
        else:
            self.words[self.index:self.index + 1] = word.code
            return -1

    def forth_eval(self, cmd) -> None:
        self.source = cmd
        self.words = forth_compile(cmd)  # some commands need the word list
        self.index = 0
        while self.index < len(self.words):
            #  print(self.data, self.words[self.index:], self.index)
            word = self.words[self.index]
            if word in self.forth_dict:
                d = self.call_word(self.forth_dict[word])
                self.index += d
            elif word in self.var_dict:
                self.data.append(VarToken(word, self.var_dict[word]))
            elif isinstance(word, str) and ' ' not in word:
                try:
                    self.data.append(int(word))
                except ValueError:
                    self.data.append(float(word))
            else:
                self.data.append(word)
            self.index += 1


DEFAULT_ENTRIES = {
    "+": ForthEntry(pops(2)(op.add)),
    "-": ForthEntry(pops(2)(op.sub)),
    "*": ForthEntry(pops(2)(op.mul)),
    "/": ForthEntry(pops(2)(op.floordiv)),
    "MOD": ForthEntry(pops(2)(op.mod)),
    ">": ForthEntry(pops(2)(op.gt)),
    "<": ForthEntry(pops(2)(op.lt)),
    "=": ForthEntry(pops(2)(op.eq)),
    "<>": ForthEntry(pops(2)(op.ne)),
    "AND": ForthEntry(pops(2)(op.and_)),
    "OR": ForthEntry(pops(2)(op.or_)),
    "ABS": ForthEntry(pops(1)(op.abs)),
    "MIN": ForthEntry(pops(2)(min)),
    "MAX": ForthEntry(pops(2)(max)),
    ".": ForthEntry(pops(1, returns=0)(partial_kw(end=' ')(print))),
    "CR": ForthEntry(pops(0, returns=0)(print)),
    "EMIT": ForthEntry(pops(1, returns=0)(lambda x: print(chr(x), end=''))),
    "?BRANCH": ForthEntry(wordimpl.jump_if_false),
    "BRANCH": ForthEntry(wordimpl.jump),
    "-?BRANCH": ForthEntry(partial_kw(direction=-1)(wordimpl.jump_if_false)),
    "-BRANCH": ForthEntry(partial_kw(direction=-1)(wordimpl.jump)),
    "DO": ForthEntry(wordimpl.forth_do),
    "LOOP": ForthEntry(wordimpl.forth_loop),
    "+LOOP": ForthEntry(wordimpl.forth_steploop),
    "I": ForthEntry(wordimpl.forth_i),
    "J": ForthEntry(wordimpl.forth_j),
    ".R": ForthEntry(pops(2, returns=0)(lambda v, s: print(f'{v:>{s}}', end=''))),
    '."': ForthEntry(wordimpl.forth_puts),
    'S"': ForthEntry(wordimpl.forth_str_literal),
    '.S': ForthEntry(wordimpl.dots),
    "DUP": ForthEntry(pops(1, returns=1)(lambda a: (a, a))),
    "2DUP": ForthEntry(pops(2, returns=1)(lambda a, b: (a, b) * 2)),
    "SWAP": ForthEntry(pops(2, returns=1)(lambda a, b: (b, a))),
    "2SWAP": ForthEntry(pops(4, returns=1)(lambda a, b, c, d: (c, d, a, b))),
    "ROT": ForthEntry((pops(3, returns=1)(lambda a, b, c: (b, c, a)))),
    "2ROT": ForthEntry((pops(6, returns=1)(lambda a, b, *c: (*c, a, b)))),
    "OVER": ForthEntry((pops(2, returns=1)(lambda a, b: (a, b, a)))),
    "2OVER": ForthEntry((pops(4, returns=1)(lambda a, b, *c: (a, b, *c, a, b)))),
    "DROP": ForthEntry((pops(1, returns=0)(lambda a: 0))),
    "2DROP": ForthEntry((pops(2, returns=0)(lambda *a: 0))),
    ".(": ForthEntry((partial_kw(char=')'))(wordimpl.forth_puts)),
    ":": ForthEntry(wordimpl.forth_def),
    ";": ForthEntry(lambda a: 0),
    "!": ForthEntry(wordimpl.vset),
    "@": ForthEntry(wordimpl.vget),
    "VARIABLE": ForthEntry(wordimpl.forth_var),
    "CONSTANT": ForthEntry(wordimpl.forth_const),
    "'": ForthEntry(wordimpl.quote),
    "R>": ForthEntry(wordimpl.from_r),
    ">R": ForthEntry(wordimpl.to_r),
    "R@": ForthEntry(wordimpl.cp_r),
    "EXECUTE": ForthEntry(wordimpl.execute),
    "C!": ForthEntry(wordimpl.ptr_set),
    "C@": ForthEntry(wordimpl.ptr_get),
    "TYPE": ForthEntry(wordimpl.forth_type),
    "VALUE": ForthEntry(wordimpl.value),
    "TO": ForthEntry(wordimpl.forth_to),
    "SOURCE": ForthEntry(wordimpl.source),

}

T = TypeVar("T")


def forth_compile(words: str) -> List[str]:
    """generates a word list from the input string. Also converts flow control into jumps"""
    scope_stacks: Dict[str, List] = {k: [] for k in {'IF', 'DO', 'BEGIN'}}
    labels = 0
    out = []
    rest = words
    while rest:
        rest = str(sub(r'\s', ' ', rest, 1))
        word, _, rest = rest.partition(' ')
        word = word.upper()
        if word == 'IF':
            scope_stacks[word].append(labels)
            out.extend((str(labels), '?BRANCH'))
            labels += 1
        elif word == 'ELSE':
            label = scope_stacks['IF'].pop()
            scope_stacks['IF'].append(labels)
            out.extend((str(labels), 'BRANCH', f' {label}'))
            labels += 1
        elif word == "THEN":
            label = scope_stacks['IF'].pop()
            out.append(f' {label}')
        elif word == "DO":
            scope_stacks[word].append(labels)
            out.extend((word, f' {labels}'))
            labels += 1
        elif word == "BEGIN":
            scope_stacks[word].append(labels)
            out.append(f' {labels}')
            labels += 1
        elif word in ("LOOP", "+LOOP"):
            label = scope_stacks["DO"].pop()
            out.extend((str(label), word))
        elif word == "UNTIL":
            label = scope_stacks["BEGIN"].pop()
            out.extend((str(label), "-?BRANCH"))
        elif word == "AGAIN":
            label = scope_stacks["BEGIN"].pop()
            out.extend((str(label), "-BRANCH"))
        elif word == "LEAVE":
            label = scope_stacks["DO"][-1]
            out.extend((str(label), "BRANCH"))
        elif word == "WHILE":
            scope_stacks["BEGIN"].append(labels)
            out.extend((str(labels), "?BRANCH"))
            labels += 1
        elif word == "REPEAT":
            self_label = scope_stacks["BEGIN"].pop()
            jump_label = scope_stacks["BEGIN"].pop()
            out.extend((str(jump_label), "-BRANCH", f' {self_label}'))
        elif word in {'.(', '."', 's"'}:
            literal, term, rest = rest.partition(')' if word[-1] == '(' else '"')
            out.extend((word, literal, term))
        elif word == "(":
            _, _, rest = rest.partition(')')
        elif word == "\\":
            _, _, rest = rest.partition('\n')
        elif word:
            out.append(word)
    assert all(not o for o in scope_stacks.values())
    return out


def repl() -> None:
    env = ForthEnv(DEFAULT_ENTRIES)
    with open(f"{__file__}/../defaults.forth") as f:
        code = f.read()
        env.forth_eval(code)

    while True:
        try:
            cmd = input("FORTH>")
            print('compiled', cmd)  # DEBUG
            env.forth_eval(cmd)
        except Exception as e:
            print(e)
            raise e
