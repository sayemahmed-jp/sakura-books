import fs from 'fs';
function load(dir,files){globalThis.BOOK={units:[]};for(const f of files)eval(fs.readFileSync(dir+'/'+f,'utf8'));return BOOK.units}
const N5=load('/home/claude/book',['data1.js','data2.js','data3.js','data4.js','data5.js']);
const N4=load('/home/claude/book4',['data1.js','data2.js','data3.js','data4.js']);
fs.writeFileSync('/home/claude/apps/books.json',JSON.stringify({N5,N4}));
console.log(fs.statSync('/home/claude/apps/books.json').size);
