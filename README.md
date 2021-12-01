<h2 align="center">SDU-LIB-SEAT</h2>

- 项目提供两种使用方式：
    1. 基本的命令行运行
    2. 更简单直观的图形化界面
- 同时项目提供[测试环境]()，但由于密码是明文存储，所以仍然推荐自己使用docker部署到自己的PC或服务器中

## 1. 命令行用法

- 在当天运行的脚本会在默认第2天00:00:01抢占第3天的座位
- 例如今天是12月2日的23:50，我需要抢后天也就是12月4日的座位，则在12月2日运行脚本，脚本会在12月3日凌晨进行抢占
```shell
cd ./src/main/
python app.py --userid [学号] --passwd [密码] --area [区域] --seats [想要占的座位] --time [脚本占座的时间]
```

### 参数说明

| 参数名 |   类型    | 必需  |                             说明                             |
| :----: | :-------: | :---: | :----------------------------------------------------------: |
| userid |    str    | True  |                        山东大学学工号                        |
| passwd |    str    | True  |                   山东大学统一身份认证密码                   |
|  area  |    str    | True  |                    图书馆-楼层-楼层内区域                    |
| seats  | List[str] | False | 想要占的座位，如果列出的座位均已无法占用，或没提供该参数，则在仍没被占用的座位进行占座 |
|  time  |    str    | False | 发起占座的时间，若没提供该参数，则在第二天00:01分开始抢后天的位置 |
| retry  |    int    | False | 如果占座失败（网络原因等）重试的次数，默认重试20次，间隔30s  |

- 特别注意area参数要规范，是官网该区域的标题**去掉最后的座位**二字，比如蒋震图书馆-蒋震6楼-D603室从下图中获得

![蒋震图书馆-蒋震6楼-D603室](doc/check-area-title.png)

### Example

```shell
cd ./src/main/
python app.py --userid 201805139999 --passwd abc123 --area 青岛校区图书馆-七楼-青岛馆七楼北阅览区 --seats N001 N011 --time 00:00:01
```

## 2. 图形界面管理

[Crontab-UI](crontab-ui/README.md)提供了添加作业、删除作业或暂停作业的图形接口。为了使多人占座，管理占座任务成为可能，在项目中引入Crontab-UI作为管理占座脚本的子模块。

### 在你的服务器上构建镜像

### 在你的服务器上运行容器

```shell
docker run -e BASIC_AUTH_USER=[用户名] -e BASIC_AUTH_PWD=[密码] -d -p 8000:8000 --name sdu-lib-seat alseambusher/crontab-ui 
```