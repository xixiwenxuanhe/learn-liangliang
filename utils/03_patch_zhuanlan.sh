#!/bin/bash

cd "$(dirname "$0")"

TASK_FILE="task.json"

# 读取未完成的任务
readarray -t unfinished < <(jq -r '.[] | select(.status=="未完成") | .name' "$TASK_FILE")

for zhuanlan in "${unfinished[@]}"; do
    echo "开始处理专栏: $zhuanlan"
    python ./03_patch_others.py --column "专栏/$zhuanlan"
    # 标记为已完成
    tmp=$(mktemp)
    jq --arg name "$zhuanlan" 'map(if .name == $name then .status = "已完成" else . end)' "$TASK_FILE" > "$tmp" && mv "$tmp" "$TASK_FILE"
    echo "已完成: $zhuanlan"
done

echo "全部专栏处理完毕。" 