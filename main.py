import requests


class ChangeDomain():
    token = None
    domain = None
    sub_domain = None

    def getIpv4(self):
        url = 'https://4.ipw.cn/api/ip/myip?json'
        response = requests.get(url=url).json()
        if response['code'] == 'querySuccess':
            return response['IP']
        return None

    def getIpv6(self):
        url = 'https://6.ipw.cn/api/ip/myip?json'
        response = requests.get(url=url).json()
        if response['code'] == 'querySuccess':
            return response['IP']
        return None

    def getRecords(self):
        url = 'https://dnsapi.cn/Record.List'
        data = {
            'login_token': self.token,
            'domain': self.domain,
            'sub_domain': self.sub_domain,
            'format': 'json',
        }
        response = requests.post(url=url, data=data).json()
        if response['status']['code'] == '1':
            return response['records']
        return None

    def changeRecord(self,record, ip):
        url = 'https://dnsapi.cn/Record.Modify'
        data = {
            'login_token': self.token,
            'domain': self.domain,
            'sub_domain': self.sub_domain,
            'record_id': record['id'],
            'record_type': record['type'],
            'record_line': record['line'],
            'value': ip,
            'mx': record['mx'],
            'format': 'json',
        }
        response = requests.post(url=url,data=data).json()
        if response['status']['code'] == '1':
            print('[INFO]： 当前域名: {}.{},value: {},修改完成.'.format(record['name'],self.domain,ip))
            return
        print('[WARN]: 修改失败：{}'.format(response))

    def changeRecordList(self):
        ipv4 = self.getIpv4()
        ipv6 = self.getIpv6()
        records = self.getRecords()
        if records is None:
            print('[ERROR]： 获取解析列表失败')
            Exception(RuntimeError)
        #   ipv4不为空
        if ipv4 is not None:
            for record in records:
                if self.sub_domain is None:
                    if record['status'] == 'enable' and record['type'] == 'A' and record['name'] == '@':
                        if record['value'] == ipv4:
                            print('[INFO]: 记录值:{},当前值:{} 存在该记录值,不需要修改.'.format(record['value'], ipv4))
                        else:
                            self.changeRecord(record, ipv4)
                else:
                    if record['status'] == 'enable' and record['type'] == 'A' and record['name'] == self.sub_domain:
                        if record['value'] == ipv4:
                            print('[INFO]: 记录值:{},当前值:{} 存在该记录值,不需要修改.'.format(record['value'], ipv4))
                        else:
                            self.changeRecord(record, ipv4)

        #   ipv6不为空
        if ipv6 is not None:
            for record in records:
                if self.sub_domain is None:
                    if record['status'] == 'enable' and record['type'] == 'AAAA' and record['name'] == '@':
                        if record['value'] == ipv6:
                            print('[INFO]: 记录值:{},当前值:{} 存在该记录值,不需要修改.'.format(record['value'], ipv6))
                        else:
                            self.changeRecord(record, ipv6)
                else:
                    if record['status'] == 'enable' and record['type'] == 'AAAA' and record['name'] == self.sub_domain:
                        if record['value'] == ipv6:
                            print('[INFO]: 记录值:{},当前值:{} 存在该记录值,不需要修改.'.format(record['value'], ipv6))
                        else:
                            self.changeRecord(record, ipv6)

        print('[INFO]: 运行结束.')

    def __init__(self, id, token, domain, sub_domain):
        #   根据dnspod需求拼接token字符串
        self.token = id + ',' + token

        self.domain = domain

        if sub_domain == '':
            self.sub_domain = None
        else:
            self.sub_domain = sub_domain

        self.changeRecordList()


if __name__ == '__main__':
    #   ID
    id = 'id'
    #   TOKEN
    token = 'token'
    #   域名
    domain = 'domain'
    #   子域名
    sub_domain = ''

    ChangeDomain(id, token, domain, sub_domain)
