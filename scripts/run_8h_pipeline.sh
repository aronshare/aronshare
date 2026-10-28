#!/usr/bin/env bash
set -e

# ==============================================================================
# AronShare 纯机械全自动流水线 (零 AI 消耗、零外部 Token 依赖)
# 周期：每 8 小时执行一次 (0 */8 * * *)
# 步骤：
#   1. 上游一手多源轮询扫描与入库 (V2EX、避难所、自学库、A姐一手等)
#   2. 规则化清洗与纯净零水印官方封面渲染
#   3. 生成无冒号、纯数字 URL 的 Markdown 标准规格文章
#   4. Astro 静态站秒级极速编译 (静态 HTML)
#   5. Rsync 热同步至 Nginx 生产目录并赋予权限
# ==============================================================================

WORK_DIR="/home/ubuntu/aronshare-resource-hub"
PYTHON_BIN="/home/ubuntu/.venvs/resource_crawler/bin/python3"
DEPLOY_DIR="/www/wwwroot/aronshare.com"

echo "=================================================================="
echo ">>> [$(date '+%Y-%m-%d %H:%M:%S')] 启动 AronShare 8小时机械全自动巡检与发布流水线"
echo "=================================================================="

cd "$WORK_DIR"

# 1. 抓取一手源头与上游素材
echo "[Step 1/5] 抓取上游一手源头与网盘/开源素材..."
"$PYTHON_BIN" "$WORK_DIR/scripts/fetch_upstream_sources.py" || true
"$PYTHON_BIN" "$WORK_DIR/scripts/fetch_ahhhhfs_100.py" || true

# 2. 渲染官方无水印封面 (Headless 原生截图)
echo "[Step 2/5] 渲染一手官网/GitHub 原生零水印高清封面..."
"$PYTHON_BIN" "$WORK_DIR/scripts/generate_clean_covers.py" || true

# 3. 规则化生产 Markdown 文章 (纯数字URL、无冒号标题、开源/网盘智能判断、多截图与深度正文)
echo "[Step 3/5] 提取全量一手多截图与丰富正文..."
"$PYTHON_BIN" "$WORK_DIR/scripts/build_rich_detail_posts.py"

# 4. Astro 静态编译
echo "[Step 4/5] 静态站点编译构建..."
npx astro build

# 5. 发布部署至生产环境
echo "[Step 5/5] 同步更新至 Nginx 生产目录..."
sudo rsync -av --delete "$WORK_DIR/dist/" "$DEPLOY_DIR/"
sudo chown -R www:www "$DEPLOY_DIR"

echo "=================================================================="
echo ">>> [$(date '+%Y-%m-%d %H:%M:%S')] 流水线执行完毕！全站资源已刷新上线。"
echo "=================================================================="
