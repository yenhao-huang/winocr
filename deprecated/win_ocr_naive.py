import asyncio
from winrt.windows.media.ocr import OcrEngine
from winrt.windows.globalization import Language
from winrt.windows.storage.streams import DataWriter
from winrt.windows.graphics.imaging import SoftwareBitmap, BitmapPixelFormat

def recognize_bytes(bytes, width, height, lang='en'):
    cmd = 'Add-WindowsCapability -Online -Name "Language.OCR~~~en-US~0.0.1.0"'
    assert OcrEngine.is_language_supported(Language(lang)), cmd
    writer = DataWriter()
    writer.write_bytes(bytes)
    sb = SoftwareBitmap.create_copy_from_buffer(writer.detach_buffer(), BitmapPixelFormat.RGBA8, width, height)
    return OcrEngine.try_create_from_language(Language(lang)).recognize_async(sb)

def recognize_pil(img, lang='en'):
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    return recognize_bytes(img.tobytes(), img.width, img.height, lang)

def picklify(o):
    if hasattr(o, 'size'):
        print("1")
        return [picklify(e) for e in o]
    elif hasattr(o, '__module__'):
        print("2")
        return dict([(n, picklify(getattr(o, n))) for n in dir(o) if not n.startswith('_')])
    else:
        print("3")
        return o

async def to_coroutine(awaitable):
    return await awaitable

def recognize_pil_sync(img, lang='en'):
    return picklify(asyncio.run(to_coroutine(recognize_pil(img, lang))))


if __name__ == '__main__':
    from PIL import Image
    img = Image.open('../data/pdf2png/moea/1111207162322696_1/1111207162322696_1_page_0001.png')
    print(recognize_pil_sync(img, "zh-Hant"))