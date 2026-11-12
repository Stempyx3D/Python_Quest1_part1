import csv
import math
import tkinter as tk
from datetime import datetime
from tkinter import ttk, filedialog, messagebox


FIELDS = ("id", "name", "category", "quantity", "price", "location", "created_at")
INPUTS = FIELDS[:-1]

class ValidationError(ValueError):
    def __init__(self, field, message):
        super().__init__(message)
        self.field = field

def make_item(data, created_at=None):
    item = {field: str(data.get(field, "")).strip() for field in INPUTS}
    if not item["id"]:
        raise ValidationError("id", "Введіть ID товару")

    for field in ("name", "category"):
        if not item[field]:
            raise ValidationError(field, "Поле не може бути порожнім")

    try:
        item["quantity"] = int(item["quantity"])
    except ValueError:
        raise ValidationError("quantity", "Потрібне ціле число")
    if item["quantity"] < 0:
        raise ValidationError("quantity", "Кількість не може бути від'ємною")

    try:
        item["price"] = float(item["price"].replace(" ", "").replace(",", "."))
    except ValueError:
        raise ValidationError("price", "Потрібне число")
    if not math.isfinite(item["price"]) or item["price"] < 0:
        raise ValidationError("price", "Ціна має бути невід'ємною")

    item["created_at"] = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return item

class CsvRepository:
    def __init__(self):
        self.items = {}
        self.path = None

    def all(self):
        return list(self.items.values())

    def get(self, item_id):
        return self.items.get(item_id)

    def add(self, item):
        self.items[item["id"]] = item

    def update(self, old_id, item):
        del self.items[old_id]
        self.add(item)

    def remove(self, item_id):
        del self.items[item_id]

    def load(self, path):
        items = {}
        with open(path, encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != list(FIELDS):
                raise ValueError("Неправильні заголовки CSV")
            for number, row in enumerate(reader, 2):
                if None in row or any(value is None for value in row.values()) or not row["id"].strip():
                    raise ValueError(f"Рядок {number}: некоректні дані")
                try:
                    item = make_item(row, row["created_at"])
                except ValidationError as error:
                    raise ValueError(f"Рядок {number}: {error}")
                if item["id"] in items:
                    raise ValueError(f"Рядок {number}: повторюється ID")
                items[item["id"]] = item
        self.items = items
        self.path = path

    def save(self, path):
        with open(path, "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(self.items.values())
        self.path = path

class InventoryWindow:
    def __init__(self, root, repo):
        self.root = root
        self.repo = repo
        self.selected = None
        self.sort_column = None
        self.reverse = False
        self.vars = {field: tk.StringVar() for field in INPUTS}
        self.search = tk.StringVar()
        self.status = tk.StringVar(value="Готово")
        self.entries = {}

        root.title("Облік товарів")
        root.geometry("1100x580")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Error.TEntry", fieldbackground="#ffd6d6")

        menu = tk.Menu(root)
        files = tk.Menu(menu, tearoff=False)
        files.add_command(label="Відкрити", command=self.open_file)
        files.add_command(label="Зберегти", command=self.save_file)
        files.add_command(label="Зберегти як", command=self.save_as)
        menu.add_cascade(label="Файл", menu=files)
        root.config(menu=menu)

        search_box = ttk.Frame(root, padding=12)
        search_box.grid(row=0, column=0, sticky="ew")
        search_box.columnconfigure(1, weight=1)
        ttk.Label(search_box, text="Пошук за назвою або категорією").grid(row=0, column=0, padx=(0, 12))
        ttk.Entry(search_box, textvariable=self.search).grid(row=0, column=1, sticky="ew")

        content = ttk.Frame(root, padding=12)
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)

        table = ttk.Frame(content)
        table.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        table.columnconfigure(0, weight=1)
        table.rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(table, columns=INPUTS, show="headings", selectmode="browse")
        for field in INPUTS:
            self.tree.heading(field, text=field, command=lambda c=field: self.sort_by(c))
            self.tree.column(field, width=110, minwidth=70)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        form = ttk.LabelFrame(content, text="Дані товару", padding=10)
        form.grid(row=0, column=1, sticky="n")
        for index, field in enumerate(INPUTS):
            ttk.Label(form, text=field).grid(row=index, column=0, sticky="w", pady=5)
            entry = ttk.Entry(form, textvariable=self.vars[field], width=24)
            entry.grid(row=index, column=1, padx=8, pady=5)
            self.entries[field] = entry

        for index, (title, action) in enumerate((
            ("Додати", self.add), ("Оновити", self.update),
            ("Видалити", self.delete), ("Очистити форму", self.clear)
        )):
            ttk.Button(form, text=title, command=action).grid(
                row=6 + index // 2, column=index % 2, sticky="ew", padx=3, pady=5
            )

        ttk.Label(root, textvariable=self.status, relief="sunken", anchor="w").grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 8))
        self.search.trace_add("write", lambda *_: self.refresh())

    def refresh(self):
        query = self.search.get().strip().lower()
        items = [item for item in self.repo.all()
                 if query in item["name"].lower() or query in item["category"].lower()]
        if self.sort_column:
            items.sort(key=lambda item: item[self.sort_column] if self.sort_column in ("quantity", "price")
                       else str(item[self.sort_column]).lower(), reverse=self.reverse)
        self.tree.delete(*self.tree.get_children())
        for item in items:
            self.tree.insert("", "end", iid=item["id"], values=[item[field] for field in INPUTS])
        if self.selected and self.tree.exists(self.selected):
            self.tree.selection_set(self.selected)

    def sort_by(self, column):
        self.reverse = not self.reverse if column == self.sort_column else False
        self.sort_column = column
        self.refresh()

    def on_select(self, event=None):
        selection = self.tree.selection()
        if selection:
            self.selected = selection[0]
            item = self.repo.get(self.selected)
            for field in INPUTS:
                self.vars[field].set(str(item[field]))
            self.status.set("Вибрано " + self.selected)

    def clear(self):
        self.selected = None
        for var in self.vars.values():
            var.set("")
        for entry in self.entries.values():
            entry.configure(style="TEntry")
        self.tree.selection_remove(self.tree.selection())
        self.status.set("Форму очищено")

    def save_item(self, update=False):
        if update and not self.selected:
            self.status.set("Спочатку виберіть товар")
            return
        for entry in self.entries.values():
            entry.configure(style="TEntry")
        data = {field: var.get() for field, var in self.vars.items()}
        old = self.repo.get(self.selected) if update else None
        try:
            item = make_item(data, old["created_at"] if old else None)
            if self.repo.get(item["id"]) and (not update or item["id"] != self.selected):
                raise ValidationError("id", "Цей ID вже існує")
        except ValidationError as error:
            self.entries[error.field].configure(style="Error.TEntry")
            self.entries[error.field].focus_set()
            self.status.set(str(error))
            return
        if update:
            self.repo.update(self.selected, item)
        else:
            self.repo.add(item)
        self.selected = item["id"]
        for field in INPUTS:
            self.vars[field].set(str(item[field]))
        self.refresh()
        self.status.set("Оновлено" if update else "Додано")

    def add(self):
        self.save_item()

    def update(self):
        self.save_item(update=True)

    def delete(self):
        if not self.selected:
            self.status.set("Спочатку виберіть товар")
            return
        if messagebox.askyesno("Підтвердження", "Видалити вибраний товар?"):
            self.repo.remove(self.selected)
            self.clear()
            self.refresh()
            self.status.set("Товар видалено")

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            try:
                self.repo.load(path)
            except (OSError, ValueError, csv.Error) as error:
                messagebox.showerror("Помилка", str(error))
                return
            self.clear()
            self.search.set("")
            self.refresh()
            self.status.set("Файл відкрито")

    def save_file(self):
        if self.repo.path:
            self.write_file(self.repo.path)
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            self.write_file(path)

    def write_file(self, path):
        try:
            self.repo.save(path)
            self.status.set("Файл збережено")
        except (OSError, csv.Error) as error:
            messagebox.showerror("Помилка", str(error))

if __name__ == "__main__":
    root = tk.Tk()
    InventoryWindow(root, CsvRepository())
    root.mainloop()