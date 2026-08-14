"""Desktop application for converting files with Docling."""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Callable

import customtkinter as ctk
from tkinter import filedialog, messagebox
from translations import LANGUAGES, TRANSLATIONS


APP_TITLE = "Docs to Text"
THEMES = ("dark-blue", "blue")
AUTO_DETECT = "Auto detect"

INPUT_FORMATS: dict[str, tuple[str, ...]] = {
    "PDF": (".pdf",),
    "PPTX": (".pptx",),
    "JPEG": (".jpg", ".jpeg"),
    "PNG": (".png",),
    "TIFF": (".tif", ".tiff"),
    "WEBP": (".webp",),
    "BMP": (".bmp",),
    "MP3": (".mp3",),
    "WAV": (".wav",),
}
OUTPUT_FORMATS: dict[str, tuple[str, str]] = {
    "JSON": (".json", "Structured document data"),
    "Text": (".txt", "Plain extracted text"),
    "Markdown": (".md", "Formatted Markdown"),
    "HTML": (".html", "Standalone HTML"),
}

FILE_DIALOG_TYPES = (
    (
        "Supported files",
        " ".join(
            f"*{extension}"
            for extensions in INPUT_FORMATS.values()
            for extension in extensions
        ),
    ),
    ("All files", "*.*"),
)


def detect_input_type(file_path: str | Path) -> str:
    """Return the matching input label for a file, or Auto detect."""
    suffix = Path(file_path).suffix.lower()
    for input_type, extensions in INPUT_FORMATS.items():
        if suffix in extensions:
            return input_type
    return AUTO_DETECT


def input_type_matches(file_path: str | Path, input_type: str) -> bool:
    """Check whether a file extension matches the selected input type."""
    if input_type == AUTO_DETECT:
        return Path(file_path).suffix.lower() in {
            extension
            for extensions in INPUT_FORMATS.values()
            for extension in extensions
        }
    return Path(file_path).suffix.lower() in INPUT_FORMATS.get(input_type, ())


def build_output_path(
    source_path: str | Path,
    output_directory: str | Path,
    output_format: str,
) -> Path:
    """Build the output filename while keeping the source file stem."""
    extension = OUTPUT_FORMATS[output_format][0]
    source = Path(source_path)
    return Path(output_directory) / f"{source.stem}{extension}"


class DocsToTextApp(ctk.CTk):
    """Main application window."""

    COLORS = {
        "canvas": ("#F5F7FB", "#0D1117"),
        "panel": ("#FFFFFF", "#151B24"),
        "panel_muted": ("#EEF2F8", "#1B2430"),
        "border": ("#DCE3EE", "#293444"),
        "text": ("#132238", "#F3F6FC"),
        "muted": ("#64748B", "#9AA8BC"),
        "success": ("#11845B", "#45D19A"),
        "warning": ("#A56700", "#F4BD52"),
    }

    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1120x760")
        self.minsize(900, 640)

        self.source_var = ctk.StringVar(value="")
        self.input_type_key = AUTO_DETECT
        self.output_format_key = "Text"
        self.input_type_var = ctk.StringVar()
        self.output_format_var = ctk.StringVar()
        self.output_directory_var = ctk.StringVar(value="")
        self.theme_var = ctk.StringVar(value="dark-blue")
        self.language_var = ctk.StringVar(value="pt-BR")
        self.status_var = ctk.StringVar()
        self.detail_var = ctk.StringVar()
        self._is_converting = False
        self._active_theme = self.theme_var.get()
        self._active_language = self.language_var.get()
        self._sync_display_values()

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme(self.theme_var.get())
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the view from persistent variables for theme swapping."""
        if hasattr(self, "main_frame"):
            self.main_frame.destroy()
        if hasattr(self, "header_frame"):
            self.header_frame.destroy()

        self.configure(fg_color=self.COLORS["canvas"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=36,
            pady=(0, 28),
        )
        self.main_frame.grid_columnconfigure(0, weight=0, minsize=270)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_converter_card()

    def _t(self, key: str, **values: str) -> str:
        text = TRANSLATIONS[self._active_language][key]
        return text.format(**values) if values else text

    def _input_label(self, input_type: str) -> str:
        if input_type == AUTO_DETECT:
            return self._t("auto_detect")
        return input_type

    def _output_label(self, output_format: str) -> str:
        return self._t(f"output_{output_format.lower()}")

    def _output_options(self) -> list[str]:
        return [
            self._output_label(output_format)
            for output_format in OUTPUT_FORMATS
        ]

    def _sync_display_values(self) -> None:
        self.input_type_var.set(self._input_label(self.input_type_key))
        self.output_format_var.set(self._output_label(self.output_format_key))
        self.status_var.set(self._t("ready"))
        self.detail_var.set(self._t("ready_detail"))

    def _build_header(self) -> None:
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=90,
        )
        self.header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=36,
            pady=(28, 18),
        )
        self.header_frame.grid_columnconfigure(1, weight=1)

        brand = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        brand.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            brand,
            text="DOCS TO TEXT",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.COLORS["muted"],
        ).pack(anchor="w")
        ctk.CTkLabel(
            brand,
            text=self._t("tagline"),
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=self.COLORS["text"],
        ).pack(anchor="w", pady=(3, 0))

        language_frame = ctk.CTkFrame(
            self.header_frame,
            fg_color="transparent",
        )
        language_frame.grid(row=0, column=2, sticky="e", padx=(0, 12))
        ctk.CTkLabel(
            language_frame,
            text=self._t("language_label"),
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.COLORS["muted"],
        ).pack(anchor="e", pady=(0, 6))
        self.language_box = ctk.CTkComboBox(
            language_frame,
            values=list(LANGUAGES),
            variable=self.language_var,
            command=self._change_language,
            width=150,
            height=34,
            state="readonly",
        )
        self.language_box.pack(anchor="e")

        theme_frame = ctk.CTkFrame(
            self.header_frame,
            fg_color="transparent",
        )
        theme_frame.grid(row=0, column=3, sticky="e")
        ctk.CTkLabel(
            theme_frame,
            text=self._t("theme_label"),
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.COLORS["muted"],
        ).pack(anchor="e", pady=(0, 6))
        self.theme_box = ctk.CTkComboBox(
            theme_frame,
            values=list(THEMES),
            variable=self.theme_var,
            command=self._change_theme,
            width=150,
            height=34,
            state="readonly",
        )
        self.theme_box.pack(anchor="e")

    def _build_sidebar(self) -> None:
        sidebar = ctk.CTkFrame(
            self.main_frame,
            corner_radius=18,
            fg_color=self.COLORS["panel_muted"],
            border_width=1,
            border_color=self.COLORS["border"],
        )
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 18))

        ctk.CTkLabel(
            sidebar,
            text=self._t("workflow_kicker"),
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.COLORS["muted"],
        ).pack(anchor="w", padx=24, pady=(28, 8))
        ctk.CTkLabel(
            sidebar,
            text=self._t("workflow_title"),
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.COLORS["text"],
            justify="left",
        ).pack(anchor="w", padx=24)
        ctk.CTkLabel(
            sidebar,
            text=self._t("workflow_description"),
            font=ctk.CTkFont(size=13),
            text_color=self.COLORS["muted"],
            justify="left",
            wraplength=215,
        ).pack(anchor="w", padx=24, pady=(14, 30))

        steps = (
            ("01", "step_source", "step_source_description"),
            ("02", "step_format", "step_format_description"),
            ("03", "step_convert", "step_convert_description"),
        )
        for number, title_key, description_key in steps:
            step = ctk.CTkFrame(sidebar, fg_color="transparent")
            step.pack(fill="x", padx=24, pady=8)
            ctk.CTkLabel(
                step,
                text=number,
                width=32,
                height=32,
                corner_radius=16,
                fg_color=self.COLORS["panel"],
                text_color=self.COLORS["muted"],
                font=ctk.CTkFont(size=11, weight="bold"),
            ).pack(side="left", anchor="n")
            copy = ctk.CTkFrame(step, fg_color="transparent")
            copy.pack(side="left", fill="x", expand=True, padx=(12, 0))
            ctk.CTkLabel(
                copy,
                text=self._t(title_key),
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=self.COLORS["text"],
                anchor="w",
            ).pack(fill="x")
            ctk.CTkLabel(
                copy,
                text=self._t(description_key),
                font=ctk.CTkFont(size=11),
                text_color=self.COLORS["muted"],
                anchor="w",
                justify="left",
                wraplength=160,
            ).pack(fill="x", pady=(2, 0))

        supported_card = ctk.CTkFrame(
            sidebar,
            fg_color=self.COLORS["panel"],
            corner_radius=12,
        )
        supported_card.pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=(18, 24),
        )
        ctk.CTkLabel(
            supported_card,
            text=self._t("supported"),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.COLORS["text"],
            anchor="w",
            justify="left",
            wraplength=220,
        ).pack(fill="x", padx=16, pady=(14, 16))

    def _build_converter_card(self) -> None:
        card = ctk.CTkFrame(
            self.main_frame,
            corner_radius=18,
            fg_color=self.COLORS["panel"],
            border_width=1,
            border_color=self.COLORS["border"],
        )
        card.grid(row=0, column=1, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(4, weight=1)

        intro = ctk.CTkFrame(card, fg_color="transparent")
        intro.grid(row=0, column=0, sticky="ew", padx=30, pady=(28, 25))
        ctk.CTkLabel(
            intro,
            text=self._t("setup_kicker"),
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.COLORS["muted"],
        ).pack(anchor="w")
        ctk.CTkLabel(
            intro,
            text=self._t("setup_title"),
            font=ctk.CTkFont(size=21, weight="bold"),
            text_color=self.COLORS["text"],
        ).pack(anchor="w", pady=(4, 0))

        source_section = ctk.CTkFrame(card, fg_color="transparent")
        source_section.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=30,
            pady=(0, 20),
        )
        source_section.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            source_section,
            text=self._t("source_label"),
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.COLORS["muted"],
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 7))
        self.source_entry = ctk.CTkEntry(
            source_section,
            textvariable=self.source_var,
            height=42,
            placeholder_text=self._t("source_placeholder"),
            border_width=1,
        )
        self.source_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        self.browse_file_button = ctk.CTkButton(
            source_section,
            text=self._t("browse"),
            width=105,
            height=42,
            command=self._choose_source,
        )
        self.browse_file_button.grid(row=1, column=1)

        selectors = ctk.CTkFrame(card, fg_color="transparent")
        selectors.grid(row=2, column=0, sticky="ew", padx=30, pady=(0, 20))
        selectors.grid_columnconfigure(0, weight=1)
        selectors.grid_columnconfigure(1, weight=1)
        self._build_selector(
            selectors,
            0,
            self._t("input_label"),
            [self._input_label(AUTO_DETECT), *INPUT_FORMATS],
            self.input_type_var,
            self._input_type_changed,
        )
        self._build_selector(
            selectors,
            1,
            self._t("output_label"),
            self._output_options(),
            self.output_format_var,
            self._output_format_changed,
        )

        destination = ctk.CTkFrame(card, fg_color="transparent")
        destination.grid(row=3, column=0, sticky="ew", padx=30, pady=(0, 20))
        destination.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            destination,
            text=self._t("output_folder_label"),
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.COLORS["muted"],
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 7))
        self.output_entry = ctk.CTkEntry(
            destination,
            textvariable=self.output_directory_var,
            height=40,
            placeholder_text=self._t("output_folder_placeholder"),
            border_width=1,
        )
        self.output_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        self.browse_folder_button = ctk.CTkButton(
            destination,
            text=self._t("choose_folder"),
            width=125,
            height=40,
            fg_color=self.COLORS["panel_muted"],
            text_color=self.COLORS["text"],
            hover_color=self.COLORS["border"],
            command=self._choose_output_directory,
        )
        self.browse_folder_button.grid(row=1, column=1)

        status = ctk.CTkFrame(
            card,
            fg_color=self.COLORS["panel_muted"],
            corner_radius=12,
        )
        status.grid(row=4, column=0, sticky="nsew", padx=30, pady=(0, 20))
        status.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            status,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.COLORS["text"],
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 2))
        ctk.CTkLabel(
            status,
            textvariable=self.detail_var,
            font=ctk.CTkFont(size=11),
            text_color=self.COLORS["muted"],
            anchor="w",
            wraplength=500,
        ).grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 15))
        self.progress_bar = ctk.CTkProgressBar(
            status,
            height=4,
            mode="indeterminate",
        )
        self.progress_bar.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 18),
        )
        self.progress_bar.set(0)

        self.convert_button = ctk.CTkButton(
            card,
            text=self._t("convert"),
            height=48,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._start_conversion,
        )
        self.convert_button.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=30,
            pady=(0, 30),
        )

    def _build_selector(
        self,
        parent: ctk.CTkFrame,
        column: int,
        label: str,
        values: list[str],
        variable: ctk.StringVar,
        command: Callable[[str], None],
    ) -> None:
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        padding = (0, 8) if column == 0 else (8, 0)
        wrapper.grid(row=0, column=column, sticky="ew", padx=padding)
        ctk.CTkLabel(
            wrapper,
            text=label,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.COLORS["muted"],
        ).pack(anchor="w", pady=(0, 7))
        ctk.CTkComboBox(
            wrapper,
            values=values,
            variable=variable,
            width=180,
            height=40,
            state="readonly",
            command=command,
        ).pack(fill="x")

    def _change_theme(self, theme: str) -> None:
        if theme not in THEMES or theme == getattr(
            self,
            "_active_theme",
            None,
        ):
            return
        self._active_theme = theme
        ctk.set_default_color_theme(theme)
        self._build_ui()

    def _change_language(self, language: str) -> None:
        if language not in LANGUAGES:
            return
        self._active_language = language
        self._sync_display_values()
        self._build_ui()

    def _input_type_changed(self, selected: str) -> None:
        self.input_type_key = (
            AUTO_DETECT
            if selected == self._input_label(AUTO_DETECT)
            else selected
        )

    def _output_format_changed(self, selected: str) -> None:
        for output_format in OUTPUT_FORMATS:
            if selected == self._output_label(output_format):
                self.output_format_key = output_format
                return

    def _choose_source(self) -> None:
        selected = filedialog.askopenfilename(
            title=self._t("source_dialog_title"),
            filetypes=FILE_DIALOG_TYPES,
        )
        if not selected:
            return
        self.source_var.set(selected)
        detected_type = detect_input_type(selected)
        self.input_type_key = detected_type
        self.input_type_var.set(self._input_label(detected_type))
        self.output_directory_var.set(str(Path(selected).parent))
        self.status_var.set(self._t("source_ready"))
        self.detail_var.set(
            self._t(
                "detected_detail",
                input_type=self._input_label(detected_type),
            )
        )

    def _choose_output_directory(self) -> None:
        selected = filedialog.askdirectory(
            title=self._t("folder_dialog_title")
        )
        if selected:
            self.output_directory_var.set(selected)

    def _start_conversion(self) -> None:
        source = Path(self.source_var.get().strip()).expanduser()
        input_type = self.input_type_key
        output_format = self.output_format_key
        if not source.is_file():
            messagebox.showerror(
                APP_TITLE,
                self._t("choose_source_error"),
            )
            return
        if not input_type_matches(source, input_type):
            messagebox.showerror(
                APP_TITLE,
                self._t(
                    "input_type_error",
                    input_type=self._input_label(input_type),
                ),
            )
            return

        output_directory = Path(
            self.output_directory_var.get().strip() or source.parent
        ).expanduser()
        try:
            output_directory.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            messagebox.showerror(
                APP_TITLE,
                self._t("output_folder_error", error=str(error)),
            )
            return
        output_path = build_output_path(
            source,
            output_directory,
            output_format,
        )
        if output_path.exists() and not messagebox.askyesno(
            APP_TITLE,
            self._t("overwrite", filename=output_path.name),
        ):
            return

        self._set_busy(
            True,
            self._t("converting", filename=source.name),
            self._t("converting_detail"),
        )
        worker = threading.Thread(
            target=self._convert_in_background,
            args=(source, output_path, output_format),
            daemon=True,
        )
        worker.start()

    def _convert_in_background(
        self,
        source_path: Path,
        output_path: Path,
        output_format: str,
    ) -> None:
        try:
            from docling.document_converter import DocumentConverter

            result = DocumentConverter().convert(source_path)
            document = result.document
            if output_format == "JSON":
                content = json.dumps(
                    document.export_to_dict(),
                    ensure_ascii=False,
                    indent=2,
                )
                output_path.write_text(content, encoding="utf-8")
            elif output_format == "Text":
                output_path.write_text(
                    document.export_to_markdown(strict_text=True),
                    encoding="utf-8",
                )
            elif output_format == "Markdown":
                output_path.write_text(
                    document.export_to_markdown(),
                    encoding="utf-8",
                )
            else:
                document.save_as_html(output_path)
        except Exception as error:
            # Docling can surface backend-specific errors.
            self.after(0, self._conversion_failed, error)
        else:
            self.after(0, self._conversion_succeeded, output_path)

    def _set_busy(
        self,
        busy: bool,
        status: str = "",
        detail: str = "",
    ) -> None:
        self._is_converting = busy
        state = "disabled" if busy else "normal"
        self.convert_button.configure(state=state)
        self.browse_file_button.configure(state=state)
        self.browse_folder_button.configure(state=state)
        self.source_entry.configure(state=state)
        self.output_entry.configure(state=state)
        self.theme_box.configure(state=state)
        self.language_box.configure(state=state)
        if busy:
            self.progress_bar.start()
            self.status_var.set(status)
            self.detail_var.set(detail)
        else:
            self.progress_bar.stop()
            self.progress_bar.set(0)

    def _conversion_succeeded(self, output_path: Path) -> None:
        self._set_busy(False)
        self.status_var.set(self._t("complete"))
        self.detail_var.set(
            self._t(
                "saved",
                filename=output_path.name,
                directory=str(output_path.parent),
            )
        )
        messagebox.showinfo(
            APP_TITLE,
            self._t("created", filename=output_path.name),
        )

    def _conversion_failed(self, error: Exception) -> None:
        self._set_busy(False)
        self.status_var.set(self._t("failed"))
        self.detail_var.set(self._t("failed_detail"))
        messagebox.showerror(
            APP_TITLE,
            self._t("failed_dialog", error=str(error)),
        )


def main() -> None:
    """Start the Docs to Text desktop application."""
    app = DocsToTextApp()
    app.mainloop()


if __name__ == "__main__":
    main()
