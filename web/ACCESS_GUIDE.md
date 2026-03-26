# 外观商业化工具 - 访问指南

## 🌐 访问地址

### 本地访问（服务器上）
```
http://localhost:5001
```

### 局域网访问
```
http://192.168.x.x:5001
```

### 公网访问
```
http://14.103.82.202:5001
```

⚠️ **公网访问需要配置云服务商安全组**

---

## 🔧 方案A：配置云服务商安全组（推荐）

### 阿里云 ECS
1. 登录阿里云控制台
2. 进入「云服务器ECS」→「实例与镜像」
3. 找到这台服务器，点击「更多」→「网络和安全组」→「安全组配置」
4. 点击「配置规则」→「快速添加」
5. 选择「HTTP(80)」，修改端口为「5001」

### 腾讯云 CVM
1. 登录腾讯云控制台
2. 进入「云服务器」→「实例」
3. 找到这台服务器，点击「更多」→「安全组」→「配置安全组」
4. 点击「添加规则」
5. 入站规则：端口 5001，协议 TCP，来源 0.0.0.0/0

### 华为云 ECS
1. 登录华为云控制台
2. 进入「弹性云服务器ECS」
3. 找到这台服务器，点击「安全组」
4. 添加入站规则：端口 5001

---

## 🔧 方案B：使用frp反向代理

如果你有另一台有公网IP的服务器，可以使用frp：

### 步骤1：服务端（公网服务器）
```bash
# frps.ini
[common]
bind_port = 7000
vhost_http_port = 8080

# 启动
./frps -c frps.ini
```

### 步骤2：客户端（当前服务器）
```bash
# frpc.ini
[common]
server_addr = 你的公网服务器IP
server_port = 7000

[appearance-tool]
type = http
local_port = 5001
custom_domains = your-domain.com

# 启动
./frpc -c frpc.ini
```

---

## 🎯 快速测试

### 1. 测试服务状态
```bash
curl http://localhost:5001/api/game-types
```

### 2. 查看日志
```bash
tail -f /tmp/appearance-tool.log
```

### 3. 重启服务
```bash
cd /workspace/projects/workspace/tools/appearance-commerce-tool/web
./start.sh
```

---

## 📱 移动端访问

如果配置了公网访问，手机浏览器直接访问：
```
http://14.103.82.202:5001
```

---

## ⚠️ 常见问题

### 问题1：无法访问公网地址
**原因**：云服务商安全组未配置  
**解决**：参考上面的「方案A」

### 问题2：服务未运行
**检查**：
```bash
ps aux | grep app.py
```
**重启**：
```bash
cd /workspace/projects/workspace/tools/appearance-commerce-tool/web
./start.sh
```

### 问题3：端口被占用
**检查**：
```bash
netstat -tuln | grep 5001
```
**解决**：修改app.py中的端口号

---

## 🎨 使用流程

1. 访问网址
2. 选择游戏品类（MOBA/FPS/模拟经营）
3. 选择外观类型（皮肤/装饰/特效等）
4. 完成决策树引导（3个决策）
5. 完成检查清单验证
6. 生成AI分析报告！

---

## 📞 需要帮助？

如果遇到问题，检查：
1. 服务是否运行：`ps aux | grep app.py`
2. 端口是否监听：`netstat -tuln | grep 5001`
3. 日志是否有错误：`tail -f /tmp/appearance-tool.log`
4. 安全组是否配置：登录云服务商控制台
