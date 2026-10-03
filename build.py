import json, urllib.request, urllib.parse, html, datetime
UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)","Accept-Encoding":"identity","Accept":"application/json"}
def fetch(url, headers=None):
    h=dict(UA); h.update(headers or {})
    req=urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))
def grab_douyin():
    try:
        d=fetch("https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/", {"Referer":"https://www.douyin.com/"})
        out=[]
        for x in d.get("word_list",[])[:25]:
            w=x.get("word","")
            u="https://www.douyin.com/search/" + urllib.parse.quote(w)
            out.append((w, x.get("hot_value",0), u))
        return out
    except Exception as e: return [("(抖音源暂不可用: %s)"%e,0,"")]
def grab_weibo():
    try:
        d=fetch("https://weibo.com/ajax/side/hotSearch", {"Referer":"https://weibo.com/"})
        out=[]
        for x in d.get("data",{}).get("realtime",[])[:25]:
            w=x.get("word","")
            scheme=x.get("word_scheme") or w
            u="https://s.weibo.com/weibo?q=" + urllib.parse.quote(scheme)
            out.append((w, x.get("num",0), u))
        return out
    except Exception as e: return [("(微博源暂不可用: %s)"%e,0,"")]
def render(title, items):
    rows=""
    for i,(w,val,u) in enumerate(items,1):
        extra=' <span class="hv">%s</span>' % format(val, ",") if val else ""
        link='<a class="t" href="%s" target="_blank" rel="noopener">%s</a>' % (html.escape(u), html.escape(w)) if u else '<span class="t">%s</span>' % html.escape(w)
        rows+='<li><span class="idx">%d</span>%s%s</li>\n' % (i, link, extra)
    return '<h2>%s</h2><ol>\n%s</ol>' % (title, rows)
dou, wb = grab_douyin(), grab_weibo()
now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
secs=render("抖音热点",dou)+render("微博热搜",wb)
css = "body{font-family:system-ui,PingFang SC,Microsoft YaHei,sans-serif;margin:0;background:#0f1117;color:#e6e8ef}.wrap{max-width:760px;margin:0 auto;padding:24px 16px 60px}h1{font-size:22px}h2{font-size:16px;margin:26px 0 10px;border-bottom:1px solid #23283a;padding-bottom:8px}.meta{color:#8a93ab;font-size:13px;margin-bottom:8px}ol{list-style:none;margin:0;padding:0}li{display:flex;align-items:baseline;gap:10px;padding:9px 6px;border-bottom:1px solid #1a1f2e;font-size:15px}.idx{color:#5b6478;min-width:22px;font-variant-numeric:tabular-nums}li:nth-child(-n+3) .idx{color:#fe6d3c;font-weight:700}.t{flex:1;color:#cbd2e6;text-decoration:none;word-break:break-word}.t:hover{color:#7aa2ff;text-decoration:underline}.hv{color:#7b5dfe;font-size:13px;font-variant-numeric:tabular-nums}"
favicon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Cdefs%3E%3ClinearGradient id='flame' x1='0' y1='1' x2='0' y2='0'%3E%3Cstop offset='0%25' stop-color='%23ff2a2a'/%3E%3Cstop offset='60%25' stop-color='%23ff7a00'/%3E%3Cstop offset='100%25' stop-color='%23ffd84d'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='64' height='64' rx='14' fill='%230f1117' stroke='%2323283a' stroke-width='1.5'/%3E%3Cpath d='M32 10 C32 10 38 18 38 26 C38 28 37 30 36 31 C39 27 46 31 46 39 C46 48 39 54 32 54 C25 54 18 48 18 39 C18 32 23 24 28 18 C30 24 34 26 32 30 C34 28 36 22 32 10 Z' fill='url(%23flame)'/%3E%3Cpath d='M32 36 C34 38 35 41 35 44 C35 48 33 50 32 50 C31 50 29 48 29 44 C29 41 31 38 32 36 Z' fill='%23ffffff' opacity='0.9'/%3E%3C/svg%3E"
page = '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>今日热榜聚合 · 全网热点实时追踪</title><link rel="icon" href="' + favicon + '"><style>' + css + '</style></head><body><div class="wrap"><h1>🔥 今日热榜聚合</h1><div class="meta">更新时间：' + now + ' · 每 30 分钟自动刷新 · 点击标题直达搜索/话题页</div>' + secs + '</div></body></html>'
open("index.html","w",encoding="utf-8").write(page)
print("ok douyin=%d weibo=%d" % (len(dou),len(wb)))
