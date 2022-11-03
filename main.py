from multiprocessing.pool import ThreadPool
from fake_useragent import UserAgent
from colorama import *
import requests,os,re
init()

c1 = Fore.MAGENTA
c2 = Fore.GREEN
c3 = Fore.WHITE
c4 = Fore.CYAN
c5 = Fore.RED
c6 = Fore.BLUE
c7 = Fore.YELLOW

paneller = [
    "wp-login.php","administrator","admin","admin.php","login","login.php","panel","panel.php","usr.php","admin/login.php","user/login.php","login/admin.php"
]

def cms_check(source):
    if ("/wp-content/" in source or "/wp-includes/" in source):
        return "WordPress"
    elif ("index.php?option=com_" in source):
        return "Joomla"
    elif ("index.php?route=common/home" in source):
        return "OpenCart"
    elif ("sites/default" in source):
        return "Drupal"
    elif ('var prestashop = {"cart"' in source or "/modules/revsliderprestashop" in source):
        return "PrestaShop"
    elif ('title="vBulletin"' in source):
        return "vBulletin"
    elif ('"mage/cookies":' in source):
        return "Magento"
    else:
        return "Unknown"

def admin_panel_finder(domain):
    url = "http://" + domain + "/"
    for panel in paneller:
        nurl = url + panel
        try:
            req = requests.get(nurl, headers={
                "User-Agent":UserAgent().random
            }, timeout=25)
            if (req.status_code != 404 and 'type="password"' in req.text):
                cms = cms_check(req.text)
                print(f" {c2}+ {c3}CMS={c1}{cms} {c3}URL={c1}{nurl}")
                open(cms+".txt","a").write(nurl+"\n")
                break
        except:
            continue

def viewdns(domain):
    siteler = []
    url = "https://viewdns.info/reverseip/?host="+domain+"&t=1"
    try:
        req = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        })
        sites = list(set(re.findall('</tr><tr> <td>(.*?)</td><td align="center">(.*?)</td>', req.text)))
        for site in sites:
            siteler.append(site[0])
        print(f"{c1}{domain}{c3} domainine ait {c1}{str(len(sites))}{c3} site bulundu.\n")
    except ConnectionError: 
        print("Bağlantı hatası, lütfen internetinizi kontrol edin!")
        exit()
    except Exception as er:
        print(er)
        exit()
    return siteler

def main():
    domain = input(f"{c3}Domain~>{c1} ")
    process = int(input(f"{c3}Process~>{c1} "))
    print("")
    linkler = viewdns(domain)
    p = ThreadPool(process)
    p.map(admin_panel_finder, linkler)

def banner():
    if (os.name == "nt"):
        os.system("cls")
    else:
        os.system("clear")

    print(fr"""
{c3}████████╗ █████╗  ██████╗ ██████╗ ██╗     ██╗██╗     ██╗      █████╗
{c6}╚══██╔══╝██╔══██╗██╔════╝██╔═══██╗██║     ██║██║     ██║     ██╔══██╗
{c3}   ██║   ███████║██║     ██║   ██║██║     ██║██║     ██║     ███████║
{c3}   ██║   ██╔══██║██║     ██║   ██║██║     ██║██║     ██║     ██╔══██║
{c4}   ██║   ██║  ██║╚██████╗╚██████╔╝███████╗██║███████╗███████╗██║  ██║
{c4}   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
{c3}       
{c7}>{c3} Coded By Will Graham {c4}| {c3}Github: cannibal-hannibal {c4}| {c3}TG: @wwillgraham {c7}<          

    """)

if (__name__=="__main__"):
    banner()
    main()