# TextProbability

This project provides utilities for roughly estimating the probability that a given string would be observed in a corpus that has some specified set of properties. No serious attempt is to be made to specify the theoretical significance of this so-called "probability." Instead, the design of "probabilities" as program output is motivated by one or two common use cases, such as
* Distinguishing between mostly correct English text and randomly produced characters, or
* Determining whether a very short snippet of text is English, German, or French, given that it comes from a corpus that is (say) 60% English, 30% German, and 10% French.

Please consider the use of the term "probability" as a pragmatic abuse of language that is used to make make certain calculations easier to explain.
