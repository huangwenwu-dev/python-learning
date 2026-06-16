# 🐙 Git 命令速查表

## 〇、一次性配置（装好 Git 后第一次做，永久生效）
- `git config --global user.name "名字"` —— 设置用户名
- `git config --global user.email "邮箱"` —— 设置邮箱

## 一、新建 / 获取仓库
- `git init` —— 把当前文件夹变成 Git 仓库（本地从零建）
- `git clone <网址>` —— 把远程仓库整个克隆到本地

## 二、关联远程仓库（开局，一个仓库只做一次）
- `git remote add origin <SSH地址>` —— 关联 GitHub 远程仓库
- `git remote -v` —— 查看当前关联了哪个远程地址
- `git branch -M main` —— 主分支命名为 main
- `git push -u origin main` —— 首次推送并建立关联

## 三、日常更新（每次改完都重复这四步）
- `git status` —— 查看改了哪些文件
- `git add .` —— 把所有改动加入暂存
- `git commit -m "说明"` —— 提交一个存档点
- `git push` —— 推送到 GitHub

## 四、拉取远程更新
- `git pull` —— 把远程最新代码拉到本地（换设备、多人协作、或 push 被拒时用）

## 五、分支操作
- `git switch -c 分支名` —— 创建并切换到新分支
- `git switch main` —— 切回主分支
- `git branch` —— 查看所有分支
- `git merge 分支名` —— 把某分支合并进当前分支
- `git branch -d 分支名` —— 删除分支

## 六、查看历史与改动
- `git log --oneline` —— 查看提交历史（简洁版）
- `git diff` —— 查看具体改了什么内容

## 七、常见报错排查（我踩过的坑）
- push 报 `[rejected]` → `git pull --no-rebase --no-edit` 再 `git push`
- push 报 `port 22 / 无法读取远程仓库` → 关掉 VPN 再推
- `git status` 报「不是 Git 仓库」→ 这文件夹还没 `git init`
- 不想提交的文件（如 `__pycache__`）→ 写进 `.gitignore`