# 📖 Youtube - Study Content

Here are the extracted sections:

**DEFINITIONS & KEY TERMS**

* **Content ID**: A system for spotting copyrighted content on YouTube
* **Fingerprint database**: A database of reference files used by Content ID to identify copyrighted content
* **Spectrogram**: A time-frequency graph used to create an acoustic fingerprint
* **Acoustic fingerprint**: A unique digital signature created from audio samples
* **Hash function**: An algorithm that creates a unique digital signature from data
* **Finite-state transducers**: A type of algorithm used by YouTube to compute the hash function
* **Kryder's Law**: The observation that the cost of storing 1GB of data has decreased exponentially over time
* **PetaByte (PB)**: A unit of measurement for digital storage, equivalent to 1,000 Terabytes (TB)
* **Content Delivery Network (CDN)**: A system for distributing content across multiple servers to improve performance and availability

**ALGORITHMS & PROCESSES**

* **Content ID process**:
	+ Step-by-step breakdown:
		- Upload a video
		- Transcode the video into multiple formats
		- Calculate an acoustic fingerprint from audio samples
		- Compare the fingerprint to reference files in the fingerprint database
	+ When/why it's used: To identify copyrighted content on YouTube
	+ Key characteristics: Uses spectrograms and hash functions to create a unique digital signature
* **Hash function**:
	+ Step-by-step breakdown: Not explicitly mentioned, but described as using finite-state transducers
	+ When/why it's used: To create a unique digital signature from data
	+ Key characteristics: Proprietary algorithm used by YouTube

**FORMULAS & CALCULATIONS**

* **Kryder's Law**: The cost of storing 1GB of data has decreased exponentially over time, with the exact rate not explicitly mentioned.
* **Storage needs calculation**:
	+ Formula: Storage needs = (Number of videos) x (Average video size) x (Number of profiles)
	+ Variables:
		- Number of videos: 1 billion
		- Average video size: 86MB
		- Number of profiles: 4
	+ Example calculation: 320PB

**IMPORTANT FACTS & NUMBERS**

* **YouTube storage needs**: Estimated to be at least 320PB, with a growth rate of 35 PB per year
* **Number of videos uploaded to YouTube**: Approximately 1 billion
* **Average video size**: Approximately 86MB
* **Cost of storing 1GB of data**: Has decreased exponentially over time, according to Kryder's Law

**CORE CONCEPTS EXPLAINED**

* **Content ID**: A system for identifying copyrighted content on YouTube using acoustic fingerprints and hash functions.
* **Acoustic fingerprint**: A unique digital signature created from audio samples used to identify copyrighted content.
* **Hash function**: An algorithm that creates a unique digital signature from data, used by Content ID to compare with reference files.

**EXAMPLES & APPLICATIONS**

* **YouTube's use of Content ID**: To identify and remove copyrighted content from the platform
* **Real-world example of Kryder's Law**: The decreasing cost of storing 1GB of data over time has enabled YouTube to store a vast library of videos.