# VHS documentation
#
# Output:
#   Output <path>.gif               Create a GIF output at the given <path>
#   Output <path>.mp4               Create an MP4 output at the given <path>
#   Output <path>.webm              Create a WebM output at the given <path>
#
# Require:
#   Require <string>                Ensure a program is on the $PATH to proceed
#
# Settings:
#   Set FontSize <number>           Set the font size of the terminal
#   Set FontFamily <string>         Set the font family of the terminal
#   Set Height <number>             Set the height of the terminal
#   Set Width <number>              Set the width of the terminal
#   Set LetterSpacing <float>       Set the font letter spacing (tracking)
#   Set LineHeight <float>          Set the font line height
#   Set LoopOffset <float>%         Set the starting frame offset for the GIF loop
#   Set Theme <json|string>         Set the theme of the terminal
#   Set Padding <number>            Set the padding of the terminal
#   Set Framerate <number>          Set the framerate of the recording
#   Set PlaybackSpeed <float>       Set the playback speed of the recording
#   Set MarginFill <file|#000000>   Set the file or color the margin will be filled with.
#   Set Margin <number>             Set the size of the margin. Has no effect if MarginFill isn't set.
#   Set BorderRadius <number>       Set terminal border radius, in pixels.
#   Set WindowBar <string>          Set window bar type. (one of: Rings, RingsRight, Colorful, ColorfulRight)
#   Set WindowBarSize <number>      Set window bar size, in pixels. Default is 40.
#   Set TypingSpeed <time>          Set the typing speed of the terminal. Default is 50ms.
#
# Sleep:
#   Sleep <time>                    Sleep for a set amount of <time> in seconds
#
# Type:
#   Type[@<time>] "<characters>"    Type <characters> into the terminal with a
#                                   <time> delay between each character
#
# Keys:
#   Escape[@<time>] [number]        Press the Escape key
#   Backspace[@<time>] [number]     Press the Backspace key
#   Delete[@<time>] [number]        Press the Delete key
#   Insert[@<time>] [number]        Press the Insert key
#   Down[@<time>] [number]          Press the Down key
#   Enter[@<time>] [number]         Press the Enter key
#   Space[@<time>] [number]         Press the Space key
#   Tab[@<time>] [number]           Press the Tab key
#   Left[@<time>] [number]          Press the Left Arrow key
#   Right[@<time>] [number]         Press the Right Arrow key
#   Up[@<time>] [number]            Press the Up Arrow key
#   Down[@<time>] [number]          Press the Down Arrow key
#   PageUp[@<time>] [number]        Press the Page Up key
#   PageDown[@<time>] [number]      Press the Page Down key
#   Ctrl+<key>                      Press the Control key + <key> (e.g. Ctrl+C)
#
# Display:
#   Hide                            Hide the subsequent commands from the output
#   Show                            Show the subsequent commands in the output

Output blat-webscraping-ai-agent.mp4
Output blat-webscraping-ai-agent.ascii

Require echo
Require blat
Require docker
Require jq

Set Shell "bash"
Set FontSize 32
# Set FontFamily "JetBrainsMonoNerdFont"
Set Width 1600
Set Height 1500
Set LineHeight 1.2
Set Theme "tokyonight-storm"
Set TypingSpeed 80ms

Set Margin 40
# Set MarginFill "#674EFF"
Set MarginFill "#FFFFFF"
Set WindowBar Colorful
Set WindowBarSize 80
Set BorderRadius 32

# Type "# BLAT AI" Enter 2 Sleep 500ms
# Type "# Are you "
# Type@200ms "...?"
# Sleep 300ms
# Backspace@200ms 4
# Sleep 300ms
# Type@150ms "tired?"
# Sleep 1000ms
# # Backspace@200ms 6
# # Sleep 300ms
# Type@150ms " annoyed?"
# Sleep 1000ms
# Type@150ms " frustrated? ..." Sleep 300ms Enter
# Type "# of creating and maintaining web scraping scripts?" Sleep 1000ms Enter 2
# Type "# Fear not!" Sleep 1000ms Enter 2
# Type "# Blat is here to help :)" Sleep 1000ms Enter
# Sleep 3s
# Ctrl+L
# Sleep 1s
# 
# 
# # INSTALL AND INTRODUCE BLAT
# Type "# 0. Meet our CLI! " Sleep 1000ms Enter
# Type "#    It allows you to interact with our Web Scraping AI Agent." Sleep 1000ms Enter
# # Type "#    (sudo is required)" Sleep 1000ms Enter
# # Type "sudo pip install blat" Sleep 2000ms Enter
# Type "blat --help" Sleep 2000ms Enter
# Sleep 10s
# Ctrl+L
# 
# # INSTALL DEPENDENCIES
# Type "# 1. First, let's init blat!" Sleep 1s Enter
# Type "#    (this might take around 1-2 minutes if it's the first time)" Sleep 1000ms Enter
# Type "blat init --api-key ${BLAT_API_KEY}" Sleep 1000ms Enter
# Sleep 2s
# Enter
# Type "sudo blat init-system" Enter
# # Sleep 3s
# Hide
# Type "ap13069145@" Enter
# Show
# Sleep 7s
# Ctrl+L

# INPUT DATA
# Type "# Step 1/3) Before generating a harvester, we need to define the input parameters." Enter
Type "# Step 1/5) Define input variables: TARGET_URL and BLAT_SCHEMA" Sleep 1000ms Enter
Type "echo ${TARGET_URL}" Sleep 1000ms Enter 2
Type "echo ${BLAT_SCHEMA} | jq ." Sleep 1000ms Enter
Sleep 7s
Ctrl+L

# CREATE EXTRACTOR
Type "# Step 2/5) Generate the extractor using blat CLI." Sleep 1000ms Enter
Type "blat harvester generate --schema ${BLAT_SCHEMA} --url ${TARGET_URL}" Enter
Sleep 1000ms
Enter
Sleep 60s
Ctrl+L

Hide
Type "rm -r ./webscraper_io_extractor/" Enter
Show

# CHECK CODE
Type "# Step 3/5) Decompress and check the extractor :)" Sleep 1000ms Enter
Type "unzip -q ./webscraper_io_extractor.zip -d webscraper_io_extractor/" Sleep 1000ms Enter
Type "cd ./webscraper_io_extractor" Sleep 1000ms Enter
Type "tree ." Sleep 1000ms Enter
Sleep 5s
Ctrl+L

# RUN EXTRACTOR
Type "# Step 4/5) Run the extractor (follow the README!)" Sleep 1000ms Enter
Type "make lock-deps build run" Sleep 1000ms Enter
Sleep 120s
Ctrl+L
