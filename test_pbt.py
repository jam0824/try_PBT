from hypothesis import given, strategies as st, settings
import pytest
import unicodedata

from pbt import is_valid_name

# Unicodeの任意の文字列を生成
def show_unicode_detail(s):
    for c in s:
        print(f"  '{c}': U+{ord(c):04X} {unicodedata.name(c, 'UNKNOWN')}")

@settings(max_examples=1000)
@given(st.text())
def test_name_validation_logs(name):
    #print(f"\n🧪 テスト文字列: {name}")
    #show_unicode_detail(name)
    for c in name:
        if c not in "ー" and not ('\u3040' <= c <= '\u309F' or '\u30A0' <= c <= '\u30FF'):
            #print("🚨 非対応文字検出 → バリデーションに失敗すべき")
            assert not is_valid_name(name)
            break

# カタカナ・ひらがなのみで構成された名前を生成して通過を確認
katakana = st.text(alphabet=st.characters(min_codepoint=0x30A0, max_codepoint=0x30FF) | st.just("ー"), min_size=1)
hiragana = st.text(alphabet=st.characters(min_codepoint=0x3040, max_codepoint=0x309F), min_size=1)
japanese_name = st.one_of(katakana, hiragana)


@settings(max_examples=1000)
@given(japanese_name)
def test_name_validation_accepts_valid_japanese(name):
    assert is_valid_name(name)
