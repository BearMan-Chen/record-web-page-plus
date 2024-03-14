# Linux Environment Install
Ubuntu 20.04 | Ubuntu 22.04

## Install apt Packages
```commandline
sudo apt -y update
sduo apt -y upgrade
sduo apt -y install grep unzip wget curl tar xvfb openjdk-19-jre-headless fonts-noto ffmpeg
sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo chown _apt google-chrome-stable_current_amd64.deb
sudo apt -y install google-chrome-stable_current_amd64.deb
allure_html=$(curl -Ls https://github.com/allure-framework/allure2/releases/latest)
allure_version=$(echo ${allure_html} | grep -oP '<h1[^>]+?>\d+\.\d+\.\d+</h1>' | grep -oP '\d+\.\d+\.\d+')
sudo curl -OLs "https://github.com/allure-framework/allure2/releases/download/${allure_version}/allure-${allure_version}.tgz"
sudo tar -zxvf allure-${allure_version}.tgz -C /opt/
sudo ln -s /opt/allure-${allure_version}/bin/allure /usr/bin/allure
```

## Install python packages
1. Into the record-web-page-plus directory
2. (Optional) Use a virtual environment
   1. Install virtual environment
      ```commandline
      sudo apt -y install python3-venv
      python3 -m venv venv
      source venv/bin/activate
      ```
3. Use pip to install packages
    ```commandline
    pip install -r .\packages\packages_linux.txt
    ```

## Run Server
1. Into the record-web-page-plus directory
2. command line to run server
   * run server by virtual environment
      ```commandline
      venv/bin/python record_web_page_plus_server.py
      ```
   * run server by global environment
      ```commandline
      python record_web_page_plus_server.py
      ```