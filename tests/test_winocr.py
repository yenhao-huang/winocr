from lib.winocr import WinOCR

def test_single_image():
    """測試範例"""
    # 測試從檔案路徑辨識
    image_path = "tests/testcases/test3.png"

    print("使用 Windows.Media.Ocr 進行文字辨識...")
    print("=" * 50)

    # 方法 1: 直接從檔案路徑辨識
    ocr_engine = WinOCR("zh-Hant")
    text1 = ocr_engine.recognize_image(image_path)
    print("方法 1 - 從檔案路徑辨識:")
    print(text1)
    print()

    # 列出可用的語言
    print("可用的 OCR 語言:")
    print(ocr_engine.get_available_languages())

def test_batch_image():
    """測試範例"""
    # 測試從檔案路徑辨識
    image_path = "tests/testcases"

    print("使用 Windows.Media.Ocr 進行文字辨識...")
    print("=" * 50)

    # 方法 1: 直接從檔案路徑辨識
    ocr_engine = WinOCR("zh-Hant")
    img_paths = ocr_engine.load_images_recursive(image_path)
    results = ocr_engine.batch_recognize_images(img_paths)
    ocr_engine.save_results(results, "tests/results", "batch_results")
    print("方法 1 - 從檔案路徑辨識:")
    print(results)


if __name__ == "__main__":
    print("=============TEST SINGLE IMAGE=============")
    test_single_image()
    print("=============TEST BATCH IMAGE=============")
    test_batch_image()
