# Docs to Text - English

Docs to Text is a small desktop converter built with Python 3.13, CustomTkinter,
and Docling. It converts supported documents, images, and audio files into
JSON, plain text, Markdown, or HTML without uploading them anywhere.

## Install UV

macOS and Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```Powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Reference: https://docs.astral.sh/uv/getting-started/installation/

## Run app

```bash
uv run python main.py
```

Choose a source file, confirm the detected input type, select an output format,
and click **Convert file**. The output is written beside the source by default;
you can choose another folder before converting.

The interface starts in Brazilian Portuguese (`pt-BR`). Use the language
selector in the header to switch to English at any time.

Supported inputs: PDF, PPTX, JPEG, PNG, TIFF, WEBP, BMP, MP3, and WAV.

The Docling audio pipeline may download its speech-recognition assets the first
time an audio file is converted.


# Docs to Text - Português (Brasil)

Docs to Text é um pequeno conversor desktop desenvolvido com Python 3.13,
CustomTkinter e Docling. Ele converte documentos, imagens e arquivos de áudio
compatíveis para JSON, texto simples, Markdown ou HTML sem enviar arquivos para
nenhum serviço externo.

## Instalar o UV

macOS e Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Referência: https://docs.astral.sh/uv/getting-started/installation/

## Executar o app

```bash
uv run python main.py
```

Escolha um arquivo de origem, confirme o tipo de entrada detectado, selecione o
formato de saída e clique em **Converter arquivo**. Por padrão, o resultado é
salvo ao lado do arquivo de origem, mas você pode escolher outra pasta antes da
conversão.

A interface começa em português do Brasil (`pt-BR`). Use o seletor de idioma no
cabeçalho para alternar para o inglês a qualquer momento.

Entradas compatíveis: PDF, PPTX, JPEG, PNG, TIFF, WEBP, BMP, MP3 e WAV.

O pipeline de áudio do Docling pode baixar os recursos de reconhecimento de fala
na primeira vez que um arquivo de áudio for convertido.
