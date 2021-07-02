# -*- coding: utf-8 -*-

# @File    : main.py
# @Date    : 2021-07-02
# @Author  : 王超逸
# @Brief   : 
import asyncio, time, sys
from logging import getLogger
from logging_config import config_logging
from functools import partial
from copy import deepcopy
from load_file import read_password_dict, read_ips
from check_passwd import check_passwd

logger = getLogger()
done_logger = getLogger("checked")
result_logger = getLogger("result")

count = 0
done = 0
submit = 0
find = 0
FLAG = type("FLAG", (object,), {})()
args_default = {"worker": 20000, "password": "password.txt", "hosts": "ssh_ip.txt"}
args_define = {
    "--worker": (int, "worker"), "-w": (int, "worker"),
    "--password": (str, "password"), "-p": (str, "password"),
    "--hosts": (str, "hosts"), "-h": (str, "hosts")
}


def progress_callback(x):
    global count
    count += 1


async def progress_display():
    time1 = 0
    count1 = 0
    while True:
        print(f"\r尝试密码{count}次，尝试主机{submit}个，"
              f" 完成{done}个，找到{find}个，"
              f" 速度{(count - count1) / (time.time() - time1):.1f}每秒",
              end=f"")
        time1 = time.time()
        count1 = count
        await asyncio.sleep(1)


def handle_args():
    cmd_args = sys.argv[1:]
    args_dict = {}
    for i, arg in enumerate(cmd_args):
        if arg in args_define:
            if i + 1 < len(cmd_args):
                type_, name = args_define[arg]
                if type_ != FLAG:
                    args_dict[name] = type_(cmd_args[i + 1])
                else:
                    args_dict[arg] = True
    ret = deepcopy(args_default)
    ret.update(args_dict)
    return ret


def handle_task_done(task, host):
    global done, find
    assert task.done()
    done += 1
    done_logger.info(host)
    if task.exception():
        logger.error(f"{host}->{repr(task.exception())}\n"
                     f"{task.get_stack()}")
        return
    logger.info(f"{host}已完成")
    if task.result():
        passwd, login_str = task.result()
        result_logger.info(login_str)
        find += 1


async def main():
    global submit
    config_logging()
    asyncio.create_task(progress_display())
    arg_dict = handle_args()
    worker = arg_dict["worker"]
    password = arg_dict["password"]
    hosts = arg_dict["hosts"]
    pw_set = read_password_dict(password)
    host_iter = read_ips(hosts)
    semaphore = asyncio.locks.Semaphore(worker)
    unfinished_task_set = set()
    all_done_event = asyncio.locks.Event()

    def done_callback(x):
        semaphore.release()
        unfinished_task_set.remove(x)
        if not unfinished_task_set:
            all_done_event.set()

    async for host in host_iter:
        await semaphore.acquire()
        task = asyncio.create_task(check_passwd(host, pw_set, progress_callback=progress_callback))
        submit += 1
        unfinished_task_set.add(task)
        all_done_event.clear()
        task.add_done_callback(done_callback)
        task.add_done_callback(partial(handle_task_done, host=host))
    await all_done_event.wait()


if __name__ == '__main__':
    asyncio.run(main())
