# 📖 Deduplication - Study Content

Here are the extracted sections:

**DEFINITIONS & KEY TERMS**

* **Jaccard Coefficient**: A measure of similarity between two sets, defined as the size of their intersection divided by the size of their union.
* **Hamming Distance**: The number of positions at which two strings differ in a sequence alignment.
* **SimHash**: A type of hash function that produces similar outputs for similar inputs, used to estimate similarity between documents.
* **Fingerprint**: A compact representation of a document's content, often used for similarity search and clustering.
* **Permutation**: An arrangement of objects in a specific order, used to preserve Hamming distance.

**ALGORITHMS & PROCESSES**

1. **SimHash Algorithm**
	* Step-by-step breakdown:
		+ Break input phrase into shingles
		+ Hash each feature using a normal 32-bit hash algorithm (MD5 or SHA)
		+ For each hash, if bit is set, add 1 to V[i], otherwise subtract 1 from V[i]
		+ Simhash bit is 1 if V[i] > 0 and 0 otherwise
	* When/why it's used: To estimate similarity between documents by producing similar outputs for similar inputs.
	* Key characteristics: Produces compact representation of document content, preserves Hamming distance.
2. **Permutation Algorithm**
	* Step-by-step breakdown:
		+ Rotate bits left and replace lowest order bit with the 'lost' highest order bit
	* When/why it's used: To preserve Hamming distance by permuting bits.
	* Key characteristics: Preserves Hamming distance, produces new fingerprints.

**FORMULAS & CALCULATIONS**

1. **Jaccard Coefficient Formula**: J = |A ∩ B| / |A ∪ B|
	* What each variable means:
		+ A and B are the two sets being compared
		+ |A ∩ B| is the size of their intersection
		+ |A ∪ B| is the size of their union
2. **Hamming Distance Formula**: HD = number of positions at which two strings differ

**IMPORTANT FACTS & NUMBERS**

* Typical values for f and k: f=64, k=3 (for SimHash)
* Bitwise Hamming distance between similar items can be small.

**CORE CONCEPTS EXPLAINED**

* Similarity search: Finding documents that are similar to a given query document.
* Clustering: Grouping similar documents together based on their content.
* Permutation: An arrangement of objects in a specific order, used to preserve Hamming distance.

**EXAMPLES & APPLICATIONS**

* Document similarity search and clustering
* Estimating similarity between documents using SimHash