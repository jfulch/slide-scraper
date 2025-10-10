# 📖 Inverted Indexing - Study Content

Here are the extracted sections:

**DEFINITIONS & KEY TERMS**

* **Inverted Index**: A data structure that maps each term (word) in a document collection to a list of documents containing that term.
* **Term Frequency**: The number of times a term appears in a document.
* **Document Frequency**: The number of documents that contain a particular term.
* **N-gram**: A sequence of n consecutive words or characters in a text.
* **Biword**: A 2-word sequence (a type of N-gram).
* **Extended Biword**: A biword with additional context, such as part-of-speech tags.
* **Part-of-Speech Tagging**: The process of identifying the grammatical category (such as noun or verb) of each word in a text.

**ALGORITHMS & PROCESSES**

1. **Inverted Index Construction**
	* Step-by-step breakdown:
		+ Tokenize documents into individual words.
		+ Create a list of unique terms (words).
		+ For each term, create a list of documents containing that term.
	* When/why it's used: To efficiently search for specific terms in a large document collection.
	* Key characteristics: Scalable, flexible, and efficient.
2. **N-gram Indexing**
	* Step-by-step breakdown:
		+ Identify all N-grams (sequences of n consecutive words) in the text.
		+ Create an inverted index for each N-gram.
	* When/why it's used: To support proximity searches, such as finding all occurrences of a phrase within a certain distance from each other.
	* Key characteristics: Can be computationally expensive and requires significant storage space.

**FORMULAS & CALCULATIONS**

None mentioned in the slides.

**IMPORTANT FACTS & NUMBERS**

* The Google n-gram sample contains:
	+ 1 trillion tokens
	+ 95 billion sentences
	+ 13.6 million unigrams (single words)
	+ 314 million bigrams (2-word sequences)
	+ 977 million trigrams (3-word sequences)
	+ 1.3 billion 4-grams (4-word sequences)
* The distribution of unique N-grams is similar between English and Chinese, but the Chinese distribution is shifted to larger N.

**CORE CONCEPTS EXPLAINED**

* An inverted index is a data structure that maps each term in a document collection to a list of documents containing that term.
* N-gram indexing is used to support proximity searches by creating an inverted index for sequences of n consecutive words.
* Part-of-speech tagging is the process of identifying the grammatical category of each word in a text.

**EXAMPLES & APPLICATIONS**

* Google's n-gram sample, which contains 1 trillion tokens and is used to support search functionality.
* Patent data, which often contains formal phrases that are frequently searched for.