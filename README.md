## Usage

```shell
cd ./src/main/
python app.py --userid [学号] --passwd [密码] --area [区域] --seats [想要占的座位]
```

### Example

```shell
cd ./src/main/
python app.py --userid 201805139999 --passwd abc123 --area 蒋震图书馆-蒋震6楼-D616室 --seats 743 220
```

## Functionality

- [ ] 查看座位信息
- [ ] 多选座位
- [ ] 用户登陆

## 图书馆选座逻辑

1. [图书馆](http://seat.lib.sdu.edu.cn/home/web/f_second)
2. [楼层](http://seat.lib.sdu.edu.cn/home/web/seat/area/1)
3. [楼层内区域](http://seat.lib.sdu.edu.cn/web/seat2/area/3/day/2021-11-28)
4. [区域内座位](http://seat.lib.sdu.edu.cn/web/seat3?area=11&day=2021-11-28&startTime=8:00&endTime=22:30)

## Crontab-UI
```shell
docker run -e BASIC_AUTH_USER=user -e BASIC_AUTH_PWD=SecretPassword -d -p 8000:8000 alseambusher/crontab-ui 
```