import re

# ひらがな or カタカナのみ許容（濁点・半濁点・長音記号含む）
HIRAGANA_KATAKANA_PATTERN = re.compile(r'^[\u3040-\u309F\u30A0-\u30FFー]+$')

# 失敗を試すときはこちら
#HIRAGANA_KATAKANA_PATTERN = re.compile(r'^[ぁ-んァ-ンー]+$')

def is_valid_name(name: str) -> bool:
    return bool(HIRAGANA_KATAKANA_PATTERN.fullmatch(name))