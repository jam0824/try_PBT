from hypothesis import given, strategies as st, settings
import pytest

from pbt import is_valid_name

# テスト設定: 各テストで10000回のランダムなケースを実行する
# デフォルトは100回だが、より多くのエッジケースを発見するため増やしている
@settings(max_examples=10000)
@given(st.text())  # 任意のUnicode文字列を生成して入力とする
def test_name_validation_logs(name):
    """
    Property-Based Test 1: 不正な文字が含まれる場合の検証
    
    目的: ひらがな、カタカナ、長音以外の文字が含まれている文字列は必ずバリデーションに失敗することを確認
    戦略: 完全にランダムなUnicode文字列を生成し、ひらがな、カタカナ、長音以外の文字があれば失敗を期待
    """
    #print(f"\nテスト文字列: {name}")  # デバッグ用（必要に応じてコメントアウト）
    
    # 文字列内の各文字をチェック
    for c in name:
        # 長音記号（ー）、ひらがな（\u3040-\u309F）、カタカナ（\u30A0-\u30FF）以外の文字があるかチェック
        if c not in "ー" and not ('\u3040' <= c <= '\u309F' or '\u30A0' <= c <= '\u30FF'):
            # 不正な文字が見つかった場合、バリデーションは失敗すべき
            assert not is_valid_name(name)
            break  # 一つでも不正な文字があれば十分なので、ループを抜ける

# ひらがな、カタカナ、長音記号のみの文字列を生成するためのカスタム戦略を定義

# カタカナ文字（ア〜ン）+ 長音記号（ー）で構成される文字列を生成
katakana = st.text(
    alphabet=st.characters(min_codepoint=0x30A0, max_codepoint=0x30FF) | st.just("ー"), 
    min_size=1  # 最低1文字は含む
)

# ひらがな文字（あ〜ん）で構成される文字列を生成
hiragana = st.text(
    alphabet=st.characters(min_codepoint=0x3040, max_codepoint=0x309F), 
    min_size=1  # 最低1文字は含む
)

# カタカナまたはひらがなのどちらか一方で構成される文字列を生成
japanese_name = st.one_of(katakana, hiragana)

@settings(max_examples=10000)  # こちらも10000回テストを実行
@given(japanese_name)  # 上で定義した文字のみの文字列を入力とする
def test_name_validation_accepts_valid_japanese(name):
    """
    Property-Based Test 2: 正しい文字の場合の検証
    
    目的: 日本語文字（ひらがな、カタカナ、長音記号）のみで構成された文字列は
          必ずバリデーションを通過することを確認
    戦略: 意図的に有効な日本語文字のみを使用した文字列を生成してテスト
    """
    # 生成された日本語文字列は必ずバリデーションを通過すべき
    assert is_valid_name(name)
