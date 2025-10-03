import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import Counter
import math
import re


class TextEntropyAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор энтропии текста")
        self.root.geometry("1200x800")

        self.text_content = ""
        self.char_frequencies = {}
        self.probabilities = {}
        self.entropy = 0

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # File selection
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(file_frame, text="Выберите файл:").grid(row=0, column=0, sticky=tk.W)
        self.file_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Обзор", command=self.browse_file).grid(row=0, column=2, padx=5)
        ttk.Button(file_frame, text="Анализировать", command=self.analyze_text).grid(row=0, column=3, padx=5)

        # Results frame
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        # Entropy result
        entropy_frame = ttk.LabelFrame(results_frame, text="Результаты энтропии", padding="10")
        entropy_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), padx=5, pady=5)

        self.entropy_label = ttk.Label(entropy_frame, text="Энтропия: -")
        self.entropy_label.pack()

        self.total_chars_label = ttk.Label(entropy_frame, text="Всего символов: 0")
        self.total_chars_label.pack()

        self.unique_chars_label = ttk.Label(entropy_frame, text="Уникальных символов: 0")
        self.unique_chars_label.pack()

        # Frequency table
        table_frame = ttk.LabelFrame(results_frame, text="Таблица частот", padding="10")
        table_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # Create treeview for frequency table
        columns = ('char', 'count', 'probability')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)

        self.tree.heading('char', text='Символ')
        self.tree.heading('count', text='Количество')
        self.tree.heading('probability', text='Вероятность')

        self.tree.column('char', width=100)
        self.tree.column('count', width=100)
        self.tree.column('probability', width=100)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Chart options
        chart_frame = ttk.LabelFrame(results_frame, text="Гистограммы", padding="10")
        chart_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Button(chart_frame, text="Полная гистограмма",
                   command=lambda: self.show_histogram('full')).grid(row=0, column=0, padx=5)
        ttk.Button(chart_frame, text="Топ 20 символов",
                   command=lambda: self.show_histogram('top20')).grid(row=0, column=1, padx=5)
        ttk.Button(chart_frame, text="По категориям",
                   command=self.show_categorical_histograms).grid(row=0, column=2, padx=5)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.columnconfigure(1, weight=1)
        results_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)

    def clean_text(self, text):
        # Удаляем указанные специальные символы
        chars_to_remove = r'[@#$^&*{}\[\]<>/\\|=+`]'
        cleaned_text = re.sub(chars_to_remove, '', text)
        return cleaned_text

    def categorize_char(self, char):
        """Категоризация символов"""
        if char.isspace():
            return 'Пробельные'
        elif char.isdigit():
            return 'Цифры'
        elif char in '.,!?;:"\'()-':
            return 'Знаки препинания'
        elif '\u0400' <= char <= '\u04FF':  # Кириллица
            return 'Кириллица'
        elif char.isalpha():  # Латиница
            return 'Латиница'
        else:
            return 'Другие'

    def analyze_text(self):
        try:
            with open(self.file_path.get(), 'r', encoding='utf-8') as file:
                text = file.read()

            # Очищаем текст
            cleaned_text = self.clean_text(text)
            self.text_content = cleaned_text

            # Подсчитываем частоты
            total_chars = len(cleaned_text)
            char_counter = Counter(cleaned_text)

            # Рассчитываем вероятности и энтропию
            self.char_frequencies = dict(char_counter)
            self.probabilities = {char: count / total_chars for char, count in char_counter.items()}

            # Вычисляем энтропию
            self.entropy = 0
            for prob in self.probabilities.values():
                if prob > 0:
                    self.entropy -= prob * math.log2(prob)

            # Обновляем интерфейс
            self.update_ui(total_chars, len(char_counter))

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {str(e)}")

    def update_ui(self, total_chars, unique_chars):
        # Обновляем метки
        self.entropy_label.config(text=f"Энтропия: {self.entropy:.4f} бит/символ")
        self.total_chars_label.config(text=f"Всего символов: {total_chars}")
        self.unique_chars_label.config(text=f"Уникальных символов: {unique_chars}")

        # Обновляем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Сортируем символы по частоте
        sorted_chars = sorted(self.probabilities.items(), key=lambda x: x[1], reverse=True)

        for char, prob in sorted_chars:
            count = self.char_frequencies[char]
            display_char = repr(char)[1:-1]  # Для отображения специальных символов
            self.tree.insert('', 'end', values=(display_char, count, f"{prob:.6f}"))

    def show_histogram(self, mode):
        if not self.probabilities:
            messagebox.showwarning("Предупреждение", "Сначала проанализируйте текст!")
            return

        fig, ax = plt.subplots(figsize=(12, 6))

        if mode == 'full':
            # Полная гистограмма
            chars = list(self.probabilities.keys())
            probs = list(self.probabilities.values())

            # Для лучшего отображения используем repr
            display_chars = [repr(char)[1:-1] for char in chars]

            ax.bar(display_chars, probs)
            ax.set_title('Полное распределение вероятностей символов')
            ax.set_xlabel('Символы')
            ax.set_ylabel('Вероятность')
            plt.xticks(rotation=45, ha='right')

        else:  # top20
            # Топ 20 символов
            sorted_probs = sorted(self.probabilities.items(), key=lambda x: x[1], reverse=True)[:20]
            chars = [item[0] for item in sorted_probs]
            probs = [item[1] for item in sorted_probs]

            display_chars = [repr(char)[1:-1] for char in chars]

            ax.bar(display_chars, probs)
            ax.set_title('Топ 20 наиболее частых символов')
            ax.set_xlabel('Символы')
            ax.set_ylabel('Вероятность')
            plt.xticks(rotation=45, ha='right')

        plt.tight_layout()

        # Показываем в отдельном окне
        chart_window = tk.Toplevel(self.root)
        chart_window.title(f"Гистограмма - {mode}")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_categorical_histograms(self):
        if not self.probabilities:
            messagebox.showwarning("Предупреждение", "Сначала проанализируйте текст!")
            return

        # Группируем символы по категориям
        categories = {
            'Кириллица': {},
            'Латиница': {},
            'Цифры': {},
            'Знаки препинания': {},
            'Пробельные': {},
            'Другие': {}
        }

        for char, prob in self.probabilities.items():
            category = self.categorize_char(char)
            categories[category][char] = prob

        # Создаем subplots
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()

        for i, (category, chars_probs) in enumerate(categories.items()):
            if chars_probs:
                sorted_probs = sorted(chars_probs.items(), key=lambda x: x[1], reverse=True)
                chars = [item[0] for item in sorted_probs]
                probs = [item[1] for item in sorted_probs]

                display_chars = [repr(char)[1:-1] for char in chars]

                axes[i].bar(display_chars, probs)
                axes[i].set_title(f'{category} ({len(chars_probs)} символов)')
                axes[i].set_xlabel('Символы')
                axes[i].set_ylabel('Вероятность')
                axes[i].tick_params(axis='x', rotation=45)

        plt.tight_layout()

        # Показываем в отдельном окне
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Гистограммы по категориям")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def main():
    root = tk.Tk()
    app = TextEntropyAnalyzer(root)
    root.mainloop()


if __name__ == "__main__":
    main()