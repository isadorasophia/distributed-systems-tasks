## Report for test 1
### Intro
The assignment consisted in applying a toy operation, which:
    - receives an input ```N``` as argument;
    - allocates an array ```v``` of 64-bit integers of size N * 2²°
    - for each position i of the array ```v```:
        + assigns a random number between 0 and 1000
    - calculates average value of ```v```

Basically, given our input ```N``` which is the size of our array, we receive an output of the average value of the array ```v```.

### Implementation
The implementation consisted of three differente approaches:
    1. Sequential application
    1. Multithread application
    1. Multiprocess application

For the multithread application, it was used the _OpenMP_ library. As for the multiprocess application, it was used standard Linux methods.

### Results
The results collected were estimated from executions with ```N = 64``` and ```k = 4```. The graph bellow speaks for itself.