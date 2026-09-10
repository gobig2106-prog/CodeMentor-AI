# CodeMentor AI — Project Report

## 1. Title

**CodeMentor AI – Smart Programming Learning Assistant**

## 2. Abstract

CodeMentor AI is a local NLP-based programming learning assistant for students.
It supports Python, Java, C, SQL, HTML/CSS, and JavaScript. The user can ask a
natural-language question, choose filters, and receive the closest educational
record from a predefined programming knowledge base. The application uses text
preprocessing, TF-IDF vectorization, and cosine similarity. It also contains a
quiz module that evaluates free-text answers, a session history, and learning
statistics. This is an information-retrieval system; it is not a deep-learning
or generative-AI system.

## 3. Introduction

Programming students often need quick explanations while learning multiple
technologies. Searching for a concept can interrupt practice, while a simple
FAQ program may return an answer without showing topic, difficulty, or related
ideas. CodeMentor AI presents a focused local study desk that is easy to run,
inspect, and explain in a college viva.

## 4. Problem statement

Students need a reliable offline assistant that can identify programming
concepts from natural-language questions and help them practise understanding,
not only read an answer.

## 5. Objectives

1. Build a multi-language programming knowledge base.
2. Match questions using understandable NLP techniques.
3. Show educational metadata and related concepts.
4. Evaluate short quiz explanations with text similarity.
5. Track real session activity without invented statistics.
6. Provide a beginner-friendly desktop interface.

## 6. Existing system

The basic existing approach is a static FAQ or a single-language keyword
chatbot. It normally returns one response and does not include practice,
difficulty filtering, related topics, or learning analytics.

## 7. Limitations of existing system

- Narrow technology coverage.
- Exact keyword dependency.
- No explainable similarity score.
- No quiz evaluation.
- No progress or session summary.
- Often dependent on internet services.

## 8. Proposed system

CodeMentor AI stores curated records in CSV and JSON. The application validates
the dataset, preprocesses the questions, builds a TF-IDF matrix, compares the
student question with candidate records, applies a threshold, and presents a
structured study response. Quiz answers go through the same preprocessing idea
and are compared with the expected explanation.

## 9. Advantages

- Works offline after package installation.
- Uses six technologies.
- Simple and explainable algorithms.
- Supports filters and difficulty levels.
- Includes learning and practice modes.
- Uses relative paths and clear error messages.
- Easy to extend by adding validated records.

## 10. Hardware requirements

- Dual-core processor or better
- 4 GB RAM recommended
- 200 MB free storage
- Keyboard and display

## 11. Software requirements

- Python 3.10 or newer
- Tkinter
- Packages in `requirements.txt`
- Windows, macOS, or Linux

## 12. Technologies used

Python, Tkinter, NLTK, Pandas, NumPy, Scikit-learn, CSV, JSON, and unittest.

## 13. System architecture

The student uses the Tkinter GUI. Learning Mode sends a question to
preprocessing, TF-IDF, cosine similarity, threshold checking, and the local
knowledge base. Quiz Mode selects a filtered record and evaluates the answer.
Both modes update session state where appropriate. See `architecture.md` for
ASCII, Mermaid, flowchart, UML, and DFD representations.

## 14. Methodology

1. Load and validate the local CSV.
2. Normalize and tokenize questions.
3. Remove conversational stopwords while retaining technical terms.
4. Apply NLTK WordNet lemmatization when available.
5. Build a TF-IDF matrix from the knowledge-base questions.
6. Transform the student question into the same feature space.
7. Calculate cosine similarity.
8. Return the best result only when the configured threshold is reached.
9. Update history and show session statistics.

## 15. Dataset description

The dataset contains 150 records: 25 for each supported technology. Every
record includes `id`, `question`, `answer`, `language`, `category`,
`difficulty`, `keywords`, and `related_topics`. Topics include variables,
types, operators, control flow, functions, collections, object-oriented
programming, exceptions, files, databases, web development, asynchronous
programming, and security.

## 16. NLP preprocessing

- **Lowercase conversion:** makes `Python` and `python` comparable.
- **Punctuation handling:** removes noise while preserving useful symbols.
- **Extra-space removal:** gives the vectorizer consistent text.
- **Tokenization:** splits a question into word-like units.
- **Stopword handling:** removes filler such as “what” and “the”.
- **Technical-word protection:** keeps terms such as `class`, `array`, and
  `database`.
- **Lemmatization:** reduces simple word variations when the NLTK resource is
  available. A safe local fallback keeps the application runnable without a
  download.

## 17. TF-IDF

For term `t` in document `d`, TF-IDF is:

```text
tfidf(t, d) = tf(t, d) × idf(t)
idf(t) = log((1 + N) / (1 + df(t))) + 1
```

`tf` measures how often a term occurs in a question. `df` is the number of
questions containing the term, and `N` is the number of questions. Common words
receive less weight, while useful concept words receive more weight.

## 18. Cosine similarity

Cosine similarity compares two vectors by their angle:

```text
cosine(A, B) = (A · B) / (||A|| × ||B||)
```

A score near 1 indicates similar direction. CodeMentor uses a default learning
threshold of `0.30` and a quiz threshold of `0.35`.

## 19. Question matching

The search applies the selected language and difficulty filters, transforms the
question, calculates cosine scores against the candidate matrix, and chooses
the maximum. A low score returns a safe unmatched message rather than an
unrelated answer.

## 20. Quiz module

The quiz selects one record from the active filters. The student writes an
explanation. The expected and submitted answers are preprocessed, vectorized,
and compared. Scores at or above the quiz threshold are marked **Correct**;
lower scores are marked **Needs Improvement**. The expected answer is shown so
the student can learn from the result.

## 21. History module

The current session stores matched learning questions, language, topic, and
similarity score in memory. A Clear session button removes this temporary data.
No personal account or cloud storage is required.

## 22. Statistics module

The interface calculates questions asked, concepts matched, quiz attempts,
quiz correct, and average similarity from `SessionHistory`. Unknown questions
are not counted as matched.

## 23. GUI design

The GUI has a dark study-desk theme, a filter sidebar, two working tabs, answer
scrolling, quick example buttons, a history window, and session pulse values.
The layout uses standard Tkinter and ttk widgets, so no browser or server is
needed.

## 24. Algorithm A — question answering

1. Receive question and filters.
2. Reject empty input.
3. Normalize, tokenize, remove safe stopwords, and lemmatize.
4. Transform the question with the fitted TF-IDF vectorizer.
5. Select records matching language and difficulty.
6. Calculate cosine similarity for every candidate.
7. Select the highest score.
8. If the score is below `0.30`, return the unmatched message.
9. Otherwise return answer, metadata, score, and related topics.
10. Add the matched question to session history.

## 25. Algorithm B — quiz evaluation

1. Select a record using active filters.
2. Receive the student's non-empty answer.
3. Preprocess expected and submitted answers.
4. Create a two-document TF-IDF matrix.
5. Calculate cosine similarity.
6. Compare score with `0.35`.
7. Display score, verdict, and expected answer.
8. Update quiz attempts and correct count.

## 26. Flowchart

See `architecture.md` for Mermaid syntax. The flow is Start → Load Dataset →
Validate → Preprocess → TF-IDF Matrix → Launch GUI → Select Mode → Process
Input → Similarity → Display Result → Update Session → Continue or Exit.

## 27. DFD

The Level 0 DFD has Student → CodeMentor AI → Response/Quiz Result, with the
knowledge base as the system's local data store. Level 1 decomposes the system
into GUI input, preprocessing, similarity processing, learning/quiz output,
and session statistics.

## 28. UML

The Student actor can ask questions, select filters, receive explanations,
view related concepts, take and submit quizzes, view history, view statistics,
clear the session, and exit. The use-case Mermaid representation is in
`architecture.md`.

## 29. Implementation

The code is separated into preprocessing, knowledge-base retrieval, learning
orchestration, quiz evaluation, history, GUI, and the `app.py` entry point.
The dataset and all paths are relative to the project folder.

## 30. Testing

The unittest suite contains more than 25 test methods. It checks preprocessing,
exact and paraphrased questions, case handling, unknown and empty input, all
six technologies, filters, dataset validation, quiz outcomes, history, and
statistics. The command is:

```bash
python -m unittest discover -s tests -v
```

## 31. Results

When executed, the app provides deterministic offline retrieval over the
bundled records, score transparency, filtered practice questions, and actual
session counters. Exact test counts and results should be reported from the
command output on the machine where the project is demonstrated.

## 32. Limitations

TF-IDF measures word overlap and does not perform deep semantic understanding.
The knowledge base is finite. Session statistics are intentionally temporary.
The optional NLTK lemmatizer depends on a local resource; the fallback keeps
the core app working without internet access.

## 33. Applications

- Classroom programming revision
- BCA mini-project demonstrations
- Offline lab practice
- Viva preparation
- Concept discovery across languages

## 34. Future enhancements

Voice input, text-to-speech, a web app, mobile app, deep learning, transformers,
sentence embeddings, a larger dataset, user login, cloud database, and
personalized recommendations are future work only.

## 35. Conclusion

CodeMentor AI demonstrates how classical NLP and information retrieval can
create a useful educational tool without paid APIs or generative models. Its
modular design is simple enough for a student to explain and strong enough to
show a complete software project workflow.

## 36. References

1. Python Documentation — https://docs.python.org/3/
2. Scikit-learn User Guide — https://scikit-learn.org/stable/user_guide.html
3. NLTK Documentation — https://www.nltk.org/
4. Tkinter Documentation — https://docs.python.org/3/library/tkinter.html
5. Manning, Raghavan, Schütze, *Introduction to Information Retrieval*