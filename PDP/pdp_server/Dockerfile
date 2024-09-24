FROM node:14

# 設定工作目錄
WORKDIR /app

# 複製 package.json 和 package-lock.json 到工作目錄
COPY package*.json ./

# 安裝應用程式的依賴
RUN npm install

# 複製應用程式的源代碼到工作目錄
COPY . .

# 安裝 nodemon 作為全局模組
RUN npm install -g nodemon


# 暴露應用程式的端口
EXPOSE 3443

# 使用 nodemon 啟動應用程式
CMD ["nodemon", "./bin/www"]
