from hypothesis import given, strategies as st, settings
import pytest

from pbt import is_valid_name

# テスト設定: 各テストで1000回のランダムなケースを実行する
# デフォルトは100回だが、より多くのエッジケースを発見するため増やしている
@settings(max_examples=1000)
@given(st.text(min_size=1))  # 任意のUnicode文字列を生成して入力とする（1文字以上）
def test_name_validation_logs(name):
    """
    Property-Based Test 1: 任意の文字列に対するバリデーション検証
    
    目的: 文字列に不正な文字が含まれる場合は失敗し、有効な文字のみの場合は成功することを確認
    戦略: 完全にランダムなUnicode文字列を生成し、文字の有効性に応じて適切な結果を期待
    """
    #print(f"\nテスト文字列: {name}")  # デバッグ用（必要に応じてコメントアウト）
    
    # 不正な文字があるかどうかを判定
    has_invalid_char = False
    for c in name:
        # 長音記号（ー）、ひらがな（\u3040-\u309F）、カタカナ（\u30A0-\u30FF）以外の文字があるかチェック
        if c not in "ー" and not ('\u3040' <= c <= '\u309F' or '\u30A0' <= c <= '\u30FF'):
            has_invalid_char = True
            break  # 一つでも不正な文字があれば十分
    
    # 不正な文字がある場合は失敗すべき、ない場合は成功すべき
    if has_invalid_char:
        assert not is_valid_name(name), f"不正な文字を含む文字列 '{name}' がバリデーションを通過しました"
    else:
        assert is_valid_name(name), f"有効な文字のみの文字列 '{name}' がバリデーションに失敗しました"

# ///////////////////////////////////////////////////////////////////////////////////////////////



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

@settings(max_examples=1000)  # こちらも1000回テストを実行
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


# ///////////////////////////////////////////////////////////////////////////////////////////////

# ひらがな、カタカナ、長音記号が混在した文字列を生成するための戦略
# 全ての有効な文字を組み合わせたアルファベットを作成
mixed_japanese_alphabet = (
    st.characters(min_codepoint=0x3040, max_codepoint=0x309F) |  # ひらがな
    st.characters(min_codepoint=0x30A0, max_codepoint=0x30FF) |  # カタカナ
    st.just("ー")  # 長音記号
)

# 混在した文字列を生成（ひらがな、カタカナ、長音記号が混じった状態）
mixed_japanese_name = st.text(
    alphabet=mixed_japanese_alphabet,
    min_size=2  # 最低2文字で混在を確認しやすくする
)

@settings(max_examples=1000)  # 1000回テストを実行
@given(mixed_japanese_name)  # 上で定義した混在文字列を入力とする
def test_name_validation_accepts_mixed_japanese(name):
    """
    Property-Based Test 3: ひらがな・カタカナ混在文字列の検証
    
    目的: ひらがな、カタカナ、長音記号が混在した文字列でも
          必ずバリデーションを通過することを確認
    戦略: ひらがな、カタカナ、長音記号を組み合わせた文字列を生成してテスト
    
    例: "あいうエオー"、"カタかな"、"ひらガナー" など
    """
    # 混在した日本語文字列も必ずバリデーションを通過すべき
    assert is_valid_name(name)
