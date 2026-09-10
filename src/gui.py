"""Modern dark Tkinter interface for CodeMentor AI."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from .chatbot import CodeMentorAssistant
from .history import SessionHistory
from .knowledge_base import KnowledgeBase, KnowledgeRecord
from .quiz import QuizEngine, QuizResult


class CodeMentorGUI:
    """Desktop study workspace with learning, quiz, history, and statistics."""

    BG = "#0b1020"
    PANEL = "#121a2d"
    PANEL_2 = "#19233a"
    TEXT = "#eef4ff"
    MUTED = "#91a1bd"
    ACCENT = "#6ee7d8"
    ACCENT_DARK = "#103d43"
    PURPLE = "#a78bfa"
    DANGER = "#fb7185"

    def __init__(self, root: tk.Tk, knowledge_base: KnowledgeBase) -> None:
        self.root = root
        self.kb = knowledge_base
        self.assistant = CodeMentorAssistant(knowledge_base)
        self.quiz = QuizEngine(knowledge_base)
        self.history = SessionHistory()
        self.current_quiz: KnowledgeRecord | None = None
        self.last_quiz_result: QuizResult | None = None
        self._configure_window()
        self._build_style()
        self._build_layout()
        self._update_stats()

    def _configure_window(self) -> None:
        self.root.title("CodeMentor AI — Programming Learning Assistant")
        self.root.geometry("1240x800")
        self.root.minsize(980, 650)
        self.root.configure(bg=self.BG)

    def _build_style(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(".", background=self.PANEL, foreground=self.TEXT, font=("Segoe UI", 10))
        style.configure("TFrame", background=self.PANEL)
        style.configure("TLabel", background=self.PANEL, foreground=self.TEXT)
        style.configure("Muted.TLabel", foreground=self.MUTED, font=("Segoe UI", 9))
        style.configure("Title.TLabel", background=self.BG, foreground=self.TEXT,
                        font=("Segoe UI", 26, "bold"))
        style.configure("Subtitle.TLabel", background=self.BG, foreground=self.MUTED,
                        font=("Segoe UI", 11))
        style.configure("Section.TLabel", foreground=self.ACCENT, font=("Segoe UI", 11, "bold"))
        style.configure("Accent.TButton", background=self.ACCENT, foreground="#07151c",
                        padding=(16, 10), font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#a7f3d0")])
        style.configure("Ghost.TButton", background=self.PANEL_2, foreground=self.TEXT,
                        padding=(12, 8))
        style.map("Ghost.TButton", background=[("active", "#263554")])
        style.configure("Stat.TLabel", background=self.PANEL_2, foreground=self.TEXT,
                        font=("Segoe UI", 15, "bold"))
        style.configure("TCombobox", fieldbackground=self.PANEL_2, background=self.PANEL_2,
                        foreground=self.TEXT, arrowcolor=self.ACCENT)
        style.configure(
            "Question.TEntry",
            fieldbackground="#f7f9fc",
            foreground="#101827",
            bordercolor=self.ACCENT,
            lightcolor=self.ACCENT,
            darkcolor=self.ACCENT,
        )
        style.configure(
            "Dataset.Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#101827",
            rowheight=26,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Dataset.Treeview.Heading",
            background=self.ACCENT_DARK,
            foreground=self.TEXT,
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Dataset.Treeview",
            background=[("selected", "#b7f7ef")],
            foreground=[("selected", "#101827")],
        )
        style.configure("Horizontal.TProgressbar", troughcolor=self.PANEL_2,
                        background=self.ACCENT, bordercolor=self.PANEL_2)

    def _build_layout(self) -> None:
        header = ttk.Frame(self.root, padding=(28, 24, 28, 18))
        header.pack(fill="x")
        header.configure(style="TFrame")
        ttk.Label(header, text="CodeMentor AI", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Your offline programming study desk  ·  retrieve, understand, practice",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        body = ttk.Frame(self.root, padding=(28, 0, 28, 24))
        body.pack(fill="both", expand=True)
        sidebar = ttk.Frame(body, padding=(0, 0, 20, 0), width=250)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        workspace = ttk.Frame(body)
        workspace.pack(side="left", fill="both", expand=True)
        self._build_sidebar(sidebar)
        self._build_workspace(workspace)

    def _build_sidebar(self, sidebar: ttk.Frame) -> None:
        filters = ttk.LabelFrame(sidebar, text="  Study filters  ", padding=14)
        filters.pack(fill="x")
        ttk.Label(filters, text="Language", style="Muted.TLabel").pack(anchor="w")
        self.language_var = tk.StringVar(value="All Languages")
        self.language_box = ttk.Combobox(
            filters, textvariable=self.language_var, state="readonly",
            values=("All Languages", "Python", "Java", "C", "SQL", "HTML/CSS", "JavaScript"),
        )
        self.language_box.pack(fill="x", pady=(5, 14))
        self.language_box.bind("<<ComboboxSelected>>", lambda _event: self._refresh_quiz())
        ttk.Label(filters, text="Difficulty", style="Muted.TLabel").pack(anchor="w")
        self.difficulty_var = tk.StringVar(value="All Levels")
        self.difficulty_box = ttk.Combobox(
            filters, textvariable=self.difficulty_var, state="readonly",
            values=("All Levels", "Beginner", "Intermediate", "Advanced"),
        )
        self.difficulty_box.pack(fill="x", pady=(5, 0))
        self.difficulty_box.bind("<<ComboboxSelected>>", lambda _event: self._refresh_quiz())

        stats = ttk.LabelFrame(sidebar, text="  Session pulse  ", padding=14)
        stats.pack(fill="x", pady=16)
        self.stat_labels: dict[str, ttk.Label] = {}
        stat_names = [
            ("asked", "Questions asked"),
            ("matched", "Concepts matched"),
            ("attempts", "Quiz attempts"),
            ("correct", "Quiz correct"),
            ("average", "Average similarity"),
        ]
        for key, caption in stat_names:
            row = ttk.Frame(stats)
            row.pack(fill="x", pady=5)
            ttk.Label(row, text=caption, style="Muted.TLabel").pack(side="left")
            label = ttk.Label(row, text="0", style="Stat.TLabel")
            label.pack(side="right")
            self.stat_labels[key] = label

        ttk.Button(sidebar, text="View study history", style="Ghost.TButton",
                   command=self._show_history).pack(fill="x", pady=(4, 8))
        ttk.Button(sidebar, text="Browse 150 concepts", style="Ghost.TButton",
                   command=self._show_dataset).pack(fill="x", pady=(0, 8))
        ttk.Button(sidebar, text="Clear session", style="Ghost.TButton",
                   command=self._clear_session).pack(fill="x")
        ttk.Label(
            sidebar,
            text="150 local concepts\nNo API key · no internet required",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(20, 0))

    def _build_workspace(self, workspace: ttk.Frame) -> None:
        tabs = ttk.Notebook(workspace)
        tabs.pack(fill="both", expand=True)
        self.learn_tab = ttk.Frame(tabs, padding=18)
        self.quiz_tab = ttk.Frame(tabs, padding=18)
        tabs.add(self.learn_tab, text="  Learn a concept  ")
        tabs.add(self.quiz_tab, text="  Practice quiz  ")
        self._build_learn_tab()
        self._build_quiz_tab()

    def _build_learn_tab(self) -> None:
        ttk.Label(self.learn_tab, text="Ask in your own words", style="Section.TLabel").pack(anchor="w")
        ttk.Label(
            self.learn_tab,
            text="CodeMentor finds the closest concept, then shows why it matched.",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(3, 10))
        input_row = ttk.Frame(self.learn_tab)
        input_row.pack(fill="x")
        self.question_var = tk.StringVar()
        # Use a classic Entry here instead of relying on platform-specific
        # ttk foreground rendering. This guarantees typed text is visible on
        # Windows themes that ignore ttk.Entry foreground styling.
        question_entry = tk.Entry(
            input_row,
            textvariable=self.question_var,
            bg="#f7f9fc",
            fg="#101827",
            insertbackground="#101827",
            selectbackground="#b7f7ef",
            selectforeground="#101827",
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.ACCENT,
            highlightcolor=self.ACCENT,
            font=("Segoe UI", 12),
        )
        question_entry.pack(side="left", fill="x", expand=True, ipady=9)
        question_entry.bind("<Return>", lambda _event: self._ask_question())
        ttk.Button(input_row, text="Find concept", style="Accent.TButton",
                   command=self._ask_question).pack(side="left", padx=(10, 0))
        examples = ttk.Frame(self.learn_tab)
        examples.pack(fill="x", pady=(10, 15))
        ttk.Label(
            examples,
            text="Quick examples (3 shortcuts — 150 concepts are available):",
            style="Muted.TLabel",
        ).pack(side="left")
        for text in ("What is a Python list?", "Explain Java inheritance", "How do SQL joins work?"):
            button = ttk.Button(examples, text=text, style="Ghost.TButton",
                                command=lambda value=text: self._use_example(value))
            button.pack(side="left", padx=(8, 0))

        answer_frame = ttk.LabelFrame(self.learn_tab, text="  Learning response  ", padding=16)
        answer_frame.pack(fill="both", expand=True)
        self.answer_text = tk.Text(
            answer_frame, wrap="word", bg=self.PANEL_2, fg=self.TEXT,
            insertbackground=self.ACCENT, relief="flat", padx=16, pady=14,
            font=("Segoe UI", 11), state="disabled",
        )
        scroll = ttk.Scrollbar(answer_frame, orient="vertical", command=self.answer_text.yview)
        self.answer_text.configure(yscrollcommand=scroll.set)
        self.answer_text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _build_quiz_tab(self) -> None:
        ttk.Label(self.quiz_tab, text="Practice by explaining", style="Section.TLabel").pack(anchor="w")
        ttk.Label(
            self.quiz_tab,
            text="Answers are evaluated with the same transparent text-similarity method.",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(3, 12))
        self.quiz_question = tk.StringVar(value="Press “New question” to begin a practice round.")
        question_card = tk.Label(
            self.quiz_tab, textvariable=self.quiz_question, justify="left", anchor="w",
            wraplength=760, bg=self.ACCENT_DARK, fg=self.TEXT, padx=18, pady=18,
            font=("Segoe UI", 13, "bold"),
        )
        question_card.pack(fill="x")
        ttk.Button(self.quiz_tab, text="New question", style="Ghost.TButton",
                   command=self._refresh_quiz).pack(anchor="w", pady=(12, 10))
        ttk.Label(self.quiz_tab, text="Your explanation", style="Muted.TLabel").pack(anchor="w")
        self.quiz_answer = tk.Text(
            self.quiz_tab, height=7, wrap="word", bg=self.PANEL_2, fg=self.TEXT,
            insertbackground=self.ACCENT, relief="flat", padx=12, pady=10,
            font=("Segoe UI", 11),
        )
        self.quiz_answer.pack(fill="x", pady=(5, 10))
        ttk.Button(self.quiz_tab, text="Evaluate answer", style="Accent.TButton",
                   command=self._evaluate_quiz).pack(anchor="w")
        self.quiz_result = tk.StringVar(value="")
        ttk.Label(self.quiz_tab, textvariable=self.quiz_result, justify="left",
                  wraplength=760).pack(anchor="w", pady=(18, 0))

    def _use_example(self, value: str) -> None:
        self.question_var.set(value)
        self._ask_question()

    def _ask_question(self) -> None:
        question = self.question_var.get().strip()
        if not question:
            messagebox.showinfo("Question needed", "Type a programming question first.")
            return
        try:
            response = self.assistant.ask(
                question, self.language_var.get(), self.difficulty_var.get()
            )
        except Exception as exc:
            messagebox.showerror("Learning error", str(exc))
            return
        self.history.add_question(question, response.match)
        self._write_answer(response.message)
        self._update_stats()

    def _write_answer(self, text: str) -> None:
        self.answer_text.configure(state="normal")
        self.answer_text.delete("1.0", "end")
        self.answer_text.insert("1.0", text)
        self.answer_text.configure(state="disabled")

    def _refresh_quiz(self) -> None:
        try:
            self.current_quiz = self.quiz.pick_question(
                self.language_var.get(), self.difficulty_var.get()
            )
            self.quiz_question.set(self.current_quiz.question)
            self.quiz_answer.delete("1.0", "end")
            self.quiz_result.set("")
        except ValueError as exc:
            self.current_quiz = None
            self.quiz_question.set(str(exc))

    def _evaluate_quiz(self) -> None:
        if self.current_quiz is None:
            self._refresh_quiz()
            return
        try:
            result = self.quiz.evaluate(self.current_quiz, self.quiz_answer.get("1.0", "end"))
        except ValueError as exc:
            messagebox.showinfo("Answer needed", str(exc))
            return
        self.last_quiz_result = result
        self.history.add_quiz_result(result)
        verdict = "CORRECT — strong explanation." if result.correct else "NEEDS IMPROVEMENT — compare with the expected idea."
        self.quiz_result.set(
            f"{verdict}\nSimilarity: {result.score:.2f}  ·  Quiz threshold: {self.quiz.threshold:.2f}\n\n"
            f"Expected answer:\n{result.expected_answer}"
        )
        self._update_stats()

    def _show_history(self) -> None:
        window = tk.Toplevel(self.root)
        window.title("Study history")
        window.geometry("760x420")
        window.configure(bg=self.BG)
        frame = ttk.Frame(window, padding=18)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Study history", style="Title.TLabel").pack(anchor="w")
        ttk.Label(frame, text="Matched learning questions from this session.",
                  style="Muted.TLabel").pack(anchor="w", pady=(4, 12))
        columns = ("question", "language", "topic", "score")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for column, heading, width in (
            ("question", "Question", 360), ("language", "Language", 110),
            ("topic", "Topic", 150), ("score", "Score", 70),
        ):
            tree.heading(column, text=heading)
            tree.column(column, width=width, anchor="w")
        for entry in reversed(self.history.entries):
            tree.insert("", "end", values=(entry.question, entry.language,
                                            entry.topic, f"{entry.similarity:.2f}"))
        tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def _show_dataset(self) -> None:
        """Show every local record, respecting the active sidebar filters."""
        window = tk.Toplevel(self.root)
        window.title("CodeMentor AI — Dataset browser")
        window.geometry("1060x560")
        window.minsize(820, 420)
        window.configure(bg=self.BG)
        window.transient(self.root)
        window.lift()
        window.focus_force()
        window.grab_set()
        frame = ttk.Frame(window, padding=18)
        frame.pack(fill="both", expand=True)
        filtered_indexes = self.kb.filter_records(
            self.language_var.get(), self.difficulty_var.get()
        )
        ttk.Label(frame, text="Programming concept dataset", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            frame,
            text=(
                f"Showing {len(filtered_indexes)} of {len(self.kb.records)} records. "
                "Double-click a question to use it in Learning Mode."
            ),
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(4, 12))
        columns = ("id", "question", "language", "category", "difficulty")
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=20,
            style="Dataset.Treeview",
        )
        for column, heading, width in (
            ("id", "ID", 55),
            ("question", "Question", 485),
            ("language", "Language", 125),
            ("category", "Category", 175),
            ("difficulty", "Difficulty", 110),
        ):
            tree.heading(column, text=heading)
            tree.column(column, width=width, anchor="w")
        record_by_id = {}
        for index in filtered_indexes:
            record = self.kb.records[index]
            record_by_id[str(record.id)] = record
            tree.insert(
                "",
                "end",
                iid=str(record.id),
                values=(
                    record.id,
                    record.question,
                    record.language,
                    record.category,
                    record.difficulty,
                ),
            )
        tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        def use_selected(_event=None) -> None:
            selected = tree.selection()
            if not selected:
                return
            record = record_by_id[selected[0]]
            self.question_var.set(record.question)
            self.learn_tab.focus_set()
            window.grab_release()
            window.destroy()
            self._ask_question()

        tree.bind("<Double-1>", use_selected)
        ttk.Button(
            frame,
            text="Close",
            style="Ghost.TButton",
            command=lambda: (window.grab_release(), window.destroy()),
        ).pack(anchor="e", pady=(12, 0))
        # On some Windows desktop configurations a newly-created Toplevel can
        # initially open behind its parent. Reassert visibility after layout.
        window.after(50, lambda: (window.lift(), window.focus_force()))

    def _clear_session(self) -> None:
        if messagebox.askyesno("Clear session", "Clear history and quiz statistics?"):
            self.history.clear()
            self._update_stats()

    def _update_stats(self) -> None:
        self.stat_labels["asked"].configure(text=str(self.history.questions_asked))
        self.stat_labels["matched"].configure(text=str(self.history.questions_matched))
        self.stat_labels["attempts"].configure(text=str(self.history.quiz_attempts))
        self.stat_labels["correct"].configure(text=str(self.history.quiz_correct))
        self.stat_labels["average"].configure(text=f"{self.history.average_similarity:.2f}")


def launch(csv_path: str | Path) -> None:
    """Load the local dataset and start the application."""
    try:
        knowledge_base = KnowledgeBase(csv_path)
    except Exception as exc:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("CodeMentor AI could not start", str(exc))
        root.destroy()
        raise
    root = tk.Tk()
    CodeMentorGUI(root, knowledge_base)
    root.mainloop()