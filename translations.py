"""Localized user-facing strings for the Docs to Text application."""

LANGUAGES = ("pt-BR", "English")

TRANSLATIONS: dict[str, dict[str, str]] = {
    "pt-BR": {
        "tagline": "Converta sem complicação",
        "theme_label": "TEMA DE CORES",
        "language_label": "IDIOMA",
        "workflow_kicker": "UM FLUXO LOCAL E SIMPLES",
        "workflow_title": "Da fonte\npara texto útil.",
        "workflow_description": (
            "O Docling faz o trabalho pesado enquanto este espaço "
            "mantém o processo claro."
        ),
        "step_source": "Escolha uma fonte",
        "step_source_description": "PDF, apresentação, imagem ou áudio",
        "step_format": "Escolha um formato",
        "step_format_description": "JSON, texto, Markdown ou HTML",
        "step_convert": "Converta localmente",
        "step_convert_description": "Seus arquivos ficam neste dispositivo",
        "supported": (
            "FORMATOS\nPDF  /  PPTX  /  JPG  /  PNG\n"
            "TIFF  /  WEBP  /  BMP\nMP3  /  WAV"
        ),
        "setup_kicker": "CONFIGURAÇÃO DA CONVERSÃO",
        "setup_title": "Selecione o que deseja transformar",
        "source_label": "ARQUIVO DE ORIGEM",
        "source_placeholder": (
            "Escolha um PDF, imagem, apresentação ou arquivo de áudio"
        ),
        "browse": "Procurar",
        "input_label": "TIPO DE ENTRADA",
        "output_label": "FORMATO DE SAÍDA",
        "output_folder_label": "PASTA DE SAÍDA",
        "output_folder_placeholder": (
            "Deixe vazio para usar a pasta do arquivo de origem"
        ),
        "choose_folder": "Escolher pasta",
        "convert": "Converter arquivo",
        "ready": "Pronto quando você estiver",
        "ready_detail": "Escolha um arquivo para começar",
        "auto_detect": "Detecção automática",
        "output_json": "JSON",
        "output_text": "Texto",
        "output_markdown": "Markdown",
        "output_html": "HTML",
        "source_ready": "Origem pronta",
        "detected_detail": (
            "Entrada detectada: {input_type}. "
            "Escolha um formato de saída e converta."
        ),
        "choose_source_error": (
            "Escolha primeiro um arquivo de origem existente."
        ),
        "input_type_error": (
            "O arquivo selecionado não corresponde ao tipo de entrada "
            "{input_type}."
        ),
        "output_folder_error": (
            "Não foi possível usar a pasta de saída:\n{error}"
        ),
        "overwrite": "{filename} já existe. Deseja substituí-lo?",
        "converting": "Convertendo {filename}",
        "converting_detail": (
            "O Docling está lendo e estruturando seu arquivo."
        ),
        "complete": "Conversão concluída",
        "saved": "Salvo {filename} em {directory}",
        "created": "{filename} foi criado.",
        "failed": "A conversão não pôde ser concluída",
        "failed_detail": "Verifique o arquivo de origem e tente novamente.",
        "failed_dialog": (
            "O Docling não conseguiu converter este arquivo:\n{error}"
        ),
        "source_dialog_title": "Escolha um arquivo de origem",
        "folder_dialog_title": "Escolha uma pasta de saída",
    },
    "English": {
        "tagline": "Convert without the clutter",
        "theme_label": "ACCENT THEME",
        "language_label": "LANGUAGE",
        "workflow_kicker": "A SMALL, LOCAL WORKFLOW",
        "workflow_title": "From source\nto usable text.",
        "workflow_description": (
            "Docling handles the heavy lifting while this focused workspace "
            "keeps the process clear."
        ),
        "step_source": "Pick a source",
        "step_source_description": "PDF, presentation, image, or audio",
        "step_format": "Choose a format",
        "step_format_description": "JSON, text, Markdown, or HTML",
        "step_convert": "Convert locally",
        "step_convert_description": "Your files stay on this device",
        "supported": (
            "SUPPORTED\nPDF  /  PPTX  /  JPG  /  PNG\n"
            "TIFF  /  WEBP  /  BMP\nMP3  /  WAV"
        ),
        "setup_kicker": "CONVERSION SETUP",
        "setup_title": "Select what you want to transform",
        "source_label": "SOURCE FILE",
        "source_placeholder": (
            "Choose a PDF, image, presentation, or audio file"
        ),
        "browse": "Browse",
        "input_label": "INPUT TYPE",
        "output_label": "OUTPUT FORMAT",
        "output_folder_label": "OUTPUT FOLDER",
        "output_folder_placeholder": "Leave empty to use the source folder",
        "choose_folder": "Choose folder",
        "convert": "Convert file",
        "ready": "Ready when you are",
        "ready_detail": "Choose a file to begin",
        "auto_detect": "Auto detect",
        "output_json": "JSON",
        "output_text": "Text",
        "output_markdown": "Markdown",
        "output_html": "HTML",
        "source_ready": "Source ready",
        "detected_detail": (
            "Detected input: {input_type}. "
            "Choose an output format and convert."
        ),
        "choose_source_error": "Choose an existing source file first.",
        "input_type_error": (
            "The selected file does not match the {input_type} input type."
        ),
        "output_folder_error": "Could not use the output folder:\n{error}",
        "overwrite": "{filename} already exists. Replace it?",
        "converting": "Converting {filename}",
        "converting_detail": "Docling is reading and structuring your file.",
        "complete": "Conversion complete",
        "saved": "Saved {filename} in {directory}",
        "created": "Created {filename}.",
        "failed": "Conversion could not be completed",
        "failed_detail": "Check the source file and try again.",
        "failed_dialog": "Docling could not convert this file:\n{error}",
        "source_dialog_title": "Choose a source file",
        "folder_dialog_title": "Choose an output folder",
    },
}
