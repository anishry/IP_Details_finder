#!/usr/bin/env python3
"""
Public IP Details Finder
============================================
A dark-themed tkinter dashboard that fetches and displays full geolocation,
network, and timezone details for any IP address (or your own public IP).

Created  by: ANISH R
Date: 2024-06-30
Version: 1.0
For any queries or suggestions, contact: anishry88@gmail.com ph: +91-9895 086 743
Developer: Anish R
Email:anishry88@gmail.com
Developer's Phone: +91-9895 086 743
Tool For CERT-K
-----------
Disclaimer:
-----------
This tool is intended for educational and ethical use only. The author is not responsible for any misuse
or damage caused by this software. Always obtain proper authorization before testing any website.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import urllib.request
import urllib.error
import json
import threading
import webbrowser
import time


# ──────────────────────────────────────────────────────────
#  COLOUR & STYLE TOKENS
# ──────────────────────────────────────────────────────────
BG_DARK   = "#0B0F1A"   # base background – deep navy
BG_CARD   = "#131929"   # card surface
BG_INPUT  = "#1A2235"   # input field bg
BG_HOVER  = "#1E2A42"   # hover / active state
BORDER    = "#1F3050"   # subtle border / divider
ACCENT    = "#3B82F6"   # electric blue – primary action
ACCENT2   = "#06B6D4"   # cyan – secondary accent
SUCCESS   = "#10B981"   # emerald – good status
WARNING   = "#F59E0B"   # amber – warning
DANGER    = "#EF4444"   # red – error
TEXT_PRI  = "#E2E8F0"   # primary text
TEXT_SEC  = "#64748B"   # secondary / label text
TEXT_MUT  = "#334155"   # muted / disabled
MONO_FONT = ("Consolas", 11)


# ──────────────────────────────────────────────────────────
#  API HELPERS
# ──────────────────────────────────────────────────────────
def fetch_my_ip() -> str:
    """Return the caller's public IPv4/IPv6 address."""
    url = "https://api64.ipify.org?format=json"
    with urllib.request.urlopen(url, timeout=8) as resp:
        data = json.loads(resp.read().decode())
    return data.get("ip", "")


def fetch_ip_info(ip: str) -> dict:
    """
    Call ip-api.com for geolocation + network details.
    Passing an empty string returns info about the caller's own IP.
    """
    fields = (
        "status,message,country,countryCode,region,regionName,"
        "city,zip,lat,lon,timezone,isp,org,as,asname,"
        "mobile,proxy,hosting,query"
    )
    target = ip.strip() if ip.strip() else ""
    url = f"http://ip-api.com/json/{target}?fields={fields}"
    with urllib.request.urlopen(url, timeout=8) as resp:
        return json.loads(resp.read().decode())


# ──────────────────────────────────────────────────────────
#  WIDGET HELPERS
# ──────────────────────────────────────────────────────────
def make_label(parent, text, fg=TEXT_SEC, font=("Segoe UI", 9), **kw):
    return tk.Label(parent, text=text, bg=BG_CARD, fg=fg, font=font, **kw)


def make_value(parent, textvariable, fg=TEXT_PRI, font=("Consolas", 11), **kw):
    return tk.Label(parent, textvariable=textvariable, bg=BG_CARD,
                    fg=fg, font=font, anchor="w", **kw)


class Divider(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, height=1, bg=BORDER, **kw)


class StatusDot(tk.Canvas):
    """A small coloured circle indicator."""
    def __init__(self, parent, color=TEXT_MUT, size=10, **kw):
        super().__init__(parent, width=size, height=size,
                         bg=BG_CARD, highlightthickness=0, **kw)
        self._size = size
        self._dot = self.create_oval(1, 1, size - 1, size - 1, fill=color, outline="")

    def set_color(self, color):
        self.itemconfig(self._dot, fill=color)


class CopyButton(tk.Label):
    """Tiny clickable 'copy' label that copies text to clipboard."""
    def __init__(self, parent, get_text, **kw):
        super().__init__(parent, text="⎘ copy", bg=BG_CARD,
                         fg=TEXT_MUT, font=("Segoe UI", 8), cursor="hand2", **kw)
        self._get = get_text
        self.bind("<Enter>", lambda _: self.config(fg=ACCENT))
        self.bind("<Leave>", lambda _: self.config(fg=TEXT_MUT))
        self.bind("<Button-1>", self._copy)

    def _copy(self, _=None):
        val = self._get()
        if val and val not in ("-", "—"):
            self.clipboard_clear()
            self.clipboard_append(val)
            self.config(text="✓ copied", fg=SUCCESS)
            self.after(1500, lambda: self.config(text="⎘ copy", fg=TEXT_MUT))


# ──────────────────────────────────────────────────────────
#  MAIN APPLICATION
# ──────────────────────────────────────────────────────────
class IPDetailsApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Public IP Details")
        self.configure(bg=BG_DARK)
        self.resizable(False, False)

        # Center on screen
        self.update_idletasks()
        w, h = 720, 820
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        self._vars = {}  # StringVar registry
        self._build_ui()
        # Auto-lookup on start
        self.after(300, self._auto_lookup)

    # ── UI Construction ────────────────────────────────────
    def _build_ui(self):
        # ── Header bar ──────────────────────────────────────
        header = tk.Frame(self, bg=BG_DARK, padx=24, pady=16)
        header.pack(fill="x")

        tk.Label(header, text="🌐", bg=BG_DARK, font=("Segoe UI Emoji", 22)).pack(side="left")
        tk.Label(header, text="  Public IP  Lookup",
                 bg=BG_DARK, fg=TEXT_PRI,
                 font=("Segoe UI", 17, "bold")).pack(side="left")

        self._status_dot = StatusDot(header, color=TEXT_MUT, size=12)
        self._status_dot.pack(side="right", padx=(0, 4))
        self._status_lbl = tk.Label(header, text="Ready",
                                    bg=BG_DARK, fg=TEXT_SEC,
                                    font=("Segoe UI", 9))
        self._status_lbl.pack(side="right")

        # ── Search bar ──────────────────────────────────────
        search_frame = tk.Frame(self, bg=BG_DARK, padx=24, pady=4)
        search_frame.pack(fill="x")

        entry_container = tk.Frame(search_frame, bg=BORDER, padx=1, pady=1)
        entry_container.pack(side="left", fill="x", expand=True)

        inner = tk.Frame(entry_container, bg=BG_INPUT)
        inner.pack(fill="x")

        self._ip_var = tk.StringVar()
        self._entry = tk.Entry(inner, textvariable=self._ip_var,
                               bg=BG_INPUT, fg=TEXT_PRI, insertbackground=ACCENT,
                               relief="flat", font=("Consolas", 12),
                               width=30)
        self._entry.pack(side="left", padx=12, pady=10, fill="x", expand=True)
        self._entry.bind("<Return>", lambda _: self._on_lookup())

        placeholder = "Enter IP address or leave blank for your IP…"
        self._entry.insert(0, placeholder)
        self._entry.config(fg=TEXT_SEC)

        def on_focus_in(_):
            if self._entry.get() == placeholder:
                self._entry.delete(0, "end")
                self._entry.config(fg=TEXT_PRI)

        def on_focus_out(_):
            if not self._entry.get():
                self._entry.insert(0, placeholder)
                self._entry.config(fg=TEXT_SEC)

        self._entry.bind("<FocusIn>", on_focus_in)
        self._entry.bind("<FocusOut>", on_focus_out)

        self._lookup_btn = tk.Button(search_frame, text="  Lookup  ",
                                     bg=ACCENT, fg="white",
                                     activebackground="#2563EB",
                                     activeforeground="white",
                                     relief="flat", font=("Segoe UI", 11, "bold"),
                                     cursor="hand2", padx=10,
                                     command=self._on_lookup)
        self._lookup_btn.pack(side="left", padx=(8, 0))

        self._my_ip_btn = tk.Button(search_frame, text="My IP",
                                    bg=BG_CARD, fg=ACCENT2,
                                    activebackground=BG_HOVER,
                                    activeforeground=ACCENT2,
                                    relief="flat", font=("Segoe UI", 9),
                                    cursor="hand2", padx=8,
                                    command=self._on_my_ip)
        self._my_ip_btn.pack(side="left", padx=(6, 0))

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(10, 0))

        # ── Scrollable content area ─────────────────────────
        canvas = tk.Canvas(self, bg=BG_DARK, highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._scroll_frame = tk.Frame(canvas, bg=BG_DARK)
        canvas_window = canvas.create_window((0, 0), window=self._scroll_frame, anchor="nw")

        def on_frame_configure(_):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        self._scroll_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        # Mouse-wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows / macOS
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux up
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))  # Linux down

        content = self._scroll_frame
        pad = {"padx": 24, "pady": 6}

        # ── IP Banner card ──────────────────────────────────
        self._banner_frame = self._make_card(content, pad)
        self._build_banner(self._banner_frame)

        # ── Geolocation card ────────────────────────────────
        geo_card = self._make_card(content, pad)
        self._build_section(geo_card, "📍  Location", [
            ("Country",     "country"),
            ("Country Code","countryCode"),
            ("Region",      "regionName"),
            ("Region Code", "region"),
            ("City",        "city"),
            ("ZIP / Postal","zip"),
            ("Latitude",    "lat"),
            ("Longitude",   "lon"),
            ("Coordinates", "coords"),
        ])

        # ── Network card ─────────────────────────────────────
        net_card = self._make_card(content, pad)
        self._build_section(net_card, "🔌  Network", [
            ("ISP",         "isp"),
            ("Organisation","org"),
            ("AS Number",   "as"),
            ("AS Name",     "asname"),
            ("Timezone",    "timezone"),
        ])

        # ── Flags card ────────────────────────────────────────
        flags_card = self._make_card(content, pad)
        self._build_flags(flags_card)

        # ── Action row ────────────────────────────────────────
        action_frame = tk.Frame(content, bg=BG_DARK)
        action_frame.pack(fill="x", **pad)
        self._map_btn = tk.Button(action_frame, text="🗺  Open in Google Maps",
                                  bg=BG_CARD, fg=ACCENT2,
                                  activebackground=BG_HOVER, activeforeground=ACCENT2,
                                  relief="flat", font=("Segoe UI", 10),
                                  cursor="hand2", padx=14, pady=7,
                                  command=self._open_map, state="disabled")
        self._map_btn.pack(side="left")

        self._copy_all_btn = tk.Button(action_frame, text="⎘  Copy all as JSON",
                                       bg=BG_CARD, fg=TEXT_SEC,
                                       activebackground=BG_HOVER, activeforeground=TEXT_PRI,
                                       relief="flat", font=("Segoe UI", 10),
                                       cursor="hand2", padx=14, pady=7,
                                       command=self._copy_all)
        self._copy_all_btn.pack(side="left", padx=(8, 0))

        # Footer
        tk.Label(content, text="Data via ip-api.com & ipify.org · No keys required",
                 bg=BG_DARK, fg=TEXT_MUT, font=("Segoe UI", 8)).pack(pady=(4, 16))

    def _make_card(self, parent, pad):
        outer = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
        outer.pack(fill="x", **pad)
        card = tk.Frame(outer, bg=BG_CARD, padx=20, pady=16)
        card.pack(fill="x")
        return card

    def _build_banner(self, card):
        row = tk.Frame(card, bg=BG_CARD)
        row.pack(fill="x")

        left = tk.Frame(row, bg=BG_CARD)
        left.pack(side="left", fill="both", expand=True)

        tk.Label(left, text="YOUR PUBLIC IP", bg=BG_CARD, fg=TEXT_SEC,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self._vars["query"] = tk.StringVar(value="—")
        ip_lbl = tk.Label(left, textvariable=self._vars["query"],
                          bg=BG_CARD, fg=ACCENT2,
                          font=("Consolas", 26, "bold"))
        ip_lbl.pack(anchor="w", pady=(2, 0))

        self._flag_lbl = tk.Label(left, text="", bg=BG_CARD, fg=TEXT_SEC,
                                  font=("Segoe UI", 10))
        self._flag_lbl.pack(anchor="w", pady=(0, 2))

        right = tk.Frame(row, bg=BG_CARD)
        right.pack(side="right")
        CopyButton(right, lambda: self._vars["query"].get()).pack(anchor="e")

    def _build_section(self, card, title, fields):
        tk.Label(card, text=title, bg=BG_CARD, fg=TEXT_PRI,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 10))
        Divider(card).pack(fill="x", pady=(0, 10))

        grid = tk.Frame(card, bg=BG_CARD)
        grid.pack(fill="x")
        grid.columnconfigure(1, weight=1)

        for i, (label, key) in enumerate(fields):
            self._vars[key] = tk.StringVar(value="—")

            tk.Label(grid, text=label, bg=BG_CARD, fg=TEXT_SEC,
                     font=("Segoe UI", 9), anchor="w",
                     width=14).grid(row=i, column=0, sticky="w",
                                    padx=(0, 16), pady=3)

            val_lbl = tk.Label(grid, textvariable=self._vars[key],
                               bg=BG_CARD, fg=TEXT_PRI,
                               font=("Consolas", 10), anchor="w")
            val_lbl.grid(row=i, column=1, sticky="w")

            CopyButton(grid, self._vars[key].get).grid(
                row=i, column=2, sticky="e", padx=(8, 0))

    def _build_flags(self, card):
        tk.Label(card, text="🛡  Network Flags", bg=BG_CARD, fg=TEXT_PRI,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 10))
        Divider(card).pack(fill="x", pady=(0, 12))

        row = tk.Frame(card, bg=BG_CARD)
        row.pack(fill="x")

        self._flag_widgets = {}
        flags = [
            ("mobile",  "📱 Mobile",   "Cellular / mobile network"),
            ("proxy",   "🔒 Proxy",    "VPN / Proxy / Tor exit node"),
            ("hosting", "🖥 Hosting",  "Datacenter / hosting provider"),
        ]
        for key, label, tooltip in flags:
            self._vars[key] = tk.StringVar(value="—")
            col = tk.Frame(row, bg=BG_CARD, padx=10, pady=10)
            col.pack(side="left", fill="both", expand=True)

            dot = StatusDot(col, color=TEXT_MUT)
            dot.pack(anchor="center")
            tk.Label(col, text=label, bg=BG_CARD, fg=TEXT_PRI,
                     font=("Segoe UI", 10, "bold")).pack()
            val = tk.Label(col, textvariable=self._vars[key], bg=BG_CARD,
                           fg=TEXT_MUT, font=("Segoe UI", 8))
            val.pack()
            self._flag_widgets[key] = (dot, val)

    # ── Status helpers ─────────────────────────────────────
    def _set_status(self, text, color=TEXT_SEC):
        self._status_lbl.config(text=text, fg=color)
        self._status_dot.set_color(color)

    def _set_busy(self, busy: bool):
        state = "disabled" if busy else "normal"
        self._lookup_btn.config(state=state)
        self._entry.config(state=state)
        self._my_ip_btn.config(state=state)

    # ── Lookup logic ───────────────────────────────────────
    def _get_ip_input(self):
        placeholder = "Enter IP address or leave blank for your IP…"
        val = self._ip_var.get().strip()
        if val == placeholder:
            return ""
        return val

    def _auto_lookup(self):
        self._do_lookup("")

    def _on_lookup(self):
        ip = self._get_ip_input()
        self._do_lookup(ip)

    def _on_my_ip(self):
        self._ip_var.set("")
        self._entry.config(fg=TEXT_PRI)
        self._do_lookup("")

    def _do_lookup(self, ip: str):
        self._set_busy(True)
        self._set_status("Fetching…", ACCENT)
        self._clear_values()
        threading.Thread(target=self._worker, args=(ip,), daemon=True).start()

    def _worker(self, ip: str):
        try:
            start = time.perf_counter()
            # If blank, discover public IP first so we can display it
            if not ip:
                discovered = fetch_my_ip()
                data = fetch_ip_info(discovered)
                if not data.get("query"):
                    data["query"] = discovered
            else:
                data = fetch_ip_info(ip)
            elapsed = (time.perf_counter() - start) * 1000

            if data.get("status") == "fail":
                self.after(0, lambda: self._show_error(data.get("message", "Lookup failed")))
            else:
                self.after(0, lambda: self._populate(data, elapsed))
        except urllib.error.URLError as e:
            self.after(0, lambda: self._show_error(f"Network error: {e.reason}"))
        except Exception as e:
            self.after(0, lambda: self._show_error(str(e)))

    def _show_error(self, msg: str):
        self._set_busy(False)
        self._set_status(f"Error: {msg}", DANGER)
        self._map_btn.config(state="disabled")

    def _clear_values(self):
        for var in self._vars.values():
            var.set("…")
        self._flag_lbl.config(text="")
        for dot, val in self._flag_widgets.values():
            dot.set_color(TEXT_MUT)
            val.config(fg=TEXT_MUT)

    def _populate(self, data: dict, elapsed_ms: float):
        self._last_data = data

        def v(key):
            val = data.get(key)
            if val is None or val == "":
                return "—"
            return str(val)

        # Banner
        self._vars["query"].set(v("query"))
        country = v("country")
        code = v("countryCode")
        city = v("city")
        self._flag_lbl.config(text=f"{country}  ({code})  ·  {city}")

        # Location
        lat = data.get("lat", "")
        lon = data.get("lon", "")
        for key in ["country", "countryCode", "regionName", "region", "city", "zip"]:
            self._vars[key].set(v(key))
        self._vars["lat"].set(str(lat) if lat != "" else "—")
        self._vars["lon"].set(str(lon) if lon != "" else "—")
        self._vars["coords"].set(f"{lat}, {lon}" if lat != "" and lon != "" else "—")

        # Network
        for key in ["isp", "org", "as", "asname", "timezone"]:
            self._vars[key].set(v(key))

        # Flags
        flag_cfg = {
            "mobile":  (data.get("mobile"),  "Yes — mobile network", "No — fixed line"),
            "proxy":   (data.get("proxy"),   "Yes — VPN / Proxy",   "No proxy detected"),
            "hosting": (data.get("hosting"), "Yes — hosting / DC",  "No — residential"),
        }
        for key, (val, yes_text, no_text) in flag_cfg.items():
            dot, lbl = self._flag_widgets[key]
            if val is True:
                dot.set_color(WARNING)
                self._vars[key].set(yes_text)
                lbl.config(fg=WARNING)
            elif val is False:
                dot.set_color(SUCCESS)
                self._vars[key].set(no_text)
                lbl.config(fg=SUCCESS)
            else:
                dot.set_color(TEXT_MUT)
                self._vars[key].set("Unknown")
                lbl.config(fg=TEXT_MUT)

        # Enable map button if we have coordinates
        if lat and lon:
            self._map_btn.config(state="normal")
            self._map_lat = float(lat)
            self._map_lon = float(lon)
        else:
            self._map_btn.config(state="disabled")

        self._set_busy(False)
        self._set_status(f"Done  ·  {elapsed_ms:.0f} ms", SUCCESS)

    # ── Actions ────────────────────────────────────────────
    def _open_map(self):
        url = f"https://www.google.com/maps?q={self._map_lat},{self._map_lon}&z=12"
        webbrowser.open(url)

    def _copy_all(self):
        if hasattr(self, "_last_data"):
            self.clipboard_clear()
            self.clipboard_append(json.dumps(self._last_data, indent=2))
            orig = self._copy_all_btn.cget("text")
            self._copy_all_btn.config(text="✓ Copied!", fg=SUCCESS)
            self.after(1800, lambda: self._copy_all_btn.config(text=orig, fg=TEXT_SEC))


# ──────────────────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = IPDetailsApp()
    app.mainloop()
