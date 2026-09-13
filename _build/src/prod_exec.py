# build_pages.py の定義（cards / css / ARTS / mag_css / art_css …）を全部そろえて、page() だけ横取りする
import os
P=os.path.dirname(os.path.abspath(__file__))+'/'
def load(hook,extra=()):
    src=open(P+'build_pages.py',encoding='utf-8').read()
    src=src.replace("def page(fname,title,body,css='',bodyattr='data-skin=\"bright\"',extra_js=''):\n","def page(fname,title,body,css='',bodyattr='data-skin=\"bright\"',extra_js=''):\n    if PROD_HOOK: return PROD_HOOK(fname,title,body,css,bodyattr,extra_js)\n",1)
    assert 'PROD_HOOK' in src
    g={'__name__':'prod_exec','P':P,'PROD_HOOK':hook}
    exec(src,g)
    for name in extra: exec(open(P+name+'.py',encoding='utf-8').read(),g)
    return g
