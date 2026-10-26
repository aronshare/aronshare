#!/usr/bin/env python3
"""
专门用于抓取和监控上游 103+ 网盘资源站、知识付费自学课与绿色软件的爬虫引擎
(fetch_pan_sources.py)
"""

import sys
import os
import re
import time
import sqlite3
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime

DB_PATH = "/home/ubuntu/.hermes/profiles/xwriter/data/content_hub.db"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

def fetch_rss_feed(source_id, source_name, feed_url, category):
    try:
        req = urllib.request.Request(feed_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            
        root = ET.fromstring(content)
        items = root.findall(".//item")
        if not items:
            items = root.findall(".//{http://www.w3.org/2005/Atom}entry")
            
        log(f"[*] [{source_name}] 解析到 {len(items)} 条最新条目...")
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        new_count = 0
        
        for item in items[:20]:
            title_node = item.find("title") or item.find("{http://www.w3.org/2005/Atom}title")
            link_node = item.find("link") or item.find("{http://www.w3.org/2005/Atom}link")
            desc_node = item.find("description") or item.find("{http://www.w3.org/2005/Atom}summary") or item.find("{http://www.w3.org/2005/Atom}content")
            
            title = title_node.text.strip() if (title_node is not None and title_node.text) else ""
            if link_node is not None:
                link = link_node.text.strip() if link_node.text else link_node.attrib.get("href", "")
            else:
                link = ""
                
            desc = desc_node.text.strip() if (desc_node is not None and desc_node.text) else ""
            desc = re.sub(r'<[^>]+>', ' ', desc)
            desc = re.sub(r'\s+', ' ', desc).strip()[:300]
            
            if not title or not link:
                continue
                
            # 清除标题可能存在的特殊前缀
            clean_t = re.sub(r'^【.*?】\s*', '', title)
            
            # 查重
            cur.execute("SELECT id FROM raw_articles WHERE url = ?", (link,))
            if cur.fetchone():
                continue
                
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("""
                INSERT INTO raw_articles (source_id, source_name, title, url, summary, content_text, score, published_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (source_id, source_name, clean_t, link, desc, desc, 85, now_str, now_str))
            new_count += 1
            
        # 更新来源的 last_fetched_at
        cur.execute("UPDATE monitor_sources SET last_fetched_at = ? WHERE id = ?", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), source_id))
        conn.commit()
        conn.close()
        log(f"[√] [{source_name}] 新收录 {new_count} 篇一手资源！")
        
    except Exception as e:
        log(f"[!] [{source_name}] 抓取异常: {str(e)}")

def run_pan_sources_crawler():
    log("==================================================")
    log("🚀 启动 100+ 上游网盘资源站与知识付费自学课全量巡检")
    log("==================================================")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, feed_url, category 
        FROM monitor_sources 
        WHERE feed_url IS NOT NULL 
          AND feed_url != ''
          AND (
            category LIKE '%网盘%' OR 
            category LIKE '%课程%' OR 
            category LIKE '%副业%' OR 
            category LIKE '%资源%' OR 
            category LIKE '%工具%' OR 
            category LIKE '%自学%'
          )
    """)
    sources = cur.fetchall()
    conn.close()
    
    log(f"[*] 筛选出 {len(sources)} 个核心网盘与资源源头...")
    for s_id, s_name, s_url, s_cat in sources:
        fetch_rss_feed(s_id, s_name, s_url, s_cat)
        time.sleep(1)
        
    log("==================================================")
    log("🎉 100+ 网盘与一手资源站巡检完毕！")
    log("==================================================")

if __name__ == '__main__':
    run_pan_sources_crawler()
