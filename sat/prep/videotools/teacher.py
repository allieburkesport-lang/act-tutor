# Original cartoon teacher: round glasses, hair in a bun, teal top, yellow chalk. Drawn with PIL.
from PIL import Image, ImageDraw
SKIN=(241,200,165);HAIR=(92,58,38);TEAL=(22,150,150);DARK=(40,30,30)
def teacher(mouth=0.0, blink=False, arm=0.0, bob=0):
    W,H=300,360;im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    oy=bob
    # body
    d.rounded_rectangle((60,230+oy,240,380+oy),60,fill=TEAL)
    d.polygon([(130,232+oy),(150,262+oy),(170,232+oy)],fill=(250,250,245))
    # neck
    d.rectangle((135,200+oy,165,236+oy),fill=SKIN)
    # bun + hair
    d.ellipse((115,20+oy,185,80+oy),fill=HAIR)
    d.ellipse((85,55+oy,215,215+oy),fill=HAIR)
    # face
    d.ellipse((95,75+oy,205,215+oy),fill=SKIN)
    d.pieslice((92,62+oy,208,150+oy),180,360,fill=HAIR)
    # ears
    d.ellipse((86,132+oy,102,160+oy),fill=SKIN);d.ellipse((198,132+oy,214,160+oy),fill=SKIN)
    # eyes
    for cx in (127,173):
        if blink: d.line((cx-9,140+oy,cx+9,140+oy),fill=DARK,width=3)
        else: d.ellipse((cx-6,133+oy,cx+6,147+oy),fill=DARK);d.ellipse((cx-2,135+oy,cx+1,139+oy),fill=(255,255,255))
        d.ellipse((cx-19,121+oy,cx+19,159+oy),outline=(60,40,40),width=4)
    d.line((146,140+oy,154,140+oy),fill=(60,40,40),width=4)
    # brows
    d.arc((110,110+oy,142,130+oy),200,340,fill=HAIR,width=4);d.arc((158,110+oy,190,130+oy),200,340,fill=HAIR,width=4)
    # cheeks
    d.ellipse((107,163+oy,125,175+oy),fill=(240,170,150));d.ellipse((175,163+oy,193,175+oy),fill=(240,170,150))
    # mouth
    mh=int(3+mouth*16)
    if mouth<0.08: d.arc((133,170+oy,167,192+oy),20,160,fill=(150,50,60),width=4)
    else:
        d.ellipse((136,178+oy-mh//3,164,180+oy+mh),fill=(130,40,50));d.ellipse((142,180+oy+mh-6,158,180+oy+mh),fill=(220,110,120))
    # arms
    if arm>0.05:
        ang=arm
        hx,hy=int(78-40*ang),int(250-140*ang)+oy
        d.line((90,260+oy,hx,hy),fill=TEAL,width=30)
        d.ellipse((hx-15,hy-15,hx+15,hy+15),fill=SKIN)
        d.line((hx-6,hy-6,hx-22,hy-26),fill=(255,230,90),width=8)
    else:
        d.line((85,262+oy,70,350+oy),fill=TEAL,width=30)
    d.line((215,262+oy,232,350+oy),fill=TEAL,width=30)
    return im
if __name__=='__main__':
    teacher(0.6,False,1).save('/tmp/teach.png')
