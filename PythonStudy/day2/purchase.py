# -*- coding: utf-8 -*-

money = int(input('Please input the money you have: '))

product_list = [
    (1, 'iPhone X', 7800),
    (2, 'MacBook Pro', 20000),
    (3, 'Coffee', 42),
    (4, 'Python Cook Book', 80),
    (5, 'USB Disk', 200)
]

shopping_cart = []


for num, prod, price in product_list:
    print('%s.\t%s\t%s' % (num, prod, price))

while True:
    action = input("Please select the product, [exit] to quit:")
    if action == 'exit':
        total = 0
        print('=' * 24)
        print('Shopping Cart:')
        for item, price in shopping_cart:
            print('%s\t%s' % (item, price))
            total += price
        print('Total:\t%s' % total)
        break
    for i in product_list:
        if int(action) == i[0]:
            if money > i[2]:
                shopping_cart.append((i[1], i[2]))
                money -= i[2]
                print('Added %s to your shopping cart!' % i[1])
                print('You have %s money left!' % money)
            else:
                print("You don't have enough money!")
                print('You have %s money left!' % money)

