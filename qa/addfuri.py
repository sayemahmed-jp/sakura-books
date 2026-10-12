import re,glob,json,sys
from sudachipy import dictionary,tokenizer
T=dictionary.Dictionary(dict="core").create(tokenizer.Tokenizer.SplitMode.C)
K=re.compile(r'[一-鿿々]')
k2h=lambda s:''.join(chr(ord(c)-0x60) if 'ァ'<=c<='ヶ' else c for c in s)
FIX={'普通形':'ふつうけい','受身形':'うけみけい','可能形':'かのうけい','意向形':'いこうけい','条件形':'じょうけんけい','命令形':'めいれいけい','使役形':'しえきけい','辞書形':'じしょけい','間':'あいだ','方':'かた','人':'ひと','物':'もの','後ろ':'うしろ','下手':'へた','上手':'じょうず','数量':'すうりょう','使役':'しえき','受身':'うけみ','歳':'さい','何歳':'なんさい','授受表現':'じゅじゅひょうげん','自動詞':'じどうし','他動詞':'たどうし','疑問詞':'ぎもんし','助数詞':'じょすうし','助詞':'じょし'}
def furi_seg(seg):
    out=''
    for t in T.tokenize(seg):
        s=t.surface()
        if not K.search(s): out+=s;continue
        r=k2h(t.reading_form())
        if s in FIX: out+='{%s|%s}'%(s,FIX[s]);continue
        pre='';post=''
        while s and not K.search(s[-1]) and r.endswith(s[-1]): post=s[-1]+post;s=s[:-1];r=r[:-1]
        while s and not K.search(s[0]) and r.startswith(s[0]): pre+=s[0];s=s[1:];r=r[1:]
        out+=pre+'{%s|%s}'%(s,r)+post
    return out
def addfuri(x):
    parts=re.split(r'(\{[^|{}]+\|[^{}]+\})',x)
    return ''.join(p if p.startswith('{') else (furi_seg(p) if K.search(p) else p) for p in parts)
if __name__=='__main__':
    changes=[]
    for f in sorted(glob.glob('/home/claude/book/data*.js')+glob.glob('/home/claude/book4/data*.js')):
        s=open(f,encoding='utf8').read();o=s
        def rep(m):
            key,val=m.group(1),m.group(2)
            outside=re.sub(r'\{[^|{}]+\|[^{}]+\}','',val)
            # skip parenthesis-reading styled strings like 開く（あく）
            if not K.search(outside) or re.search(r'（[ぁ-ん・]+）',val): return m.group(0)
            nv=addfuri(val);changes.append((f.split('/')[-2]+'/'+f.split('/')[-1],val,nv));return f'{key}:"{nv}"'
        s=re.sub(r'\b(pt|t):"([^"\n]*)"',rep,s)
        if '--apply' in sys.argv and s!=o: open(f,'w',encoding='utf8').write(s)
    for c in changes: print(c[0],'|',c[1],'=>',c[2])
