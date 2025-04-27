# Network messages for the installer

The data in the messages are read and written to by ByteStream (Stream.btb).
- Structs described here do not have any invisible padding.
- Strings are encoded with 1-byte length followed by that number of characters with a null terminator (not included in the length). An empty string takes up two bytes.
- Everything is little endian. Big endian is standard for network messages but since these programs will always run on little endian machines it's would be unnecessary to convert integers to and from different endians.

## MSG_GET_VERSIONS
Ask server for latest game version.

```c
struct Format_GET_VERSIONS {
    message_type: i32;
    
}
struct Format_RESPONSE_GET_VERSIONS {
    message_type: i32;
    version: string8;
}
```

## MSG_GET_FILE
Ask server for game files. Installer will ask for signature and manifest first. If valid, it will download the other files.

```c
struct Format_GET_FILE {
    message_type: i32;
    version: string8;
    file: string8;
}
```

```c
struct Format_GET_FILE {
    message_type: i32;
    version: string8;
    file: string8;
    file_size: i32;
    data: u8[file_size];
}
```
