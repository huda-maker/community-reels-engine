"""HwznGo reel, flat-illustration version with synthesized sound effects (after the creator's second reference).

Run from the repo root. Writes the composition and sfx.wav (original, generated here; no third-party audio).
Speech text appears in framed labels at the measured phrase times of the approved captions.
"""
import json
import math
import shutil
import wave
from pathlib import Path

import numpy as np

P = Path("projects/hwzngo-direct-channel")
SRC = next(d for d in (P / "style-hwzngo-faceless" / "assets", P / "style-hwzngo-flat" / "assets") if d.exists())
OUT = P / "style-hwzngo-flat"
TOTAL = 30.0

O, D, K, C, PEACH, SKIN, SKIN_D = "#EB573E", "#C94530", "#36373B", "#FBF3EA", "#F8D9CC", "#E9A27F", "#D0835F"

STORE = f'''<svg viewBox="0 0 600 560"><rect x="20" y="520" width="560" height="14" rx="7" fill="{K}" opacity=".15"/>
<rect x="60" y="150" width="480" height="372" rx="10" fill="#F3E2CF"/><rect x="60" y="470" width="480" height="52" fill="#E7CDB2"/>
<rect x="40" y="118" width="520" height="44" rx="10" fill="{K}"/>
<g>{''.join(f'<path d="M{40+i*65} 162h65v60a32.5 32.5 0 0 1-65 0z" fill="{O if i%2==0 else "#FFFFFF"}"/>' for i in range(8))}</g>
<rect x="170" y="28" width="260" height="84" rx="18" fill="{O}"/><text x="300" y="88" text-anchor="middle" font-family="Cairo" font-weight="900" font-size="50" fill="#fff">مطعمك</text>
<rect x="96" y="282" width="200" height="160" rx="12" fill="#CFE6EE" stroke="{K}" stroke-width="8"/><path d="M196 282v160M96 362h200" stroke="{K}" stroke-width="6"/>
<rect x="346" y="272" width="150" height="250" rx="12" fill="{D}"/><circle cx="470" cy="402" r="9" fill="#FFD36B"/><rect x="366" y="292" width="110" height="80" rx="8" fill="#F6B3A3"/>
<circle cx="120" cy="470" r="34" fill="#7BAE7F"/><rect x="104" y="476" width="32" height="46" rx="6" fill="{D}"/></svg>'''

def person(c1="#FFFFFF", band=K, scale=1):
    return f'''<svg viewBox="0 0 220 420"><ellipse cx="110" cy="408" rx="80" ry="10" fill="{K}" opacity=".12"/>
<path d="M40 410c0-130 20-220 70-220s70 90 70 220z" fill="{c1}" stroke="#E2D3C2" stroke-width="4"/>
<path d="M110 196v60" stroke="#E2D3C2" stroke-width="4"/>
<circle cx="110" cy="112" r="50" fill="{SKIN}"/>
<path d="M54 120c-6-58 26-86 56-86s62 28 56 86l14 70H40z" fill="#FFFFFF" stroke="#E2D3C2" stroke-width="4"/>
<circle cx="110" cy="120" r="40" fill="{SKIN}"/><rect x="60" y="62" width="100" height="16" rx="8" fill="{band}"/>
<circle cx="96" cy="118" r="5" fill="{K}"/><circle cx="124" cy="118" r="5" fill="{K}"/>
<path d="M92 140c10 10 26 10 36 0" stroke="{K}" stroke-width="5" fill="none" stroke-linecap="round"/>
<path d="M84 146c4 22 48 22 52 0" fill="{K}" opacity=".85"/></svg>'''

HAND_BACK = f'''<svg viewBox="0 0 560 760" class="hand-b"><rect x="170" y="560" width="230" height="220" fill="#FFFFFF" stroke="#E2D3C2" stroke-width="4"/>
<path d="M120 380c0-60 40-90 100-90h140c60 0 90 40 90 100v160c0 70-50 120-120 120H220c-60 0-100-50-100-110z" fill="{SKIN}"/></svg>'''
HAND_FRONT = f'''<svg viewBox="0 0 560 760" class="hand-f">
<path d="M440 330c40-10 70 10 70 50v50c0 34-24 52-60 52" fill="{SKIN}" stroke="{SKIN_D}" stroke-width="4"/>
<g fill="{SKIN}" stroke="{SKIN_D}" stroke-width="4">{''.join(f'<rect x="78" y="{300+i*66}" width="110" height="56" rx="28"/>' for i in range(4))}</g></svg>'''

CHAT = '<svg viewBox="0 0 64 64"><path d="M32 6C17 6 6 16.5 6 29.5c0 6 2.4 11.4 6.4 15.5L9 58l13.8-5.2c2.9 1 6 1.5 9.2 1.5 15 0 26-10.5 26-23.5S47 6 32 6z" fill="currentColor"/><path d="M23 22c1 6 7 13 16 16l4-4" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/></svg>'
SPARK = f'<svg viewBox="0 0 100 100"><path d="M50 4l10 34 34 12-34 12-10 34-10-34L6 50l34-12z" fill="{O}"/></svg>'
HEART = f'<svg viewBox="0 0 64 64"><path d="M32 56S6 40 6 22a13 13 0 0 1 26-4 13 13 0 0 1 26 4c0 18-26 34-26 34z" fill="{O}"/></svg>'

SCREEN_HOME = """<div class="sb"><span>٤:٠٢</span><span>5G ▮▮▮</span></div>
<div class="hdr"><span class="hi">هلا 👋</span><b class="brandname">مطعمك</b><span class="hd-r">EN 🔔</span>
<div class="search">ابحث عن منتج <i>⌕</i></div></div>
<div class="tog"><span class="on">استلام</span><span>التوصيل</span></div>
<div class="branch"><small>الفرع المحدد</small><b>الرياض · فرعك</b><span class="bt">استلام</span></div>
<div class="map"><svg viewBox="0 0 400 190" preserveAspectRatio="none"><g stroke="#d9dde3" stroke-width="3"><path d="M0 40h400M0 95h400M0 150h400M60 0v190M150 0v190M250 0v190M340 0v190"/></g><path d="M0 170L400 20" stroke="#9fb1c7" stroke-width="9"/><circle cx="210" cy="95" r="18" fill="#EB573E"/><circle cx="210" cy="95" r="7" fill="#fff"/></svg></div>
<div class="banner"><div class="bt1">عروض</div><div class="bt2">حصرية</div><div class="cup"></div><div class="box"></div></div>
<div class="cats"><span class="on">الكل</span><span>المشروبات</span><span>الوجبات</span></div>"""
SCREEN_DONE = """<div class="sb"><span>٤:٠٣</span><span>5G ▮▮▮</span></div>
<div class="hdr short"><b class="brandname">مطعمك</b></div>
<div class="done"><div class="tick">✓</div><b>تم استلام طلبك</b><small>طلب رقم 1024 · قيد التجهيز</small>
<div class="steps"><i class="on"></i><i class="on"></i><i></i></div></div>"""

# framed speech labels: (id, start, end, html) at the measured phrase times
LABELS = [("L1", .19, 1.25, "عندك <em>مطعم؟</em>"), ("L2", 1.29, 2.4, "سؤال سريع:"),
          ("L3", 2.45, 4.95, "<em>عملائك</em>، فعلًا <em>عملائك؟</em>"),
          ("L4", 5.38, 8.0, "إذا طلباتك كلها تجيك<br>من تطبيق توصيل <em>غيرِك</em>،"),
          ("L5", 8.1, 10.35, "فإنت تدفع <em>عمولة</em><br>على كل طلب،"),
          ("L6", 10.44, 12.85, "والعميل يرجع للتطبيق،<br><em>مو لك.</em>"),
          ("L7", 13.08, 14.15, "مع <em>هوزن قو</em>،"),
          ("L8", 14.2, 17.8, "يصير لمطعمك تطبيق طلبات<br><em>باسمك وهويتك</em>،"),
          ("L9", 17.88, 19.5, "والطلب يوصلك <em>مباشرة.</em>"),
          ("L10", 19.61, 24.05, "وتكافئ عملائك بنقاط ولاء وكاشباك،<br>يخليهم <em>يرجعون لك إنت.</em>")]

labels = "".join(f'<div class="lbl" id="{i}"><span>{h}</span></div>' for i, a, b, h in LABELS)

act0 = f'''<section id="a0" class="clip act" data-start="0" data-duration="5.2" data-track-index="2">
<div class="store big" id="st0">{STORE}</div>
{''.join(f'<div class="qm" id="q{k}">؟</div>' for k in range(3))}</section>'''

act1 = f'''<section id="a1" class="clip act" data-start="5.2" data-duration="7.8" data-track-index="2">
<div class="store sm" id="st1">{STORE}</div>
<div class="gphone" id="gp"><div class="gscreen"></div><div class="fee" id="fee">عمولة</div></div><div class="gplabel" id="gpl">تطبيق غيرك</div>
<div class="crowd" id="crowd">{''.join(f'<div class="pp" id="pp{k}">{person(band=[K,D,K][k])}</div>' for k in range(3))}</div>
{''.join(f'<div class="rcpt" id="r{k}"><i></i><i></i><i></i></div>' for k in range(4))}
{''.join(f'<div class="coin" id="c{k}">%</div>' for k in range(4))}
<div class="stamp" id="stamp">مو لك</div></section>'''

act2 = f'''<section id="a2" class="clip act" data-start="13.0" data-duration="11.2" data-track-index="2">
<img class="hero-logo" id="hlogo" src="assets/hwzngo-logo.png" alt="HwznGo">
<div class="handphone" id="hp">{HAND_BACK}<div class="phone"><div class="screen" id="scA">{SCREEN_HOME}</div><div class="screen" id="scB">{SCREEN_DONE}</div>
<img class="screen" id="scC" src="assets/app-loyalty-points-light.jpg" alt="نقاط الولاء"><img class="screen" id="scD" src="assets/app-wallet-light.jpg" alt="المحفظة والكاشباك"></div>{HAND_FRONT}</div>
<div class="step" id="sp1"><b>1</b>باسمك</div><div class="step" id="sp2"><b>2</b>بهويتك</div><div class="step" id="sp3"><b>3</b>يوصلك مباشرة</div>
<div class="step" id="sp4"><b>★</b>نقاط ولاء</div><div class="step" id="sp5"><b>٪</b>كاشباك</div>
<div class="rcpt fly" id="rf"><i></i><i></i><i></i></div>
{''.join(f'<div class="heart" id="h{k}">{HEART}</div>' for k in range(4))}</section>'''

act3 = f'''<section id="a3" class="clip act" data-start="24.2" data-duration="5.8" data-track-index="2">
<div class="badge" id="badge"><div class="b1">خل عميلك</div><div class="b2" id="b2">عميلك</div><div class="tail"></div></div>
<div class="check" id="chk">✓</div>
{''.join(f'<div class="spark" id="sk{k}">{SPARK}</div>' for k in range(5))}
<div class="endcard" id="end"><img src="assets/hwzngo-logo.png" alt="HwznGo"><div class="tag">خل عميلك عميلك</div>
<div class="wa"><span class="wa-ico">{CHAT}</span><span class="wa-t">تواصل معنا واتساب</span></div><div class="num">920033443</div></div></section>'''

css = f'''@font-face{{font-family:Cairo;src:url(assets/Cairo.ttf);font-weight:200 1000}}
*{{box-sizing:border-box}}html,body{{margin:0;background:{C}}}
#reel{{position:relative;width:1080px;height:1920px;overflow:hidden;background:{C};font-family:Cairo,sans-serif;color:{K};direction:rtl}}
em{{font-style:normal;color:{O}}}
.floor{{position:absolute;left:0;right:0;bottom:0;height:330px;background:#F3E4D3}}
.lamp{{position:absolute;top:0;width:8px;height:120px;background:{K}}}.lamp:after{{content:'';position:absolute;top:118px;left:-46px;width:100px;height:50px;border-radius:50px 50px 8px 8px;background:{O}}}
.logo-top{{position:absolute;top:110px;left:0;right:0;text-align:center;z-index:6;opacity:0}}.logo-top img{{height:52px}}
.lbl{{position:absolute;top:250px;left:70px;right:70px;text-align:center;z-index:5;opacity:0}}
.lbl>span{{display:inline-block;background:#fff;border:5px solid {O};border-radius:44px;padding:16px 46px 20px;font-weight:800;font-size:62px;line-height:1.45;box-shadow:0 10px 0 {O}26;position:relative}}
.lbl>span:before,.lbl>span:after{{content:'';position:absolute;top:50%;width:16px;height:16px;margin-top:-8px;border-radius:50%;background:{O}}}.lbl>span:before{{right:-34px}}.lbl>span:after{{left:-34px}}
.act{{position:absolute;inset:0;visibility:hidden;z-index:2}}
.store{{position:absolute}}.store svg{{width:100%;height:100%}}.store.big{{top:640px;left:150px;width:780px;height:728px}}
.store.sm{{top:860px;left:640px;width:420px;height:392px}}
.qm{{position:absolute;width:150px;height:150px;border-radius:50%;background:{O};color:#fff;font:900 110px/150px Cairo;text-align:center;opacity:0}}
#q0{{top:560px;left:120px}}#q1{{top:500px;left:780px}}#q2{{top:470px;left:450px;background:{K}}}
.gphone{{position:absolute;top:800px;left:400px;width:280px;height:540px;border-radius:46px;border:13px solid #A3A3A8;background:#ECE4DA}}
.gphone .gscreen{{position:absolute;inset:36px 22px;border-radius:18px;background:repeating-linear-gradient(#DCD2C5 0 16px,transparent 16px 40px)}}
.gplabel{{position:absolute;top:1356px;left:340px;width:400px;text-align:center;font-size:46px;font-weight:800;color:#6E6E74}}
.fee{{position:absolute;top:-70px;left:50%;margin-left:-110px;width:220px;background:{O};color:#fff;font-size:44px;font-weight:900;text-align:center;border-radius:30px;padding:4px 0;opacity:0}}
.crowd{{position:absolute;top:900px;left:10px;width:380px;height:460px}}.pp{{position:absolute;width:170px;height:325px}}.pp svg{{width:100%;height:100%}}
#pp0{{left:0;top:40px}}#pp1{{left:120px;top:0}}#pp2{{left:200px;top:90px}}
.rcpt{{position:absolute;top:1000px;left:180px;width:110px;height:130px;background:#fff;border-radius:12px;box-shadow:0 10px 24px {K}2a;padding:20px 16px;opacity:0}}
.rcpt i{{display:block;height:10px;border-radius:5px;background:{O}55;margin-bottom:16px}}.rcpt i:first-child{{background:{O};width:70%}}
.coin{{position:absolute;top:900px;left:800px;width:110px;height:110px;border-radius:50%;background:{O};color:#fff;font:900 56px/110px Cairo;text-align:center;box-shadow:inset 0 -9px 0 {D};opacity:0;direction:ltr}}
.stamp{{position:absolute;top:1470px;left:50%;width:560px;margin-left:-280px;border:12px solid {D};color:{D};border-radius:30px;font-size:120px;font-weight:900;text-align:center;line-height:1.3;opacity:0;background:#fff}}
.hero-logo{{position:absolute;top:820px;left:50%;width:820px;margin-left:-410px;opacity:0}}
.handphone{{position:absolute;top:640px;left:50%;width:560px;height:1280px;margin-left:-280px;opacity:0}}
.hand-b,.hand-f{{position:absolute;left:0;top:330px;width:560px;height:760px}}.hand-f{{z-index:3}}
.phone{{position:absolute;top:0;left:120px;width:340px;height:720px;border-radius:52px;background:{K};padding:12px;z-index:2;box-shadow:0 30px 60px {K}33}}
.screen{{position:absolute;inset:12px;border-radius:40px;overflow:hidden;background:#fff;opacity:0;object-fit:cover;object-position:top;width:calc(100% - 24px);height:calc(100% - 24px)}}#scA{{opacity:1}}
.step{{position:absolute;right:40px;height:92px;padding:0 30px 0 26px;border-radius:46px;background:#fff;border:4px solid {O};font-size:46px;font-weight:800;display:flex;align-items:center;gap:16px;opacity:0;white-space:nowrap}}
.step b{{width:62px;height:62px;border-radius:50%;background:{O};color:#fff;font:900 38px/62px Cairo;text-align:center}}
#sp1{{top:700px}}#sp2{{top:820px}}#sp3{{top:940px}}#sp4{{top:700px}}#sp5{{top:820px}}
.rcpt.fly{{top:760px;left:80px;width:120px;height:140px}}
.heart{{position:absolute;top:880px;width:96px;height:96px;opacity:0}}.heart svg{{width:100%;height:100%}}#h0{{left:150px}}#h1{{left:300px}}#h2{{left:700px}}#h3{{left:840px}}
.badge{{position:absolute;top:560px;left:50%;width:820px;height:820px;margin-left:-410px;border-radius:50%;background:{O};color:#fff;text-align:center;display:flex;flex-direction:column;justify-content:center;opacity:0;box-shadow:0 30px 0 {D}}}
.badge .b1{{font-size:120px;font-weight:900;line-height:1.2}}.badge .b2{{font-size:190px;font-weight:900;line-height:1.15;color:{K};background:#fff;border-radius:40px;margin:16px 110px 0;padding:0 0 14px}}
.tail{{position:absolute;bottom:-70px;left:170px;width:0;height:0;border-left:60px solid transparent;border-right:60px solid transparent;border-top:110px solid {O};transform:rotate(25deg)}}
.check{{position:absolute;top:1220px;left:150px;width:190px;height:190px;border-radius:50%;background:{K};color:#fff;font:900 120px/190px Cairo;text-align:center;opacity:0;border:10px solid {C}}}
.spark{{position:absolute;width:90px;height:90px;opacity:0}}.spark svg{{width:100%;height:100%}}
#sk0{{top:520px;left:120px}}#sk1{{top:470px;left:880px;width:120px;height:120px}}#sk2{{top:1300px;left:880px}}#sk3{{top:960px;left:40px;width:60px;height:60px}}#sk4{{top:1440px;left:420px;width:60px;height:60px}}
.endcard{{position:absolute;inset:0;background:{C};display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0}}
.endcard img{{width:740px}}.endcard .tag{{margin-top:40px;font-size:70px;font-weight:900;color:{O}}}
.endcard .wa{{margin-top:70px;display:flex;align-items:center;gap:20px;background:#fff;border:5px solid {O};border-radius:60px;padding:14px 44px;font-size:54px;font-weight:800}}
.wa-ico{{width:70px;height:70px;color:#25D366;display:inline-block}}.wa-ico svg{{width:70px;height:70px}}
.endcard .num{{margin-top:30px;font-size:140px;font-weight:900;color:{K};letter-spacing:6px;direction:ltr}}
.sb{{display:flex;justify-content:space-between;padding:12px 30px 0;background:{D};color:#fff;font-size:15px;font-weight:700;direction:ltr}}
.hdr{{background:{D};color:#fff;padding:4px 18px 18px;border-radius:0 0 24px 24px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center}}.hdr.short{{display:block;text-align:center}}
.hdr .hi{{font-size:16px;font-weight:700}}.hdr .hd-r{{font-size:14px;text-align:left;direction:ltr}}.brandname{{font-size:32px;font-weight:900;text-align:center;line-height:1.5}}
.search{{grid-column:1/4;margin-top:10px;background:#fff;color:#62656b;border-radius:28px;padding:7px 16px;font-size:15px;display:flex;justify-content:space-between}}.search i{{font-style:normal;color:{D}}}
.tog{{margin:14px 14px 0;background:#f1f2f4;border-radius:28px;display:flex;padding:5px}}.tog span{{flex:1;text-align:center;font-size:17px;font-weight:700;color:#5c5f65;padding:5px}}.tog .on{{background:#fff;color:{D};border-radius:22px}}
.branch{{margin:12px 14px 0;border:2px solid #eceef1;border-radius:18px;padding:8px 14px;display:grid;grid-template-columns:1fr auto}}.branch small{{font-size:13px;color:#62656b}}.branch b{{grid-row:2;font-size:18px}}.branch .bt{{grid-row:1/3;grid-column:2;align-self:center;background:#FDE9E5;color:{D};font-size:14px;font-weight:800;padding:3px 10px;border-radius:10px}}
.map{{margin:10px 14px 0;height:110px;border-radius:18px;overflow:hidden;background:#f6f7f9}}.map svg{{width:100%;height:100%}}
.banner{{position:relative;margin:10px 14px 0;height:120px;border-radius:20px;background:{D};overflow:hidden}}.bt1,.bt2{{position:absolute;right:20px;font-weight:900;line-height:1.3}}.bt1{{top:4px;font-size:30px;color:#FFE3A0}}.bt2{{top:52px;font-size:36px;color:#fff;line-height:1.5}}
.cup{{position:absolute;left:26px;top:40px;width:48px;height:64px;background:#fff;border-radius:6px 6px 16px 16px}}.box{{position:absolute;left:84px;top:60px;width:64px;height:44px;background:#FFD36B;border-radius:8px}}
.cats{{display:flex;gap:8px;margin:12px 14px 0;overflow:hidden}}.cats span{{white-space:nowrap;font-size:15px;font-weight:700;border:2px solid #eceef1;border-radius:20px;padding:5px 12px}}.cats .on{{background:{D};border-color:{D};color:#fff}}
.done{{text-align:center;padding-top:110px}}.done .tick{{width:150px;height:150px;margin:0 auto 28px;border-radius:50%;background:#25B862;color:#fff;font:900 96px/150px Cairo}}
.done b{{display:block;font-size:34px;font-weight:900}}.done small{{display:block;margin-top:8px;font-size:18px;color:#6d7076}}
.done .steps{{display:flex;gap:10px;justify-content:center;margin-top:40px}}.done .steps i{{width:60px;height:10px;border-radius:5px;background:#e3e5e8}}.done .steps i.on{{background:{O}}}
.wipe{{position:absolute;top:960px;left:540px;width:2400px;height:2400px;margin:-1200px 0 0 -1200px;border-radius:50%;background:{O};z-index:7;transform:scale(0)}}
'''

# animation (seconds); SFX events are listed next to the motion they belong to
SFX = []
def sfx(kind, t, gain=1.0):
    SFX.append((kind, round(t, 3), gain))

js = ['''const tl=gsap.timeline({paused:true});
const show=(s,t)=>tl.set(s,{visibility:'visible'},t), hide=(s,t)=>tl.set(s,{visibility:'hidden'},t);
const pop=(s,t,d=.4,f=.5)=>tl.fromTo(s,{scale:f,opacity:0},{scale:1,opacity:1,duration:d,ease:'back.out(2)'},t);
const out=(s,t,d=.18)=>tl.to(s,{scale:.9,opacity:0,duration:d,ease:'power2.in'},t);''']
for i, a, b, h in LABELS:
    js.append(f"pop('#{i}',{a},.35,.7);out('#{i}',{b});")
    sfx("pop", a, .7)
js.append('''// act 0: the restaurant, then the question
show('#a0',0);hide('#a0',5.2);
tl.fromTo('#st0',{y:500,scale:.8,opacity:0},{y:0,scale:1,opacity:1,duration:.7,ease:'back.out(1.4)'},0);
tl.to('#st0',{scale:1.02,y:-6,duration:.5,yoyo:true,repeat:3,ease:'sine.inOut'},.8);
['#q0','#q1','#q2'].forEach((q,k)=>{pop(q,2.7+k*.4,.4,.2);tl.to(q,{rotation:k%2?14:-14,duration:.3,yoyo:true,repeat:3,ease:'sine.inOut'},3.1+k*.4);});
tl.to('#a0',{opacity:0,duration:.25},4.95);''')
sfx("whoosh", 0.0); [sfx("pop", 2.7 + k * .4, .9) for k in range(3)]
js.append('''// act 1: orders go through someone else's app; commission; the customer stays with the app
show('#a1',5.2);
tl.fromTo('#st1',{x:400,opacity:0},{x:0,opacity:1,duration:.5,ease:'power3.out'},5.25);
pop('#gp',5.35,.45,.6);pop('#gpl',5.5,.35,.6);
['#pp0','#pp1','#pp2'].forEach((p,k)=>tl.fromTo(p,{y:420,opacity:0},{y:0,opacity:1,duration:.45,ease:'back.out(1.6)'},5.45+k*.12));
[0,1,2,3].forEach(k=>{const t=5.9+k*.5;
  tl.fromTo('#r'+k,{x:0,y:0,opacity:0,rotation:-15},{x:360,y:-120,opacity:1,rotation:0,duration:.3,ease:'power2.out'},t);
  tl.to('#r'+k,{x:690,y:20,duration:.3,ease:'power2.in'},t+.3);tl.to('#r'+k,{opacity:0,scale:.5,duration:.12},t+.6);});
pop('#fee',8.15,.4,.4);
[0,1,2,3].forEach(k=>{const t=8.5+k*.42;
  tl.fromTo('#c'+k,{x:0,y:0,opacity:0,scale:.6},{x:-170,y:-160,opacity:1,scale:1,duration:.22,ease:'power2.out'},t);
  tl.to('#c'+k,{x:-300,y:-40,scale:.5,duration:.2,ease:'power2.in'},t+.22);tl.to('#c'+k,{opacity:0,duration:.08},t+.42);});
tl.to('#fee',{scale:1.15,duration:.12,yoyo:true,repeat:5,ease:'sine.inOut'},8.6);
tl.to(['#pp0','#pp2'],{opacity:0,duration:.25},10.4);
tl.to('#pp1',{x:250,y:-30,duration:1.1,ease:'power1.inOut'},10.6);
tl.to('#pp1',{y:-50,duration:.18,yoyo:true,repeat:5,ease:'sine.inOut'},10.6);
tl.to('#st1',{opacity:.3,duration:.4},11.3);
tl.to('#gpl',{opacity:0,duration:.15},12.0);tl.fromTo('#stamp',{scale:2.2,rotation:-18,opacity:0},{scale:1,rotation:-8,opacity:1,duration:.25,ease:'power3.in'},12.17);
tl.to('#a1',{opacity:0,duration:.2},12.85);hide('#a1',13.0);
// wipe into the solution
tl.fromTo('#wipe',{scale:0},{scale:1,duration:.32,ease:'power2.in'},12.72);
tl.to('#wipe',{opacity:0,duration:.3,ease:'power1.out'},13.04);''')
sfx("whoosh", 5.25, .8); [sfx("swish", 5.9 + k * .5, .55) for k in range(4)]; sfx("ding", 8.15, .5)
[sfx("coin", 8.5 + k * .42, .6) for k in range(4)]; sfx("thud", 12.17, 1.0); sfx("whoosh", 12.72, 1.0)
js.append('''// act 2: HwznGo, an app in your own name, steps, loyalty
show('#a2',13.0);hide('#a2',24.2);
tl.fromTo('#hlogo',{scale:.4,opacity:0},{scale:1,opacity:1,duration:.5,ease:'back.out(1.8)'},13.08);
tl.to('#hlogo',{y:-200,scale:.5,opacity:0,duration:.35,ease:'power2.in'},13.85);
tl.fromTo('#hp',{y:900,opacity:0},{y:0,opacity:1,duration:.7,ease:'power3.out'},14.0);
tl.to('#hp',{y:-14,duration:1.2,yoyo:true,repeat:7,ease:'sine.inOut'},14.8);
pop('#sp1',15.6,.4,.5);pop('#sp2',16.4,.4,.5);pop('#sp3',17.95,.4,.5);
tl.fromTo('#rf',{x:-60,y:-300,rotation:-20,opacity:0},{x:330,y:200,rotation:0,opacity:1,duration:.4,ease:'power2.in'},17.95);
tl.to('#rf',{opacity:0,scale:.4,duration:.1},18.35);
tl.to('#scB',{opacity:1,duration:.2},18.35);tl.set('#scA',{opacity:0},18.56);
tl.to(['#sp1','#sp2','#sp3'],{opacity:0,x:60,duration:.2,stagger:.05},19.45);
tl.to('#scC',{opacity:1,duration:.25},19.7);tl.set('#scB',{opacity:0},19.96);pop('#sp4',20.0,.4,.5);
tl.to('#scD',{opacity:1,duration:.25},20.9);tl.set('#scC',{opacity:0},21.16);pop('#sp5',21.0,.4,.5);
[0,1,2,3].forEach(k=>{tl.fromTo('#h'+k,{y:120,opacity:0,scale:.4},{y:-260,opacity:1,scale:1,duration:1.1,ease:'power1.out'},21.95+k*.2);tl.to('#h'+k,{opacity:0,duration:.3},22.85+k*.2);});
tl.to('#a2',{opacity:0,duration:.2},24.0);''')
sfx("whoosh", 13.0, .9); sfx("ding", 13.1, .8); sfx("whoosh", 14.0, .8)
[sfx("pop", t, .8) for t in (15.6, 16.4, 17.95)]; sfx("swish", 17.95, .6); sfx("ding", 18.35, .9)
sfx("click", 19.7, .8); sfx("pop", 20.0, .8); sfx("click", 20.9, .8); sfx("pop", 21.0, .8)
[sfx("pop", 21.95 + k * .2, .45) for k in range(4)]
js.append('''// act 3: the line as a badge, then the end card
show('#a3',24.2);
tl.fromTo('#badge',{scale:.2,opacity:0,rotation:-12},{scale:1,opacity:1,rotation:0,duration:.55,ease:'back.out(1.7)'},24.3);
tl.fromTo('#b2',{scale:.3,opacity:0},{scale:1,opacity:1,duration:.4,ease:'back.out(2.4)'},25.3);
pop('#chk',25.75,.4,.2);
['#sk0','#sk1','#sk2','#sk3','#sk4'].forEach((s,k)=>{tl.fromTo(s,{scale:0,opacity:0,rotation:-60},{scale:1,opacity:1,rotation:0,duration:.35,ease:'back.out(2)'},25.85+k*.08);tl.to(s,{scale:.7,duration:.4,yoyo:true,repeat:2,ease:'sine.inOut'},26.3+k*.08);});
tl.to('#badge',{scale:1.03,duration:.35,yoyo:true,repeat:3,ease:'sine.inOut'},26.2);
tl.to('#end',{opacity:1,duration:.35,ease:'power1.inOut'},27.8);tl.set(['#badge','#chk','#sk0','#sk1','#sk2','#sk3','#sk4'],{opacity:0},28.16);
tl.fromTo('#end img',{scale:.8},{scale:1,duration:.5,ease:'back.out(1.6)'},27.8);
tl.fromTo('#end .tag',{y:40,opacity:0},{y:0,opacity:1,duration:.35,ease:'power3.out'},28.0);
tl.fromTo('#end .wa',{y:40,opacity:0},{y:0,opacity:1,duration:.35,ease:'back.out(1.6)'},28.2);
tl.fromTo('#end .num',{scale:.7,opacity:0},{scale:1,opacity:1,duration:.4,ease:'back.out(1.8)'},28.4);
tl.set({},{},REEL.duration);
window.__timelines=window.__timelines||{};window.__timelines.reel=tl;''')
sfx("whoosh", 24.2, .9); sfx("pop", 24.3, 1.0); sfx("pop", 25.3, 1.0); sfx("ding", 25.75, 1.0); sfx("sparkle", 25.85, .7)
sfx("whoosh", 27.8, .7); sfx("pop", 28.2, .8); sfx("ding", 28.4, .9)

OUT.mkdir(exist_ok=True)
(OUT / "assets").mkdir(exist_ok=True)
for f in ("gsap.min.js", "GSAP-LICENSE.txt", "Cairo.ttf", "CAIRO-OFL.txt", "hwzngo-logo.png", "app-loyalty-points-light.jpg", "app-wallet-light.jpg"):
    if (SRC / f).exists() and (SRC / f).resolve() != (OUT / "assets" / f).resolve():
        shutil.copy2(SRC / f, OUT / "assets" / f)
lamps = "".join(f'<div class="lamp" style="left:{x}px"></div>' for x in (190, 540, 890))
doc = f'''<!doctype html><html lang="ar"><head><meta charset="utf-8"><title>hwzngo-direct-channel · flat</title><script src="assets/gsap.min.js"></script><style>{css}</style></head>
<body><main id="reel" data-composition-id="reel" data-start="0" data-width="1080" data-height="1920" data-duration="{TOTAL}" data-fps="30">
<div class="floor"></div>{lamps}
{act0}{act1}{act2}{act3}{labels}<div class="wipe" id="wipe"></div>
</main><script>const REEL={{"duration":{TOTAL}}};
{chr(10).join(js)}</script></body></html>'''
(OUT / "index.html").write_text(doc, encoding="utf-8")
(OUT / "hyperframes.json").write_text(json.dumps({"name": "hwzngo-direct-channel-flat"}))

# ---- original sound effects, synthesized here ----
SR = 48000
rng = np.random.default_rng(7)  # fixed seed: the same file every build
def env(n, a, r):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)
def tone(f0, f1, dur, a=.002, r=.05):
    n = int(dur * SR); t = np.arange(n) / SR
    f = np.linspace(f0, f1, n); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(n, a, r)
def noise_band(dur, lo, hi, a, r):
    n = int(dur * SR); x = rng.standard_normal(n)
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(n, 1 / SR); X[(fr < lo) | (fr > hi)] = 0
    y = np.fft.irfft(X, n); y /= np.abs(y).max() + 1e-9
    return y * env(n, a, r)
def whoosh():
    n = int(.42 * SR); x = rng.standard_normal(n); out = np.zeros(n); lp = 0.0
    cut = np.concatenate([np.linspace(.02, .35, n // 2), np.linspace(.35, .03, n - n // 2)])
    for i in range(n):
        lp += cut[i] * (x[i] - lp); out[i] = lp
    w = np.sin(np.linspace(0, np.pi, n)) ** 2
    return out / (np.abs(out).max() + 1e-9) * w * .7
LIB = {"pop": lambda: tone(520, 980, .09, .001, .035) * .9,
       "click": lambda: noise_band(.03, 2000, 9000, .0005, .006) * .6 + tone(1800, 1800, .03, .0005, .01)[:int(.03 * SR)] * .4,
       "ding": lambda: (tone(1318, 1318, .7, .002, .22) + .5 * tone(1976, 1976, .7, .002, .15) + .25 * tone(2637, 2637, .7, .002, .1)) * .45,
       "coin": lambda: np.concatenate([tone(1500, 1500, .07, .001, .03), tone(2000, 2000, .18, .001, .06)]) * .45,
       "swish": lambda: noise_band(.2, 1500, 7000, .02, .05) * .35,
       "thud": lambda: tone(140, 60, .25, .001, .09) + np.pad(noise_band(.06, 200, 1500, .001, .02) * .3, (0, int(.25 * SR) - int(.06 * SR))),
       "sparkle": lambda: sum(np.pad(tone(f, f, .25, .001, .07), (int(k * .045 * SR), int(.5 * SR)))[:int(.5 * SR)] * .25 for k, f in enumerate((2093, 2637, 3136, 4186))),
       "whoosh": whoosh}
mix = np.zeros(int(TOTAL * SR) + SR)
for kind, t, g in SFX:
    s = LIB[kind](); i = int(t * SR); mix[i:i + len(s)] += s * g
mix = mix[:int(TOTAL * SR)]
mix = mix / max(1e-9, np.abs(mix).max()) * .5
pcm = (np.clip(mix, -1, 1) * 32767).astype("<i2")
with wave.open(str(OUT / "sfx.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
(OUT / "sfx-events.json").write_text(json.dumps(SFX))
print("written", OUT / "index.html", len(SFX), "sfx events")
