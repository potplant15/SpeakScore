# 详细开发日志

## 开发周期与实际耗时

- 本阶段开发时间为 9 月 17 日至 9 月 20 日，实际投入约 13小时，主要完成微服务开发、联调、容器化和云服务器部署。
- 其中较多时间用于 Kaldi、声学模型、OpenPronounce、Whisper 和 Kokoro 模型的准备，以及云服务器网络受限情况下的资源迁移。

## 主要难点与解决方案

- TTS 服务：完成 FastAPI 和 gTTS 初版后，由于TTS库不支持英音美音的区分以及不同性别的发音，根据项目需求改为 Kokoro，并通过 Reference Service 统一处理英音、美音、性别和 IPA 参考音频。
- 发音评估：曾尝试接入 GOPT 和 Kaldi GOP 流程，但 Kaldi 编译、OpenBLAS/LAPACK 兼容性和模型资源准备成本较高，且实际部署后效果欠佳，最终采用 Whisper 负责内容识别、OpenPronounce 负责音素分析的方案。
- 模型下载：本地和云服务器多次遇到 GitHub、Hugging Face 及 Debian/PyPI 下载不稳定的问题。最终采用 Docker volume 缓存、镜像地址、离线模型目录挂载和本地下载后上传等方式，避免服务运行时重复下载模型。
- Docker 构建：Reference Service 和 Evaluation Service 存在较大的 Python 和系统依赖，构建时间较长。最终保留独立 Dockerfile 和 Docker Compose 服务编排，并通过缓存卷复用模型资源。
- 微服务联调：Practice Service 需要同时调用 Reference Service 和 Evaluation Service，期间出现音频返回错误报告、multipart 请求失败、模型加载超时和 Nginx 499 等问题。最终统一由 Practice Service 协调业务流程，并补充服务健康检查、错误提示和超时排查方式。
- 浏览器录音：公网 HTTP 环境无法稳定使用麦克风，曾使用 Cloudflare Quick Tunnel 临时提供 HTTPS，随后尝试配置正式域名、Let's Encrypt 证书和 Nginx 反向代理。
- 云端访问：曾遇到前端容器监听异常、Cloudflare Tunnel 回源地址不一致、HTTP 525 和备案限制等问题。最终放弃直接回源到服务器的域名方案，改为 Cloudflare Named Tunnel，并通过 host 网络让 Tunnel 访问服务器本机的前端端口。
- 用户输入与反馈：根据问卷反馈增加音频文件上传能力，并加入格式、大小、时长和音频可识别性校验；评分错误提示改为 `Expected`、`Heard` 和针对性解释，降低学习者理解成本。

## 关键判断与假设
- 采用微服务架构，是因为语音合成、标准发音生成、音频评估和练习业务的依赖、资源占用和迭代速度差异较大。拆分后可以独立开发、测试、部署和扩容，也能避免模型依赖影响核心业务服务。
- Practice Service 选择 Java 21、Spring Boot 和 MySQL，负责练习创建、状态管理、服务协调和数据持久化；Java 生态适合构建稳定的业务接口，MySQL 适合保存结构化练习记录和评分结果。
- Reference Service 选择 Python、FastAPI 和 Kokoro，负责生成标准参考音频和 IPA；Python 便于接入语音模型，FastAPI 适合提供轻量的音频 API，Kokoro 可以根据英音、美音和性别生成参考声音。
- Evaluation Service 选择 Python、FastAPI、Whisper 和 OpenPronounce，分别负责内容识别和发音音素评估；将模型计算与业务服务分离，可以独立处理模型加载、缓存和 CPU 资源限制。
- Frontend 选择 Vue 3 和 Vite，主要考虑其组件化开发体验、构建速度和对录音、音频播放、响应式布局等浏览器能力的支持。
- 使用 Docker 和 Docker Compose 管理服务，是为了统一本地、GitHub Actions 和云服务器的运行环境，并通过 volume 保存模型缓存和数据库数据。
- 最终公网入口采用 Cloudflare DNS 和 Named Tunnel；cloudflared 通过 `--network host` 和 HTTP/2 访问服务器本机的前端端口，Nginx/Certbot 直连方案作为曾经尝试过的中间方案保留在开发过程记录中。
- 第一版优先保证“标准句子、参考音频、用户音频、评分结果”的可运行链路，因此没有继续扩展数据库业务和复杂模型训练。
- 录音文件不长期保存到数据库，评估完成后由服务清理临时文件；系统主要保存练习信息和评分结果。
- 模型文件不提交到 Git 仓库，使用 Docker volume 或服务器本地目录挂载，以控制仓库体积和部署成本。
- 生产环境默认通过域名和 HTTPS 访问，8001、8002、8080、3306 等内部服务端口不应直接暴露到公网。

## 已知局限

- Kokoro、Whisper 和 OpenPronounce 模型仍然占用较多磁盘空间和内存，2 核 2 GB 服务器可以运行，但并发能力和首次评分速度有限。
- 模型下载和依赖安装依赖网络环境，完全自动化下载仍可能受到镜像不可用、网络超时或上游地址变化影响。
- OpenPronounce 的音素反馈依赖声学模型和音频质量，嘈杂环境、过短音频、口音差异和快速语速可能导致识别偏差。
- IPA 展示目前以机器生成和格式化结果为主，不完全等同于词典级人工标注。
- 当前发音错误反馈主要展示错误音素片段，还不能完整展示单词级或音节级的预期发音，学习者可能需要结合参考音频理解。
- 麦克风录音依赖浏览器权限、HTTPS、操作系统输入设备和浏览器兼容性；demo项目难以做多平台多设备适配，部分用户仍可能无法直接录音，需要使用音频文件上传作为替代方案。
- 音频文件上传目前只支持有限格式和大小，无法保证所有编码格式都能被浏览器和后端正确解码。
- 自动补全依赖 ECDICT 词典和后端查询，暂时主要提供前缀联想，不具备基于上下文的句子预测能力；网络延迟或词典服务异常时，提示可能变慢或不可用。
- 当前练习历史和趋势分析、错误发音专项训练、中文界面及更细粒度的音节评分仍属于后续优化方向。


# Development Log

## DAY1 / 9.17

- 创建 SpeakScore 项目仓库。
- 完成 TTS Service 基础功能：FastAPI、gTTS、健康检查和语音生成接口。
- 配置项目级和 TTS Service 级运行依赖、开发依赖。
- 添加 pytest 测试，测试结果为 3 passed。
- 添加 Dockerfile。
- 添加 GitHub Actions，完成 Docker 构建和接口测试。

当前进度：TTS Service 第一版开发完成，Docker 云端测试通过。

## DAY2 / 9.19

- 完成 Practice Service 第一版基础结构。
- 配置 Java 21、Spring Boot 3.5、Maven 和 MySQL 相关环境。
- 实现练习创建、查询、分页历史和标准音频接口。
- 接入 Reference Service 和 Evaluation Service。
- 实现练习状态管理、评分结果保存和 MySQL 持久化。
- 完成 Reference Service 改造，支持英音、美音以及不同性别声音选择。
- 更新 Reference Service 依赖和 Dockerfile，完成音频生成及 IPA 测试。
- 完成 Evaluation Service 改造，接入 OpenPronounce 进行发音评分。
- 完善 Evaluation Service 的音频识别、音素分析和评分结果返回。
- 配置 Maven 阿里云镜像并完成项目编译打包。

当前进度：Practice Service 基础功能完成，下一步进行三个服务的联调测试，并补充 Java 测试用例。

## DAY3 / 9.20

- 完成 Docker Compose 多服务部署配置和云服务器部署。
- 配置 MySQL、Kokoro 模型、Whisper 模型和 Hugging Face 缓存卷。
- 解决云服务器网络限制导致的 Kokoro、Whisper 和 OpenPronounce 模型下载失败问题。
- 完成 Kokoro 模型和 Whisper 模型的本地上传及容器挂载。
- 下载 OpenPronounce 所需的 Wav2Vec2 模型，并整理 Hugging Face 缓存目录结构。
- 配置 Evaluation Service 离线加载模型，避免运行时访问 Hugging Face。
- 修复前端 Nginx 代理和云端 API 访问问题。
- 使用 Cloudflare Quick Tunnel 提供 HTTPS 访问，使浏览器可以使用麦克风。
- 定位评分超时、Nginx 499 和模型缓存路径错误等部署问题。
- 创建完整错误日志，记录项目开发和部署过程中的问题及解决方法。

当前进度：项目已完成主要微服务和 Docker Compose 云端部署，当前重点是验证 OpenPronounce 离线模型缓存后的完整评分链路。

## DAY4 / 9.20

- 曾尝试将 `www.speakscore.icu` 的 DNS A 记录解析到云服务器。
- 曾使用 Certbot 为域名申请并部署 Let's Encrypt HTTPS 证书。
- 曾配置 Nginx 将 80/443 请求反向代理到前端容器 5173；该方案属于中间部署方案。
- 将前端、Reference Service、Evaluation Service、Practice Service 和 MySQL 的公网访问收敛到域名入口。
- 将 5173 改为仅监听服务器本机，关闭 8001、8002、8080 和 3306 的公网访问。
- 由于直接回源时出现 Cloudflare 525、备案限制和源站 HTTPS 握手问题，删除旧的 `@`、`www` A 记录，改用 Cloudflare Named Tunnel 的 Published Application。
- 最终架构为：Cloudflare DNS → Cloudflare Named Tunnel → `cloudflared --network host --protocol http2` → `127.0.0.1:5173` → 前端 Nginx → Practice Service 及其他内部服务。
- 收集并分析用户体验反馈问卷，确定移动端适配、评分解释、中文提示和练习历史为后续重点方向。
- 为前端增加 MP3、WAV、WEBM 和 M4A 音频上传功能，作为麦克风不可用时的备用方案。
- 增加上传文件格式、文件大小、音频时长和音频可识别性检查。
- 优化评分失败提示，区分音频无法识别、文件过大和评分服务暂时不可用等情况。
- 优化发音错误展示，改为 `Expected`、`Heard` 和针对性解释的学习者友好格式。
- 修复前端 Docker 镜像未及时更新导致远程页面仍显示旧版评分提示的问题，并完成重新构建说明。

当前进度：SpeakScore 已通过 Cloudflare Named Tunnel 和正式域名提供 HTTPS 访问，并支持麦克风录音和音频文件上传评分；Nginx/Certbot 直连方案不作为当前公网架构。
