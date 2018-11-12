# Assignment 6

This assignment contains a program to predict the category of a news by just reading the headline of the news and applying decision tree classification algorithm C4.5. The category class set is {"Business", "Comedy", "Sports", "Crime", "Religion"}.

### Requirements
1. nltk
1. sklearn
1. graphviz

**Note:** Weka wrapper can also be used after slight modifications in the code. Follow [this](https://fracpete.github.io/python-weka-wrapper/api.html#classifiers) link for weka wrapper.

### Code

The code is written in jupyter notebook in python and is quite understandable. We recommend to run the program in jupyter notebook only.

### Sample Run

#### Both Lexical and Syntactical features are included

10 Fold Cross validation scores (accuracy):

```
[ 0.56743145  0.55319149  0.58566629  0.58487395  0.57006726  0.57959641
  0.56365676  0.49102132  0.46071829  0.44668911]
```

Average accuracy: `0.540291234886`

#### Only lexical features are included

10 Fold Cross validation scores (accuracy):

```
[ 0.60940123  0.58454647  0.63773796  0.58263305  0.58688341  0.59753363
  0.60011217  0.5308642   0.54096521  0.51402918]
```

Average accuracy: `0.578470651554`
