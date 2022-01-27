from pyrogram import Client, filters
from config import sudo
import subprocess as s
import re, json, os, random
from pathlib import Path
import utils

CURSED_COMMANDS = ['rm -rf *','rm -rf /','mv ~ dev/null',':(){ :|: & };:']
BAD_COMMANDS = ['neofetch','pip install','pkg install','apt install','python3','python','python -v','python3 -v']
pwd = Path.cwd()

async def run(cmd: list, *args):
    try:
        if cmd[0] in ['echo','curl']:
            x = s.run(' '.join(cmd),shell = True, capture_output = True)
        else:
            x = s.run(cmd, capture_output = True)
        if x.returncode == 0:
            print('execution success')
            return x.stdout.decode("utf-8")
        else:
            print('execution success but with output error')
            return x.stderr.decode("utf-8")
    except Exception as e:
        print('execution failed')
        return f'`{e}`'


@Client.on_message(filters.regex('^\/sh\s+?(?P<args>.+?)?$') & filters.user(sudo))
async def zsh(bot,msg):
    path = Path('.')
    args = msg.matches[0].group('args')
    pre = await msg.reply('`waitt...`', quote = True, parse_mode = 'markdown')
    #print(args)
    if args == None:
        pass
    elif args in CURSED_COMMANDS:
        await pre.edit_text('Anda mencoba command paling terkutuk dalam sejarah')
    elif args in BAD_COMMANDS:
        await pre.edit_text('Sepertinya command ini tidak menarik')
    else:
        cmd = args.split(' ')
        #handle cd
        if cmd[0] == 'cd':
            if len(cmd) == 2:
                try:
                    os.chdir(cmd[1])
                    x = f'`{Path.cwd()}`'
                except Exception as e:
                    x = str(e)
            else:
                os.chdir(pwd)
                x = f'`{Path.cwd()}`'
        
        #handle ls
        elif cmd[0] == 'ls':
            cwd = Path.cwd()
            ex = {
                '.py':'🐍','.js':'☕️','.html':'🔰','.css':'🎨',
                '.mp3':'🎵','.mp4':'📼','.mkv':'📼','.gif':'📼',
                '.txt':'📝','.json':'📝'
            }
            x = f'`{cwd}`\n'
            file = []
            dir = []
            for i in sorted(cwd.iterdir()):
                if i.is_dir():
                    dir.append(i)
                else:
                    file.append(i)
            for f in [*dir,*file]:
                size = f.stat().st_size
                if f.is_dir():
                    x += f'📂 `{f.name}`\n'
                else:
                    ex.setdefault(f.suffix,'📄')
                    x += f'{ex[f.suffix]} `{f.name}` `({utils.humansized(size)})`\n'
        
        #handle cwd 
        elif cmd[0] == 'cwd':
            x = f'`{Path.cwd()}`'
        
        #curl with pretty json
        elif cmd[0] == 'curl':
            js = await run(cmd)
            try:
                res = json.dumps(json.loads(js), indent = 1, separators=(',', ': '))
                x = f'`{res}`'
            except Exception as e:
                x = f'`{e}`'
        
        elif cmd[0] == 'rm':
            cwd = Path.cwd()
            os.remove(cwd / ' '.join(cmd).replace('rm ', ''))
            x = '`success remove file`'
        else:
            res = await run(cmd)
            x = f'`{res}`'
        length = len(x)
        if length >= 4096:
            file = f'temp/output-{random.randint(1,100)}.txt'
            op = open(file,'a')
            op.write(x)
            await pre.edit_text('output teks lebih dari [4 KB](https://limits.tginfo.me/id-ID), sebagai gantinya output dikirim dalam bentuk file')
            await msg.reply_document(
                file, 
                quote = True, 
                file_name = 'output.txt'
            )
            os.remove(file)
        else:
            pesan = x
            await pre.edit_text(pesan, parse_mode = 'markdown')