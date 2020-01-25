\ Default words which can be implemented in forth

: SPACE 32 EMIT ;
: SPACES ?DUP IF 0 DO SPACE LOOP THEN ;
: 0> 0 > ;
: 0< 0 < ;
: 0= 0 = ;
: ?DUP DUP IF DUP THEN ;
: 1+ 1 + ;
: 1- 1 - ;
: 2+ 2 + ;
: 2- 2 - ;
: 2* 2 * ;
: 2/ 2 / ;
: */ ROT ROT * SWAP / ;
: /MOD 2DUP MOD ROT ROT / ;
: */MOD ROT ROT * SWAP /MOD ;
: NEGATE -1 * ;
: NIP SWAP DROP ;
: U.R .R ;
: ? @ . ;
: +! DUP @ ROT + SWAP ! ;
: CREATE HERE 1+ VALUE ; \ probably not correct, but it works
: , 1 ALLOT HERE C! ;
: C, , ;
