import asyncio
from PIL import Image
import winrt.windows.media.ocr as ocr
import winrt.windows.globalization as globalization
import winrt.windows.graphics.imaging as imaging
from winrt.windows.storage.streams import InMemoryRandomAccessStream
import io
import os
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from tqdm import tqdm


class WinOCR:
    """Windows.Media.Ocr 封裝類別"""

    def __init__(self, language_code: str = "zh-Hant"):
        """
        初始化 OCR 引擎

        Args:
            language_code: 語言代碼 (例如: "ja", "en", "zh-Hant", "zh-Hans")
        """
        self.language_code = language_code
        self.ocr_engine = None

        self._init_engine()


    def _init_engine(self):
        """初始化 OCR 引擎"""
        if self.ocr_engine is None:
            language = globalization.Language(self.language_code)
            self.ocr_engine = ocr.OcrEngine.try_create_from_language(language)

            if self.ocr_engine is None:
                available_languages = [lang.display_name for lang in ocr.OcrEngine.available_recognizer_languages]
                raise RuntimeError(f"無法為語言 '{self.language_code}' 創建 OCR 引擎。可用語言: {available_languages}")

    async def _recognize_pil_async(self, image: Image.Image) -> str:
        """
        非同步辨識 PIL Image

        Args:
            image: PIL Image 物件

        Returns:
            辨識出的文字內容
        """
        # 將 PIL Image 轉換為字節流
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # 創建 InMemoryRandomAccessStream & 轉成 bitmap
        stream = InMemoryRandomAccessStream()
        writer = stream.get_output_stream_at(0)
        await writer.write_async(img_byte_arr.read())
        await writer.flush_async()

        decoder = await imaging.BitmapDecoder.create_async(stream)
        software_bitmap = await decoder.get_software_bitmap_async()

        # 執行 OCR
        result = await self.ocr_engine.recognize_async(software_bitmap)

        # 組合文字結果
        lines = []
        for line in result.lines:
            lines.append(line.text)

        return "\n".join(lines)

    def recognize_image(self, image_path: str) -> str:
        """
        辨識圖片檔案中的文字

        Args:
            image_path: 圖片檔案路徑

        Returns:
            辨識出的文字內容
        """
        image = Image.open(image_path)
        return asyncio.run(self._recognize_pil_async(image))

    def load_images_recursive(self, directory: str, extensions: tuple = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')) -> List[str]:
        """
        遞迴載入目錄中的所有圖片檔案

        Args:
            directory: 目錄路徑
            extensions: 圖片副檔名

        Returns:
            圖片檔案路徑列表
        """
        image_paths = []
        directory_path = Path(directory)

        for ext in extensions:
            image_paths.extend([str(p) for p in directory_path.rglob(f'*{ext}')])

        return sorted(image_paths)

    def batch_recognize_images(self, image_paths: List[str]) -> List[Dict[str, str]]:
        """
        批次辨識多張圖片

        Args:
            image_paths: 圖片檔案路徑列表

        Returns:
            辨識結果列表，格式為 [{"image_url": "xxx", "ocr_result": "xxx"}, ...]
        """
        results = []

        for image_path in tqdm(image_paths, desc="OCR 辨識進度"):
            try:
                ocr_result = self.recognize_image(image_path)
                results.append({
                    "image_url": image_path,
                    "ocr_result": ocr_result
                })
                print(f"✓ 已辨識: {image_path}")
            except Exception as e:
                print(f"✗ 辨識失敗: {image_path}, 錯誤: {e}")
                results.append({
                    "image_url": image_path,
                    "ocr_result": f"ERROR: {str(e)}"
                })

        return results

    def save_results(self, results: List[Dict[str, str]], o_dir: str, filename: str = None) -> str:
        """
        儲存辨識結果到指定目錄

        Args:
            results: 辨識結果列表
            o_dir: 輸出目錄路徑
            filename: 檔案名稱 (不含副檔名)，若為 None 則使用時間戳記

        Returns:
            儲存的檔案路徑
        """
        # 建立輸出目錄
        output_dir = Path(o_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 產生檔案名稱
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ocr_results_{timestamp}"

        # 儲存為 JSON
        output_path = output_dir / f"{filename}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"✓ 已儲存結果到: {output_path}")
        return str(output_path)

    @staticmethod
    def get_available_languages() -> List[str]:
        """取得可用的 OCR 語言"""
        return [(lang.language_tag, lang.display_name) for lang in ocr.OcrEngine.available_recognizer_languages]