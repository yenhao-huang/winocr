import argparse
import sys
from pathlib import Path

# 添加父目錄到路徑以便導入 lib
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.winocr import WinOCR


def main():
    """CLI 主程式"""
    parser = argparse.ArgumentParser(
        description="Windows OCR 批次辨識工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  # 使用預設目錄
  python main.py

  # 指定輸入目錄
  python main.py --in_dir ../data/images

  # 指定輸入和輸出目錄
  python main.py --in_dir ../data/images --o_dir ../output

  # 指定語言
  python main.py --language zh-Hant-TW
        """
    )

    parser.add_argument(
        '--in_dir',
        type=str,
        default='data',
        help='輸入目錄路徑 (預設: data)'
    )

    parser.add_argument(
        '--o_dir',
        type=str,
        default='results',
        help='輸出目錄路徑 (預設: results)'
    )

    parser.add_argument(
        '--language',
        type=str,
        default='zh-Hant',
        help='OCR 語言代碼 (預設: zh-Hant)'
    )

    parser.add_argument(
        '--extensions',
        type=str,
        nargs='+',
        default=['.png', '.jpg', '.jpeg', '.bmp', '.tiff'],
        help='圖片副檔名 (預設: .png .jpg .jpeg .bmp .tiff)'
    )

    parser.add_argument(
        '--filename',
        type=str,
        default=None,
        help='輸出檔案名稱 (不含副檔名)，預設使用時間戳記'
    )

    parser.add_argument(
        '--list-languages',
        action='store_true',
        help='列出所有可用的 OCR 語言'
    )

    args = parser.parse_args()

    # 列出可用語言
    if args.list_languages:
        print("可用的 OCR 語言:")
        for lang_tag, lang_name in WinOCR.get_available_languages():
            print(f"  - {lang_tag}: {lang_name}")
        return

    # 檢查輸入目錄
    in_dir = Path(args.in_dir)
    if not in_dir.exists():
        print(f"錯誤: 輸入目錄不存在: {in_dir}")
        sys.exit(1)

    print("=" * 60)
    print("Windows OCR 批次辨識工具")
    print("=" * 60)
    print(f"輸入目錄: {in_dir.absolute()}")
    print(f"輸出目錄: {args.o_dir}")
    print(f"語言代碼: {args.language}")
    print(f"圖片副檔名: {', '.join(args.extensions)}")
    print("=" * 60)

    try:
        # 初始化 OCR 引擎
        print(f"\n初始化 OCR 引擎 (語言: {args.language})...")
        ocr_engine = WinOCR(language_code=args.language)

        # 載入圖片
        print(f"\n載入圖片從目錄: {in_dir}")
        image_paths = ocr_engine.load_images_recursive(
            str(in_dir),
            extensions=tuple(args.extensions)
        )

        if not image_paths:
            print(f"警告: 在目錄中找不到圖片檔案")
            print(f"支援的副檔名: {', '.join(args.extensions)}")
            sys.exit(0)

        print(f"找到 {len(image_paths)} 張圖片")

        # 批次辨識
        print(f"\n開始批次辨識...")
        print("-" * 60)
        results = ocr_engine.batch_recognize_images(image_paths)

        # 儲存結果
        print("-" * 60)
        print(f"\n辨識完成，共處理 {len(results)} 張圖片")

        output_path = ocr_engine.save_results(
            results,
            o_dir=args.o_dir,
            filename=args.filename
        )

        # 顯示統計
        success_count = sum(1 for r in results if not r['ocr_result'].startswith('ERROR'))
        error_count = len(results) - success_count

        print("\n" + "=" * 60)
        print("處理統計:")
        print(f"  總計: {len(results)} 張")
        print(f"  成功: {success_count} 張")
        print(f"  失敗: {error_count} 張")
        print(f"  結果檔案: {output_path}")
        print("=" * 60)

    except Exception as e:
        print(f"\n錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
