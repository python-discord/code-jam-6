import sys


class FooBar:
    pass


try:
    int("a")
except:
    pass

a = 1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567

friend = "something"

print(f"hello {friend}", file=sys.stderr)
print(sys.version, file=sys.stderr)
