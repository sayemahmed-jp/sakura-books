import sys,json
data=open('/home/claude/apps/books.json',encoding='utf8').read().replace('</','<\\/')
tts=open('/home/claude/apps/tts.json',encoding='utf8').read().replace('</','<\\/')
for src in sys.argv[1:]:
    s=open(src,encoding='utf8').read().replace('/*BOOKS*/null',data).replace('/*TTS*/{}',tts)
    open(src.replace('.src',''),'w',encoding='utf8').write(s)
