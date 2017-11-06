# -*- encoding: utf-8 -*-

from ..day1.account_func import register, login

file_prod = open('product_list.txt', 'r')
file_account = open('account.txt', 'r')
file_cart = open('shopping_cart.txt', 'r')

Menu = [
    'Login', 'Register'
]
