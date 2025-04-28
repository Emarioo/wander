Regression and integration tests. Mostly black box testing from users perspective. We rarely test individual functions.


|Tests|What|
|-|-|
|--verify|Verify local game files. When files exist and are valid. When files don't exist. When files exist but aren't valid.|
|--run|Just one test checking that the game runs afterwards.|
|--list-channels|Check that we get list of versions. Check what happens when server is done. What happens when msg_version is invalid.|
|--channel <name>|Try downloading default release and non default version. Try channel with correct files. With tampered files. With missing files. Manifest and sig being modified. And other game files being modified. Test different long folder nested files. Try downloading manifest with missing fields. Corrupt file random garbage manifest. |
|--install-dir <path>|Test that different folder can be chosen.|
|--upload <channel> <game_files_dir>|Test uploading correct files. Manifest with no files. Test valid dev token. Missing dev token (server and installer). Test invalid dev tokens.|
|--ip <server_ip>[:port]|Test different port numbers, no port number. Testing ip would always be local host in testing so can't test different server.|
|--unsafe|Do we need test for this?|
|Range checks|Test download/uploading large game file. Test too large path in manifest. Test to long channel name on client side.|
|Corrupt net messages|Test sending unsuported versions. Test sending zero sized messages. Half complete messages for all the message types.|


