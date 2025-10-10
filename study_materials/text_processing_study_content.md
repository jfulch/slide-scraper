# 📖 Text Processing - Study Content

Here are the extracted sections:

## DEFINITIONS & KEY TERMS

* **Information Retrieval (IR)**: The process of searching for and retrieving relevant information from a large database or corpus.
* **Text Classification**: The task of automatically assigning categories or labels to text data based on its content, such as spam vs. non-spam emails.
* **Standing Queries**: Pre-defined search queries that are run periodically to find new documents related to a specific topic or category.
* **Google Alerts**: A service that sends users email updates when new content matching their search query is found online.
* **Bag of Words**: A simple representation of text data where each document is represented as a vector of its word frequencies.
* **Naive Bayes (NB)**: A type of supervised learning algorithm used for classification tasks, which assumes independence between features.
* **k-Nearest Neighbors (kNN)**: A type of supervised learning algorithm used for classification tasks, which classifies an instance based on the majority vote of its k-nearest neighbors.
* **Centroid/Prototype**: The average vector representation of a set of instances in a high-dimensional space.
* **Rocchio**: An algorithm that forms a simple representative for each class by computing the centroid (prototype) of all instances in that class.

## ALGORITHMS & PROCESSES

### Naive Bayes (NB)

1. Compute the probability of each feature given the class label
2. Compute the probability of the class label given the features
3. Use Bayes' theorem to compute the posterior probability of the class label given the features
* Used for: Classification tasks where the features are independent
* Characteristics: Simple, fast, and effective

### k-Nearest Neighbors (kNN)

1. Compute the similarity between the test instance and all training instances
2. Select the k-nearest neighbors based on their similarity scores
3. Classify the test instance based on the majority vote of its k-nearest neighbors
* Used for: Classification tasks where the data is high-dimensional or has complex relationships
* Characteristics: Robust to noise, can handle non-linear relationships

### Rocchio

1. Compute the centroid (prototype) of each class by averaging all instances in that class
2. Classify a new instance based on its similarity to the centroids of each class
* Used for: Classification tasks where the data is high-dimensional and has complex relationships
* Characteristics: Simple, fast, and effective

## FORMULAS & CALCULATIONS

### Bayes' Theorem

P(C|D) = P(D|C) \* P(C) / P(D)

* Where:
	+ P(C|D): Posterior probability of class C given data D
	+ P(D|C): Likelihood of data D given class C
	+ P(C): Prior probability of class C
	+ P(D): Marginal likelihood of data D

## IMPORTANT FACTS & NUMBERS

* 10,000 - 1,000,000 unique words in a typical text collection
* kNN can be more accurate than NB or Rocchio for high-dimensional data
* Naive Bayes is widely used in spam filtering due to its simplicity and effectiveness

## CORE CONCEPTS EXPLAINED

* **Text Classification**: The task of automatically assigning categories or labels to text data based on its content.
* **Bag of Words**: A simple representation of text data where each document is represented as a vector of its word frequencies.
* **High-Dimensional Space**: A space with many dimensions, such as the bag-of-words representation of text data.

## EXAMPLES & APPLICATIONS

* Google Alerts: A service that sends users email updates when new content matching their search query is found online.
* Spam filtering: Naive Bayes is widely used in spam filtering due to its simplicity and effectiveness.
* Text classification: Rocchio is an algorithm that forms a simple representative for each class by computing the centroid (prototype) of all instances in that class.