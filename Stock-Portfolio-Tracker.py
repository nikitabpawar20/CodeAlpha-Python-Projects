"""
╔══════════════════════════════════════════════════════════╗
║         📈 Stock Portfolio Tracker                        ║
║         Python Tkinter GUI Application                    ║
║         Uses only standard Python libraries               ║
╚══════════════════════════════════════════════════════════╝

How the program works:
─────────────────────
1. A hardcoded dictionary holds stock prices for 4 major stocks.
2. The user selects a stock from a dropdown and enters quantity.
3. Clicking "Add Stock" calculates value = quantity × price and
   displays the entry in a table (Treeview).
4. The Total Investment label auto-updates after every addition.
5. The portfolio can be exported as TXT or CSV, stocks can be
   removed individually, or the whole portfolio can be cleared.
6. A status bar at the bottom shows real-time feedback messages.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import datetime


# ──────────────────────────────────────────────────────────────
# HARDCODED STOCK PRICE DICTIONARY
# ──────────────────────────────────────────────────────────────
STOCK_PRICES = {
    "AAPL":  180,   # Apple Inc.
    "TSLA":  250,   # Tesla Inc.
    "GOOGL": 150,   # Alphabet Inc.
    "MSFT":  400,   # Microsoft Corp.
}

# ──────────────────────────────────────────────────────────────
# COLOR PALETTE  (dark professional theme)
# ──────────────────────────────────────────────────────────────
BG_DARK    = "#0D1117"   # main background
BG_CARD    = "#161B22"   # card / panel background
BG_ROW_ALT = "#1C2128"   # alternating table row
ACCENT     = "#58A6FF"   # blue accent
ACCENT2    = "#3FB950"   # green (positive values)
DANGER     = "#F85149"   # red (remove / errors)
WARN       = "#D29922"   # yellow (warnings)
FG_PRIMARY = "#E6EDF3"   # primary text
FG_MUTED   = "#8B949E"   # muted / secondary text
BORDER     = "#30363D"   # border / separator colour

FONT_TITLE  = ("Segoe UI", 18, "bold")
FONT_HEADER = ("Segoe UI", 10, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_TOTAL  = ("Segoe UI", 14, "bold")
FONT_STATUS = ("Segoe UI", 9)


# ══════════════════════════════════════════════════════════════
# MAIN APPLICATION CLASS
# ══════════════════════════════════════════════════════════════
class StockPortfolioTracker:
    """
    Main application class.
    Organises the window into distinct sections (frames) and
    wires all callbacks together.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self._configure_window()
        self._apply_styles()
        self._build_ui()

    # ──────────────────────────────────────────────────────────
    # WINDOW SETUP
    # ──────────────────────────────────────────────────────────
    def _configure_window(self):
        """Set title, size, background, and make resizable."""
        self.root.title("📈 Stock Portfolio Tracker")
        self.root.geometry("820x680")
        self.root.minsize(700, 580)
        self.root.configure(bg=BG_DARK)
        # Allow window columns/rows to stretch
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)

    # ──────────────────────────────────────────────────────────
    # TTK STYLE CONFIGURATION
    # ──────────────────────────────────────────────────────────
    def _apply_styles(self):
        """Apply a custom dark theme to all ttk widgets."""
        style = ttk.Style(self.root)
        style.theme_use("clam")          # closest to fully customisable

        # General frame / label background
        style.configure("TFrame",       background=BG_DARK)
        style.configure("Card.TFrame",  background=BG_CARD)
        style.configure("TLabel",       background=BG_DARK,
                        foreground=FG_PRIMARY, font=FONT_BODY)
        style.configure("Card.TLabel",  background=BG_CARD,
                        foreground=FG_PRIMARY, font=FONT_BODY)
        style.configure("Muted.TLabel", background=BG_CARD,
                        foreground=FG_MUTED,   font=FONT_SMALL)
        style.configure("Title.TLabel", background=BG_DARK,
                        foreground=FG_PRIMARY, font=FONT_TITLE)
        style.configure("Total.TLabel", background=BG_CARD,
                        foreground=ACCENT2,    font=FONT_TOTAL)

        # Separator
        style.configure("TSeparator", background=BORDER)

        # Combobox
        style.configure("TCombobox",
                        fieldbackground=BG_CARD,
                        background=BG_CARD,
                        foreground=FG_PRIMARY,
                        selectbackground=ACCENT,
                        selectforeground=FG_PRIMARY,
                        arrowcolor=ACCENT)
        style.map("TCombobox",
                  fieldbackground=[("readonly", BG_CARD)],
                  foreground=[("readonly", FG_PRIMARY)])

        # Entry
        style.configure("TEntry",
                        fieldbackground=BG_CARD,
                        foreground=FG_PRIMARY,
                        insertcolor=FG_PRIMARY,
                        bordercolor=BORDER,
                        lightcolor=BORDER,
                        darkcolor=BORDER)

        # Treeview (table)
        style.configure("Portfolio.Treeview",
                        background=BG_CARD,
                        foreground=FG_PRIMARY,
                        fieldbackground=BG_CARD,
                        rowheight=30,
                        font=FONT_BODY,
                        borderwidth=0)
        style.configure("Portfolio.Treeview.Heading",
                        background=BG_DARK,
                        foreground=ACCENT,
                        font=FONT_HEADER,
                        relief="flat",
                        borderwidth=0)
        style.map("Portfolio.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", BG_DARK)])
        style.map("Portfolio.Treeview.Heading",
                  background=[("active", BORDER)])

        # Scrollbar
        style.configure("TScrollbar",
                        background=BG_CARD,
                        troughcolor=BG_DARK,
                        arrowcolor=FG_MUTED,
                        bordercolor=BORDER)

        # Buttons — accent, danger, secondary
        for name, bg, fg, active_bg in [
            ("Accent.TButton",    ACCENT,  BG_DARK, "#79BFFF"),
            ("Danger.TButton",    DANGER,  "#FFF",  "#FF736B"),
            ("Secondary.TButton", BORDER,  FG_PRIMARY, "#444C56"),
            ("Green.TButton",     ACCENT2, BG_DARK, "#56D364"),
        ]:
            style.configure(name,
                            background=bg, foreground=fg,
                            font=FONT_HEADER, relief="flat",
                            borderwidth=0, padding=(10, 6))
            style.map(name,
                      background=[("active", active_bg),
                                  ("pressed", active_bg)],
                      foreground=[("active", fg)])

    # ──────────────────────────────────────────────────────────
    # UI CONSTRUCTION
    # ──────────────────────────────────────────────────────────
    def _build_ui(self):
        """Build all UI sections top-to-bottom."""
        # Root container
        container = ttk.Frame(self.root, style="TFrame", padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(2, weight=1)   # table row expands

        self._build_header(container)
        self._build_input_section(container)
        self._build_table_section(container)
        self._build_summary_section(container)
        self._build_action_buttons(container)
        self._build_status_bar()

    # ── Header ────────────────────────────────────────────────
    def _build_header(self, parent):
        """Title bar at the top."""
        hdr = ttk.Frame(parent, style="TFrame")
        hdr.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        ttk.Label(hdr, text="📈  Stock Portfolio Tracker",
                  style="Title.TLabel").pack(side="left")

        # Date/time badge
        now = datetime.datetime.now().strftime("%d %b %Y  %H:%M")
        ttk.Label(hdr, text=now,
                  style="Muted.TLabel",
                  background=BG_DARK).pack(side="right", pady=4)

    # ── Input Section ─────────────────────────────────────────
    def _build_input_section(self, parent):
        """Card with stock dropdown, quantity entry, and Add button."""
        card = ttk.Frame(parent, style="Card.TFrame", padding=14)
        card.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        card.columnconfigure((1, 3, 5), weight=1)

        # Section title
        ttk.Label(card, text="Add Stock", style="Card.TLabel",
                  font=FONT_HEADER,
                  foreground=ACCENT).grid(row=0, column=0,
                                          columnspan=6, sticky="w",
                                          pady=(0, 10))

        # Stock label + combobox
        ttk.Label(card, text="Stock Symbol", style="Card.TLabel",
                  foreground=FG_MUTED).grid(row=1, column=0,
                                             sticky="w", padx=(0, 6))
        self.stock_var = tk.StringVar()
        stock_combo = ttk.Combobox(card, textvariable=self.stock_var,
                                   values=list(STOCK_PRICES.keys()),
                                   state="readonly", width=12)
        stock_combo.grid(row=1, column=1, sticky="ew", padx=(0, 20))
        stock_combo.bind("<<ComboboxSelected>>", self._on_stock_select)

        # Price preview label
        ttk.Label(card, text="Price / Share",
                  style="Card.TLabel",
                  foreground=FG_MUTED).grid(row=1, column=2,
                                             sticky="w", padx=(0, 6))
        self.price_label = ttk.Label(card, text="—",
                                     style="Card.TLabel",
                                     foreground=ACCENT2, width=8)
        self.price_label.grid(row=1, column=3, sticky="ew", padx=(0, 20))

        # Quantity label + entry
        ttk.Label(card, text="Quantity",
                  style="Card.TLabel",
                  foreground=FG_MUTED).grid(row=1, column=4,
                                             sticky="w", padx=(0, 6))
        self.qty_var = tk.StringVar()
        qty_entry = ttk.Entry(card, textvariable=self.qty_var, width=10)
        qty_entry.grid(row=1, column=5, sticky="ew", padx=(0, 20))
        qty_entry.bind("<Return>", lambda e: self._add_stock())

        # Add Stock button
        ttk.Button(card, text="＋ Add Stock",
                   style="Accent.TButton",
                   command=self._add_stock).grid(row=1, column=6,
                                                  padx=(0, 0))

    # ── Table Section ─────────────────────────────────────────
    def _build_table_section(self, parent):
        """Treeview table that lists all portfolio entries."""
        card = ttk.Frame(parent, style="Card.TFrame", padding=14)
        card.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        card.columnconfigure(0, weight=1)
        card.rowconfigure(1, weight=1)

        ttk.Label(card, text="Portfolio Holdings",
                  style="Card.TLabel",
                  font=FONT_HEADER,
                  foreground=ACCENT).grid(row=0, column=0,
                                           sticky="w", pady=(0, 8))

        # Treeview + vertical scrollbar
        table_frame = ttk.Frame(card, style="Card.TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("stock", "qty", "price", "total")
        self.tree = ttk.Treeview(table_frame,
                                  columns=columns,
                                  show="headings",
                                  style="Portfolio.Treeview",
                                  selectmode="browse")

        # Column headers
        self.tree.heading("stock", text="Stock Name")
        self.tree.heading("qty",   text="Quantity")
        self.tree.heading("price", text="Price / Share ($)")
        self.tree.heading("total", text="Total Value ($)")

        # Column widths
        self.tree.column("stock", width=160, anchor="center")
        self.tree.column("qty",   width=100, anchor="center")
        self.tree.column("price", width=160, anchor="center")
        self.tree.column("total", width=160, anchor="center")

        # Alternating row tags
        self.tree.tag_configure("odd",  background=BG_CARD)
        self.tree.tag_configure("even", background=BG_ROW_ALT)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical",
                                   command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    # ── Summary Section ───────────────────────────────────────
    def _build_summary_section(self, parent):
        """Card showing the total investment value."""
        card = ttk.Frame(parent, style="Card.TFrame", padding=14)
        card.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        card.columnconfigure(1, weight=1)

        ttk.Label(card, text="💰  Total Investment Value",
                  style="Card.TLabel",
                  font=FONT_HEADER,
                  foreground=FG_MUTED).grid(row=0, column=0,
                                             sticky="w", padx=(0, 20))

        self.total_label = ttk.Label(card, text="$0.00",
                                      style="Total.TLabel")
        self.total_label.grid(row=0, column=1, sticky="w")

        # Holdings count badge
        self.holdings_label = ttk.Label(card, text="0 holdings",
                                         style="Muted.TLabel",
                                         background=BG_CARD)
        self.holdings_label.grid(row=0, column=2, sticky="e", padx=10)

    # ── Action Buttons ────────────────────────────────────────
    def _build_action_buttons(self, parent):
        """Row of action buttons: Save TXT, Save CSV, Remove, Clear."""
        btn_frame = ttk.Frame(parent, style="TFrame")
        btn_frame.grid(row=4, column=0, sticky="ew")

        buttons = [
            ("💾  Save as TXT",       "Secondary.TButton", self._save_txt),
            ("📊  Save as CSV",       "Secondary.TButton", self._save_csv),
            ("🗑   Remove Selected",  "Danger.TButton",    self._remove_selected),
            ("✖   Clear Portfolio",  "Danger.TButton",    self._clear_portfolio),
        ]

        for i, (text, style, cmd) in enumerate(buttons):
            ttk.Button(btn_frame, text=text,
                       style=style, command=cmd).grid(
                row=0, column=i, padx=(0 if i == 0 else 8, 0))

    # ── Status Bar ────────────────────────────────────────────
    def _build_status_bar(self):
        self.status_var = tk.StringVar(
        value="Ready — add a stock to begin."
        )
        
        status_frame = tk.Frame(
        self.root,
        bg=BG_DARK
        )
        
        status_frame.grid(
        row=1,
        column=0,
        sticky="ew"
        )
        
        status_frame.columnconfigure(0, weight=1)
        
        tk.Frame(
        status_frame,
        bg=BORDER,
        height=1
        
        ).grid(
            row=0,
            column=0,
            sticky="ew"
            )
        
        self.status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            bg=BG_DARK,
            fg=FG_MUTED,
            font=FONT_STATUS,
            anchor="w",
            padx=16,
            pady=4
            )
        
        self.status_label.grid(
            row=1,
            column=0,
            sticky="ew"
            )

    # ──────────────────────────────────────────────────────────
    # EVENT: Stock selection changed
    # ──────────────────────────────────────────────────────────
    def _on_stock_select(self, event=None):
        """Update the price preview label when user picks a stock."""
        symbol = self.stock_var.get()
        if symbol in STOCK_PRICES:
            self.price_label.config(
                text=f"${STOCK_PRICES[symbol]:,.2f}")

    # ──────────────────────────────────────────────────────────
    # ACTION: Add Stock
    # ──────────────────────────────────────────────────────────
    def _add_stock(self):
        """
        Validate inputs → calculate value → insert row into table
        → update total investment.
        """
        symbol = self.stock_var.get().strip()
        qty_str = self.qty_var.get().strip()

        # ── Validation ────────────────────────────────────────
        if not symbol:
            self._set_status("⚠️  Please select a stock symbol.", WARN)
            messagebox.showwarning("Missing Input",
                                   "Please select a stock symbol.")
            return

        if not qty_str:
            self._set_status("⚠️  Please enter a quantity.", WARN)
            messagebox.showwarning("Missing Input",
                                   "Please enter a quantity.")
            return

        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            self._set_status("❌  Quantity must be a positive integer.", DANGER)
            messagebox.showerror("Invalid Quantity",
                                 "Quantity must be a positive whole number "
                                 "(e.g. 10, 50, 100).")
            return

        # ── Calculate value ───────────────────────────────────
        price = STOCK_PRICES[symbol]
        total_value = qty * price                # core formula

        # ── Alternating row colour ────────────────────────────
        row_count = len(self.tree.get_children())
        tag = "even" if row_count % 2 == 0 else "odd"

        # ── Insert into Treeview ──────────────────────────────
        self.tree.insert("", "end",
                         values=(symbol,
                                 qty,
                                 f"${price:,.2f}",
                                 f"${total_value:,.2f}"),
                         tags=(tag,))

        # ── Update summary ────────────────────────────────────
        self._update_total()

        # ── Clear inputs ──────────────────────────────────────
        self.qty_var.set("")
        self.stock_var.set("")
        self.price_label.config(text="—")

        self._set_status(
            f"✅  Added {qty} × {symbol}  →  ${total_value:,.2f}", ACCENT2)

    # ──────────────────────────────────────────────────────────
    # ACTION: Remove Selected Row
    # ──────────────────────────────────────────────────────────
    def _remove_selected(self):
        """Remove whichever row the user has highlighted."""
        selected = self.tree.selection()
        if not selected:
            self._set_status("⚠️  No row selected. Click a row first.", WARN)
            messagebox.showwarning("Nothing Selected",
                                   "Please select a row in the table first.")
            return

        # Confirm
        values = self.tree.item(selected[0], "values")
        confirm = messagebox.askyesno(
            "Remove Stock",
            f"Remove {values[1]} shares of {values[0]} "
            f"(Value: {values[3]}) from portfolio?")
        if confirm:
            self.tree.delete(selected[0])
            self._update_total()
            self._set_status(f"🗑  Removed {values[0]} from portfolio.", WARN)

    # ──────────────────────────────────────────────────────────
    # ACTION: Clear Portfolio
    # ──────────────────────────────────────────────────────────
    def _clear_portfolio(self):
        """Delete all rows after confirmation."""
        if not self.tree.get_children():
            self._set_status("ℹ️  Portfolio is already empty.", FG_MUTED)
            return

        confirm = messagebox.askyesno(
            "Clear Portfolio",
            "This will remove ALL stocks from the portfolio.\n"
            "Are you sure?")
        if confirm:
            for item in self.tree.get_children():
                self.tree.delete(item)
            self._update_total()
            self._set_status("🗑  Portfolio cleared.", WARN)

    # ──────────────────────────────────────────────────────────
    # ACTION: Save as TXT
    # ──────────────────────────────────────────────────────────
    def _save_txt(self):
        """Export portfolio to a formatted plain-text report."""
        rows = self._get_all_rows()
        if not rows:
            messagebox.showinfo("Empty Portfolio",
                                "Add some stocks before saving.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile="portfolio_report.txt",
            title="Save Portfolio as TXT")
        if not filepath:
            return

        total = self._calculate_total()
        now   = datetime.datetime.now().strftime("%d %b %Y %H:%M:%S")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=" * 52 + "\n")
            f.write("   📈  STOCK PORTFOLIO REPORT\n")
            f.write(f"   Generated: {now}\n")
            f.write("=" * 52 + "\n\n")
            f.write(f"{'Stock':<10} {'Quantity':>10} {'Price ($)':>12}"
                    f" {'Total Value ($)':>16}\n")
            f.write("-" * 52 + "\n")
            for stock, qty, price, total_val in rows:
                f.write(f"{stock:<10} {qty:>10} {price:>12} {total_val:>16}\n")
            f.write("-" * 52 + "\n")
            f.write(f"\n  TOTAL INVESTMENT VALUE : ${total:,.2f}\n\n")
            f.write("=" * 52 + "\n")

        self._set_status(f"💾  Report saved → {filepath}", ACCENT2)
        messagebox.showinfo("Saved", f"Portfolio saved to:\n{filepath}")

    # ──────────────────────────────────────────────────────────
    # ACTION: Save as CSV
    # ──────────────────────────────────────────────────────────
    def _save_csv(self):
        """Export portfolio to a CSV file."""
        rows = self._get_all_rows()
        if not rows:
            messagebox.showinfo("Empty Portfolio",
                                "Add some stocks before saving.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            initialfile="portfolio.csv",
            title="Save Portfolio as CSV")
        if not filepath:
            return

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Stock Name", "Quantity",
                             "Price Per Share ($)", "Total Value ($)"])
            writer.writerows(rows)
            # Blank row then total
            writer.writerow([])
            writer.writerow(["", "", "TOTAL",
                             f"${self._calculate_total():,.2f}"])

        self._set_status(f"📊  CSV saved → {filepath}", ACCENT2)
        messagebox.showinfo("Saved", f"CSV saved to:\n{filepath}")

    # ──────────────────────────────────────────────────────────
    # HELPERS
    # ──────────────────────────────────────────────────────────
    def _get_all_rows(self):
        """Return all Treeview rows as a list of tuples."""
        rows = []
        for item in self.tree.get_children():
            rows.append(self.tree.item(item, "values"))
        return rows

    def _calculate_total(self):
        """
        Sum the total values from all rows.
        Values are stored as strings like '$1,800.00'; strip $ and commas.
        """
        total = 0.0
        for item in self.tree.get_children():
            val_str = self.tree.item(item, "values")[3]   # 4th column
            total  += float(val_str.replace("$", "").replace(",", ""))
        return total

    def _update_total(self):
        """Recalculate and refresh the total investment label."""
        total    = self._calculate_total()
        count    = len(self.tree.get_children())
        self.total_label.config(text=f"${total:,.2f}")
        self.holdings_label.config(
            text=f"{count} holding{'s' if count != 1 else ''}")

    def _set_status(self, message: str, colour: str = FG_MUTED):
        self.status_var.set(message)
        self.status_label.config(fg=colour)

# ══════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════
def main():
    root = tk.Tk()
    app  = StockPortfolioTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()