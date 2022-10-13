# -*- coding: utf-8 -*-
#Bibliotecas que precisei importar
import email.message
import smtplib
from zabbix_api import ZabbixAPI

# Função para fazer login:
zapi = ZabbixAPI(server="http://endereçodozabbix/zabbix")
login = zapi.login("Admin","zabbix")

# Json de consulta a o zabbix
host_inf = zapi.host.get({
    "output":[
        "hostid",
        "host"
    ],
    "filter":{
        "status":[
            "1"
        ]
    },
    "sortfield": "name"
})

# Condição para verificar se há hosts a serem removidos, caso haja removelos e disparar email para cada host removido,
# caso não haja enviar email avisando.
if host_inf == []:
    #mensagem do email exemplo:
    html = "Prezados, <br> <br> Nenhum host foi removido. <br> <br> Att."
    #emails de destino exemplo
    emails = ['meuemail@gmail.com.br']
    msg = email.message.Message()
    msg.set_payload(html)
    #titulo do email exemplo:
    msg['Subject'] = '[Alerta] Hosts removidos'
    #email de origem e nome do sujeito que está enviando exemplo
    msg['From'] = "Alertas Zabbix <info@gmail.com>"
    msg['To'] = ", ".join(emails)
    msg.add_header('Content-Type', 'text/html')
    #endereço do servidor smtp exemplo:
    s = smtplib.SMTP('email-smtp.amazonaws.com', 587)
    s.ehlo()
    s.starttls()
    #login no servidor smtp:
    s.login('login', 'senha')
    s.sendmail(msg['From'], emails, msg.as_string())
    s.quit()
else:
   for hostid in host_inf:
        host_del = zapi.host.delete({
            "hostid": hostid['hostid']
        })
        #mensagem do email exemplo:
        html = "Prezados, <br> <br>" + hostid['hostid'] + "  |  " +"<strong>"+ hostid['host'] + "</strong>" + " - " + "removido com sucesso" + "<br> <br> Att."
        #emails de destino exemplo
        emails = ['meuemail@gmail.com.br']
        msg = email.message.Message()
        msg.set_payload(html)
        #titulo do email exemplo:
        msg['Subject'] = '[Alerta] Hosts removidos'
        #email de origem e nome do sujeito que está enviando exemplo
        msg['From'] = "Alertas Zabbix <info@gmail.com>"
        msg['To'] = ", ".join(emails)
        msg.add_header('Content-Type', 'text/html')
        #endereço do servidor smtp exemplo:
        s = smtplib.SMTP('email-smtp.amazonaws.com', 587)
        s.ehlo()
        s.starttls()
        #login no servidor smtp:
        s.login('login', 'senha')
        s.sendmail(msg['From'], emails, msg.as_string())
        s.quit()

# caso não va usar a função para disparar email comente o if e else acima e descomente o código abaixo:
# for hostid in host_inf:
#         host_del = zapi.host.delete({
#             "hostid": hostid['hostid']
#         })