# LianJiaSpider
- https://github.com/linpingta/lianjia-eroom-analysis/issues
- 利用[此网页](https://sh.lianjia.com/ditu/)接口实现功能 

## API Used
Example of API used:
```
https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/bubblelist?cityId=310000&dataSource=ESF&condition=&id=5011000017968&groupType=community&maxLatitude=31.295840493838348&minLatitude=31.269793772980677&maxLongitude=121.52728029602387&minLongitude=121.48229315608417
```
### API 基本格式
- `https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/bubblelist?cityId=310000&dataSource=ESF&condition=&id=5011000017968&groupType=community&maxLatitude=31.295840493838348&minLatitude=31.269793772980677&maxLongitude=121.52728029602387&minLongitude=121.48229315608417`
- `https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/bubblelist?cityId=440300&dataSource=ESF&condition=&id=&groupType=community&maxLatitude=22.56559612283492&minLatitude=22.559772217361235&maxLongitude=114.1349382596455&minLongitude=114.12687147616856`

https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/bubblelist?cityId={cityId}&dataSource={dataSource}&condition={condition}&id={id}&groupType={groupType}&maxLatitude={maxLatitude}&minLatitude={minLatitude}&maxLongitude={maxLongitude}&minLongitude={minLongitude}

### 用到的查询字段
|字段|含义|
|---|---|
|cityId|城市ID|
|dataSource|数据源|
|condition|条件|
|id|ID|
|groupType|组类型|
|maxLatitude|最大纬度|
|minLatitude|最小纬度|
|maxLongitude|最大经度|
|minLongitude|最小经度|

https://map.lianjia.com/map/440300/ESF