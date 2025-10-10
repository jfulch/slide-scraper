# 📖 Info Retrieval - Study Content

Here are the extracted sections:

**DEFINITIONS & KEY TERMS**

* **Vector**: A mathematical representation of a document as a set of weighted terms
* **Term Frequency (tf)**: The frequency of a term in a document
* **Inverse Document Frequency (idf)**: A measure of how rare a term is across all documents
* **tf-idf weight**: A combined importance indicator for a term, calculated as tf \* idf
* **Cosine Similarity**: A measure of similarity between two vectors, calculated as the cosine of the angle between them
* **Inner Product**: The sum of the products of corresponding elements in two vectors
* **Hamming Distance**: The number of positions at which two binary strings differ

**ALGORITHMS & PROCESSES**

1. **Vector Space Model (VSM)**
	* Step-by-step breakdown:
		1. Convert documents to weighted term vectors
		2. Convert queries to weighted term vectors
		3. Compute cosine similarity between query and each document vector
		4. Rank documents by decreasing score
	* When/why it's used: For information retrieval tasks, such as searching and ranking documents
	* Key characteristics: Provides partial matching and ranked results; tends to work well in practice despite weaknesses
2. **Preprocessing**
	* Step-by-step breakdown:
		1. Pre-compute, for each term, its k nearest documents (treat each term as a 1-term query)
		2. Store the "preferred list" for each term
	* When/why it's used: To improve efficiency in searching and ranking documents
	* Key characteristics: Allows efficient implementation for large document collections

**FORMULAS & CALCULATIONS**

1. **tf-idf weight**
	* Formula: tf \* idf = (1 + log tf) \* log(N/df)
	* What each variable means:
		+ tf: term frequency
		+ idf: inverse document frequency
		+ N: total number of documents
		+ df: document frequency of a term
2. **Cosine Similarity**
	* Formula: cosSim(d, q) = (d \* q) / (|d| \* |q|)
	* What each variable means:
		+ d: document vector
		+ q: query vector
		+ |d|: magnitude of document vector
		+ |q|: magnitude of query vector

**IMPORTANT FACTS & NUMBERS**

1. **Collection size**: 10,000 documents
2. **Vocabulary size**: 7 terms
3. **Document frequency**: A(50), B(1300), C(250)

**CORE CONCEPTS EXPLAINED**

1. **Vector Space Model (VSM)**: A mathematical representation of documents and queries as vectors in a high-dimensional space.
2. **Cosine Similarity**: A measure of similarity between two vectors, calculated as the cosine of the angle between them.
3. **tf-idf weight**: A combined importance indicator for a term, calculated as tf \* idf.

**EXAMPLES & APPLICATIONS**

1. **Searching and ranking documents**: The VSM algorithm is used to search and rank documents based on their similarity to a query.
2. **Preprocessing**: Preprocessing is used to improve efficiency in searching and ranking documents by pre-computing the "preferred list" for each term.