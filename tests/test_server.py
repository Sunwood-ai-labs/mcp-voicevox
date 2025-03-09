import os
import sys
from unittest.mock import MagicMock, patch

import pytest
import requests

from mcp_server_voicevox.server import VoiceVoxServer


def test_server_connection():
    """VoiceVoxサーバーへの接続が正常に確認できるかテスト"""
    
    voicevox_url = "http://localhost:50021/version"
    response = requests.get(f"{voicevox_url}")    
    response.raise_for_status() 


def test_init_success(mock_requests, mock_os_operations):
    """VoiceVoxServerの初期化が正常に行われるかテスト"""
    mock_makedirs, _, _ = mock_os_operations
    server = VoiceVoxServer("http://voicevox:50021")
    
    # os.makedirsが呼ばれたかを確認
    mock_makedirs.assert_called_once()
    
    # VoiceVox APIに接続確認リクエストが送信されたかを確認
    mock_get, _ = mock_requests
    mock_get.assert_called_with("http://voicevox:50021/version")


def test_init_connection_error(mock_os_operations):
    """VoiceVox APIに接続できない場合のエラーハンドリングをテスト"""
    # リクエストでエラーが発生するようにモック化
    with patch("requests.get", side_effect=Exception("Connection error")):
        # エラーが捕捉され、サーバーが正常に初期化されることを確認
        server = VoiceVoxServer("http://nonexistent:50021")
        assert server.voicevox_url == "http://nonexistent:50021"


def test_get_speakers(voicevox_server, mock_requests):
    """get_speakersメソッドが正常に動作するかテスト"""
    speakers = voicevox_server.get_speakers()
    
    # 正しい数のスピーカーが返されるか確認
    assert len(speakers) == 2
    assert speakers[0]["name"] == "四国めたん"
    assert len(speakers[0]["styles"]) == 2
    
    # APIリクエストが正しく行われたか確認
    mock_get, _ = mock_requests
    mock_get.assert_any_call("http://voicevox:50021/speakers")


def test_text_to_speech(voicevox_server, mock_requests, mock_file_operations, mock_os_operations):
    """text_to_speechメソッドが正常に動作するかテスト"""
    # play_audioメソッドをモック化
    with patch.object(voicevox_server, 'play_audio') as mock_play_audio:
        filepath = voicevox_server.text_to_speech("こんにちは", speaker_id=1, speed=1.2)
        
        # APIリクエストが正しいパラメータで呼ばれたか確認
        _, mock_post = mock_requests
        mock_post.assert_any_call(
            "http://voicevox:50021/audio_query",
            params={"text": "こんにちは", "speaker": 1}
        )
        
        # 速度パラメータが正しく設定されたか確認 (audio_queryの結果を修正しているか)
        assert mock_post.call_args_list[1][1]['data'] == '{"speedScale": 1.2}'
        
        # ファイルが正しく保存されたか確認
        mock_open, mock_file = mock_file_operations
        mock_file.__enter__.return_value.write.assert_called_once_with(b"MOCK_AUDIO_DATA")
        
        # 音声が再生されたか確認
        mock_play_audio.assert_called_once()


@pytest.mark.parametrize("platform,expected_method", [
    ("win32", "os.startfile"),
    ("darwin", "subprocess.run with afplay"),
    ("linux", "subprocess.run with aplay")
])
def test_play_audio(voicevox_server, platform, expected_method, mock_subprocess):
    """play_audioメソッドが各プラットフォームで正しく動作するかテスト"""
    # プラットフォームをモック化
    with patch("sys.platform", platform):
        if platform == "win32":
            with patch("os.startfile") as mock_startfile:
                voicevox_server.play_audio("/path/to/audio.wav")
                mock_startfile.assert_called_once_with("/path/to/audio.wav")
        elif platform == "darwin":
            voicevox_server.play_audio("/path/to/audio.wav")
            mock_subprocess.assert_called_once_with(["afplay", "/path/to/audio.wav"], check=True)
        else:  # linux
            # aplayが成功するケース
            voicevox_server.play_audio("/path/to/audio.wav")
            mock_subprocess.assert_called_once_with(["aplay", "-q", "/path/to/audio.wav"], check=True)
            
            # aplayが失敗してxdg-openにフォールバックするケース
            mock_subprocess.reset_mock()
            mock_subprocess.side_effect = [FileNotFoundError, None]  # 最初は失敗、2回目は成功
            voicevox_server.play_audio("/path/to/audio.wav")
            assert mock_subprocess.call_count == 2
            mock_subprocess.assert_any_call(["xdg-open", "/path/to/audio.wav"], check=True)
