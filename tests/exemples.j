1 2 3    NB. resultat: 1 2 3

1 1 1 + 1 2 3    NB. resultat: 2 3 4

1 + 1 2 3    NB. resultat: 2 3 4

1 1 + 1 2 3   NB. resultat: length error

5 + 2 * 3    NB. resultat: 11

5 * 2 + 3    NB. resultat: 25

(5 * 2) + 3    NB. resultat: 13

_1 * 2 3    NB. resultat: _2 _3

5 - 2    NB. resultat: 3

2 * 3    NB. resultat: 6

6 % 2    NB. resultat: 3

2 | 7    NB. resultat: 1

2 ^ 3    NB. resultat: 8

5 4 9 > 6 4 4    NB. resultat: 0 0 1

5 < 1 7 1    NB. resultat: 0 1 0

NB. Pendents de revisar 2 >= 3    NB. resultat: 0

NB. Pendents de revisar _6 <= _6    NB. resultat: 1

1 2 5 = 5 6 5    NB. resultat: 0 0 1

0 0 _1 3 <> 1 0 _1 3    NB. resultat: 1 0 0 0

] 1    NB. resultat: 1

1 , 2 3    NB. resultat: 1 2 3

# 1 2    NB. resultat: 2

1 0 1 0 # 1 2 3 4    NB. resultat: 1 3

0 2 { 2 3 4   NB. resultat: 2 4

i. 4    NB. resultat: 0 1 2 3

+: 1 2 3    NB. resultat: 2 4 6

+ / 1 2 3    NB. resultat: 6

7 | ~ 2    NB. resultat: 1

x =: 1 2 3
1 + x        NB. resultat: 2 3 4

square =: *:
square 1 2 3 4    NB. resultat: 1 4 9 16

mod2 =: 2 | ]
mod2 i. 4    NB. resultat: 0 1 0 1

square =: *:
square 1 + i. 3    NB. resultat: 1 4 9

mod2 =: 2 | ]
eq0 =: 0 = ]

eq0 mod2 i. 6    NB. resultat: 1 0 1 0 1 0

parell =: eq0 @: mod2
parell i. 6    NB. resultat: 1 0 1 0 1 0

parell =: 0 = ] @: 2 | ]
parell i. 6    NB. resultat: 1 0 1 0 1 0

inc =: 1 + ]
test =: +/ @: inc @: i.
test 3    NB. resultat: 6
