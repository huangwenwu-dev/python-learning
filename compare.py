import httpx
import asyncio
import time

urls = ["https://httpbin.org/delay/2"] * 3

# ===== 同步版 =====
def sync_fetch():
    start = time.time()
    for url in urls:
        httpx.get(url, timeout=30)
    return time.time() - start

# ===== 异步并发版 =====
async def fetch(client, url):
    await client.get(url)

async def async_fetch():
    start = time.time()
    async with httpx.AsyncClient(timeout=30) as client:
        await asyncio.gather(*[fetch(client, url) for url in urls])
    return time.time() - start

# ===== 对比 =====
print("开始测试 3 个请求...\n")

sync_time = sync_fetch()
print(f"🐌 同步串行：{sync_time:.1f} 秒")

async_time = asyncio.run(async_fetch())
print(f"⚡ 异步并发：{async_time:.1f} 秒")

print(f"\n异步快了约 {sync_time / async_time:.1f} 倍！")