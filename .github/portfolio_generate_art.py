from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W,H=1600,1000
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F90=ImageFont.truetype(BOLD,90); F54=ImageFont.truetype(BOLD,54); F38=ImageFont.truetype(BOLD,38); F27=ImageFont.truetype(REG,27)

def rr(d,box,r,fill,outline=None,width=1):
    d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)

def save(im,slug):
    im.save(f'cover-{slug}.webp','WEBP',quality=84,method=6)
    im.resize((880,550),Image.Resampling.LANCZOS).save(f'thumb-{slug}.webp','WEBP',quality=82,method=6)

# RAFIQI WEB / PWA
im=Image.new('RGB',(W,H),(247,244,235)); d=ImageDraw.Draw(im)
for x in range(-100,W+100,90):
    for y in range(-100,H+100,90):
        d.rectangle((x-20,y-20,x+20,y+20),outline=(216,225,210),width=2)
        d.line((x-28,y,x,y-28,x+28,y,x,y+28,x-28,y),fill=(225,231,220),width=2)
rr(d,(95,90,1505,910),48,(252,250,244),(209,219,207),3)
d.rounded_rectangle((95,90,1505,205),radius=48,fill=(20,91,69)); d.rectangle((95,155,1505,205),fill=(20,91,69))
d.ellipse((180,355,460,635),fill=(229,238,227)); d.ellipse((232,407,408,583),fill=(20,91,69)); d.ellipse((280,390,428,565),fill=(229,238,227))
d.polygon(((230,650),(315,620),(315,720),(230,744)),fill=(20,91,69)); d.polygon(((315,620),(400,650),(400,744),(315,720)),fill=(27,119,89))
d.text((1450,300),'RAFIQI',font=F90,fill=(20,91,69),anchor='ra'); d.text((1450,420),'QURAN · DHIKR · SALAH',font=F38,fill=(55,68,60),anchor='ra'); d.text((1450,500),'WEB / PWA',font=F54,fill=(142,113,54),anchor='ra')
for i,t in enumerate(['QURAN','RECITATION','ADHKAR','PRAYER','QIBLA','KHATMA']):
    x=680+(i%3)*250; y=620+(i//3)*90; rr(d,(x,y,x+220,y+62),20,(238,242,235),(205,217,203),2); d.text((x+110,y+31),t,font=F27,fill=(35,77,61),anchor='mm')
d.text((1450,145),'rafiqi.iegy.net',font=F38,fill=(246,241,226),anchor='rm'); save(im,'rafiqi-web')

# RAFIQI ANDROID
im=Image.new('RGB',(W,H),(12,55,45)); d=ImageDraw.Draw(im)
for x in range(0,W,80): d.line((x,0,x,H),fill=(20,75,61),width=1)
for y in range(0,H,80): d.line((0,y,W,y),fill=(20,75,61),width=1)
rr(d,(150,90,650,910),70,(9,30,26),(193,163,91),5); rr(d,(185,145,615,840),48,(247,244,235))
rr(d,(220,185,580,285),26,(20,91,69)); d.text((400,235),'RAFIQI',font=F38,fill=(250,246,235),anchor='mm')
for txt,yy in [('QURAN',335),('ADHKAR',455),('PRAYER',575),('WIRD',695)]:
    rr(d,(230,yy,570,yy+88),24,(236,240,232),(211,219,207),2); d.ellipse((250,yy+25,288,yy+63),fill=(193,163,91)); d.text((320,yy+44),txt,font=F27,fill=(20,91,69),anchor='lm')
d.text((1460,250),'RAFIQI',font=F90,fill=(245,237,215),anchor='ra'); d.text((1460,375),'ANDROID APP',font=F54,fill=(197,216,205),anchor='ra'); d.text((1460,470),'v1.2.0 · FREE DOWNLOAD',font=F38,fill=(222,187,105),anchor='ra')
for i,t in enumerate(['Quran & recitation','Tafsir & adhkar','Prayer, qibla & wird','No accounts · No ads']):
    y=585+i*76; d.ellipse((780,y-10,800,y+10),fill=(222,187,105)); d.text((1460,y),t,font=F27,fill=(229,237,231),anchor='ra')
save(im,'rafiqi-android')

# ADWYA EGYPT
im=Image.new('RGB',(W,H),(245,250,249)); d=ImageDraw.Draw(im)
for x in range(0,W,48): d.line((x,0,x,H),fill=(225,239,236),width=1)
for y in range(0,H,48): d.line((0,y,W,y),fill=(225,239,236),width=1)
rr(d,(90,85,1510,915),48,(252,254,253),(183,220,213),3); d.rounded_rectangle((90,85,245,915),radius=48,fill=(11,116,109)); d.rectangle((170,85,245,915),fill=(11,116,109))
d.ellipse((275,340,585,650),fill=(230,245,242)); cap=Image.new('RGBA',(380,220),(0,0,0,0)); c=ImageDraw.Draw(cap); c.rounded_rectangle((25,50,355,170),radius=60,fill=(11,116,109)); c.rectangle((190,50,355,170),fill=(214,239,233)); c.line((190,55,190,165),fill=(245,250,249),width=6); cap=cap.rotate(-28,resample=Image.Resampling.BICUBIC,expand=True); im.paste(cap,(430-cap.width//2,500-cap.height//2),cap); d=ImageDraw.Draw(im)
d.text((1450,300),'ADWYA EGYPT',font=F90,fill=(11,105,99),anchor='ra'); d.text((1450,430),'SMART EGYPTIAN DRUG SEARCH',font=F38,fill=(55,91,87),anchor='ra'); d.text((1450,520),'25K+ MEDICINES',font=F54,fill=(30,71,68),anchor='ra')
for i,(v,l) in enumerate([('AR / EN','SMART SEARCH'),('PWA','INSTALLABLE'),('SEO','STATIC PAGES')]):
    x=730+i*245; rr(d,(x,650,x+215,785),24,(238,247,245),(197,226,221),2); d.text((x+108,695),v,font=F38,fill=(11,116,109),anchor='mm'); d.text((x+108,750),l,font=F27,fill=(70,101,96),anchor='mm')
d.text((168,500),'ADWYA',font=F27,fill=(237,250,247),anchor='mm'); save(im,'adwya')

for slug in ('rafiqi-web','rafiqi-android','adwya'):
    for prefix,size in [('cover',(1600,1000)),('thumb',(880,550))]:
        p=Path(f'{prefix}-{slug}.webp'); assert p.exists(); assert Image.open(p).size==size
print('PORTFOLIO_ART_OK')
