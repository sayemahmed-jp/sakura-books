import json,re
from sudachipy import dictionary,tokenizer
D=dictionary.Dictionary(dict="core")
TC=D.create(tokenizer.Tokenizer.SplitMode.C);TA=D.create(tokenizer.Tokenizer.SplitMode.A)
def norm(s):return re.sub(r'[^゠-ヿ]','',''.join(chr(ord(c)+0x60) if 'ぁ'<=c<='ゖ' else c for c in s)).replace('ヲ','オ').replace('ヅ','ズ').replace('ヂ','ジ').replace('ー','ウ')
pat=re.compile(r'\{([^|{}]+)\|([^{}]+)\}')
out={};n=0
for it in json.load(open('jp2.json')):
    s=it['s']
    if '{' not in s or s in out: continue
    plain=pat.sub(r'\1',s);toks={m:[(t.begin(),t.end(),t.reading_form()) for t in T.tokenize(plain)] for m,T in (('C',TC),('A',TA))}
    res='';last=0;changed=False
    for m in pat.finditer(s):
        res+=s[last:m.start()];last=m.end()
        st=len(pat.sub(r'\1',s[:m.start()]));base,rd=m.group(1),m.group(2);en=st+len(base);ok=False
        for mode in 'CA':
            cov=[t for t in toks[mode] if t[0]<en and t[1]>st]
            if cov and cov[0][0]==st and cov[-1][1]==en and norm(''.join(t[2] for t in cov))==norm(rd): ok=True
            if len(cov)==1:
                t=cov[0]
                if norm(t[2])==norm(plain[t[0]:st])+norm(rd)+norm(plain[en:t[1]]): ok=True
        if ok: res+=base
        else: res+=rd;changed=True
    res+=s[last:]
    out[s]=res;n+=changed
json.dump(out,open('/home/claude/apps/tts.json','w'),ensure_ascii=False)
print(len(out),'with kana substitutions',n)
