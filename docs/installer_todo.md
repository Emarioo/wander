# Installer and backend server todos.

- [ ] If a developer uploads files to channel and a user tries to download it should wait downloading until upload is finished. User will receive a message "Developer is currently uploading game files to 'release', 35% done (53MB / 150MB)."
- [ ] Is users are downloading from channel and developer starts to upload then user downloads should stop and restart giving them the "Developer is currently uploading..." message.

- [ ] Rate limit on downloads per IP. Token Bucket.
- [ ] Authentication when uploading to server. A password token is required. Plain text is fine, we can add TLS and certificate later on the installer.
- [ ] Upload limit per IP in case password token is compromised.
- [ ] Sanitize messages. Discard abnormally large file requests, paths and so on.
- [ ] Reject to big files.
- [ ] Flag to bypass and ignore manifest hash verification.

# Future todos
- [ ] When game files get larger we can implement a system that uploads the files that have changed. (manifest and signature always needs to change)
- [ ] When a user downloads files we can check the new manifest if the files we have (if any) are on the game files list and download the ones that differ.