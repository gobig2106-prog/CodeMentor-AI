# CodeMentor AI — 12-Slide Presentation Content

## Slide 1 — Title

- CodeMentor AI
- Smart Programming Learning Assistant
- Offline NLP-based BCA mini project
- Student name, roll number, guide, institution

## Slide 2 — Introduction

- Students learn several programming technologies.
- Quick concept revision is useful during practice.
- CodeMentor AI gives focused explanations from a local knowledge base.

## Slide 3 — Problem statement

- Basic FAQ bots are narrow and answer-only.
- Students need topic, difficulty, related concepts, and practice.
- Internet or paid AI APIs are not suitable for every lab environment.

## Slide 4 — Objectives

- Support Python, Java, C, SQL, HTML/CSS, and JavaScript.
- Match natural-language questions with NLP.
- Add explainable quizzes and session analytics.
- Keep the application offline and beginner-friendly.

## Slide 5 — Existing system

- Static FAQ or single-language keyword chatbot.
- Exact wording often required.
- No score transparency, quiz mode, history, or difficulty filtering.

## Slide 6 — Proposed system

- 150 curated local records.
- Text preprocessing → TF-IDF → cosine similarity.
- Threshold protects against unrelated answers.
- Learning Mode and Quiz Mode share transparent retrieval ideas.

## Slide 7 — Features

- Six-language filters
- Three difficulty levels
- Related concepts
- Quiz answer evaluation
- Study history
- Learning statistics
- Dark Tkinter GUI

## Slide 8 — Architecture

- Student enters question.
- GUI sends text to preprocessing.
- TF-IDF and cosine similarity find the best record.
- Result is displayed and session state is updated.

## Slide 9 — Technologies

- Python 3
- Tkinter
- NLTK
- NumPy and Pandas
- Scikit-learn
- CSV / JSON
- unittest

## Slide 10 — Working demo

- Ask: “Explain inheritance in Java”.
- Show topic, language, difficulty, score, answer, and related concepts.
- Switch to Quiz Mode and submit an explanation.
- Open history to show actual session events.

## Slide 11 — Results and testing

- More than 25 automated tests.
- Tests cover all six technologies and filters.
- Empty, unknown, and invalid dataset cases are handled.
- Statistics are calculated from real session activity.

## Slide 12 — Conclusion and future enhancements

- A complete offline study assistant can be built with classical NLP.
- The design is modular and easy to explain in a viva.
- Future: voice, web/mobile UI, embeddings, larger dataset, login, cloud database.