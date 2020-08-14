# Flappy Bird AI

A small neural network that was created in the hopes of "beating" Flappy Bird. Uses PyGame to create the game itself and the NEAT evolution model.

---

## About NEAT and the Neural Network

NeuroEvolution of Augmenting Topologies (NEAT) is an evolution model that is built on the thought that beginning with a very simple neural network and slowly making the network more complex as the learning process countinues. As the AI continues to learn, more nodes are added as needed until the model is perfect for the specific problem it is meant to solve

The network begins by simply taking input from the y-coodinate of the bird, as well as the distance between the bird and the top and bottom pipes. With this imformation it must decide whether to jump or not. The activation function used is a Sigmoid Function where if the output is >=0.5, the AI will jump. 

---
