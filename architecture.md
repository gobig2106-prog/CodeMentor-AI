# CodeMentor AI — Architecture Notes

## ASCII architecture

```text
Student
  |
  v
Tkinter GUI
  |
  +--> Learning Mode --> Preprocessing --> TF-IDF --> Cosine Similarity
  |                                      |              |
  |                                      +--------------v
  |                                             Best match + threshold
  |                                                     |
  |                                                     v
  |                                           Local programming KB
  |                                                     |
  |                                                     v
  |                                      Educational response + related topics
  |
  +--> Quiz Mode --> Question selection --> Answer preprocessing
                                           --> TF-IDF + cosine similarity
                                           --> Result + score
  |
  +--> Session history and statistics
```

## Mermaid architecture

```mermaid
flowchart TD
  User[Student] --> GUI[Tkinter GUI]
  GUI --> Mode{Mode selection}
  Mode --> Learn[Learning mode]
  Learn --> Prep[Text preprocessing]
  Prep --> TFIDF[TF-IDF vectorization]
  TFIDF --> Cosine[Cosine similarity]
  Cosine --> Threshold{Score >= threshold?}
  Threshold -->|Yes| KB[Local knowledge base]
  KB --> Response[Answer, metadata, related topics]
  Threshold -->|No| Unknown[Helpful unmatched message]
  Mode --> Quiz[Quiz mode]
  Quiz --> Pick[Filtered question selection]
  Pick --> Evaluate[TF-IDF answer evaluation]
  Evaluate --> Result[Correct / Needs Improvement + score]
  Response --> Session[Session history and statistics]
  Result --> Session
```

## Flowchart

```mermaid
flowchart TD
  Start([Start]) --> Load[Load CSV dataset]
  Load --> Validate[Validate columns and records]
  Validate --> Prep[Preprocess knowledge-base questions]
  Prep --> Matrix[Create TF-IDF matrix]
  Matrix --> GUI[Launch GUI]
  GUI --> Select[Select learning or quiz mode]
  Select --> Input[Process user input]
  Input --> Similarity[Calculate cosine similarity]
  Similarity --> Display[Display result]
  Display --> Update[Update history and statistics]
  Update --> Continue{Continue?}
  Continue -->|Yes| Select
  Continue -->|No| Exit([Exit])
```

## UML / use case

```mermaid
flowchart LR
  Student((Student))
  Student --- Ask[Ask programming question]
  Student --- Language[Select programming language]
  Student --- Difficulty[Select difficulty]
  Student --- Explanation[Receive explanation]
  Student --- Related[View related topics]
  Student --- Quiz[Take quiz]
  Student --- Submit[Submit quiz answer]
  Student --- History[View history]
  Student --- Stats[View statistics]
  Student --- Clear[Clear history]
  Student --- Exit[Exit application]
```

## Data flow diagrams

### Level 0

```text
Student --> [CodeMentor AI] --> Response / Quiz Result
                 ^
                 |
       Local Knowledge Base
```

### Level 1

```text
Student
  |
  v
1. GUI input and filters
  |
  v
2. Text preprocessing <--> local stopwords / optional NLTK lemmatizer
  |
  v
3. TF-IDF + cosine similarity <--> programming_qa.csv
  |
  +--> 4a. Learning response
  |
  +--> 4b. Quiz evaluation
  |
  v
5. Session history and statistics
  |
  v
Student
```