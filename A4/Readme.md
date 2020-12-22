# Decision Trees

This assigment constructs a decision tree for a given problem statement. In order to build the decision tree, we need to pick a deciding attribute at each stage so as to branch the examples from the data-set and place them in different buckets.

## Entropy: 
At each level in the tree, entropy is the measure of randomness in the data. It
is a measure of the uncertainty of the random variable. Throughout this report the entropy
is represented in terms of B(q) where q is the fraction of examples whose result is positive.

## Information Gain: 
For an attribute A is the expected reduction The attribute with the maximum information gain will help arrive at a decision faster. It is critical to select the right attribute for the partitioning since otherwise the depth of the tree may increase.

This same process is repeated at every intermediate node to determine the best attribute based on which the examples at that node must be split.