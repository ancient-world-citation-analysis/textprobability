# TextProbability

This project provides utilities for roughly estimating the probability that a given
string would be observed in a corpus that has some specified set of properties. No
serious attempt is to be made to specify the theoretical significance of this so-called
"probability." Instead, the use of "probabilities" as program output is motivated by one
or two common use cases, such as
- Distinguishing between mostly correct English text and randomly produced characters,
  or
- Determining whether a very short snippet of text is English, German, or French, given
  that it comes from a corpus that is (say) 60% English, 30% German, and 10% French.

Please consider the use of the term "probability" as a pragmatic abuse of language that
is used to make make certain calculations easier to explain.

## Data

This project uses data collected from Wikipedia on the following languages:
- German (de)
- English (en)
- Spanish (es)
- French (fr)
- Italian (it)
- Portuguese (pt)
- Turkish (tr)

Feel free to read the [data collection
logs](https://github.com/ancient-world-citation-analysis/textprobability/tree/main/textprobability/data/data-collection-logs)
to see what kinds of sources were used for language data.

This includes on the order of 10 MB of data per language. This incurs a one-time cost on
program startup when data is initially loaded from JSON files. This quantity of data is
from *after* summarizing the original data, a process which can reduce its size by up to
an order of magnitude. It is not yet clear what the consequences are of summarizing the
language data. For example, it may have a helpful de-noising effect, or it may
adversely affect the quality of the model by limiting its worldly knowledge -- probably
the latter.

## Usage

To determine the language of a string:
```python
from textprobability.classify import default_classifier

probabilities_by_language_with_default_priors = default_classifier(snippet)
```
The most probable language will be the argmax of the resulting map.

To determine a rough "probability" of observing a particular string in a corpus having
some language:
```python
bcp_47_langcode = "fr"
p_given_french = markov(bcp_47_langcode)  # The result is a function.
my_text = "le sigle"
probability_of_my_text = p_given_french(my_text)  # The result is a float in [0, 1].
```

To run examples, run:
```bash
python3 -m textprobability.examples.classification
```
Or:
```bash
python3 -m textprobability.examples.defaults
```

For help collecting new language data, run:
```bash
python3 -m textprobability.data.get_data --help
```
