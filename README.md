# ants on a log visual
 For college CS, visual simulation of a pretty common math question

## The question:

Ninety-nine ants are dropped randomly along a log, with each ant facing one end or the
other. The log is 1 meter long from end to end. Each ant travels either toward the left
or the right end with a constant speed of 1 meter per minute. When two ants meet,
they bounce off each other and reverse directions, keeping their speed intact. When an
ant reaches an end of the log, it falls off. At some point, all of the ninety-nine ants will
fall off.
Over all the possible initial configurations, what is the longest amount of time you
would need to wait to guarantee that the log will have no ants? Provide justification
for your answer.

## The answer: 

While 99 ants bouncing off of each other make this seem too chaotic to solve, one key
observation simplifies the problem, which can be seen more easily if you consider two
ants rather than 99. When two ants bounce off each other and go in opposite directions,
since their speeds are not changing, this is equivalent to the ants passing by one another
in the sense that the positions of the ants in each case are identical. So you can ignore
all the collisions and treat the 99 ants as acting with independent motions. Viewing it
this way, the longest you would have to wait is potentially for one ant to move along
the entire log, which would take 1 minute.

<sub>Note both question and answer have been taken from [APSU](https://www.apsu.edu/mathematics/Problem2Solution.pdf)</sub>

## This project:

This project is essentially just a visual representation of this problem, in addition to the base problem (which all the default values are set to, ) it also allows for the user to adjust the speed, toggle collisions (WIP), and change the speed of the ants (which will change the time). 
