import sys,json
data=open('/home/claude/apps/books.json',encoding='utf8').read().replace('</','<\\/')
for src in sys.argv[1:]:
    s=open(src,encoding='utf8').read().replace('/*BOOKS*/null',data)
    open(src.replace('.src',''),'w',encoding='utf8').write(s)
