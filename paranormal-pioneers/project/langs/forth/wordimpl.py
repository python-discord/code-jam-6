import itertools as it
from functools import reduce, partial
from typing import Iterable, TypeVar, Callable

T = TypeVar('T')
ForthEnv = 'src.forth.ForthEnv'


def _step_to(to_search: Iterable[T], item: T, predicate: Callable[[T, T], bool] = lambda i, x: x != i) -> int:
    return reduce(lambda a, _: a + 1,
                  it.takewhile(
                      partial(predicate, item),
                      to_search),
                  0)


def _jump(env: ForthEnv, label, direction=1) -> int:
    to_search = env.words[env.index::direction]
    return _step_to(to_search, f' {label}') * direction


def jump_if_false(env: ForthEnv, direction=1) -> int:
    label = env.data.pop()
    cond = env.data.pop()
    if cond:
        return 0
    return _jump(env, label, direction=direction)


def jump(env: ForthEnv, direction=1) -> int:
    label = env.data.pop()
    return _jump(env, label, direction=direction)


def forth_do(env: ForthEnv) -> int:
    start = env.data.pop()
    end = env.data.pop()
    env.rstack.append(end)
    env.rstack.append(start)
    return 0


#  256 0 DO I 16 MOD 0= IF CR THEN 1 . LOOP


def forth_loop(env: ForthEnv) -> int:
    label = env.data.pop()
    env.rstack[-1] += 1
    *_, end, start = env.rstack
    if start < end:
        return _jump(env, label, -1)
    env.rstack.pop()
    env.rstack.pop()
    return 0


def forth_steploop(env: ForthEnv):
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


def forth_i(env: ForthEnv) -> int:
    env.data.append(env.rstack[-1])
    return 0


def forth_j(env: ForthEnv) -> int:
    env.data.append(env.rstack[-3])
    return 0


def forth_puts(env: ForthEnv, char='"') -> int:
    print(env.words[env.index + 1], end='')
    return 2


def forth_def(env: ForthEnv) -> int:
    from .forth import ForthEntry
    idx = _step_to(env.words[env.index:], ';')
    words_ = {env.words[env.index + 1]: ForthEntry(env.words[env.index + 2: env.index + idx], special=False)}
    print('defined', words_)  # DEBUG
    env.forth_dict.update(words_)
    return idx


def forth_var(env: ForthEnv) -> int:
    name = env.words[env.index + 1]
    env.var_dict.update({name: None})
    return 1


def vset(env: ForthEnv) -> int:
    token = env.data.pop()
    newval = env.data.pop()
    env.var_dict[token.name] = newval
    return 0


def vget(env: ForthEnv) -> int:
    token = env.data.pop()
    env.data.append(token.val)
    return 0


def dots(env: ForthEnv) -> int:
    print(f'<{len(env.data)}>', *env.data, end=' ')
    return 0


def to_r(env: ForthEnv) -> int:
    env.astack.append(env.data.pop())
    return 0


def from_r(env: ForthEnv) -> int:
    env.data.append(env.astack.pop())
    return 0


def cp_r(env: ForthEnv) -> int:
    env.data.append(env.astack[-1])
    return 0
