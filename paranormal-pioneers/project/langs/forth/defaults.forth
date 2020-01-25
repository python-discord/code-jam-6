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
: STAR ." *" ;
: STARS 0 DO STAR LOOP ;
: TRIANGLE
   DO  CR  9 I - SPACES  I 2* 1+ STARS  DUP +LOOP  DROP ;

: DIAMONDS
   0 DO  1 10 0 TRIANGLE  -1 0 9 TRIANGLE  LOOP ;