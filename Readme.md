# 简介

> 对羊了个羊的自动化脚本，采用贪婪策略.

当前脚本循环下方逻辑：

1. 检查是否已经结束，如果已经结束但有重生机会，则看广告或转发重生，否则结束重来。如果没有结束则去 2
2. 检查桌面上是否有牌能和手牌一起凑出 3 个，如果有，则点他们凑起来，并回到 1 重新循环，否则 3
3. 检查是否需要使用随机道具，个人判断条件为手牌有 6 张以上，要用则获得并使用，并回到 1。不用或用不了则 4
4. 检查手牌空位是否只剩下 1 个，如果是且还没有用过移出道具，则看广告或转发获得道具并使用，并且回到 1 重新循环
5. 找桌面上是否有和手牌相同的牌（避免手牌太花），如果有拿一张并且回到 1，否则 6
6. 找桌面上重复 2 次的牌，拿 1 张（似乎更有可能能快速消去），拿到则回 1，否则7
7. 拿桌面上任意一张牌，回 1


由于策略上极度贪心，且并没有考虑桌面上被压住的牌，所以目前而言，策略上会弱于人。


## 安装

```
安装python3
按pre_2_install_packages.bat 里安装python依赖包（多python的环境注意安装到使用的环境中）
```

手机端，使用了appium链接模拟器或者真实机，兼容ios和android，但是需要appium的环境，比较繁琐。简单使用安卓手机或者模拟器的话可以修改mobile_controller.py里的方法为python adb调试代码。

## 使用
在python环境中执行yang_processor.py