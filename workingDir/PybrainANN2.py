import os
from random import randint, shuffle
import matplotlib.pyplot as plt
from pybrain.structure import FeedForwardNetwork, FullConnection
from pybrain.structure import LinearLayer, SigmoidLayer, SoftmaxLayer
from pybrain.tools.xml import NetworkWriter
from pybrain.tools.xml import NetworkReader
from pybrain.utilities import percentError
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import ClassificationDataSet

from pylab import imshow
from scipy import io, ndimage
from numpy import *
import os

from PIL import Image
import numpy as np

im =Image.open("images/1.png").resize((28,28)).convert('L')
img = np.array(im).astype(float)
print img.shape

def plotTheNum(X, Y, ca):
    # plots the given image
    # the image matrix is transposed
    # color set to grey
    inputImage = X[ca, :]
    #imshow((inputImage.reshape(20, 20)).T, cmap='Greys')
    # plot the same output case
    print('the digit printed is', Y[ca][0])


def convertToOneOfMany(Y):
    # converts Y to one of many types
    # or one output per label
    rows, cols = Y.shape
    classes = unique(Y).size  # should get 10 classes
    newY = zeros((rows, classes))

    for i in range(0, rows):
        newY[i, Y[i]] = 1

    return newY  # load the MNIST data

digits = io.loadmat('ex4data1.mat')

# making X and Y numpy arrays
X = digits['X']
Y = digits['y']

Y[Y == 10] = 0  # 0 has the 10th position, this line gives it the 0th position

numOfLabels = unique(Y).size  # gets your 10 labels

print('show a random number from the MNIST database')
randomInd = randint(0, X.shape[0])  # gets a random number between 0 and the size of the X array
plotTheNum(X, Y, randomInd)
#plt.show()

# build the dataset
X = c_[ones(X.shape[0]), X]
numOfExamples, sizeOfExample = X.shape
# convert the test data to one of many (10)
Y = convertToOneOfMany(Y)

# seperating training and test datasets

X1 = hstack((X, Y))
shuffle(X1)

X = X1[:, 0:sizeOfExample]
Y = X1[:, sizeOfExample: X1.shape[1]]

# add the contents of digits to a dataset
#daSet = ClassificationDataSet(sizeOfExample, numOfLabels)
#for k in xrange(len(X)):
#    daSet.addSample(X.ravel()[k], Y.ravel()[k])

#testData, trainData = daSet.splitWithProportion(0.25)

trainData = ClassificationDataSet(sizeOfExample, numOfLabels)
testData = ClassificationDataSet(sizeOfExample, numOfLabels)

cutoff = int(numOfExamples * 0.7)


for i in range(0, cutoff):
   trainData.addSample(X[i,:], Y[i,:])

# setting the field names
trainData.setField('input', X[0:cutoff, :])
trainData.setField('target', Y[0:cutoff, :])


for i in range(cutoff, numOfExamples):
    testData.addSample(X[i, :], Y[i, :])

testData.setField('input', X[cutoff:numOfExamples, :])
testData.setField('target', Y[cutoff:numOfExamples, :])


# split the dataset into training and testing
# testData, trainData = daSet.splitWithProportion(0.25)

# convert the data into 10 separate digits
#trainData._convertToOneOfMany()
#testData._convertToOneOfMany()

if os.path.isfile('dig.xml'):
    net = NetworkReader.readFrom('dig.xml')
    net.sorted = False
    net.sortModules()
else:
    inputLayerSize = sizeOfExample
    hiddenLayerSize0 = sizeOfExample/2
    outputLayerSize = numOfLabels

    inputLayer = LinearLayer(inputLayerSize)
    hiddenLayer0 = SigmoidLayer(hiddenLayerSize0)
    outputLayer = SoftmaxLayer(outputLayerSize)

    net = FeedForwardNetwork()
    # add layers to FFN
    net.addInputModule(inputLayer)
    net.addModule(hiddenLayer0)
    net.addOutputModule(outputLayer)

    # create connections between the layers
    in_to_hidden = FullConnection(inputLayer, hiddenLayer0)
    hidden_to_out = FullConnection(hiddenLayer0, outputLayer)
    # add connections
    net.addConnection(in_to_hidden)
    net.addConnection(hidden_to_out)

   # net.sorted = False
    net.sortModules()



testIndex = randint(0, X.shape[0])
testInput = X[testIndex, :]

print("Number to predict is", Y[testIndex][0])

realTrain = trainData['target'].argmax(axis=1)
realTest = testData['target'].argmax(axis=1)

EPOCHS = 50

trainer = BackpropTrainer(net, dataset=trainData, momentum=0.3, learningrate=0.01,verbose=False)


trainResultArr = []
epochs =  []
testResultArr = []

for i in range(EPOCHS):
    # set the epochs
    trainer.trainEpochs(1)

    outputTrain = net.activateOnDataset(trainData)
    outputTrain = outputTrain.argmax(axis=1)
    trainResult = percentError(outputTrain, realTrain)

    outputTest = net.activateOnDataset(testData)
    outputTest = outputTest.argmax(axis=1)
    testResult = percentError(outputTest, realTest)

    finalTrainRes = 100-trainResult
    finalTestRes = 100-testResult
    print('Epoch: ', i, 'training set accuracy:', finalTrainRes, 'test set accuracy:', finalTestRes)

    trainResultArr.append((finalTestRes))
    testResultArr.append((finalTrainRes))
    epochs.append((i))
   # if finalTrainRes >= 100 or finalTestRes >= 100:
    #    break


prediction = net.activate(testInput)
p = argmax(prediction, axis=0)

NetworkWriter.writeToFile(net, 'dig.xml')

# plotData(X[:, 0:sizeOfExample-1], Y, randomIndex)
print("predicted output after training is", p)

plt.plot(epochs,trainResultArr)
plt.plot(epochs,testResultArr)

plt.show()