Installer specifications

# Channels
These are standardized channels that always exist.
- `release` holds the latest stable game version.
- `dev` holds the latest unstable game version.
- `test` holds the last version in the most recent test period. Some test periods may be named `test-fire-magic`.

You can find more game versions using `installer --list-channels` where you will find `release-X.X.X`. These are specific game versions.

# Limits

|What|Limit|Note|
|-|-|-|
|Max concurrent connections|64|Excluding upload connections.|
|Download from server|10 MB/s per IP address||
|Upload to server|50 MB/s per IP address||
|Max channels on server|10||
|(derived) Max file storage usage|2 GB = 10 * (200 MB + 160 MB)|200 MB = worst case size for game files, 160 MB = worst case size for zipped game files|


**NOTE:** My home network can only handle uploads of 10 Mb/s which is 1.25 MB/s.

# Command line arguments
Older versions of the installer doesn't support newer flags. These are the current ones (on this git commit).

```bash
# install/update to latest release version
installer

# print installer information and available flags
installer -h
installer --help

# print installer version
installer -v
installer --version

# download files even if they have been tampered with
installer --unsafe

# Verify game files against the manifest and signature (does not download anything)
installer --verify

# install/update latest version and run the game
installer --run

# list available channels on the content server
installer --list-channels

# download specific game version
installer --channel <name>

# Game versions are installed in the folder you specify. The default path is the folder where installer is located.
installer --install-dir <path>
```

These are specifically for developers.
```bash
# upload files to server (requires dev.token)
installer --upload <channel> <game_files_dir>

# Change which content server to connect to (default is btb-lang.org)
installer --ip localhost:5000
```

**NOTE:** channel is similar to game version. The difference is that a game version (`core.exe --version`) refers to a fixed state of the game code while channel is the name for the latest game version uploaded to that channel. Some channels such as `release-0.0.1` refer to a specific game version and will never be updated. Other channels like `dev` are meant for testing and are unstable because new versions are uploaded continously. 

# Manifest file
- Manifest file is split into lines by `\n`.
- Spaces and tabs seperate words.
- A word is a sequence of non-space characters.
- The first two words in a line is a key-value pair. Remaining words are ignored.
- Empty lines are ignored.
- Lines with one word are ignored.
- Quotes is used to get a word with spaces in it. The word does not include the quote characters.
- Quotes can have backslash for special characters like newline and quotes.
- Lines where first word is `#` are sections.
- Installers may utilize or ignore sections depending on the version. New installers can parse all section types while older ones have no knowledge of new section types.

## Standard sections
All installers can parse these sections: **metadata**, **game_files**.

A typcial manifest file:
```yaml
# metadata
game_version wander-0.1.0 
date    2025-04-27

# game_files
core.exe 4814ab51dac
assets/sprite.png f6a7b12d62c79
```

## Section: **metadata**
This section provides metadata about the game version. Here are some examples:
```yaml
# metadata
manifest_version 1.0
game_version wander-0.1.0 
date    2025-04-27
commit  728d4a51c3
```

- **manifest_version** is the version of the manifest file.
- **game_version** is the game version.
- **date** is the year-month-day when the manifest was created.
- **commit** is the git commit which allows you to search up the exact state of all the code for this game version. This may not be available on testing versions where code isn't committed.

## Section: **game_files**
The **game_files** section contains a list of path-hash pairs. The path describes a game file such as an executable, dynamic library, image, model, terrain data. The SHA-256 hash is always 64 hexidecimal characters (32 bytes).

All installers are aware of this section and it will never change.

```yaml
# game_files
core.exe 4814ab51dac
assets/sprite.png f6a7b12d62c79
```

# Network messages for the installer

The data in the messages are read and written to by ByteStream (Stream.btb).
- Structs described here do not have any invisible padding.
- Strings are encoded with 1-byte length followed by that number of characters with a null terminator (not included in the length). An empty string takes up two bytes.
- Everything is little endian. Big endian is standard for network messages but since these programs will always run on little endian machines it's would be unnecessary to convert integers to and from different endians.

All response messages have: *message_type*, *msg_version*, *result*, and *server_message*.
`ResponseResult` is defined in [](/installer/src/util.btb).

## MSG_GET_CHANNELS
Ask server for channels.

```c
struct Format_GET_CHANNELS {
    message_type: i32;
    msg_version: i32;

    // version 1
}

struct Format_RESPONSE_GET_CHANNELS {
    message_type: i32;
    msg_version: i32;
    result: ResponseResult;
    server_message: string8;

    // version 1
    channel_len: i32;
    channels: string8[channels_len];
}
```

## MSG_GET_FILE
Ask server for game files. Installer will ask for signature and manifest first. If valid, it will download the other files.

```c
struct Format_GET_FILE {
    message_type: i32;
    msg_version: i32;

    // version 1
    channel: string8;
    file: string8;
}

struct Format_RESPONSE_GET_FILE {
    message_type: i32;
    msg_version: i32;
    result: ResponseResult;
    server_message: string8;

    // version 1
    channel: string8;
    file: string8;
    file_size: i32;
    data: u8[file_size];
}
```

## MSG_UPLOAD_FILE

```c
struct Format_UPLOAD_FILE {
    message_type: i32;
    msg_version: i32;

    // version 1
    dev_token: string8;
    channel: string8;
    file: string8;
    file_size: i32;
    file_data: char[file_size];
}

struct Format_RESPONSE_UPLOAD_FILE {
    message_type: i32;
    msg_version: i32;
    result: ResponseResult;
    server_message: string8;

    // version 1
}
```
