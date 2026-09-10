# CodeMentor AI — Viva Questions and Answers

1. **What is CodeMentor AI?**  
   It is an offline programming learning assistant using information retrieval.

2. **Is it a generative-AI system?**  
   No. It retrieves curated answers with TF-IDF and cosine similarity.

3. **What is NLP?**  
   Natural Language Processing helps software work with human language.

4. **What is a chatbot?**  
   A program that communicates with users through text or speech.

5. **How is this different from a basic chatbot?**  
   It supports six technologies, filters, related concepts, quizzes, history,
   and session statistics.

6. **What is a knowledge base?**  
   A structured collection of domain facts and answers.

7. **Why use a predefined knowledge base?**  
   It makes answers reliable, offline, explainable, and easy to test.

8. **What is information retrieval?**  
   Finding the most relevant item from a collection for a query.

9. **What is text preprocessing?**  
   Preparing text into a consistent form before comparison.

10. **Why convert text to lowercase?**  
    It prevents case differences from creating different features.

11. **What is tokenization?**  
    Splitting text into meaningful units called tokens.

12. **What are stopwords?**  
    Frequent words with little retrieval value, such as “the” or “what”.

13. **Why protect technical terms from stopword removal?**  
    Words such as `class`, `array`, and `database` carry programming meaning.

14. **What is lemmatization?**  
    Reducing related word forms to a base dictionary form.

15. **What is NLTK?**  
    A Python toolkit for natural-language processing.

16. **What is TF-IDF?**  
    A weighting method that emphasizes useful terms in documents.

17. **What does TF mean?**  
    Term frequency: how often a term occurs in a document.

18. **What does IDF mean?**  
    Inverse document frequency: it lowers the weight of terms common across documents.

19. **Why does IDF help?**  
    Common filler words become less important than distinctive topic terms.

20. **What is cosine similarity?**  
    A vector comparison based on the angle between two vectors.

21. **What is the range of cosine similarity here?**  
    For these non-negative TF-IDF vectors, it is normally from 0 to 1.

22. **What is the similarity threshold?**  
    The minimum score required before returning a match.

23. **Why is the learning threshold 0.30?**  
    It balances useful paraphrase matches with protection against unrelated answers.

24. **What happens below the threshold?**  
    The system explains that no relevant local concept was found.

25. **Which machine-learning technique is used?**  
    Classical vector-space information retrieval with TF-IDF.

26. **Why is it not deep learning?**  
    It does not train or use a neural network or transformer model.

27. **What is Tkinter?**  
    Python's standard library interface for the Tk GUI toolkit.

28. **Why choose Tkinter?**  
    It is local, lightweight, beginner-friendly, and usually bundled with Python.

29. **What is Pandas used for?**  
    It is listed for dataset inspection and future data analysis; core loading
    uses CSV validation directly to keep runtime simple.

30. **What is NumPy used for?**  
    It helps choose the best score from the similarity result array.

31. **What does Scikit-learn provide?**  
    `TfidfVectorizer` and `cosine_similarity`.

32. **How many dataset records are included?**  
    150, with 25 for each of six technologies.

33. **What fields does each record contain?**  
    ID, question, answer, language, category, difficulty, keywords, and related topics.

34. **Which languages are supported?**  
    Python, Java, C, SQL, HTML/CSS, and JavaScript.

35. **Why include difficulty classification?**  
    It lets students practise at an appropriate level.

36. **How does language filtering work?**  
    Retrieval considers only records whose language matches the selected value.

37. **How does quiz mode work?**  
    It selects a filtered question and compares the user's explanation with the
    expected answer using TF-IDF and cosine similarity.

38. **What is the quiz threshold?**  
    0.35 by default.

39. **What does a correct quiz answer mean?**  
    Its text similarity reaches or exceeds the configured threshold.

40. **Is quiz scoring semantic or perfect marking?**  
    It is a simple, explainable lexical similarity score, not human marking.

41. **What is session history?**  
    A temporary list of matched questions asked during the current run.

42. **What statistics are displayed?**  
    Questions asked, concepts matched, quiz attempts, quiz correct, and average similarity.

43. **Are statistics invented?**  
    No. They are calculated from in-memory session events.

44. **What happens if the CSV is missing?**  
    The loader raises a meaningful knowledge-base error and the GUI shows it.

45. **What happens if input is empty?**  
    The search or quiz evaluator rejects it with a clear message.

46. **Why use relative paths?**  
    The project can be copied to another computer without editing source code.

47. **Why provide CSV and JSON?**  
    CSV is easy to inspect and edit; JSON is convenient for programmatic use.

48. **What is a limitation of TF-IDF?**  
    It depends on word overlap and may miss semantically similar wording.

49. **How could retrieval be improved later?**  
    Sentence embeddings or transformer-based semantic search could be added.

50. **What is the main future enhancement?**  
    A larger curated dataset combined with personalized learning recommendations.