import itertools as it
import sys
from functools import reduce, partial
from typing import Iterable, TypeVar, Callable

T = TypeVar('T')
ForthEnv = 'project.langs.forth.forthimpl.ForthEnv'


# BRANCH, :
def _step_to(
        to_search: Iterable[T],
        item: T,
        predicate: Callable[[T, T], bool] = lambda i, x: x != i
) -> int:
    return reduce(
        lambda a, _: a + 1,
        it.takewhile(
            partial(predicate, item),
            to_search
        ), 0
    )


# BRANCH, LOOP
def _jump(env: ForthEnv, label, direction=1) -> int:
    to_search = env.words[env.index::direction]
    return _step_to(to_search, f' {label}') * direction


def _str_literal(env: ForthEnv, literal: str):
    from project.langs.forth.forthimpl import Pointer
    env.data.append(Pointer(0, list(literal)))
    env.data.append(len(literal))


# BRANCH
def jump_if_false(env: ForthEnv, direction=1) -> int:
    label = env.data.pop()
    cond = env.data.pop()
    if cond:
        return 0
    return _jump(env, label, direction=direction)


# BRANCH
def jump(env: ForthEnv, direction=1) -> int:
    label = env.data.pop()
    return _jump(env, label, direction=direction)


# DO
def forth_do(env: ForthEnv) -> int:
    start = env.data.pop()
    end = env.data.pop()
    env.rstack.append(end)
    env.rstack.append(start)
    return 0


# LOOP
def forth_loop(env: ForthEnv) -> int:
    label = env.data.pop()
    env.rstack[-1] += 1
    *_, end, start = env.rstack
    if start < end:
        return _jump(env, label, -1)
    env.rstack.pop()
    env.rstack.pop()
    return 0


# +LOOP
def forth_steploop(env: ForthEnv) -> int:
    label = env.data.pop()
    step = env.data.pop()
    env.rstack[-1] += step
    *_, end, idx = env.rstack
    oidx = idx - step
    if oidx < end <= idx or oidx >= end > idx:
        env.rstack.pop()
        env.rstack.pop()
        return 0
    return _jump(env, label, -1)


# I
def forth_i(env: ForthEnv) -> int:
    env.data.append(env.rstack[-1])
    return 0


# J
def forth_j(env: ForthEnv) -> int:
    env.data.append(env.rstack[-3])
    return 0


# .", .(
def forth_puts(env: ForthEnv, char='"') -> int:
    print(env.words[env.index + 1], end='')
    return 2


# s"
def forth_str_literal(env: ForthEnv) -> int:
    literal = env.words[env.index + 1]
    _str_literal(env, literal)
    return 2


# C!
def ptr_set(env: ForthEnv) -> int:
    ptr = env.data.pop()
    val = env.data.pop()
    ptr.set(val)
    return 0


# C@
def ptr_get(env: ForthEnv) -> int:
    ptr = env.data.pop()
    env.data.append(ptr.resolve())
    return 0


# :
def forth_def(env: ForthEnv) -> int:
    from .forthimpl import ForthEntry
    idx = _step_to(env.words[env.index:], ';')
    words_ = {env.words[env.index + 1]: ForthEntry(
        env.words[env.index + 2: env.index + idx],
        special=False
    )}
    #  print('defined', words_)  # DEBUG
    env.forth_dict.update(words_)
    return idx


# VARIABLE
def forth_var(env: ForthEnv) -> int:
    name = env.words[env.index + 1]
    env.var_dict.update({name: None})
    return 1


# CONSTANT
def forth_const(env: ForthEnv) -> int:
    val = env.data.pop()
    name = env.words[env.index + 1]
    env.var_dict.update({name: val})
    return 1


# !
def vset(env: ForthEnv) -> int:
    token = env.data.pop()
    newval = env.data.pop()
    env.var_dict[token.name] = newval
    return 0


# @
def vget(env: ForthEnv) -> int:
    token = env.data.pop()
    env.data.append(token.val)
    return 0


# type
def forth_type(env: ForthEnv) -> int:
    n = env.data.pop()
    ptr = env.data.pop()
    print(''.join(ptr.arr[ptr.idx:ptr.idx + n]), end='')
    return 0


# .S
def dots(env: ForthEnv) -> int:
    print(f'<{len(env.data)}>', *env.data, end=' ')
    return 0


# >R
def to_r(env: ForthEnv) -> int:
    env.astack.append(env.data.pop())
    return 0


# R>
def from_r(env: ForthEnv) -> int:
    env.data.append(env.astack.pop())
    return 0


# R@
def cp_r(env: ForthEnv) -> int:
    env.data.append(env.astack[-1])
    return 0


# '
def quote(env: ForthEnv) -> int:
    from project.langs.forth.forthimpl import ExecToken
    name = env.words[env.index + 1]
    env.data.append(ExecToken(name))
    return 1


# EXECUTE
def execute(env: ForthEnv) -> int:
    to_call = env.data.pop().name
    env.words[env.index] = to_call
    return -1


# VALUE
def value(env: ForthEnv) -> int:
    name = env.words[env.index + 1].upper()
    val = env.data.pop()
    env.val_dict.update({name: val})
    return 1


# TO
def forth_to(env: ForthEnv) -> int:
    return value(env)


# SOURCE
def source(env: ForthEnv) -> int:
    _str_literal(env, env.source)
    return 0


# HERE
def here(env: ForthEnv) -> int:
    from project.langs.forth.forthimpl import Pointer
    pointer = Pointer(len(env.data_space) - 1, env.data_space)
    env.data.append(pointer)
    return 0


# ALLOT
def allot(env: ForthEnv) -> int:
    env.data_space.extend([0] * env.data.pop())
    return 0


# 0X
def hex_literal(env: ForthEnv) -> int:
    literal = env.words[env.index + 1].upper()
    env.data.append(int(literal, 16))
    return 1


# ACCEPT
def accept(env: ForthEnv) -> int:
    max_count = env.data.pop()
    addr = env.data.pop()
    data = sys.stdin.readline(max_count).rstrip('\n')
    datalen = min(len(data),max_count)
    addr.arr[addr.idx:addr.idx+datalen] = data
    env.data.append(datalen)
    return 0
