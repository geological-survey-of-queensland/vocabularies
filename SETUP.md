## Setup
These instructions are to setup the servers to deliver vocabularies.

* Server 1: **VocBench + VocPrez**, the vocabs management and display tool
* Server 2: **GraphDB**, the triplestore (graph DB) for the vocabs and other RDF data


## 1. Server 1
### 1.1. VocBench Setup

For Ubuntu 18.04, likely on AWS, these are basic installation instructions for VocBench:

#### VocBench install.sh
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

### 1.2. VocPrez setup
```
# 
#       Get VocPrez
#
sudo apt -y install git
git clone https://github.com/CSIRO-enviro-informatics/VocPrez.git /home/ubuntu/VocPrez

#
#       Configure VocPrez
#
# checkout the branhc you want
git checkout gsq
# set the app.wsgi file to indicate the installation home
nano app.wsgi
# > sys.path.insert(0, '/home/ubuntu/VocPrez')
cp VocPrez/_config/template.py VocPrez/_config/__init__.py
nano VocPrez/_config/__init__.py
# set at least:
# > VB_ENDPOINT = ''
# > VB_USER = ''
# > VB_PASSWORD = ''
# and:
# > VOCABS = {...}


#
#       Install Apache server
#
sudo apt install -y apache2
sudo rm /etc/apache2/sites-available/*
sudo rm /etc/apache2/sites-enabled/*

# install WSGI module for Python 3
sudo apt install -y libapache2-mod-wsgi-py3
# install proxy modules
sudo a2enmod proxy proxy_http

#
#       Python for VocPrez
#
sudo apt install -y python3-pip
? sudo apt install -y python3-venv
virtualenv --python=/usr/bin/python3 venv
source venv/bin/activate
# now in virtualenv, install VocPrez' required Python modules via pip
pip install -r requirements.txt
# drop out of venv
deactivate

#
#       configure Apache sites
#
sudo nano /etc/apache2/sites-available/vocabs.gsq.cat.conf
```
<VirtualHost *:80>
        ServerName vocabs.gsq.cat

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        Alias "/vocprez/static" "/home/ubuntu/VocPrez/view/static/"
        WSGIDaemonProcess vocprez user=www-data python-home=/home/ubuntu/VocPrez/venv threads=5
        WSGIScriptAlias / /home/ubuntu/VocPrez/app.wsgi
        <Directory /home/ubuntu/VocPrez/>
                WSGIProcessGroup vocprez
                WSGIApplicationGroup %{GLOBAL}
                Require all granted
        </Directory>

        ProxyPreserveHost On
</VirtualHost>
```
sudo a2ensite vocabs.gsq.cat.conf

sudo nano /etc/apache2/sites-available/vocabs.gsq.cat.conf
```
<VirtualHost *:80>
        ServerName vocbench.gsq.cat

        ProxyPass / http://127.0.0.1:1979/vocbench3/
        ProxyPassReverse / http://127.0.0.1:1979/vocbench3/
</VirtualHost>
```
sudo a2ensite vocbench.gsq.cat.conf

sudo service apache2 restart

# dissable the port redirecting from 80 -> 1979
sudo iptables -t nat -D PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 1979
```


## 2. Server 2
### 2.1. GraphDB setup
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
```
