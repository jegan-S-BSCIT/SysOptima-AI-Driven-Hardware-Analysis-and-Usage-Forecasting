"""
Benchmarks view for SysOptima
"""

from tkinter import ttk, messagebox

class BenchmarksView(ttk.Frame):
    """UI for running benchmarks"""
    def __init__(self, parent, handlers=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.handlers = handlers or {}
        self._build()

    def _build(self):
        title = ttk.Label(self, text="Performance Benchmarks", font=("Arial", 16, "bold"))
        title.pack(pady=12)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=8)

        ttk.Button(btn_frame, text="CPU Benchmark", command=lambda: self._call_handler("cpu")).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Memory Benchmark", command=lambda: self._call_handler("memory")).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Disk Benchmark", command=lambda: self._call_handler("disk")).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Run All", command=lambda: self._call_handler("all")).pack(side="left", padx=4)

        self.status = ttk.Label(self, text="Idle")
        self.status.pack(pady=6)

    def _call_handler(self, key):
        handler = self.handlers.get(key)
        if handler:
            self.status.config(text=f"Running {key} benchmark...")
            handler()
            self.status.config(text="Completed")
        else:
            messagebox.showinfo("Info", "Handler not wired yet")
