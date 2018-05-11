from os import walk
from datetime import datetime
from ast import literal_eval
import base64


def get_key(dic, key_search):
    if type(dic) is dict:
        for item in dic.keys():
            if key_search.lower() == item.lower():
                return item
    return ''


if __name__ == '__main__':
    contador = 0
    app_server = {}
    hardlock_clientes = literal_eval(open('d:\\hardlockcloud.csv', 'r').read())
    arquivo_auditing = open('D:\\teste\\json\\output\\Discovery_Auditing.csv', 'a')
    arquivo_companies = open('D:\\teste\\json\\output\\Discovery_Companies.csv', 'a')
    arquivo_users = open('D:\\teste\\json\\output\\Discovery_Users.csv', 'a')
    arquivo_license = open('D:\\teste\\json\\output\\Discovery_License.csv', 'a')
    arquivo_support = open('D:\\teste\\json\\output\\Discovery_TechnicalSupport.csv', 'a')

    print("INICIO:", datetime.today())
    for (dirpath, dirnames, filenames) in walk('d:\\teste\\json'):
        if filenames.__len__() > 0:
            for file in filenames:
                if '.JSON' in file.upper():
                    contador += 1
                    arquivo = open(dirpath+'\\'+file, 'r')
                    data_arquivo = arquivo.name.split('\\')
                    if 'log' in data_arquivo:
                        info_geral = []
                        arquivo_json = literal_eval(arquivo.read())
                        index_log = data_arquivo.index('log')
                        dateLogReceived = '{}-{}-{}T00:00:00.0000000'.format(data_arquivo[index_log + 1],
                                                                          data_arquivo[index_log + 2],
                                                                          data_arquivo[index_log + 3])
                        hardlock_id = data_arquivo[index_log + 4].split('_')[1]
                        LocalId = arquivo_json[get_key(arquivo_json, "LocalId")]
                        LSBuild = arquivo_json[get_key(arquivo_json, "LSBuild")]
                        LSVersion = arquivo_json[get_key(arquivo_json, "LSVersion")]
                        cliente = hardlock_clientes[hardlock_id][0]
                        loja = hardlock_clientes[hardlock_id][1]
                        key_auditing = get_key(arquivo_json, 'auditing')
                        if key_auditing:
                            for audit in arquivo_json[key_auditing]:
                                key_data = get_key(audit, 'data')
                                if key_data:
                                    dados_audit = audit.get(key_data)
                                    arquivo_auditing.write('"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",'
                                                           '"{}","{}","{}","{}","{}","{}","{}","{} {}","{}"'
                                                           '\n'.format(dateLogReceived,
                                                                       hardlock_id,
                                                                       LocalId,
                                                                       LSBuild,
                                                                       LSVersion,
                                                                       cliente,
                                                                       loja,
                                                                       dados_audit[0],
                                                                       dados_audit[1],
                                                                       dados_audit[2],
                                                                       dados_audit[3],
                                                                       dados_audit[4],
                                                                       dados_audit[5],
                                                                       dados_audit[6],
                                                                       dados_audit[7],
                                                                       dados_audit[8],
                                                                       dados_audit[9],
                                                                       dados_audit[10],
                                                                       dados_audit[11][0][0:10],
                                                                       dados_audit[11][1],
                                                                       dados_audit[12]))

                        key_companies = get_key(arquivo_json, 'companies')
                        if key_companies:
                            for companie in arquivo_json[key_companies]:
                                key_id = get_key(companie, 'id')
                                key_federalid = get_key(companie, 'federalid')
                                key_nome = get_key(companie, 'nome')
                                key_apelido = get_key(companie, 'apelido')
                                arquivo_companies.write('"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"'
                                                        '\n'.format(dateLogReceived,
                                                                    hardlock_id,
                                                                    LocalId,
                                                                    LSBuild,
                                                                    LSVersion,
                                                                    cliente,
                                                                    loja,
                                                                    companie[key_id] if key_id else '',
                                                                    companie[key_federalid] if key_federalid else '',
                                                                    companie[key_nome] if key_nome else '',
                                                                    companie[key_apelido] if key_apelido else ''))

                        key_users = get_key(arquivo_json, 'users')
                        if key_users:
                            for user in arquivo_json[key_users]:
                                arquivo_users.write('"{}","{}","{}","{}","{}","{}","{}","{}","{}"'
                                                    '\n'.format(dateLogReceived,
                                                                hardlock_id,
                                                                LocalId,
                                                                LSBuild,
                                                                LSVersion,
                                                                cliente,
                                                                loja,
                                                                user['id'],
                                                                user['nome']))

                        key_users = get_key(arquivo_json, 'licensebalance')
                        if key_users:
                            for license_balance in arquivo_json[key_users]:
                                key_year = get_key(license_balance, 'year')
                                key_month = get_key(license_balance, 'month')
                                key_day = get_key(license_balance, 'day')
                                key_slotid = get_key(license_balance, 'slotid')
                                key_total = get_key(license_balance, 'total')
                                key_peak = get_key(license_balance, 'peak')
                                arquivo_license.write('"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"'
                                                      '\n'.format(dateLogReceived,
                                                                  hardlock_id,
                                                                  LocalId,
                                                                  LSBuild,
                                                                  LSVersion,
                                                                  cliente,
                                                                  loja,
                                                                  license_balance[key_year] if key_year else '',
                                                                  license_balance[key_month] if key_month else '',
                                                                  license_balance[key_day] if key_day else '',
                                                                  license_balance[key_slotid] if key_slotid else '',
                                                                  license_balance[key_total] if key_total else '',
                                                                  license_balance[key_peak] if key_peak else ''))

                        key_support = get_key(arquivo_json, 'technicalsupport')
                        if key_support:
                            for support in arquivo_json[key_support]:
                                key_data = get_key(support, 'data')
                                if key_data:
                                    dados_support = base64.b64decode(support.get(key_data))
                                    dados_support = dados_support.decode("utf-8", "ignore")
                                    dados_support = dados_support.replace(":null", ':""')
                                    if dados_support and dados_support != '':
                                        dados_support = literal_eval(dados_support)
                                        key_method = get_key(dados_support, 'method')
                                        key_code = get_key(dados_support, 'code')
                                        key_product = get_key(dados_support, 'productline')
                                        key_app_srv = get_key(dados_support, 'applicationserver')
                                        if key_app_srv != '':
                                            key_op_sys = get_key(dados_support[key_app_srv], 'operationsystem')
                                            key_memory = get_key(dados_support[key_app_srv], 'memory')
                                            key_processor = get_key(dados_support[key_app_srv], 'processor')
                                            key_core = get_key(dados_support[key_app_srv], 'core')
                                            key_clock = get_key(dados_support[key_app_srv], 'clock')
                                            key_idioma = get_key(dados_support[key_app_srv], 'idioma')
                                        else:
                                            key_op_sys = ''
                                            key_memory = ''
                                            key_processor = ''
                                            key_core = ''
                                            key_clock = ''
                                            key_idioma = ''
                                        arquivo_support.write('"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}",'
                                                              '"{}","{}","{}","{}","{}"'
                                                              '\n'.format(dateLogReceived,
                                                                          hardlock_id,
                                                                          LocalId,
                                                                          LSBuild,
                                                                          LSVersion,
                                                                          cliente,
                                                                          loja,
                                                                          dados_support[key_method] if key_method else '',
                                                                          dados_support[key_code] if key_code else '',
                                                                          dados_support[key_product] if key_product else '',
                                                                          dados_support[key_app_srv][key_op_sys] if key_app_srv and key_op_sys else '',
                                                                          dados_support[key_app_srv][key_memory] if key_app_srv and key_memory else '',
                                                                          dados_support[key_app_srv][key_processor] if key_app_srv and key_processor else '',
                                                                          dados_support[key_app_srv][key_core] if key_app_srv and key_core else '',
                                                                          dados_support[key_app_srv][key_clock] if key_app_srv and key_clock else '',
                                                                          dados_support[key_app_srv][key_idioma] if key_app_srv and  key_idioma else ''))

                    else:
                        print('Caminho raiz para pasta de log não enconrado!')
                    arquivo.close()
                    print(contador)
                    if contador == 2000:
                        print("2000:", datetime.today())

    arquivo_auditing.close()
    arquivo_companies.close()
    arquivo_users.close()
    arquivo_license.close()
    arquivo_support.close()
    print("FIM:", datetime.today())
