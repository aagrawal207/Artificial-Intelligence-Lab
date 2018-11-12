# Assignment 7

1. To create a neural network which shows the functionality of a XOR function.

1. To write a program that predicts the category of a news by just reading the headline of the news and applying a neural network experimenting with different parameters. The category class set is {"Business", "Comedy", "Sports", "Crime", "Religion"}.

### Requirements
1. nltk
1. sklearn
1. pyTorch
1. Keras
2. numpy


### Code

The first part of code is written in jupyter notebook in python and is quite understandable. We recommend to run the program in jupyter notebook only. PyTorch library is used for creating the neural network.

The second part is done using both Keras and PyTorch and two different program are written one for each. The code is written in jupyter notebook in python and is recommended to run in that only.

### Sample Run of XOR program
 ```
 Loss Function = MSE
 Activation function = SGD
 Hidden Layer dimension = 100
 Number of inputs = 10 (so total of 2**10 = 1024 data points)
 Test size = 20%
 Epochs = 2500

 ```
Accuracy: `0.78048`


### Sample Run of news classification program

#### PyTorch including unigram, bigram and trigram

```
Loss function =  MSE
Activation function = Sigmoid function
Optimizer = SGD
One hidden layer of 64 nodes.
Test size = 20%
```

Average accuracy: `0.7825721490613617`


#### Keras including unigram, bigram and trigram

```
Loss function =  MSE
Activation function = ReLU
Optimizer = Adam
Two hidden layers of 64 and 16 nodes.
Test size = 20%
```

Average accuracy: `0.6615298402913982`
