import requests, re

def drcms(url):
    def version(cms,html):
        versions = {'wordpress':'(?<=content=\"WordPress.)[0-9](?:.[0-9]|)(?:.[0-9]|)','drupal':'(?<=content=\"Drupal.)[0-9](?:.[0-9]|)(?:.[0-9]|)'}
        if cms in [keys for keys in versions.keys()]:
            ver = re.compile(versions[cms]).findall(html)
            if ver:
                return {'cms':cms,'version':ver[0]}
        else:
            return {'cms':cms,'version':'unknown'}      
        
    def req(url):
        try:
            headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'}
            r=requests.get(url,headers=headers,timeout=5)
            return r.text
        except:return False
            
    def search(html, regexM, regexL):
        find = re.compile(regexM, re.IGNORECASE).findall(html)
        if find:
            clean = " ".join(find)
            for dictS in regexL:
                for dictK,dictV in dictS.items():
                    if re.compile(dictV,re.IGNORECASE).findall(clean):
                        return dictK   
    
    if isinstance(url,dict):                
        html = url['html']
        url = url['url']
    else:
        html = req(url)
        
    regex = {'meta':'<meta*.*','script':r'(<script type.*\">|<script type.*\'\>)','meta_regex':[
            {'wordpress':'(wp-content/themes|wp-content/uploads|(?<=content=\"WordPress.)[0-9](?:.[0-9]|)(?:.[0-9]|)|Powered by Slider Revolution|WordPress.com)'},
            {'drupal':'(Drupal [0-9])'},
            {'joomla':'(Joomla. - Open Source Content Management)'},
            {'prestashop':'(PrestaShop)'}],'script_regex':[
            {'wordpress':'(/wp-content/plugins/|/wp-includes)'},
            {'drupal':'(/misc/drupal.js)'},
            {'magento':'(text/x-magento-init)'}]}
    
    if html:
        check = search(html, regex['meta'],regex['meta_regex'])
        if check:return version(check,html)
        check = search(html, regex['script'],regex['script_regex'])
        if check:return {'cms':check,'version':'unknown'}
        opencart = req(url+"/admin/index.php?route=common/dashboard")
        if opencart and "OpenCart" in opencart:return {'cms':'opencart','version':'unknown'}
        return 'unknown'




