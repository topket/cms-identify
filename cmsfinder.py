import requests, re

def drcms(url):
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
                    
    html = req(url)
    regex = {'meta':'<meta*.*','script':r'(<script type.*\">|<script type.*\'\>)','meta_regex':[
            {'wordpress':'(wp-content/themes|wp-content/uploads|WordPress.[0-9].[0-9].[0-9]|Powered by Slider Revolution|WordPress.com)'},
            {'drupal':'(Drupal [0-9])'},
            {'joomla':'(Joomla. - Open Source Content Management)'},
            {'prestashop':'(PrestaShop)'}],'script_regex':[
            {'wordpress':'(/wp-content/plugins/)'},
            {'drupal':'(/misc/drupal.js)'},
            {'magento':'(text/x-magento-init)'}]}
    
    if html:
        check = search(html, regex['meta'],regex['meta_regex'])
        if check:return check
        check = search(html, regex['script'],regex['script_regex'])
        if check:return check
        opencart = req(url+"/admin/index.php?route=common/dashboard")
        if opencart and "OpenCart" in opencart:return 'opencart'
        return 'unknown'
