# A limited-feature interpreter for an imaginary forth-like language

26.01.2019

no dependencies

## Example programs

```
>1 2 + 10 * 6 / print
[5] <top
```
```
>: AVERAGE3 + + 3 / ; 12 8 10 AVERAGE3 print
[10] <top
```

```
>: A 30 ; : B 70 ; A B (this is a comment) A B + print
[30, 70, 100] <top
```

```
>: average-n (--0, val1, val2,...)
(init) 0 swap (v1 -> 0, v1)
(loop)
rot 1 + rot (v1, c, v2 -> c+1, v2, v1)
dup 5 branch? (are we there yet?)
drop swap / (c, v1, 0 -> v1/c)
5 branch (return)
(else)
+ (c+1, v2, v1 -> c+1, v1+v2)
17 0 - branch
;
0 10 20 70 80 average-n print
[45]<top
```


## Problems/negative features
* no negative number pushing, except with ` : neg 0 swap - ; `
* branch logic fuzzy
* macros permantently lengthen the program code 