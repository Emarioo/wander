# Installer and backend server todos.

- [ ] Rate limit on downloads per IP. Token Bucket.
- [ ] Authentication when uploading to server. A password token is required. Plain text is fine, we can add TLS and certificate later on the installer.
- [ ] Upload limit per IP in case password token is compromised.
- [ ] Sanitize messages. Discard abnormally large file requests, paths and so on.
- [ ] Reject to big files.
- [ ] Flag to bypass and ignore manifest hash verification.


## Flags

```bash
# install/update to latest release version
installer

# download files even if they have been tampered with
installer --unsafe

# install/update latest version and run the game
installer --run

# upload files to server (requires dev.token)
installer --upload <version> <game_files_dir>
```