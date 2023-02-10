<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-extrautils

_✨ Extra utility functions for easier development. 方便开发的更多小功能。 ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/NCBM/nonebot-plugin-extrautils.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-extrautils">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-extrautils.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

## 📖 介绍

本插件集成了一些便于开发的小功能。

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-extrautils

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

> 注意：如果机器人在某个虚拟环境中运行，请确保安装前已经进入虚拟环境

<details>
<summary>pip</summary>

    pip install nonebot-plugin-extrautils
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-extrautils
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-extrautils
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-extrautils
</details>

然后**自行加载本插件**

</details>

## 🎉 使用

在插件中导入对应的功能组或函数：

    from nonebot_plugin_extrautils.ob11 import universal
    # 或者
    from nonebot_plugin_extrautils.ob11.gocq import send_forward_msg

然后按需调用即可。

本插件目前不会涉及框架本身功能，**不需要**通过 `nonebot.load_plugin()` 或 `require()` 作为功能插件加载。

### 功能集

| 功能组 | 函数 | 说明 | 参数 | 备注 |
|:-------|:-----|:-----|:-----|:-----|
| ob11.universal | get_avatar_url | 获取指定 QQ 用户头像 URL | (uid: int \| str, size: int = ...) -> str | - |
| ob11.universal | get_avatar_bytes | 下载指定 QQ 用户头像 | [async] (uid: int \| str, size: int = ...) -> bytes | - |
| ob11.universal | get_user_name | 获取指定 QQ 用户所在会话的昵称 | [async] (\*, bot: \_OneBotV11Bot, event: \_OneBotV11MessageEvent, no_cache: bool = ...) -> str | 优先级：群名片>用户昵称, W.I.P. |
| ob11.universal | get_user_name_bare | 获取指定 QQ 用户昵称 | [async] (\*, bot: \_OneBotV11Bot, event: \_OneBotV11MessageEvent, no_cache: bool = ...) -> str | 有未封装版本 |
| ob11.universal | get_user_name_group | 获取指定 QQ 用户群昵称 | [async] (\*, bot: \_OneBotV11Bot, event: \_OneBotV11GroupMessageEvent, no_cache: bool = ...) -> str | 有未封装版本 |
| ob11.gocq | send_forward_msg | 发送合并转发消息 | [async] (\*, bot: \_OneBotV11Bot, event: \_OneBotV11MessageEvent, nodes: Sequence[Message \| Sequence[dict[str, Any]] \| str]) -> dict[str, Any] | 有未封装版本, W.I.P. |
| ob11.gocq | send_forward_msg_custom | 发送合并转发消息 | [async] (\*, bot: \_OneBotV11Bot, event: \_OneBotV11MessageEvent, nodes: Sequence[MessageNode \| MessageSegment \| dict[str, Any]]) -> dict[str, Any] | 允许自定义发送者信息, 有未封装版本, W.I.P. |
