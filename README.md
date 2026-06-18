<div align="center">

<img src="assets/logo.png" alt="Wavium Logo" width="96"/>

# Wavium

**The best audio converter ever made. By artists, for artists.**





</div>

***

## What is Wavium?

Wavium is a Windows desktop application that lets you download videos and audio from YouTube quickly and effortlessly. Built specifically for musicians and producers who need high-quality audio extraction directly into their workflow.

- 🎵 Extract audio as **WAV, MP3, M4A**
- 🎬 Download video in **up to 1080p** MP4
- ⚡ **Auto-updates** yt-dlp on every launch
- 🖥️ Clean, minimal interface built with **PySide6**
- 📦 **Single executable** — no installation, no dependencies

***

## Screenshots

> *Coming soon*

***

## Download

Grab the latest executable from [Releases](https://github.com/tu-usuario/wavium/releases/latest) — no Python or installation required.

| Version | Platform | Download |
|---|---|---|
| Beta v0.2 | Windows 10/11 (64-bit) | [Wavium Beta v0.2.exe](https://github.com/tu-usuario/wavium/releases/latest) |

***

## Usage

1. Paste a YouTube URL into the input field
2. Click **Get info** to load the video metadata
3. Choose a mode: **Audio only** or **Video**
4. Select a destination folder
5. Click **Download**

***

## Build from source

### Requirements

- Python 3.10 or higher
- `ffmpeg.exe` and `yt-dlp.exe` placed inside the `assets/` folder

```bash
# 1. Clone the repository
git clone https://github.com/tu-usuario/wavium.git
cd wavium

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download external binaries
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe -o assets/yt-dlp.exe
# ffmpeg.exe → https://ffmpeg.org/download.html → copy to assets/

# 4. Build
python -m PyInstaller --onefile --noconsole --name "Wavium Beta v0.2" --add-data "assets;assets" --icon "assets/logo.ico" main.py
```

### Project structure

```
wavium/
├── main.py                  # Entry point
├── requirements.txt
├── assets/
│   ├── logo.png
│   ├── logo.ico
│   ├── ffmpeg.exe           # Not included in the repo
│   └── yt-dlp.exe           # Not included in the repo
├── core/
│   ├── __init__.py
│   ├── downloader.py        # Download logic via yt-dlp
│   ├── extractor.py         # Metadata and format extraction
│   └── validator.py         # URL validation
└── gui/
    ├── main_window.py       # Main window
    ├── workers.py           # QThreads for async downloads
    └── styles.py            # QSS stylesheets
```

***

## Dependencies

| Package | Purpose |
|---|---|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Download engine |
| [PySide6](https://doc.qt.io/qtforpython/) | GUI framework |
| [ffmpeg](https://ffmpeg.org/) | Audio/video conversion |
| [PyInstaller](https://pyinstaller.org/) | Executable packaging |

***

## Legal

Wavium is open-source software distributed under the **GNU GPLv3** license.

Using this tool to download copyright-protected content without the rights holder's permission may violate applicable law. The author takes no responsibility for how the application is used. Only download content you have the right to access.

***

## Contributing

Contributions are welcome. Open an [issue](https://github.com/tu-usuario/wavium/issues) to report bugs or suggest improvements, or submit a pull request directly.

***

<div align="center">

Made with ♥ by [tu-usuario](https://github.com/tu-usuario)

</div>
