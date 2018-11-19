# Assignment 8

To write a program that predicts the intent of a flight utterance.

### Requirements
1. sklearn
1. Keras
2. numpy


### Code

The code is written in Keras using Jupyter notebook in python.

### Dataset

Description of the dataset can be found in
https://github.com/Microsoft/CNTK/tree/master/Examples/LanguageUnderstanding/ATIS

Dataset can be downloaded here: https://github.com/Microsoft/CNTK/tree/master/Examples/LanguageUnderstanding/ATIS/Data

### Sample Run of intent classification program

#### Keras including unigram

```
Loss function =  Categorical Cross Entropy
Activation function = ReLU and Softmax in output layer
Optimizer = Adam
Two hidden layers of 64 and 16 nodes.
```

Average accuracy: `0.9289940828402367`
F1-Score: `0.5743886763225182`
Recall: `0.5729309856298727`
Precision: `0.6738049331290883`
