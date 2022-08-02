import argparse
import requests
from urllib3 import PoolManager
from requests.adapters import HTTPAdapter


class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=self.ssl_version
        )


def main_program(url: str, test_tls: str, arg_proxy: str):

    if not test_tls or test_tls.upper() == 'ALL' :
        tls_protocols = 'TLSv1,TLSv1_1,TLSv1_2'.split(',')
    else:
        tls_protocols = test_tls.split(',')
    for version in tls_protocols:
        print('Testing protocol ' + version)
        s = requests.Session()
        test_version = 'PROTOCOL_' + version.upper().replace('V', 'v')
        
        try:
            MyAdapter.ssl_version = test_version
            s.mount('https://', MyAdapter())
            proxy = {'http':arg_proxy , 'https': arg_proxy}
            r = s.get(url=url,proxies=proxy, allow_redirects=False)
            r.close()
            s.close()
            print("[\u2713] The "+ version + " is supported")
        except requests.exceptions.SSLError:
            print("[X] The " + version + " is not supported")
        except AttributeError:
            print("Please verify the protocol typed")


if __name__ == '__main__':
    """Program to test different TLS versions in a website"""

    parser = argparse.ArgumentParser(description='Test different TLS version over a given website')
    parser.add_argument('--url', type=str, required=True, help='Url on which you want to test the TLS version that accept')
    parser.add_argument('--tls', type=str, required=False, help='Insert the tls versions separate by comma to test, e.g tlsv1,tlsv1_1 or All to test from tlsv1 through tlsv1.2')
    parser.add_argument('--proxy', type=str, required=False, help='In case you want to pass the request thorugh a proxy')
    
    args = parser.parse_args()
    url = args.url
    tls = args.tls
    proxy = args.proxy

    main_program(url, tls, proxy)
