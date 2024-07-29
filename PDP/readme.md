# PDP 決策引擎

## INSTALL
* docker 安裝

    https://docs.docker.com/engine/install/ubuntu/

    ```
        apt install docker-compose
    ```

* 運行程式
```
    docker compose up -d 
```

* node 本地安裝

## 使用 NVM 管理node版本、npm版本
為了能夠方便管理node、npm的版本，會使用nvm這個套件做管理
下載NVM：
```
　　wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```
執行NVM：
```
    source ~/.bashrc
```
使用NVM下載nodeJS，install 時直接安裝版本編號 16.16.0是LTS(長期服務)版
```
    nvm install node
```
確認目前版本
```
    node -v 
    npm -v 
```

## 可能發生的狀況

### no module named http-errors 

重新安裝
```
    npm install http-errors 
```