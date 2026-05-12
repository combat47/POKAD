from huggingface_hub import snapshot_download
import requests

# تنظیم تایم‌اوت بالاتر
requests.adapters.DEFAULT_RETRIES = 5  # تلاش دوباره
requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=5)

# اسم مدل
model_name = "jamesdborin/ct2-int8-llama-2-7b-chat"

# دانلود با تنظیمات
model_path = snapshot_download(
    repo_id=model_name,
    local_dir="./models/llama-2-7b-chat-int8",
    local_files_only=False,
    resume_download=True,  # ادامه دانلود اگه قطع بشه
    max_workers=4,         # دانلود موازی با ۴ رشته
)

print(f"مدل توی {model_path} دانلود شد!")
