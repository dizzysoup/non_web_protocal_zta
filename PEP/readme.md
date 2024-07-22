# PEP 說明

## agent 核心程式
yunagent.py
Fido 驅動程式 >> Fido 資料夾
credentials >> 憑證資料夾(local stored)
### gRPC 核心
sshgrpc_pb2

## register 
```python
    yunagent register --pep 192.168.71.3:50051 --user admin
```

## Server 


進入python虛擬環境
```python
    source myvenv/bin/activate
```

生成python code 
```python
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. credentials.proto
```
### Log 設計

格式：
```log
    2024-07-16 06:29:23 - MyLogger - DEBUG - 這是一個測試訊息
    2024-07-16 06:29:23 - MyLogger - INFO - 這是普通訊息
    2024-07-16 06:29:23 - MyLogger - WARNING - 這是警告訊息
    2024-07-16 06:29:23 - MyLogger - ERROR - 這是錯誤訊息
    2024-07-16 06:29:23 - MyLogger - CRITICAL - 這是嚴重錯誤訊息
```

可以建立log.py，執行單支程式碼純粹測試
```python
import logging

    # log setting 

    logging.basicConfig(
        level=logging.DEBUG,
        format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='app.log',
        filemode='w'
    )
    # 初始化
    logger = logging.getLogger('MyLogger')

    logger.debug("這是一個測試訊息")
    logger.info("這是普通訊息")
    logger.warning("這是警告訊息")
    logger.error("這是錯誤訊息")
    logger.critical("這是嚴重錯誤訊息")

    print("測試用途")
```

