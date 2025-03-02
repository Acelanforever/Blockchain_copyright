# 贡献指南

感谢您考虑为区块链版权保护系统做出贡献！以下是一些指导方针，帮助您参与到项目中来。

## 开发环境设置

1. 克隆仓库：
   ```bash
   git clone https://github.com/您的用户名/blockchain-copyright-protection.git
   cd blockchain-copyright-protection
   ```

2. 创建虚拟环境：
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 运行应用：
   ```bash
   python run.py
   ```

## 代码规范

- 遵循PEP 8 Python代码风格指南
- 为所有新功能编写测试
- 保持代码简洁明了
- 添加适当的注释和文档字符串

## 提交流程

1. 创建一个新分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. 进行更改并提交：
   ```bash
   git add .
   git commit -m "描述您的更改"
   ```

3. 推送到您的分支：
   ```bash
   git push origin feature/your-feature-name
   ```

4. 创建Pull Request：
   - 前往GitHub仓库页面
   - 点击"Compare & pull request"
   - 填写PR描述，解释您的更改
   - 提交PR

## 报告问题

如果您发现了bug或有新功能建议，请创建一个issue：

1. 前往GitHub仓库的Issues页面
2. 点击"New issue"
3. 选择适当的模板（如果有）
4. 提供详细描述，包括：
   - 问题的详细描述
   - 复现步骤
   - 预期行为与实际行为
   - 截图（如适用）
   - 环境信息（操作系统、浏览器等）

## 代码审查

所有提交的代码都将经过审查。请耐心等待反馈，并准备根据反馈进行修改。

## 行为准则

请尊重所有项目参与者，保持专业和友好的交流方式。

## 许可

通过贡献代码，您同意您的贡献将在MIT许可下发布。

感谢您的贡献！