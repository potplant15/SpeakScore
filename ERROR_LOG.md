# SpeakScore 错误日志

本文记录项目从初始化、服务开发、联调到云服务器部署过程中遇到的问题及处理方式。

## 1. Git 与初始化

- GitHub HTTPS 推送出现 403。GitHub 不再接受账号密码，需要 Personal Access Token（勾选 repo）或 SSH 密钥。

## 2. TTS / Reference Service

- Swagger Execute 返回 MP3 数据，但不会自动生成文件。使用 curl 的 --output test.mp3 保存响应。
- Practice Service 下载到的 mp3 实际是 JSON 错误报告。原因是上游 Reference Service 返回 500，而客户端仍用 mp3 文件名保存。使用 curl -fS 并检查 file 可以及时发现。


## 3. Kaldi / GOPT

- Kaldi 提示 Python 2.7、MKL 缺失。使用 Python 3 和 OpenBLAS 继续构建。
- fst/fst.h 找不到。原因是 OpenFST 没安装成功或路径错误；确认 tools/openfst-1.8.4/include/fst/fst.h 存在后重新配置。
- 旧版 OpenBLAS 构建脚本与新编译器不兼容，出现 SGEMM_DEFAULT_UNROLL_* undeclared。改用系统包 libopenblas-dev、liblapack-dev、liblapacke-dev。
- Ubuntu 24.04 新版 LAPACK 与旧 Kaldi wrapper ABI 不兼容，出现多个函数参数过少错误。没有继续完整编译，改为只编译实际需要的 GOP 工具。
- latbin、online2bin 部分目标链接时出现 undefined reference to main。最终采用最小构建方案，只生成 compute-gop。
- GOPT 对短音频和合成音频评分不稳定。曾尝试按 40～50 个音素分段加权平均，效果仍不满足需求，之后删除 GOPT 代码和资源，改用 OpenPronounce。

## 4. Practice Service / Maven

- Java 编译找不到 PageableDefault。补充 org.springframework.data.web.PageableDefault import。
- Practice Service 与上游服务调用失败时，下载接口可能把错误 JSON 保存成 MP3。通过直接检查上游健康状态和 curl -fS 定位。

## 5. Evaluation Service

- Whisper 首次运行访问 Hugging Face 失败，出现 Network is unreachable。将模型下载到 /home/ubuntu/whisper-model，挂载到容器 /models/whisper，并设置 WHISPER_MODEL=/models/whisper。
- Whisper 本地化后，OpenPronounce 仍需要 facebook/wav2vec2-lv-60-espeak-cv-ft，因此还会访问 Hugging Face。
- OpenPronounce 模型已经下载，但第一次复制缓存时缺少 hub 层级，导致服务仍请求远程地址。正确路径应为 /root/.cache/huggingface/hub/models--facebook--wav2vec2-lv-60-espeak-cv-ft。
- Compose 中加入 HF_HUB_OFFLINE=1 和 TRANSFORMERS_OFFLINE=1，可避免运行时继续联网。
- /health 只能说明 Uvicorn 进程正常，不能证明模型可用。必须直接 POST /api/v1/evaluate 验证。

## 6. 前端 / npm / 麦克风

- WSL 中混用了 Windows Node/npm，导致 UNC paths are not supported 和找不到 C:\Windows\install.js。应在 WSL 内使用 Linux Node/npm。
- 前端 Nginx 曾出现宿主机连接重置。检查容器端口、Nginx 配置和容器状态，重建 frontend 容器后恢复。
- ECDICT 补全下拉框曾超出宽度、遮挡按钮、截断释义。通过限制面板宽度、调整网格布局和移动端样式修复。
- 浏览器不允许普通 HTTP 页面使用麦克风。使用 localhost 或 Cloudflare HTTPS Tunnel。
- 浏览器录音是内存中的 Blob，不会自动生成服务器文件。测试时可下载 Reference Service 生成的音频作为测试输入。

## 7. Docker Compose

- Evaluation Service 仅健康检查通过，不代表评分模型已加载；应实际执行评分请求。

## 8. 云服务器 / Cloudflare

- 容器内部页面返回 200，但宿主机 5173 连接重置。通过检查 Nginx 监听、端口映射、容器日志并重新创建 frontend 容器解决。
- Cloudflare Quick Tunnel 每次重启可能生成新的 trycloudflare.com 地址，通过 docker logs speakscore-tunnel 查看。

