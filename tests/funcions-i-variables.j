x =: 1 + 2 3 4
x                     NB. resultat: 3 4 5
x = x                 NB. resultat: 1 1 1
x =: x + 1
*: x                  NB. resultat: 16 25 36

doble =: ((2 * ]))
doble _1 _2 _3        NB. resultat: _2 _4 _6

inc =: 1 + ]
inc2 =: inc @: inc
decr =: _1 * ] @: 1 - ]
fact =: */ @: inc2 @: i. @: decr
fact 6                NB. resultat: 720

zero =: 0
parells =: zero = ] @: (zero + 2) | ]

i2 =: inc @: i.
v =: i2 10
v                     NB. resultat: 1 2 3 4 5 6 7 8 9 10
v_filtrat =: v #~ parells v
v_filtrat             NB. resultat: 2 4 6 8 10
