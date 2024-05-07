from loguru import logger
import random

from help import Account, send_message, sleeping_between_wallets, intro, outro
from settings import bot_status, shuffle, bot_id, bot_token, network_okex, deposit_chain_from_Mode, withdraw_from_okex, rotes_modules
from module import LayerBank, SwapMode, IONIC, Ironclad, Nitro, Okex, SupSwap, KimExchange, Claim_airdrop




def main():
    with open('proxies.txt', 'r') as file:  # login:password@ip:port в файл proxy.txt
        proxies = [row.strip() for row in file]
    with open('wallets.txt', 'r') as file:
        wallets = [row.strip() for row in file]
    send_list = []
    intro(wallets)
    count_wallets = len(wallets)

    if len(proxies) == 0:
        proxies = [None] * len(wallets)
    if len(proxies) != len(wallets):
        logger.error('Proxies count doesn\'t match wallets count. Add proxies or leave proxies file empty')
        return

    data = [(wallets[i], proxies[i]) for i in range(len(wallets))]
    all_tokens = 0

    if shuffle:
        random.shuffle(data)

    for idx, (wallet, proxy) in enumerate(data, start=1):
        if ':' in wallet:
            private_key, addressokx = wallet.split(':')[0], wallet.split(':')[1]
        else:
            private_key = wallet
            addressokx = None

        account = Account(idx, private_key, proxy, "Mode")
        print(f'{idx}/{count_wallets} : {account.address}\n')
        send_list.append(f'{account.id}/{count_wallets} : [{account.address}]({"https://debank.com/profile/" + account.address})')

        try:
            for module in rotes_modules:
                if len(module) > 1:
                    random.shuffle(module)
                    for module_shuffle in module:
                        send_list.append(globals()[module_shuffle[0]](id=account.id, private_key=account.private_key, proxy=account.proxy, rpc="Mode").main())
                elif module[0] == 'Okex_withdrawal' and withdraw_from_okex:
                    send_list.append(Okex(id=account.id, private_key=account.private_key, proxy=account.proxy, rpc=network_okex).withdraw_from_okex())
                elif module[0] == 'Nitro_to_Mode':
                    send_list.append(Nitro(id=account.id, private_key=account.private_key, proxy=account.proxy, rpc=network_okex).main(toChain='Mode'))
                elif module[0] == 'Nitro_from_Mode':
                    send_list.append(Nitro(id=account.id, private_key=account.private_key, proxy=account.proxy, rpc='Mode').main(toChain=deposit_chain_from_Mode))
                elif module[0] == 'Okex_deposit':
                    if addressokx != None:
                        send_list.append(Okex(account.id, account.private_key, account.proxy, deposit_chain_from_Mode).deposit_to_okex(addressokx))
                    else:
                        logger.info(f'Не найден адрес депозита...')
                elif module[0] == 'Swap_to_eth':
                    send_list.append(SwapMode(id=account.id, private_key=account.private_key, proxy=account.proxy, rpc='Mode').swap_to_eth())
                elif module[0] == 'Claim_airdrop':
                    send_listt, claimed_tokens = Claim_airdrop(id=account.id, private_key=account.private_key, proxy=account.proxy, rpc='Mode').claim()
                    send_list.append(send_listt)
                    all_tokens += claimed_tokens
                else:
                    send_list.append(globals()[module[0]](id=account.id, private_key=account.private_key, proxy=account.proxy, rpc="Mode").main())
        except Exception as e:
            logger.error(f'{idx}/{count_wallets} Failed: {str(e)}')
            sleeping_between_wallets()

        if bot_status == True:
            if account.id == count_wallets:
                send_list.append(f'\nSubscribe: https://t.me/CryptoMindYep')
            send_message(bot_token, bot_id, send_list)
            send_list.clear()

        if idx != count_wallets:
            sleeping_between_wallets()
            print()

    if all_tokens != 0:
        print()
        logger.info(f'All {all_tokens} MODE')
    outro()
main()