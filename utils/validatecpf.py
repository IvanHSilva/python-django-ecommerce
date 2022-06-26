# Validação de CPF

def validatecpf(CPF):
    # CPF = '158.487.118-01'
    # 01234567890123
    tot = 0
    cont = 10
    for digito in CPF:
        if digito.isnumeric():  # print(digito)
            tot += int(digito) * cont
            cont -= 1
    result = 11 - (tot % 11)
    verif1 = 0 if result > 9 else result
    print(tot, verif1)

    tot = 0
    cont = 11
    for digito in CPF:
        if digito.isnumeric() and cont > 2:  # print(digito)
            tot += int(digito) * cont
            cont -= 1
    result = 11 - (tot % 11)
    verif2 = 0 if result > 9 else result
    print(tot, verif2)

    # print('CPF Válido!' if (verif1 == int(CPF[12]) and verif2 == int(CPF[13])) else 'CPF Inválido!!!!')
