# -*- coding: utf-8 -*-

# @File    : load_file.py
# @Date    : 2021-07-02
# @Author  : 王超逸
# @Brief   : 从我的ssh扫描器中读取ip列表
import aiofiles
import asyncio


async def read_ips(file_name: str):
    async with aiofiles.open(file_name) as f:
        async for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ip = line.split("->")[0].split("]")[1].strip()
                yield ip
            except IndexError as e:
                yield line


def read_password_dict(file_name: str):
    pd_set = set()
    with open(file_name) as f:
        for line in f:
            pd_set.add(line.strip())
    return pd_set


if __name__ == '__main__':
    async def main():
        async for ip in read_ips("ssh_ip.txt"):
            print(ip)


    asyncio.run(main())
