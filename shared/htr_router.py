import os, json, subprocess, tempfile
from pathlib import Path
from shared.crawler import download

def paddle_ocr(image_path: Path) -> str:
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang='latin', show_log=False)
    result = ocr.ocr(str(image_path), cls=True)
    return "\n".join([line[1][0] for line in result])

def transkribus_ocr(image_path: Path) -> str:
    # stub – real implementation will use Transkribus PyClient
    return "transkribus dummy text"

def route(image_path: Path, engine: str = "auto") -> str:
    if engine == "paddle":
        return paddle_ocr(image_path)
    elif engine == "transkribus":
        return transkribus_ocr(image_path)
    else:  # auto – use paddle for now
        return paddle_ocr(image_path)