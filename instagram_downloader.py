"""
Instagram Downloader - Interface Grafica
Baixa videos, reels, fotos e carrosseis do Instagram em qualidade original,
usando yt-dlp como motor de download.

Uso previsto: conteudo proprio ou conteudo publico com autorizacao do autor.
Respeite os termos de uso do Instagram e direitos autorais de terceiros.
"""

import os
import sys
import threading
import subprocess
from pathlib import Path

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    import yt_dlp
except ImportError:
    yt_dlp = None


APP_TITLE = "Instagram Downloader"
DEFAULT_DOWNLOAD_DIR = str(Path.home() / "Downloads" / "InstagramDownloads")


class InstagramDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("560x420")
        self.root.resizable(False, False)

        self.download_dir = tk.StringVar(value=DEFAULT_DOWNLOAD_DIR)
        self.url_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pronto.")
        self.progress_var = tk.DoubleVar(value=0)

        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        pad = {"padx": 12, "pady": 6}

        title_lbl = ttk.Label(
            self.root, text=APP_TITLE, font=("Segoe UI", 16, "bold")
        )
        title_lbl.pack(pady=(16, 0))

        subtitle = ttk.Label(
            self.root,
            text="Cole o link do post, reel ou foto do Instagram abaixo",
            font=("Segoe UI", 9),
        )
        subtitle.pack(pady=(0, 10))

        # URL input
        url_frame = ttk.Frame(self.root)
        url_frame.pack(fill="x", **pad)
        ttk.Label(url_frame, text="URL do Instagram:").pack(anchor="w")
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=60)
        url_entry.pack(fill="x", pady=(4, 0))

        # Download folder
        dir_frame = ttk.Frame(self.root)
        dir_frame.pack(fill="x", **pad)
        ttk.Label(dir_frame, text="Pasta de destino:").pack(anchor="w")
        dir_inner = ttk.Frame(dir_frame)
        dir_inner.pack(fill="x", pady=(4, 0))
        ttk.Entry(dir_inner, textvariable=self.download_dir, width=48).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(dir_inner, text="Escolher...", command=self._choose_dir).pack(
            side="left", padx=(6, 0)
        )

        # Quality options
        opts_frame = ttk.LabelFrame(self.root, text="Opcoes")
        opts_frame.pack(fill="x", **pad)

        self.best_quality = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            opts_frame,
            text="Forcar melhor qualidade disponivel (sem recompressao)",
            variable=self.best_quality,
        ).pack(anchor="w", padx=8, pady=4)

        self.audio_only = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            opts_frame, text="Extrair somente audio (MP3)", variable=self.audio_only
        ).pack(anchor="w", padx=8, pady=(0, 6))

        # Download button
        self.download_btn = ttk.Button(
            self.root, text="Baixar", command=self._start_download
        )
        self.download_btn.pack(pady=12)

        # Progress bar
        self.progress = ttk.Progressbar(
            self.root, variable=self.progress_var, maximum=100, length=480
        )
        self.progress.pack(pady=(0, 6))

        # Status
        status_lbl = ttk.Label(self.root, textvariable=self.status_var, wraplength=500)
        status_lbl.pack(pady=(0, 10))

        footer = ttk.Label(
            self.root,
            text="Use apenas para conteudo proprio ou com autorizacao do autor.",
            font=("Segoe UI", 8),
            foreground="#777777",
        )
        footer.pack(side="bottom", pady=8)

    def _choose_dir(self):
        chosen = filedialog.askdirectory(initialdir=self.download_dir.get() or str(Path.home()))
        if chosen:
            self.download_dir.set(chosen)

    # ---------- Download logic ----------
    def _start_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning(APP_TITLE, "Cole a URL do Instagram primeiro.")
            return

        if "instagram.com" not in url:
            if not messagebox.askyesno(
                APP_TITLE, "Essa URL nao parece ser do Instagram. Continuar mesmo assim?"
            ):
                return

        if yt_dlp is None:
            messagebox.showerror(
                APP_TITLE,
                "A biblioteca 'yt-dlp' nao esta instalada.\n"
                "Instale com: pip install yt-dlp",
            )
            return

        os.makedirs(self.download_dir.get(), exist_ok=True)

        self.download_btn.config(state="disabled")
        self.status_var.set("Iniciando download...")
        self.progress_var.set(0)

        thread = threading.Thread(target=self._download_worker, args=(url,), daemon=True)
        thread.start()

    def _progress_hook(self, d):
        if d.get("status") == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total:
                pct = downloaded / total * 100
                self.progress_var.set(pct)
                self.status_var.set(f"Baixando... {pct:.1f}%")
        elif d.get("status") == "finished":
            self.status_var.set("Processando arquivo final...")
            self.progress_var.set(100)

    def _download_worker(self, url):
        outtmpl = os.path.join(self.download_dir.get(), "%(title).80s_%(id)s.%(ext)s")

        ydl_opts = {
            "outtmpl": outtmpl,
            "progress_hooks": [self._progress_hook],
            "quiet": True,
            "noprogress": True,
            "merge_output_format": "mp4",
        }

        if self.best_quality.get():
            ydl_opts["format"] = "bestvideo+bestaudio/best"
        else:
            ydl_opts["format"] = "best"

        if self.audio_only.get():
            ydl_opts["format"] = "bestaudio/best"
            ydl_opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "0",
                }
            ]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.root.after(0, self._on_success)
        except Exception as exc:  # noqa: BLE001
            self.root.after(0, self._on_error, str(exc))

    def _on_success(self):
        self.status_var.set(f"Concluido! Arquivo salvo em: {self.download_dir.get()}")
        self.download_btn.config(state="normal")
        messagebox.showinfo(APP_TITLE, "Download concluido com sucesso!")

    def _on_error(self, message):
        self.status_var.set("Erro ao baixar. Veja detalhes na janela.")
        self.download_btn.config(state="normal")
        messagebox.showerror(
            APP_TITLE,
            "Nao foi possivel baixar esse conteudo.\n\n"
            f"Detalhes: {message}\n\n"
            "Possiveis causas: post privado, exige login, link invalido, "
            "ou o yt-dlp precisa ser atualizado (pip install -U yt-dlp).",
        )


def main():
    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass

    app = InstagramDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
