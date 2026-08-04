# -*- coding: utf-8 -*-
# @File : sensors_addon.py
# mitmproxy 插件：拦截神策埋点上报请求，解析事件并写入 JSONL 文件
# 由 sensorsCapture.py 通过 mitmdump -s 加载，不依赖项目其它模块

import os
import json
import base64
import gzip
import threading
from urllib.parse import parse_qs

from mitmproxy import http

EVENTS_FILE = os.environ.get("SENSORS_EVENTS_FILE")
HOST_FILTER = os.environ.get("SENSORS_HOST_FILTER", "sensorsjourney.com")
_lock = threading.Lock()


def _b64gunzip_json(data_str, gzip_flag):
    raw = base64.b64decode(data_str)
    if gzip_flag:
        try:
            raw = gzip.decompress(raw)
        except OSError:
            pass
    return json.loads(raw.decode("utf-8", errors="ignore"))


def _extract_events(obj):
    """从解析后的 payload 中提取事件列表，兼容多种神策 SDK 上报格式"""
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for key in ("data", "data_list"):
            val = obj.get(key)
            if isinstance(val, str):
                try:
                    return _b64gunzip_json(val, obj.get("gzip") == 1)
                except Exception:
                    return []
            if isinstance(val, list):
                return val
    return []


def _append(event, flow):
    if not isinstance(event, dict):
        return
    record = {
        "capture_ts": int(__import__("time").time() * 1000),
        "url": flow.request.pretty_url,
        "event": event.get("event"),
        "type": event.get("type"),
        "distinct_id": event.get("distinct_id"),
        "time": event.get("time"),
        "properties": event.get("properties", {}),
    }
    if not EVENTS_FILE:
        return
    line = json.dumps(record, ensure_ascii=False)
    with _lock:
        try:
            with open(EVENTS_FILE, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass


def request(flow: http.HTTPFlow):
    if HOST_FILTER not in flow.request.pretty_host:
        return
    events = []
    raw = flow.request.get_text(strict=False) or ""
    payload_obj = None
    if raw:
        try:
            payload_obj = json.loads(raw)
        except Exception:
            qs = parse_qs(raw)
            if "data" in qs:
                payload_obj = {"data": qs["data"][0],
                               "gzip": int(qs.get("gzip", ["0"])[0])}
            elif "data_list" in qs:
                payload_obj = {"data_list": qs["data_list"][0]}
    if payload_obj is not None:
        events = _extract_events(payload_obj)
    if not events:
        qdata = flow.request.query.get("data") or flow.request.query.get("data_list")
        if qdata:
            try:
                events = _b64gunzip_json(qdata, flow.request.query.get("gzip") == "1")
                if isinstance(events, dict):
                    events = [events]
            except Exception:
                events = []
    if isinstance(events, dict):
        events = [events]
    for ev in events or []:
        _append(ev, flow)
