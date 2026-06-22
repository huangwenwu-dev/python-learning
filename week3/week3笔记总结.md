# 第三周笔记：Git/GitHub + 工程

## 📁 本周文件清单
| 文件 | 练的是什么 |
|------|-----------|
| 01_计算器_模块与异常.py | import mymath + try/except 安全计算器 |
| mymath.py | 自定义模块 add/subtract/divide（被 01 import，保留原名） |

## 一、用法速查（我要吃透的）
- Git 日常四步：`init` → `add` → `commit -m "说明"` → `push`
- 分支：`branch`、`merge`、冲突解决
- GitHub 认证：浏览器 OAuth 或 Personal Access Token（PAT）
- 模块化：自定义模块 + `if __name__ == "__main__":` 守卫
- 异常：`try` / `except` 针对具体异常类型
- README 用 Markdown 写；建立自己的 AI 使用守则

## 二、关键直觉（一句话记牢）
- Git 像游戏存档：`add` = 挑要存的进度，`commit` = 正式存档（在本地），`push` = 上传到云（GitHub）
- 分支 = 另开一个存档做实验，玩好了再 `merge` 回主线
- `if __name__ == "__main__":` = "只有直接运行我时才执行，被 import 时不执行"

## 三、本周踩坑记录
- `git commit` 忘 `-m` → 掉进 Vim 出不来（`:q!` 退出）
- GitHub 不再收账号密码，push 要 OAuth 或 PAT
- （我的机器）Windows 中文用户名 → SSH 路径编码报错（`\316\304`），改用 HTTPS 克隆绕过

## 四、回头补的盲区
- SSH 中文路径问题彻底修复 vs 长期用 PAT → 待决定
- `rebase`、`stash`、`tag` 等进阶 Git → 用到再学