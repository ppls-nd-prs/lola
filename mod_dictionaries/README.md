This folder contains all dictionaries that are modified compared to the original translations provided by the LogicLLaMA model. 

Each file name is formatted as follows: <br>
<code>[*modification ids*]*name of original dictionary*.json</code> <br>
In case multiple modification ids are relevant, they are separated with an underscore (_). 

### Modification/addition ids:
**e_i2c**: if the first quantifier is existential, implications are changed into quantifiers.

**a2e**: all universal quantifiers are changed into existential quantifiers 

**i2c**: all implications are changed into conjunctions

**split_verb**: all predicates consisting of 2 words are split like a verb of the form *verb object*. 

**split_adj**: all predicates consisting of 2 words are split like a verb of the form *adjective object*. 