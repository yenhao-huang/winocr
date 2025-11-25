# OCR Tool

使用 Windows.Media.Ocr API 進行圖片文字辨識

## 安裝

```bash
pip install pillow 
Add-WindowsCapability -Online -Name "Language.OCR~~~en-US~0.0.1.0
```

輸出格式
多個 dict
```
{
  'as_': {},
  'text': '經 濟 部 商 業 司 函',
  'words': [
    {
      'as_': {},
      'bounding_rect': {
        'height': 18.0,
        'unpack': {},
        'width': 22.0,
        'x': 266.0,
        'y': 86.0
      },
      'text': '經'
    },
    ...
  ]
}
```