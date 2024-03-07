# FAQ

## Windows

### `UnicodeEncodeError: 'charmap' codec can't encode characters in position ...` というエラーが出る

環境変数に `PYTHONUTF8=1` を追加して、PythonのUTF-8 Modeを有効にしてください。

コマンドプロンプトの場合の例:

```cmd
set PYTHONUTF8=1
```

PowerShellの場合の例:

```powershell
$Env:PYTHONUTF8=1
```
