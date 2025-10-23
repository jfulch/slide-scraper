#!/usr/bin/env python3
"""
Test script for specific question about web searches that involve database queries
"""

from course_qa_system import CourseQASystem

def test_specific_question():
    """Test the specific question about web searches and database queries"""
    
    # Initialize the QA system
    qa_system = CourseQASystem()
    
    # Build the content database
    print("Setting up QA system...")
    if not qa_system.extract_text_from_files():
        print("❌ No course content found!")
        return
    
    # Build embeddings
    qa_system.build_embeddings()
    
    # The specific question
    question = """Increasingly, the distinction between 'search' and 'database access' is becoming blurred - after all, the end-user doesn't care how the information they want is being retrieved.

What are three examples where searching (via a web browser) "actually" involves a database query/search? For each example, provide both of these: sample search query, what data might be retrieved to answer it."""

    print("="*80)
    print("TESTING SPECIFIC QUESTION")
    print("="*80)
    print(f"Question: {question}")
    print("="*80)
    
    # Get the answer
    result = qa_system.answer_question(question)
    
    print("ANSWER:")
    print("-"*80)
    print(result['answer'])
    print("-"*80)
    
    if result['has_context']:
        print(f"💡 Based on {result['sources_used']} relevant course content sections")
    else:
        print(f"⚠️  Answer not based on specific course content")
    
    print("\n" + "="*80)
    print("MANUAL ANSWER ATTEMPT")
    print("="*80)
    
    # Let's also try a more targeted approach
    manual_answer = """
Based on the course content, here are three examples where web browser searches actually involve database queries:

**Example 1: E-commerce Product Search**
- Sample search query: "iPhone 15 Pro 256GB black"
- Database query: The search engine queries product databases containing:
  - Product specifications (model, storage, color)
  - Inventory levels
  - Pricing information
  - Customer reviews and ratings
  - Retailer information

**Example 2: Academic Paper Search**
- Sample search query: "machine learning natural language processing 2024"
- Database query: The system searches academic databases containing:
  - Paper titles, abstracts, and keywords
  - Author information and affiliations
  - Publication dates and journals
  - Citation counts and references
  - Full-text content indexes

**Example 3: Real Estate Search**
- Sample search query: "3 bedroom house under $500k Los Angeles"
- Database query: The platform queries property databases with:
  - Property specifications (bedrooms, bathrooms, square footage)
  - Location data (address, neighborhood, zip code)
  - Price history and current listing prices
  - Property tax information
  - School district ratings

In each case, what appears to be a simple web search is actually a complex database query that:
1. Parses the user's natural language query
2. Translates it into structured database queries
3. Searches multiple related tables/indexes
4. Ranks and filters results
5. Presents them in a user-friendly format

The user doesn't see the underlying SQL queries, API calls, or database operations - they just see search results that appear to come from a simple search interface.
    """
    
    print(manual_answer)

if __name__ == "__main__":
    test_specific_question()