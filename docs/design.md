# Code structure
- **build.btb** : Build the game with libraries
- **main.btb** : Entry point of the executable
- **core.btb** : General game stuff?

# Upload download process

The idea is developer runs `build.py dist release` which:
- Compiles game
- Collects game files into `bin/dist/*`
- Zip game files
- Creates manifest with hashes for the game files and zip file.
- Creates signature for the manifest.
- Run `installer.exe --upload release bin/dist`
- Server receives manifest, signature, zip, and game files and puts it in `channels/release/*`

On the user side they run `installer.exe --channel release` which:
- Downloads `release/manifest.txt` and `release/manifest.sig`.
- If verification fails then ask user if they want to download anyway.
- Is user has 7-zip or tar installed, download the zip file and unzip the game files.
- Otherwise download the raw game files.
- Then verify that the hashes in manifest matches when running certutil (or sha256sum) on the game files.