# 📖 Web Crawling - Study Content

Here are the extracted sections:

**DEFINITIONS & KEY TERMS**

* **Crawler**: A program that systematically explores and indexes web pages.
* **Googlebot**: The name of Google's crawler.
* **Sitemap**: A list of a website's URLs, used to help search engines like Google understand its structure.
* **Uniform policy**: A re-visiting policy where all pages are revisited with the same frequency, regardless of their rates of change.
* **Proportional policy**: A re-visiting policy where pages that change more frequently are revisited more often.
* **Shadowing**: A technique where a new set of pages is collected and stored separately from the current index.
* **LastModified indicator**: A metadata attribute that indicates when a page was last modified.

**ALGORITHMS & PROCESSES**

1. **Uniform policy**
	* Step-by-step breakdown: Revisit all pages with the same frequency, regardless of their rates of change.
	* When/why it's used: To ensure that all pages are kept up-to-date, even if some change more frequently than others.
	* Key characteristics: Uniform frequency, no consideration for page rate of change.
2. **Proportional policy**
	* Step-by-step breakdown: Revisit pages that change more frequently more often.
	* When/why it's used: To prioritize revisiting pages that are changing rapidly.
	* Key characteristics: Frequency proportional to page rate of change.
3. **Shadowing**
	* Step-by-step breakdown: Collect and store a new set of pages separately from the current index.
	* When/why it's used: To update the index without disrupting ongoing queries.
	* Key characteristics: Separate storage, simultaneous update.

**FORMULAS & CALCULATIONS**

None mentioned in the slides.

**IMPORTANT FACTS & NUMBERS**

* Google uses multiple crawlers, including Googlebot Images, Googlebot News, and Googlebot Video.
* Google's sitemap format is represented in XML.
* The uniform policy outperforms the proportional policy in terms of average freshness.
* As of 2019, Googlebot runs the latest Chromium rendering engine.

**CORE CONCEPTS EXPLAINED**

* **Crawling**: A process where a program systematically explores and indexes web pages to build a search index.
* **Indexing**: The process of building a database of web page content for searching purposes.
* **Freshness**: The accuracy of the search results, which is affected by how often the crawler revisits pages.

**EXAMPLES & APPLICATIONS**

* Google's sitemap format is used on websites like example.com to help search engines understand their structure.
* Googlebot uses multiple machines located near the site being indexed to improve crawling speed and efficiency.