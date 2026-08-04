# -*- coding: utf-8 -*-
# @Author: leikaifu
# @File : sensorsQuery.py
# 神策埋点数据查询工具，用于测试埋点验证

import time
import requests
from commons.utils.readconfig import INIConfigReader
from commons.utils.myLogging import get_logger

logger = get_logger()


class SensorsQuery:
    """
    神策（Sensors Data）SQL 查询接口封装
    通过 config.ini 中 [sensors] 段的 key / url / project 发起查询
    """

    def __init__(self):
        cfg = INIConfigReader()
        self.token = cfg.getconfig('sensors', 'key')
        self.url = cfg.getconfig('sensors', 'url').rstrip('/')
        self.project = cfg.getconfig('sensors', 'project')
        self.query_api = f'{self.url}/api/sql/query'

    def query_sql(self, sql):
        """
        执行神策 SQL 查询
        :param sql: 神策 SQL 语句
        :return: 查询结果列表（list[dict]），失败返回 None
        """
        try:
            resp = requests.post(
                self.query_api,
                params={
                    'project': self.project,
                    'token': self.token,
                    'q': sql,
                    'format': 'json'
                },
                timeout=30
            )
            resp.raise_for_status()
            result = resp.json()
            logger.info(f"神策查询成功，返回 {len(result) if isinstance(result, list) else '?'} 条记录")
            return result
        except Exception as e:
            logger.error(f"神策查询失败: {e}")
            return None

    def query_event(self, event_name, minutes=5, limit=10):
        """
        查询最近 N 分钟内指定事件的上报记录
        :param event_name: 埋点事件名
        :param minutes: 向前查询的分钟数，默认5
        :param limit: 返回条数上限
        :return: 事件记录列表，无记录返回空列表，查询失败返回 None
        """
        start_ms = int((time.time() - minutes * 60) * 1000)
        sql = (f"SELECT * FROM events WHERE event = '{event_name}' "
               f"AND time > {start_ms} ORDER BY time DESC LIMIT {limit}")
        result = self.query_sql(sql)
        if result is None:
            return None
        logger.info(f"事件 [{event_name}] 最近{minutes}分钟内上报 {len(result)} 条")
        return result

    def assert_event_reported(self, event_name, minutes=5, retries=3, interval=20):
        """
        断言某事件已上报（带重试，应对埋点批量上报延迟）
        :param event_name: 埋点事件名
        :param minutes: 每次查询向前覆盖的分钟数
        :param retries: 重试次数
        :param interval: 重试间隔秒数
        :return: True 查询到记录；否则抛 AssertionError
        """
        for attempt in range(1, retries + 1):
            result = self.query_event(event_name, minutes)
            if result:
                logger.info(f"埋点验证通过: {event_name}")
                return True
            if attempt < retries:
                logger.info(f"第{attempt}次未查询到 [{event_name}]，{interval}s 后重试...")
                time.sleep(interval)
        raise AssertionError(f"埋点验证失败: 未查询到事件 [{event_name}] 的上报记录")


if __name__ == '__main__':
    sq = SensorsQuery()
    data = sq.query_event('$AppViewScreen', minutes=60)
    logger.info(data)
