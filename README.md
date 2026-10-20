# Biao (Joseph) Yin — 个人主页

## 简介

单文件静态网站（`index.html`），无需构建，可直接部署到 GitHub Pages。`tools/` 下是 Citation map 生成脚本。

## 部署到 GitHub Pages

1. 在 GitHub 新建仓库，名称为 `用户名.github.io`（例如 `josephyin.github.io`），Public，不勾选 README。
2. 在本文件夹执行：
   ```bash
   git init
   git add .
   git commit -m "Initial homepage"
   git branch -M main
   git remote add origin https://github.com/用户名/用户名.github.io.git
   git push -u origin main
   ```
3. 仓库 Settings → Pages → Source 选 `Deploy from a branch`，Branch 选 `main`，目录 `/(root)`，Save。
4. 1–2 分钟后访问 `https://用户名.github.io/`。

> 如果仓库名不是 `用户名.github.io`，网址会是 `https://用户名.github.io/仓库名/`。

## Citation map（引用者世界地图）

网站里已预留 “Citations” 板块，**默认完全隐藏**（导航里也不显示）。只有当仓库根目录存在 `citation_map.html` 时，板块和导航项才会自动出现。所以没审核过的地图不会上线。

1. 安装：`pip install citation-map`（需本机已安装 Google Chrome）。
2. 在**本地**仓库根目录运行（Scholar ID 已填好）：
   ```bash
   python tools/make_citation_map.py PyuaaWAAAAAJ --processes 1
   ```
   不要放到 GitHub Actions 里跑，Google Scholar 会屏蔽云服务器 IP。
3. 审核：用浏览器打开 `citation_map.html` 看地图，逐条核对 `citation_info.csv`（引用者、引用论文、被引论文、机构、地点）。
   - 机构或坐标有误：直接改 `citation_info.csv`，再运行 `python tools/make_citation_map.py PyuaaWAAAAAJ --from-csv` 重新出图（不会重新抓取）。
   - 想去掉自引：在 CSV 里删掉对应行后同样用 `--from-csv` 重新出图。
4. 确认无误后上线：
   ```bash
   git add citation_map.html
   git commit -m "Add citation map"
   git push
   ```
   `citation_info.csv` 含引用者姓名，已写入 `.gitignore`，默认不上传。

注意事项：

- 运行中可能弹出 CAPTCHA，需在 Chrome 窗口中手动完成。
- 如被屏蔽：换网络 / VPN 换 IP，或加 `--proxy` 使用代理。
- `--conservative` 只用 Scholar 认证过的机构信息，更准但会漏一些。
- 不要频繁运行，每隔几个月更新一次即可。
- 想下线地图：删除仓库里的 `citation_map.html` 并 push，板块会自动隐藏。

## 需要你自己补充的内容

打开 `index.html`，搜索 `Edit here`：

- `LINKS`：Google Scholar 和邮箱已填好；LinkedIn、GitHub、CV 填上链接后会出现在顶部导航栏的图标里，留空的不显示。
- 简历 PDF：把 CV 存为 `cv.pdf` 放进仓库（**先删掉电话号码**），然后把 `CV` 的 `href` 改为 `"cv.pdf"`。
- 头像：把照片存为 `photo.jpg` 放进仓库，在 `<div class="portrait" id="mark">` 内加入 `<img src="photo.jpg" alt="">`，默认的晶粒纹理占位图会自动隐藏。
- Path（履历）：`<ol class="path">` 中每个 `<li>` 是一站，按时间从早到晚；当前一站加 `now` 类会用蓝线高亮。
- What's new：直接写在 HTML 的 `<ul class="news">` 中，新动态放最上面；旧动态移到 “More” 折叠区（`<details>`）。
- `PUBS`：论文列表。`first:true` 表示一作（显示为 †）；`tag` 取 `clinical` | `science` | `ml` | `learning` 之一；论文正式发表后把 `"Under review"` 改为年份。

## 本地预览

```bash
python3 -m http.server 8000
```

然后打开 <http://localhost:8000>。（Citations 板块只在这种方式或线上才会检测并显示；直接双击打开 `file://` 时不显示。）

## 自定义域名（可选）

在仓库根目录新建 `CNAME` 文件，写入域名（如 `josephyin.ai`），并在域名服务商处添加指向 GitHub Pages 的 DNS 记录。
