head08_test — UI 工作区

说明
- 这是专门用于把 Figma 设计稿落地的工作目录（head08）。
- 建议把所有导出的切图 / SVG 放到 `assets/`：
  - `assets/images/` - 背景图、位图切片
  - `assets/ui/` - 按钮/控件切图
  - `assets/icons/` - SVG 图标

依赖
- 当前 index.html 默认引用了 `../head07_test/vendor/gsap.min.js` 和 `../head07_test/vendor/Tone.min.js`，因为项目里已有拷贝。你可以：
  - 保持不动（允许复用现有 vendor），或
  - 把 vendor 库复制到 `head08_test/vendor/` 并把 index.html 中脚本指向本地 `vendor/`。

运行（开发）
1. 打开 PowerShell：
   ```powershell
   cd 'c:\Users\fi\Desktop\try\EmotiKeys_2_Fifi\EmotiKeys_2\head08_test'
   python -m http.server 3000
   ```
2. 在浏览器打开 `http://localhost:3000` 来预览 UI。

下一步建议
- 把 Figma 导出的图像放到 `assets/`，然后在 `styles.css` 中引入并替换按钮样式。
- 如果你希望我替你把导出的 assets 加入仓库并更新 HTML/CSS/JS，我可以帮你完成并提交变更。