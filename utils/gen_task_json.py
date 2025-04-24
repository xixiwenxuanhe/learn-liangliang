import os
import json

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "专栏"))
task_path = os.path.join(os.path.dirname(__file__), "task.json")

zhuanlans = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
tasks = [{"name": z, "status": "未完成"} for z in zhuanlans]

with open(task_path, "w", encoding="utf-8") as f:
    json.dump(tasks, f, ensure_ascii=False, indent=2)

print(f"已生成 {task_path}")