import asyncio
import time

async def task(name, seconds):
    print(f"⏳ {name} 开始...")
    await asyncio.sleep(seconds)
    print(f"✅ {name} 完成(用了 {seconds} 秒)")

async def main():
    start = time.time()
    # 现在是一个接一个 await(串行),还没用上并发
    await task("烧水", 3)
    await task("切菜", 2)
    print(f"总耗时：{time.time() - start:.1f} 秒")

asyncio.run(main())