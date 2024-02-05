This folder contains all evaluation results after a modification or addition to the original translations provided by the LogicLLaMA model. 

Each file name is formatted as follows: <br>
<code>[*modification ids*][*lexical knowledge used*]*data-set*\_[evaluation/exceptions].json</code> <br>
In case multiple modification IDs are relevant, they are separated with an underscore (_). 
Files with <code>[metrics]</code> added at the end, contain a confusion matrix for that specific evaluation file. 

### Modification/addition ids:
**e_i2c**: if the first quantifier is existential, implications are changed into quantifiers.

**a2e**: all universal quantifiers are changed into existential quantifiers 

**i2c**: all implications are changed into conjunctions

**split_verb**: all predicates consisting of 2 words are split like a verb of the form *verb object*. 

**split_adj**: all predicates consisting of 2 words are split like a verb of the form *adjective object*. 