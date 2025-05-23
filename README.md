# 区块链版权保护系统

## 项目介绍

这是一个基于区块链技术的版权保护系统，作为区块链课程的大作业项目。该系统利用区块链的不可篡改性和分布式账本特性，为数字作品提供可信的版权登记、转让和验证服务。

## 技术栈

- 后端：Flask 2.0.1
- 数据库：SQLAlchemy 1.4.23
- 用户认证：Flask-Login 0.5.0
- 加密：cryptography 3.4.7
- 前端：Bootstrap 5.1.3

## 系统功能

### 1. 用户管理
- 用户注册与登录
- 个人信息管理

### 2. 版权管理
- 作品上传与版权登记
- 版权信息查询
- 版权转让申请与确认

### 3. 区块链功能
- 版权信息上链
- 区块链浏览器
- 版权转让记录查询

## 使用教程

### 环境准备

1. 确保已安装Python 3.7+
2. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```

### 系统启动

1. 运行应用：
   ```
   python run.py
   ```
2. 访问 http://localhost:5000 进入系统

### 功能使用指南

#### 1. 用户注册与登录
1. 访问首页，点击"登录"按钮
2. 如果没有账号，点击"注册"链接
3. 填写用户名、邮箱和密码完成注册
4. 使用注册的账号登录系统

#### 2. 版权登记
1. 登录后，点击导航栏的"上传作品"按钮
2. 填写作品标题、描述
3. 上传作品文件（支持格式：png, jpg, jpeg, gif, pdf, doc, docx）
4. 点击"提交"按钮，系统会自动计算文件哈希并将版权信息记录到区块链
5. 上传成功后，可在首页查看已登记的版权信息

#### 3. 版权转让
1. 在版权详情页面，点击"申请转让"按钮
2. 选择转让对象（系统用户）
3. 确认转让信息并提交
4. 转让接收方登录系统后，可在"待处理转让"中查看并确认转让请求
5. 确认后，版权所有权将更新，并在区块链上记录此次转让

#### 4. 区块链浏览
1. 点击导航栏的"区块链浏览器"按钮
2. 查看所有区块信息，包括区块哈希、时间戳和交易记录
3. 点击具体区块可查看详细交易信息

#### 5. 版权验证
1. 在首页或搜索结果中点击版权条目
2. 查看版权详情，包括区块链记录
3. 通过区块哈希可验证版权信息的真实性和完整性

## 注意事项

1. 本系统仅用于学习和演示，不具备法律效力
2. 上传的文件应确保无侵权行为
3. 系统默认使用SQLite数据库，数据存储在本地
4. 区块链数据仅在应用运行期间有效，重启应用后会重新同步

## 开发者信息

本项目作为区块链课程大作业，展示了区块链技术在数字版权保护领域的应用。
