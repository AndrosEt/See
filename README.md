# 抖音机器人


##  原理

- 打开《抖音短视频》APP，进入主界面
- 获取手机截图，并对截图进行压缩 (Size < 1MB)；
- 请求 [人脸识别 API](http://ai.qq.com/)；
- 解析返回的人脸 Json 信息，对人脸检测切割；
- 当颜值大于门限值 `BEAUTY_THRESHOLD`时，点赞并关注；
- 下一页，返回第一步；

## 使用教程
- Python版本：3.0及以上
- 相关软件工具安装和使用步骤请参考 [wechat_jump_game](https://github.com/wangshub/wechat_jump_game) 和 [Android 操作步骤](https://github.com/wangshub/wechat_jump_game/wiki/Android-%E5%92%8C-iOS-%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4)
- 在 [ai.qq.com](https://ai.qq.com) 免费申请 `AppKey` 和 `AppID`
1. 获取源码：`git clone https://github.com/wangshub/Douyin-Bot.git`
2. 进入源码目录： `cd Douyin-Bot`
3. 安装依赖： `pip install -r requirements.txt`
4. 运行程序：`python douyin-bot.py`

## 注意

- 目前暂时只适配了 一加5(1920x1080 分辨率)，如果手机不是该分辨率，请修改 `config/` 文件夹下面的配置文件；
- `config.json`配置文件参考：
    - `center_point`: 屏幕中心点`(x, y)`，区域范围 `rx, ry`
    - `follow_bottom`: 关注按钮位置`(x, y)`，区域范围 `rx, ry`
    - `star_bottom`: 点赞按钮位置`(x, y)`，区域范围 `rx, ry`
    

## 脸部截取

![](./screenshot/faces.png)

## LICENSE

MIT

欢迎 Star 和 Fork ~

如果你有什么问题请提 Issue

