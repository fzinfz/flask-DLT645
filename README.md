# 介绍
DLT645 批量抄表  
基于: [meter-dlt645](https://github.com/glx-technologies/meter-dlt645)

# 运行

1. 编辑`conf/conf.py`：COM口、电表通信地址等  
2.

    ./start_web.sh # 自行安装uv，或修改.sh

    # 开机运行
    apt install supervisor 
    ./scripts/supervisord/setup.sh

![](https://imgur.com/frgWGHF.png)

3. 打开浏览器，访问以下页面：

- [首页 /](http://localhost:5000/) — 导航入口
- [读数 /meters/](http://localhost:5000/meters/) — 显示各电表当前度数
- [功率 /power/](http://localhost:5000/power/) — 显示各房间当前功率

## 写入InfluxDB数据库（可选）

1. 编辑以上conf文件  
2. 

    uv run lib/influxdb2.py --push # 发送当前度数
    uv run lib/influxdb2.py --pull --range_start=-3d # 拉取历史数据

    ./scripts/cron_setup.sh # crontab任务，修改CRON_LINE自定义时间

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

# TODO
- conf.py -> conf.toml