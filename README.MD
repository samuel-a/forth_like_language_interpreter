# A limited-feature interpreter for an imaginary forth-like language

26.01.2019

no dependencies

## Example programs

```
\> 1 2 + 10 * 6 / print
[5] <top
```
```
\> : AVERAGE3 + + 3 / ; 12 8 10 AVERAGE3 print
[10] <top
```

```
\> : A 30 ; : B 70 ; A B (this is a comment) A B + print
[30, 70, 100] <top
```

```
\> : IF 2 branch? 0 1 ; 1 IF print

[1] <top
```


## Problems/negative features
* no negative number popping, except with ` : neg 0 swap - ; `
* branch logic fuzzy, comments affect branch logic