# VocBench Setup

For Ubuntu 18.04, likely on AWS, these are basic installation instructions for VocBench:

## install.sh
```
#
#       Basic server config
#
sudo timedatectl set-timezone Australia/Brisbane
sudo apt update
sudo apt -y upgrade


#
#       Install Java
#
sudo apt install -y openjdk-8-jdk


#
#       Get VB
#
wget https://bitbucket.org/art-uniroma2/vocbench3/downloads/vocbench3-5.0.0_full.zip
sudo apt install unzip
unzip vocbench3-5.0.0_full.zip

#
#       Set Java options for Karaf
#
nano semanticturkey-5.0/bin/setenv

# at least...
# > export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/jre" # Location of Java installation
# > export JAVA_MIN_MEM=512M # Minimum memory for the JVM
# > export JAVA_MAX_MEM=1024M # Maximum memory for the JVM
# > export JAVA_PERM_MEM=256M # Minimum perm memory for the JVM
# > export JAVA_MAX_PERM_MEM=512M # Maximum perm memory for the JVM


#
#       VB start file
#
sudo chmod u+x semanticturkey-5.0/bin/start
nano vb_start.sh
# > sh /home/ubuntu/semanticturkey-5.0/bin/karaf server
# > echo "Starting Vocbench"
sudo chmod u+x vb_start.sh


#
#       Redirect the server's Port 80 to VB's port
#
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 1979

```
