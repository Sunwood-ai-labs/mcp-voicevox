<div align="center">

![Image](https://github.com/user-attachments/assets/702f7c91-1a23-41f0-8b7a-3ea4ce43ce2c)

# 🎙️ VoiceVox MCP サーバー

</div>


<div align="center">

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pytest](https://img.shields.io/badge/tested%20with-pytest-00AEEF?logo=pytest)](https://pytest.org)

[![GitHub Repo stars](https://img.shields.io/github/stars/Sunwood-ai-labs/mcp-voicevox?style=social)](https://github.com/Sunwood-ai-labs/mcp-voicevox/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Sunwood-ai-labs/mcp-voicevox?style=social)](https://github.com/Sunwood-ai-labs/mcp-voicevox/network/members)
[![GitHub release](https://img.shields.io/github/v/release/Sunwood-ai-labs/mcp-voicevox)](https://github.com/Sunwood-ai-labs/mcp-voicevox/releases)
[![GitHub tag](https://img.shields.io/github/v/tag/Sunwood-ai-labs/mcp-voicevox)](https://github.com/Sunwood-ai-labs/mcp-voicevox/tags)

</div>

VoiceVox を介してテキスト読み上げ機能を提供する Model Context Protocol サーバーです。このサーバーにより、Claude は VoiceVox エンジンが提供する様々な音声を使用してテキストから音声を生成することができます。

---

## 🔗 リンク

[![GitHub Repo stars](https://img.shields.io/github/stars/Sunwood-ai-labs/mcp-voicevox?style=social)](https://github.com/Sunwood-ai-labs/mcp-voicevox/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Sunwood-ai-labs/mcp-voicevox?style=social)](https://github.com/Sunwood-ai-labs/mcp-voicevox/network/members)
[![GitHub release](https://img.shields.io/github/v/release/Sunwood-ai-labs/mcp-voicevox)](https://github.com/Sunwood-ai-labs/mcp-voicevox/releases)
[![GitHub tag](https://img.shields.io/github/v/tag/Sunwood-ai-labs/mcp-voicevox)](https://github.com/Sunwood-ai-labs/mcp-voicevox/tags)

- GitHub: [https://github.com/Sunwood-ai-labs/mcp-voicevox](https://github.com/Sunwood-ai-labs/mcp-voicevox)
  - [タグ一覧](https://github.com/Sunwood-ai-labs/mcp-voicevox/tags)
- PyPI: [https://pypi.org/project/mcp-server-voicevox/](https://pypi.org/project/mcp-server-voicevox/)



## ✨ 機能

- **テキスト読み上げ**: 指定したテキストを VoiceVox の音声で読み上げます。
- **話者選択**: 多数の個性的な話者から音声を選択できます。
- **音声の自動再生**: 生成した音声をその場で自動的に再生します。
- **音声ファイル保存**: 生成した音声は `sound` フォルダに `.wav` ファイルとして保存されます。

## 🚀 前提条件

- VoiceVox エンジンが動作していること（ローカルまたはリモートで）
- Python 3.10 以上

## 📦 インストール

### uv の使用（推奨）

[`uv`](https://docs.astral.sh/uv/) を使用する場合は特別なインストールは必要ありません。直接 [`uvx`](https://docs.astral.sh/uv/guides/tools/) を使用して *mcp-server-voicevox* を実行します。

## ⚙️ 設定

### VoiceVox エンジン

このサーバーは動作するために VoiceVox エンジンが必要です。エンジンの起動は手動で行う必要があります。
デフォルトでは `http://localhost:50021` への接続を試みます。`--voicevox-url` 引数で別の URL を指定することができます。

VoiceVox エンジンは [公式 VoiceVox リポジトリ](https://github.com/VOICEVOX/voicevox_engine) からダウンロードしてインストールできます。

### Claude Desktop 用の設定

Claude Desktop の設定に追加：

<details>
<summary>uvx を使用する場合</summary>

```json
{
  "mcpServers": {
    "voicevox": {
      "command": "uvx",
      "args": ["mcp-server-voicevox", "--voicevox-url=http://localhost:50021"]
    }
  }
}

```
</details>

## 🛠️ 利用可能なツール

- `get_voices` - VoiceVox から利用可能な音声のリストを取得
  - 引数は必要ありません

- `text_to_speech` - VoiceVox を使用してテキストを音声に変換
  - 必須引数：
    - `text` (文字列): 音声に変換するテキスト
  - オプション引数：
    - `speaker_id` (整数、デフォルト: 1): 使用する音声の ID
    - `speed` (数値、デフォルト: 1.3): 再生速度の倍率

## 🎵 特別な機能

- 生成後の音声は、プラットフォーム固有の方法で自動的に再生されます：
  - **Windows**: デフォルトのシステムプレーヤーを使用
  - **macOS**: 内蔵の `afplay` ユーティリティを使用
  - **Linux**: まず `aplay` を試し、失敗した場合は `xdg-open` にフォールバック

## 📁 プロジェクト構造

- `src/mcp_server_voicevox`: [ソースコード](./src/mcp_server_voicevox/README.md)
- `tests`: [テストコード](./tests/README.md)

## 📄 ライセンス

mcp-server-voicevox は MIT ライセンスの下で提供されています。これは、MIT ライセンスの条件に従い、自由に使用、修正、配布することができることを意味します。


## 🔗 リンク

- GitHub: [https://github.com/Sunwood-ai-labs/mcp-voicevox](https://github.com/Sunwood-ai-labs/mcp-voicevox)
  - [タグ一覧](https://github.com/Sunwood-ai-labs/mcp-voicevox/tags)
- PyPI: [https://pypi.org/project/mcp-server-voicevox/](https://pypi.org/project/mcp-server-voicevox/)
