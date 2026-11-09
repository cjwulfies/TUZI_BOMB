## The Tuzi Bomb
This project tests the capability of Suricata in detecting and logging SSH and TCP connections, both inbound and outbound. To do this, a Ducky script is run off of a Flipper Zero using BadUSB into WSL, which then attempts to SSH into an Ubuntu virtual machine running on Virtual Box. After successfully SSH-ing into the VM, the script then clones this repository and runs the three bash scripts within in. Three actions should be logged within Suricata's fast.log: the SSH into the virtual machine, the TCP connection outbound to GitHub, and the connection back in through cloning the repository. 

### File Descriptions
**install.sh: **
`This file's purpose is to set up and install necessary packages onto the virtual machine.`

**build.sh: **
`This file's purpose is to set up the build for the script`

**run.sh: **
`This file's purpose is to run the script, which opens windows playing reaction.gif`

**reaction.gif: **
`This file is a gif that is opened in a selected amount of windows`
