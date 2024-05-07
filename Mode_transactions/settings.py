
# ===================================== options ===================================== #

#----main-options----#
shuffle = True                                                      # True / False. если нужно перемешать кошельки
decimal_places = 7                                                  # количество знаков, после запятой для генерации случайных чисел
value_eth = ['70', '80']                                            # минимальное и максимальное кол-во ETH для свапов и ликвы, в ковычках ("90") можно указать процент
delay_wallets = [2, 3]                                              # минимальная и максимальная задержка между кошельками
delay_transactions = [3, 4]                                         # минимальная и максимальная задержка между транзакциями
RETRY_COUNT = 2                                                     # кол-во попыток при возникновении ошибок

slippage = 5                                                        # слипейдж для свапов USDT и USDC
count_swaps = [1, 1]                                                # количество свапов для SwapMode, SupSwap, KimExchange
swap_list = ['MOLTEN', 'ezETH', 'SMD','USDC', 'USDT', 'MODE']       # список токенов для 100% свапа в эфир на SwapMode, можно добавить новые в module.py, Swap_to_eth
deposit_chain_from_Mode = 'Base'                                    # сеть для вывода из MODE и депозита на биржевой адрес, Nitro_from_Mode, Okex_deposit
value_nitro_bridge = [0.0031, 0.0032]                               # минимальное и максимальное кол-во ETH для бриджа через нитро, в ковычках ("90") можно указать процент, Nitro_to_Mode, Nitro_from_Mode
stay_eth = [0.0013, 0.0015]                                         # сколько оставлять эфира в сети перед депозитом на биржу, Okex_deposit

#------okex-options------#
withdraw_from_okex = True                                           # True / False. если нужно выводить с окекса
symbolWithdraw = "ETH"                                              # символ токена, не менять, нахуя вам другой токен
network_okex = "Base"                                               # ID сети используется для вывода с окекса и бриджа в MODE, Optimism | ERC20 | zkSync | Linea | Base
amount = [0.0032, 0.0039]                                           # минимальная и максимальная сумма
transfer_subaccount = False                                         # перевод эфира с суббакков на мейн, используется в Okex_withdrawal

class API:
    # okx API
    okx_apikey = ""
    okx_apisecret = ""
    okx_passphrase = ""

#------bot-options------#
bot_status = False                                                  # True / False
bot_token  = ''                                                     # telegram bot token
bot_id     = 0                                                      # telegram id

'''
Okex_withdrawal, Nitro_to_Mode, LayerBank, SwapMode, IONIC, Ironclad, SupSwap, KimExchange, Nitro_from_Mode, Okex_deposit, Swap_to_eth
Eсли указать модули для дексов в MODE в [], то они перемешаются. Например [['Nitro_to_Mode'], [['SwapMode'], ['SupSwap'], ['LayerBank']], ['Nitro_from_MOde']]
'''

rotes_modules = [
            ['Claim_airdrop'],
]

# =================================== end-options =================================== #


