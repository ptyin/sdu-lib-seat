<h2 align="center">SDU-LIB-SEAT</h2>

### CHANGE LOG
- [x] 2022/04/01 解决威海校区分时段预约座位问题
- [x] 2022/02/20 图书馆空间预约系统UI变动导致爬虫进程失效，已适配
- [x] 2022/02/16 图书馆开放预约时间调整为06:00，目前脚本已经适配，默认06:02:00预约

---

## 两种使用方式：
1. [基本的命令行运行](#命令行用法)
2. [直观的图形化界面](#图形界面管理)

## 命令行用法

### 下载和安装

```shell
git clone https://github.com/PTYin/sdu-lib-seat.git
# 如使用图形界面则需带参数--recurse-submodules
# git clone --recurse-submodules https://github.com/PTYin/sdu-lib-seat.git
# 切换进入项目目录
cd sdu-lib-seat
# 安装python依赖
pip install -r requirements.txt
```

### 运行

- 在当天上午6点前运行的脚本会在默认06:02:00预约第2天的座位

```shell
cd ./src/main/
python app.py --userid [学号] --passwd [密码] --area [区域] --seats [想要约的座位] --time [脚本约座的时间]  --delta [约座的日期间隔] --starttime [座位开始时间] --endtime [座位结束时间]
```

### 参数说明

| 参数名 |   类型    | 必需  |                             说明                             |
| :----: | :-------: | :---: | :----------------------------------------------------------: |
| userid |    str    | True  |                        山东大学学工号                        |
| passwd |    str    | True  |                   山东大学统一身份认证密码                   |
|  area  |    str    | True  |                    图书馆-楼层-楼层内区域(威海校区注意用单引号引用)                    |
| seats  | List[str] | False | 想要约的座位，如果列出的座位均已无法约用，或没提供该参数，则在仍没被约用的座位进行约座 |
|  time  |    str    | False | 发起约座的时间，若没提供该参数，则在06:02分开始约第2天的位置 |
| delta  |    int    | False |  0代表预约第2天，1代表预约第3天，以此类推，默认预约第2天 |
| retry  |    int    | False | 如果约座失败（网络原因等）重试的次数，默认重试10次，间隔30s  |
| starttime  |    str    | False | 济南校本部、青岛校区默认为早上08:00，威海校区上午时间段为08:00,下午时间段为14:00  |
| endtime  |    str    | False | 济南校本部、青岛校区默认为晚上22:30，威海校区上午时间段为12:00,下午时间段为22:00  |

- 特别注意area参数要规范，是官网该区域的标题**去掉最后的座位**二字，比如蒋震图书馆-蒋震6楼-D603室从下图中获得

![蒋震图书馆-蒋震6楼-D603室](doc/check-area-title.png)

### Example

```shell
cd ./src/main/
python app.py --userid 201805139999 --passwd abc123 --area 青岛馆-七楼-青岛馆七楼北阅览区 --seats N001 N011 --time 06:02:00  --delta 0
```

威海校区参考下方,Linux下可以用nohup后台运行
```shell
cd ./src/main/

python app.py --userid 201900800xxx --passwd abc123 --area '威海馆-主楼(3-12)-三楼阅览室' --time 06:02:00 --delta 0 --seats 200 --starttime '08:00' --endtime '12:00'
python app.py --userid 201900800xxx --passwd abc123 --area '威海馆-主楼(3-12)-三楼阅览室' --time 06:02:00 --delta 0 --seats 200 --starttime '14:00' --endtime '22:00'

```

## 图形界面管理

- [Crontab-UI](https://github.com/alseambusher/crontab-ui)提供了添加任务、删除任务或暂停任务的图形接口。为了使多人约座，管理约座任务成为可能，在项目中引入Crontab-UI作为管理约座脚本的子模块。
- 具体Crontab-UI的操作见[Crontab-UI](crontab-ui/README.md)
- [测试环境](http://101.34.91.143:7000/)
  - 测试用户：test123
  - 测试密码：test123@sdulib

## 安装

- 由于利用crontab-ui执行脚本山东大学统一身份认证密码会暴露出来
- 推荐自己在服务器上利用docker进行搭建

```shell
  sudo docker build --tag ptyin/crontab-ui:latest .
```

## 运行
```shell
sudo docker run -e BASIC_AUTH_USER=user -e BASIC_AUTH_PWD=yoursecretpassword -d -p 8000:8000 --name crontab-ui ptyin/crontab-ui
```
- 运行之后，会在本地拉起一个端口8000的web服务
- 登陆用户名和密码为你命令提供的环境变量，例子为user和yoursecretpassword

#### 新建任务

![新建任务](doc/1.png)

#### 编辑任务

![编辑任务](doc/2.png)

#### 邮件提示

![邮件提示](doc/3.png)

#### 保存任务

![保存任务](doc/4.png)

## 3. 对开发者

- 如果需要运行src/test文件夹下单元测试
    - 需要安装pytest包
    - 需要src/resrc文件夹下有user.json文件，样例：
```json
{
    "username": "张三",
    "userid": "2018XXXXXXXX",
    "passwd": "YourPassword"
}
```
