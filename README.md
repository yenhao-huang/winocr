# OCR Tool

基於 Windows.Media.Ocr API 的圖片文字辨識工具，支援批次處理與多語言辨識。

## 安裝

### 系統需求

- Windows 10/11
- Python 3.7+

### 安裝步驟

1. 安裝 Python 依賴套件：

```bash
pip install pillow winrt tqdm
```

2. 安裝 Windows OCR 語言包（以繁體中文為例）：

```powershell
# 以管理員身份執行 PowerShell
Add-WindowsCapability -Online -Name "Language.OCR~~~zh-TW~0.0.1.0"
```

其他語言包：
- 英文：`Language.OCR~~~en-US~0.0.1.0`
- 日文：`Language.OCR~~~ja-JP~0.0.1.0`
- 簡體中文：`Language.OCR~~~zh-CN~0.0.1.0`

查詢可用語言包：

```bash
python -m core.main --list-languages
```

## 使用方法

### CLI 命令列工具

基本用法：

```bash
# 使用預設設定（輸入目錄：data，輸出目錄：results，語言：zh-Hant）
python -m core.main

# 指定輸入目錄
python -m core.main --in_dir ./images

# 指定輸入和輸出目錄
python -m core.main --in_dir ./images --o_dir ./output

# 指定語言（繁體中文）
python -m core.main --language zh-Hant

# 指定圖片副檔名
python -m core.main --extensions .png .jpg

# 指定輸出檔案名稱
python -m core.main --filename my_ocr_results

# 列出所有可用的 OCR 語言
python -m core.main --list-languages
```

### Python API

```python
from lib.winocr import WinOCR

# 初始化 OCR 引擎
ocr_engine = WinOCR(language_code="zh-Hant")

# 方法 1: 辨識單張圖片
text = ocr_engine.recognize_image("path/to/image.png")
print(text)

# 方法 2: 批次辨識多張圖片
# 載入目錄中的所有圖片
image_paths = ocr_engine.load_images_recursive("path/to/images")

# 批次辨識
results = ocr_engine.batch_recognize_images(image_paths)

# 儲存結果為 JSON
ocr_engine.save_results(results, o_dir="output", filename="ocr_results")

# 查詢可用語言
languages = WinOCR.get_available_languages()
for lang_tag, lang_name in languages:
    print(f"{lang_tag}: {lang_name}")
```

### 進階範例

參考 [tests/test_winocr.py](tests/test_winocr.py) 查看更多使用範例。

```bash
# 執行測試
python tests/test_winocr.py
```

## 專案結構

```
ocr_tool/
├── core/                   # 核心應用程式
│   ├── __init__.py
│   └── main.py            # CLI 主程式
├── lib/                   # 核心函式庫
│   └── winocr.py          # WinOCR 主要模組
├── tests/                 # 測試檔案
│   ├── __init__.py
│   ├── test_winocr.py     # 測試腳本
│   └── testcases/         # 測試用圖片
├── data/                  # 預設輸入目錄
├── results/               # 預設輸出目錄
├── deprecated/            # 已棄用的舊版本
└── README.md             # 專案說明文件
```

## 主要模組說明

### lib/winocr.py

`WinOCR` 類別是本專案的核心模組，封裝了 Windows.Media.Ocr API 的功能。

#### 主要功能

- **初始化 OCR 引擎**：支援多語言設定
- **單圖辨識**：`recognize_image(image_path)` - 辨識單張圖片
- **批次辨識**：`batch_recognize_images(image_paths)` - 批次處理多張圖片
- **遞迴載入圖片**：`load_images_recursive(directory)` - 自動載入目錄中所有圖片
- **結果儲存**：`save_results(results, o_dir, filename)` - 將結果儲存為 JSON
- **查詢可用語言**：`get_available_languages()` - 靜態方法，列出系統支援的 OCR 語言

#### 核心依賴

```python
import winrt.windows.media.ocr as ocr
import winrt.windows.globalization as globalization
import winrt.windows.graphics.imaging as imaging
from winrt.windows.storage.streams import InMemoryRandomAccessStream
```

這些是 Windows Runtime (WinRT) API 的 Python 綁定，提供存取 Windows 原生 OCR 功能的介面。

## 輸出格式

辨識結果以 JSON 格式儲存：

```json
[
  {
    "image_url": "path/to/image1.png",
    "ocr_result": "辨識出的文字內容..."
  },
  {
    "image_url": "path/to/image2.png",
    "ocr_result": "辨識出的文字內容..."
  }
]
```

若辨識失敗，`ocr_result` 會包含錯誤訊息：

```json
{
  "image_url": "path/to/failed.png",
  "ocr_result": "ERROR: 錯誤描述"
}
```

## 參考資源

- [Windows.Media.Ocr API 官方文件](https://learn.microsoft.com/zh-tw/uwp/api/windows.media.ocr?view=winrt-26100)
- [winocr 專案參考](https://github.com/GitHub30/winocr)

## 常見問題

### Q: 辨識結果不準確怎麼辦？

A:
1. 確認圖片清晰度是否足夠
2. 檢查是否使用了正確的語言代碼
3. 嘗試預處理圖片（調整對比度、銳化等）

### Q: 如何安裝更多語言包？

A: 使用 PowerShell 以管理員身份執行：

```powershell
Add-WindowsCapability -Online -Name "Language.OCR~~~<language-code>~0.0.1.0"
```

### Q: 支援哪些圖片格式？

A: 預設支援 `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`，可透過 `--extensions` 參數自訂。

## License

本專案基於 Windows.Media.Ocr API 開發，請遵守相關使用條款。
