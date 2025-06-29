# 日本語名前検証 PBT プロジェクト

このプロジェクトは、日本語（ひらがな・カタカナ）の名前を検証する機能を、Property-Based Testing（PBT）を使用して徹底的にテストするサンプルプロジェクトです。

## 概要

日本語の名前が正しい文字（ひらがな、カタカナ、長音記号）のみで構成されているかを検証する機能を提供し、Hypothesisライブラリを使用した property-based testing で品質を保証します。

## ファイル構成

- `pbt.py` - 日本語名前検証の実装
- `test_pbt.py` - Property-Based Testing のテストケース
- `README.md` - このファイル

## 機能

### `is_valid_name(name: str) -> bool`

指定された文字列が有効な日本語の名前かどうかを判定します。

**有効な文字:**
- ひらがな（あ〜ん）
- カタカナ（ア〜ン）
- 長音記号（ー）
- 濁点・半濁点を含む

**例:**
```python
from pbt import is_valid_name

# 有効な名前
print(is_valid_name("たなか"))     # True
print(is_valid_name("タナカ"))     # True
print(is_valid_name("たーち"))     # True
print(is_valid_name("づけ"))       # True（濁点含む）

# 無効な名前
print(is_valid_name("田中"))       # False（漢字）
print(is_valid_name("tanaka"))     # False（英字）
print(is_valid_name("12345"))      # False（数字）
print(is_valid_name(""))           # False（空文字）
```

## セットアップ

### 前提条件

- Python 3.7以上

### インストール

```bash
# 依存関係のインストール
pip install hypothesis pytest
```

## テストの実行

### 基本的なテスト実行

```bash
# 全テストの実行
pytest test_pbt.py

# 詳細なログ出力付きでテスト実行
pytest test_pbt.py -s
```

### Property-Based Testing について

このプロジェクトでは、以下の2つの property-based test を実装しています：

1. **`test_name_validation_logs`**
   - 任意のUnicode文字列を入力として使用
   - 日本語以外の文字が含まれている場合は必ず失敗することを確認
   - 各文字のUnicode詳細をログ出力

2. **`test_name_validation_accepts_valid_japanese`**
   - 有効な日本語文字のみで構成された文字列を生成
   - 生成された文字列が必ず検証を通過することを確認

### テスト例

```bash
# 詳細なログ出力でテスト実行
pytest test_pbt.py::test_name_validation_logs -s

# 特定のテストのみ実行
pytest test_pbt.py::test_name_validation_accepts_valid_japanese -v
```

## 技術的な詳細

### 正規表現パターン

```python
HIRAGANA_KATAKANA_PATTERN = re.compile(r'^[\u3040-\u309F\u30A0-\u30FFー]+$')
```

- `\u3040-\u309F`: ひらがなの範囲
- `\u30A0-\u30FF`: カタカナの範囲
- `ー`: 長音記号

### Property-Based Testing の利点

1. **包括的なテスト:** 手動では思いつかない多様な入力パターンでテスト
2. **エッジケースの発見:** 予期しない境界値での動作を自動的に検証
3. **回帰テストの強化:** 変更後も同じ性質が保たれることを確認

## 開発者向け情報

### 新しいテストケースの追加

```python
@given(st.text(alphabet=your_custom_alphabet))
def test_your_property(input_text):
    # あなたのテストロジック
    assert some_property(input_text)
```

### カスタム戦略の使用

```python
# 特定の文字セットを使用した文字列生成
custom_strategy = st.text(
    alphabet=st.characters(
        min_codepoint=0x3040, 
        max_codepoint=0x309F
    ),
    min_size=1,
    max_size=10
)
```

## ライセンス

このプロジェクトはサンプルコードとして提供されています。

## 貢献

バグ報告や機能改善の提案は、GitHubのIssueまたはPull Requestでお気軽にお寄せください。 