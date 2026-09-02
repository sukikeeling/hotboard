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
page = '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>热榜聚合 · HotBoard</title><style>' + css + '</style></head><body><div class="wrap"><h1>🔥 热榜聚合</h1><div class="meta">更新时间：' + now + ' · 每 30 分钟自动刷新 · 点击标题直达搜索/话题页</div>' + secs + '</div></body></html>'
open("index.html","w",encoding="utf-8").write(page)
print("ok douyin=%d weibo=%d" % (len(dou),len(wb)))
