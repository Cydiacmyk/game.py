"""枪战小游戏 - 局域网版 (合并为单个 .py 文件)
运行:
    pip install flask
    python game.py
本机:  http://127.0.0.1
家人:  http://192.168.1.13   (需连同一 WiFi/路由器)
"""
import socket
from flask import Flask

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>枪战游戏</title>
<style>*{margin:0;padding:0}body{background:#000;overflow:hidden}canvas{display:block}</style>
</head><body><canvas id="c"></canvas><script>
var c=document.getElementById("c"),ctx=c.getContext("2d");
c.width=innerWidth;c.height=innerHeight;
var p={x:c.width/2,y:c.height-50,w:40,h:30},b=[],e=[],eb=[],score=0,over=false,keys={},wave=0,st=0;
addEventListener("keydown",function(v){keys[v.key]=1});
addEventListener("keyup",function(v){keys[v.key]=0});
function hit(a,x){return a.x<x.x+x.w&&a.x+a.w>x.x&&a.y<x.y+x.h&&a.y+a.h>x.y}
function spawn(){wave++;var cols=4+wave,rows=2+Math.floor(wave/3),gap=60,sx=(c.width-cols*gap)/2;
  for(var r=0;r<rows;r++)for(var cc=0;cc<cols;cc++)e.push({x:sx+cc*gap,y:40+r*50,w:36,h:28,vx:1.2+wave*0.15})}
function loop(){if(over){ctx.fillStyle="#111";ctx.fillRect(0,0,c.width,c.height);ctx.fillStyle="#fff";
  ctx.font="40px Arial";ctx.fillText("Game Over",c.width/2-110,c.height/2);
  ctx.font="24px Arial";ctx.fillText("Score: "+score,c.width/2-60,c.height/2+40);
  ctx.fillText("Press F5 to Restart",c.width/2-110,c.height/2+80);return}requestAnimationFrame(loop);U();D()}
function U(){
  if(keys["ArrowLeft"]||keys["a"])p.x-=6;if(keys["ArrowRight"]||keys["d"])p.x+=6;
  if(p.x<0)p.x=0;if(p.x>c.width-p.w)p.x=c.width-p.w;
  if(keys[" "]){b.push({x:p.x+p.w/2-2,y:p.y,w:4,h:12});keys[" "]=0}
  for(var i=b.length-1;i>=0;i--){b[i].y-=9;if(b[i].y<0)b.splice(i,1)}
  st--;if(e.length===0&&st<=0){spawn();st=30}
  var edge=false;for(var j=0;j<e.length;j++){e[j].x+=e[j].vx;if(e[j].x<0||e[j].x>c.width-e[j].w)edge=true}
  if(edge)for(var k=0;k<e.length;k++){e[k].vx*=-1;e[k].y+=20}
  if(e.length>0&&Math.random()<0.03+wave*0.005){var sh=e[Math.floor(Math.random()*e.length)];
    eb.push({x:sh.x+sh.w/2-2,y:sh.y+sh.h,w:4,h:10,vy:5})}
  for(var m=eb.length-1;m>=0;m--){eb[m].y+=eb[m].vy;if(eb[m].y>c.height)eb.splice(m,1)}
  for(var i=b.length-1;i>=0;i--)for(var j=e.length-1;j>=0;j--)if(hit(b[i],e[j])){b.splice(i,1);e.splice(j,1);score+=10;break}
  for(var k=eb.length-1;k>=0;k--)if(hit(eb[k],p)){eb.splice(k,1);over=true}
  for(var f=0;f<e.length;f++)if(e[f].y+e[f].h>c.height-30)over=true;
}
function D(){
  ctx.fillStyle="#111";ctx.fillRect(0,0,c.width,c.height);
  ctx.fillStyle="#0f0";ctx.fillRect(p.x,p.y,p.w,p.h);
  ctx.fillStyle="#ff0";for(var i=0;i<b.length;i++)ctx.fillRect(b[i].x,b[i].y,b[i].w,b[i].h);
  ctx.fillStyle="#f44";for(var j=0;j<e.length;j++)ctx.fillRect(e[j].x,e[j].y,e[j].w,e[j].h);
  ctx.fillStyle="#fa0";for(var k=0;k<eb.length;k++)ctx.fillRect(eb[k].x,eb[k].y,eb[k].w,eb[k].h);
  ctx.fillStyle="#fff";ctx.font="18px Arial";ctx.fillText("Score: "+score,10,25);ctx.fillText("Wave: "+wave,10,48);
}
loop();
</script></body></html>"""


@app.route("/")
def index():
    return HTML


def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.168.1.1", 80)); ip = s.getsockname()[0]
    except Exception:
        ip = None
    finally:
        s.close()
    if ip and ip.startswith("192.168."): return ip
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None):
            if info[4][0].startswith("192.168."): return info[4][0]
    except Exception: pass
    return "192.168.1.13"


if __name__ == "__main__":
    ip = get_lan_ip()
    print("=" * 40)
    print("  枪战游戏 - 局域网服务器")
    print("=" * 40)
    print(f"  本机:  http://127.0.0.1")
    print(f"  家人:  http://{ip}")
    print("=" * 40)
    print("  家人需连同一 WiFi; 打不开请放行防火墙 TCP 80")
    print("=" * 40)
    app.run(host="0.0.0.0", port=80, debug=True)
