"""
集成了一些便于开发 nonebot2 插件的小功能

## 使用

在插件中导入对应的功能组或函数：

    >>> from nonebot_plugin_extrautils.ob11 import universal
    >>> # 或者
    >>> from nonebot_plugin_extrautils.ob11.gocq import send_forward_msg

然后按需调用即可。

本插件目前不会涉及框架本身功能，**不需要**通过 `nonebot.load_plugin()` 或 `require()` 作为功能插件加载。

### 功能集

| 功能组 | 函数 | 说明 | 备注 |
|:-------|:-----|:-----|:-----|
| ob11.universal | get_avatar_url | 获取指定 QQ 用户头像 URL | - |
| ob11.universal | get_avatar_bytes | 下载指定 QQ 用户头像 | - |
| ob11.universal | get_self_name | 获取机器人自身所在会话的昵称 | 优先级：群名片>用户昵称 |
| ob11.universal | get_user_name | 获取指定 QQ 用户所在会话的昵称 | 优先级：群名片>用户昵称 |
| ob11.universal | get_user_name_bare | 获取指定 QQ 用户昵称 | 有未封装版本 |
| ob11.universal | get_user_name_group | 获取指定 QQ 用户群昵称 | 有未封装版本 |
| ob11.gocq | Node | 构造适用于 go-cqhttp 的简单自定义消息节点 | - |
| ob11.gocq | msg2node_self | 转化多条消息到发送者为自身的消息节点 | - |
| ob11.gocq | msg2node_custom | 转化多条消息到发送者为指定用户的消息节点 | - |
| ob11.gocq | send_forward_msg | 发送合并转发消息 | 发送者为机器人自身 |
| ob11.gocq | send_forward_msg_custom | 发送合并转发消息 | 允许自定义发送者信息, 有未封装版本 |
"""