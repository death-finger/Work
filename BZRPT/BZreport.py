import mysql.connector

date_1 = '2017-10-01 00:00:00'
date_2 = '2017-10-31 23:59:59'
print("时间段： %s - %s" % (date_1, date_2))

result = open('result.txt', 'w')
cnx = mysql.connector.connect(user='joshua', password='bagakira', host='192.168.16.10', database='BZRPT')
cursor = cnx.cursor()


def modify_fetch(result, out):
    while result:
        out.append(result[0][0])
        result = result[1:]

# shops = ['reebok京东旗舰店', 'reebok官方商城', 'reebok官方旗舰店']
# payment = ['微信支付', '支付宝', '货到付款', '银行电汇']

# Get All Shops
query = "SELECT 店铺名 FROM sales GROUP BY 店铺名"
cursor.execute(query)
tmp = cursor.fetchall()
shops = []
modify_fetch(tmp, shops)

# Get All Payments
def get_pay(shop):
    query = "SELECT 付款方式 FROM sales WHERE 店铺名='%s' GROUP BY 付款方式" % shop
    cursor.execute(query)
    tmp = cursor.fetchall()
    result = []
    modify_fetch(tmp, result)
    return result


print('Patform\tSold\tReturn\tReturnRate\tExchange\tExchangeRate')
for shop in shops:
    print(shop)
    result.write(shop + '\n')
    payment = get_pay(shop)
    while payment:
        pay = payment[0]
        payment = payment[1:]

        # query Total
        query = "SELECT COUNT(id_seq) FROM sales WHERE 店铺名='%s' AND 付款方式='%s' AND 出入库类型='销售出库' \
        AND 原始订单创建时间 BETWEEN '%s' AND '%s'" % (shop, pay, date_1, date_2)
        cursor.execute(query)
        tmp = cursor.fetchone()
        total = tmp[0]

        # query Return
        query = "SELECT COUNT(id_seq) FROM sales WHERE 店铺名='%s' AND 付款方式='%s' AND 出入库类型='退货入库' \
        AND 原始订单创建时间 BETWEEN '%s' AND '%s'" % (shop, pay, date_1, date_2)
        cursor.execute(query)
        tmp = cursor.fetchone()
        retn = tmp[0]
        if total == 0:
            retn_rate = 'NA'
        else:
            retn_rate = retn / total

        # query Exchange
        query = "SELECT COUNT(id_seq) FROM sales WHERE 店铺名='%s' AND 付款方式='%s' AND 出入库类型='换货入库' \
        AND 原始订单创建时间 BETWEEN '%s' AND '%s'" % (shop, pay, date_1, date_2)
        cursor.execute(query)
        tmp = cursor.fetchone()
        exchange = tmp[0]
        if total == 0:
            exch_rate = 'NA'
        else:
            exch_rate = exchange / total

        print("%s\t%s\t%s\t%s\t%s\t%s" % (pay, total, retn, retn_rate, exchange, exch_rate))
        result.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (pay, total, retn, retn_rate, exchange, exch_rate))

result.flush()

# 排序

def order_article(date_1, date_2):
    # Total
    query = "SELECT 货号, COUNT(id_seq) FROM sales WHERE 出入库类型='销售出库' AND 原始订单创建时间 BETWEEN '%s' AND '%s' \
    GROUP BY 货号 ORDER BY COUNT(id_seq) DESC" % (date_1, date_2)
    cursor.execute(query)
    total = cursor.fetchall()

    # Return
    query = "SELECT 货号, COUNT(id_seq) FROM sales WHERE 出入库类型='退货入库' AND 原始订单创建时间 BETWEEN '%s' AND '%s' \
    GROUP BY 货号 ORDER BY COUNT(id_seq) DESC" % (date_1, date_2)
    cursor.execute(query)
    retn = cursor.fetchall()

    # Return
    query = "SELECT 货号, COUNT(id_seq) FROM sales WHERE 出入库类型='换货入库' AND 原始订单创建时间 BETWEEN '%s' AND '%s' \
    GROUP BY 货号 ORDER BY COUNT(id_seq) DESC" % (date_1, date_2)
    cursor.execute(query)
    exchange = cursor.fetchall()

    print('\n=======================\n')
    result.write('\n=======================\n')
    print('Article\tSold\tReturn\tReturnRate\tExchange\tExchangeRate')
    result.write('Article\tSold\tReturn\tReturnRate\tExchange\tExchangeRate\n')

    for art, num in total:
        print(art, num, sep='\t', end='\t')
        result.write('%s\t%s\t' % (art, num))

        check = 0
        for a, b in retn:
            if art == a:
                check += 1
                rate = b / num
                print(b, rate, sep='\t', end='\t')
                result.write('%s\t%s\t' % (b, rate))
        if check == 0:
            print('NA\tNA', end='\t')
            result.write('NA\tNA\t')

        check = 0
        for x, y in exchange:
            if art == x:
                check += 1
                rate = y / num
                print(y, rate, sep='\t')
                result.write('%s\t%s\n' % (y, rate))
        if check == 0:
            print('NA\tNA')
            result.write('NA\tNA\n')

    result.flush()


def order_model(date_1, date_2):
    # Total
    query = "SELECT Master.Model, COUNT(id_seq) FROM Master, sales WHERE Master.Article=sales.货号 \
    AND 出入库类型='销售出库' AND 原始订单创建时间 BETWEEN '%s' AND '%s' \
    GROUP BY Model ORDER BY COUNT(id_seq) DESC" % (date_1, date_2)

    cursor.execute(query)
    total = cursor.fetchall()

    # Return
    query = "SELECT Master.Model, COUNT(id_seq) FROM Master, sales WHERE Master.Article=sales.货号 \
    AND 出入库类型='退货入库' AND 原始订单创建时间 BETWEEN '%s' AND '%s' \
    GROUP BY Model ORDER BY COUNT(id_seq) DESC" % (date_1, date_2)
    cursor.execute(query)
    retn = cursor.fetchall()

    # Return
    query = "SELECT Master.Model, COUNT(id_seq) FROM Master, sales WHERE Master.Article=sales.货号 \
    AND 出入库类型='换货入库' AND 原始订单创建时间 BETWEEN '%s' AND '%s' \
    GROUP BY Model ORDER BY COUNT(id_seq) DESC" % (date_1, date_2)
    cursor.execute(query)
    exchange = cursor.fetchall()

    print('\n=======================\n')
    result.write('\n=======================\n')
    print('Model\tSold\tReturn\tReturnRate\tExchange\tExchangeRate')
    result.write('Model\tSold\tReturn\tReturnRate\tExchange\tExchangeRate\n')

    for art, num in total:
        print(art, num, sep='\t', end='\t')
        result.write('%s\t%s\t' % (art, num))

        check = 0
        for a, b in retn:
            if art == a:
                check += 1
                rate = b / num
                print(b, rate, sep='\t', end='\t')
                result.write('%s\t%s\t' % (b, rate))
        if check == 0:
            print('NA\tNA', end='\t')
            result.write('NA\tNA\t')

        check = 0
        for x, y in exchange:
            if art == x:
                check += 1
                rate = y / num
                print(y, rate, sep='\t')
                result.write('%s\t%s\n' % (y, rate))
        if check == 0:
            print('NA\tNA')
            result.write('NA\tNA\n')

    result.flush()

order_article(date_1, date_2)
order_model(date_1, date_2)


result.flush()
result.close()