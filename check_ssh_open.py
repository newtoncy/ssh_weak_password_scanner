# -*- coding: utf-8 -*-

# @File    : check_ssh_open.py
# @Date    : 2021-07-01
# @Author  : 王超逸
# @Brief   :
from asyncio import wait_for, TimeoutError, open_connection, run


async def check_ssh_open(ip: str, port: int = 22):
    try:
        reader, writer = await wait_for(open_connection(ip, port), 2)
    except (TimeoutError, OSError) as e:
        return False

    try:
        s = await wait_for(reader.readuntil(b"\n"), 3)
        s = s.decode()
        if s.startswith("SSH"):
            return ip, s.strip()
    except TimeoutError as e:
        pass
    finally:
        writer.close()
        # await writer.wait_closed()
    return False


async def main():
    print(await check_ssh_open("139.224.83.179"))


if __name__ == '__main__':
    run(main())
