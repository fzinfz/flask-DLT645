# 介绍
DLT645 批量抄表  
基于: [meter-dlt645](https://github.com/glx-technologies/meter-dlt645)

# 运行
编辑`lib/conf.py`：COM口、电表通信地址等  

## Docker

    ./docker_run.sh # 可修改`custom_config`值自定义conf.py位置
    docker exec flask-dlt645 bash -c "cd /app && echo y | ./push_to_influxdb.sh"

![](https://i.imgur.com/t5iecct.png)

## 手动

    pip -r requirements.txt
    ./start_web.sh

![](https://imgur.com/frgWGHF.png)

## 写入InfluxDB数据库（可选）

1. 编辑以上conf文件  
2. 

    ./push_to_influxdb.sh # 发送当前度数

3. 生成报表

        from(bucket: "YOUR_BUCKET_NAME")
          |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
          |> filter(fn: (r) => r["_measurement"] == "度数")
          |> filter(fn: (r) => r["_field"] == "当前")
        |> difference()

![](https://i.imgur.com/wwYoqzl.png)

使用Jupyter分析数据：https://nbviewer.jupyter.org/github/fzinfz/ipynb/tree/main/python/DB/influxdb-client.ipynb

# 作为库使用
Demo：[多表](https://nbviewer.jupyter.org/github/fzinfz/ipynb/blob/main/python/hw/power_meter_DLT645/multi.ipynb) | 
[单表](https://nbviewer.jupyter.org/github/fzinfz/ipynb/blob/main/python/hw/power_meter_DLT645/single.ipynb)
    
# 参考资料
说明书范例：[威胜](http://www.wasion.com/UploadFiles/files/DTSD342DSSD342-5N5D5Z%E5%AF%BC%E8%BD%A8%E5%AE%89%E8%A3%85%E7%94%B5%E5%AD%90%E5%BC%8F%E5%A4%9A%E5%8A%9F%E8%83%BD%E7%94%B5%E8%83%BD%E8%A1%A8%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E%E4%B9%A6.pdf)  
液晶全屏及显示说明: 第9页
