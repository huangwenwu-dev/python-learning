# 🐙 Git 命令速查表

## 一、开局：新建仓库（一个仓库只做一次）
- `git init` —— 把文件夹变成 Git 仓库（新建相册）
- `git remote add origin <SSH地址>` —— 连接 GitHub 仓库
- `git branch -M main` —— 主分支命名为 main
- `git push -u origin main` —— 第一次推送

## 二、日常更新（每次改完都重复这四步）
- `git status` —— 查看改了哪些文件
- `git add .` —— 把所有改动加入暂存
- `git commit -m "说明"` —— 提交一个存档点
- `git push` —— 推送到 GitHub

## 三、分支操作
- `git switch -c 分支名` —— 创建并切换到新分支
- `git switch main` —— 切回主分支
- `git branch` —— 查看所有分支
- `git merge 分支名` —— 把某分支合并进当前分支
- `git branch -d 分支名` —— 删除分支

## 四、查看历史与改动
- `git log --oneline` —— 查看提交历史（简洁版）
- `git diff` —— 查看具体改了什么内容

## 五、常见报错排查（我踩过的坑）
- push 报 `[rejected]` → `git pull --no-rebase --no-edit` 再 `git push`
- push 报 `port 22 / 无法读取远程仓库` → 关掉 VPN 再推
- `git status` 报「不是 Git 仓库」→ 这文件夹还没 `git init`
- 不想提交的文件（如 `__pycache__`）→ 写进 `.gitignore`