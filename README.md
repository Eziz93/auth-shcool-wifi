# auth-shcool-wifi
江苏科技大学 张家港校区/苏州理工学院 校园网认证脚本

## 脚本说明
运行环境：Win10 pytho3.6及以上

auth-login.py: 登录校园网脚本 

conf/data_post.json: 配置登录用户名、密码和域（电信或移动）

conf/configure.json: 配置文件，不需要改动

log/login.log: 登录脚本日志

## 使用方法

### auth-login.py 登录

1. 配置用户名、密码和域
    * username: 用户名
    * password: 密码
    * domain: 移动填写"CMCC"/电信填写"ChinaNet"
    * enablemacauth: 0
2. 打开powershell或者cmd
```bash
python /path/auth-login.py
```

## TODO List

- [ ] Linux运行支持
- [ ] 优化代码
- [ ] 优化日志框架

