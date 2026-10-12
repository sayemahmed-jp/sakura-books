import json,re,collections
from sudachipy import dictionary,tokenizer
D=dictionary.Dictionary(dict="core")
TC=D.create(tokenizer.Tokenizer.SplitMode.C);TA=D.create(tokenizer.Tokenizer.SplitMode.A)
H2K=str.maketrans({chr(c):chr(c+0x60) for c in range(0x3041,0x3097)})
def norm(s):return re.sub(r'[^゠-ヿ]','',s.translate(H2K)).replace('ヲ','オ').replace('ヅ','ズ').replace('ヂ','ジ').replace('ー','ウ')
items=json.load(open('jp.json'))
pat=re.compile(r'\{([^|{}]+)\|([^{}]+)\}')
pairs=collections.defaultdict(list)
for it in items:
    s=it['s'];plain=pat.sub(r'\1',s)
    # build span map in plain
    pos=0;spans=[]
    for m in pat.finditer(s):
        pre=pat.sub(r'\1',s[:m.start()]);st=len(pre);spans.append((st,st+len(m.group(1)),m.group(1),m.group(2)))
    for mode,T in (('C',TC),('A',TA)):
        toks=[(t.begin(),t.end(),t.reading_form()) for t in T.tokenize(plain)]
        it.setdefault('tok',{})[mode]=toks
    for st,en,base,rd in spans:
        ok=False
        for mode in ('C','A'):
            toks=it['tok'][mode]
            cov=[t for t in toks if t[0]<en and t[1]>st]
            if cov and cov[0][0]==st and cov[-1][1]==en:
                if norm(''.join(t[2] for t in cov))==norm(rd): ok=True
            # token larger than span: check rd is prefix/suffix part of token reading consistent
            if len(cov)==1:
                t=cov[0];full=norm(t[2])
                surf=plain[t[0]:t[1]]
                # okurigana trailing kana in token after span
                tail=norm(plain[en:t[1]]);head=norm(plain[t[0]:st])
                if full==head+norm(rd)+tail: ok=True
        for T in (TC,TA):
            if norm(''.join(t.reading_form() for t in T.tokenize(base)))==norm(rd): ok=True
        if not ok: pairs[(base,rd)].append(plain)
res=sorted(pairs.items(),key=lambda x:-len(x[1]))
with open('pairs.txt','w') as f:
    for (b,r),ctx in res:
        alt=''.join(t.reading_form() for t in TC.tokenize(b))
        f.write(f"{b}|{r}  dict:{alt}  x{len(ctx)}  e.g. {ctx[0][:60]}\n")
print(len(res))
