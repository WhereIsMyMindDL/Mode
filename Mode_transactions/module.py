from sys import stderr
import time
import json
from pyuseragents import random as random_ua
from requests import Session
import random
import ccxt
from loguru import logger
from hexbytes import HexBytes

from settings import count_swaps, amount, symbolWithdraw, network_okex, decimal_places, transfer_subaccount, API, slippage, swap_list, value_nitro_bridge, stay_eth
from help import Account, retry, sign_and_send_transaction, sleeping_between_transactions, SUCCESS, FAILED, get_tx_data_withABI, get_tx_data, get_min_to_amount


send_list = ''
tokens = {
        "ezETH": "0x2416092f143378750bb29b79ed961ab195cceea5",
        "USDC": "0xd988097fb8612cc24eec14542bc03424c656005f",
        "MODI": "0x598f9cb99bafc8346b4c153a61b3a27c8f13b10f",
        "MOLTEN": "0x66e535e8d2ebf13f49f3d49e5c50395a97c137b1",
        "SMD": "0xfda619b6d20975be80a10332cd39b9a4b0faa8bb",
        "USDT": "0xf0F161fDA2712DB8b566946122a5af183995e2eD",
        "ETH": "0x4200000000000000000000000000000000000006",
        "MODE": "0xDfc7C877a950e49D2610114102175A06C2e3167a",
    }
    
layerbank_abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"lToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"newBorrowCap","type":"uint256"}],"name":"BorrowCapUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"newCloseFactor","type":"uint256"}],"name":"CloseFactorUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"lToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"newCollateralFactor","type":"uint256"}],"name":"CollateralFactorUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"target","type":"address"},{"indexed":true,"internalType":"address","name":"initiator","type":"address"},{"indexed":true,"internalType":"address","name":"asset","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"premium","type":"uint256"}],"name":"FlashLoan","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newKeeper","type":"address"}],"name":"KeeperUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newLABDistributor","type":"address"}],"name":"LABDistributorUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newLeverager","type":"address"}],"name":"LeveragerUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"newLiquidationIncentive","type":"uint256"}],"name":"LiquidationIncentiveUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"lToken","type":"address"},{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"MarketEntered","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"lToken","type":"address"},{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"MarketExited","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"lToken","type":"address"}],"name":"MarketListed","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"address","name":"lToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"uAmount","type":"uint256"}],"name":"MarketRedeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"address","name":"lToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"uAmount","type":"uint256"}],"name":"MarketSupply","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newRebateDistributor","type":"address"}],"name":"RebateDistributorUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"lToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"newSupplyCap","type":"uint256"}],"name":"SupplyCapUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newValidator","type":"address"}],"name":"ValidatorUpdated","type":"event"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"accountLiquidityOf","outputs":[{"internalType":"uint256","name":"collateralInUSD","type":"uint256"},{"internalType":"uint256","name":"supplyInUSD","type":"uint256"},{"internalType":"uint256","name":"borrowInUSD","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"allMarkets","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"lToken","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"borrow","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"borrower","type":"address"},{"internalType":"address","name":"lToken","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"borrowBehalf","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"lToken","type":"address"}],"name":"checkMembership","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimLab","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"market","type":"address"}],"name":"claimLab","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"accounts","type":"address[]"}],"name":"claimLabBehalf","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"closeFactor","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"lockDuration","type":"uint256"}],"name":"compoundLab","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"lTokens","type":"address[]"}],"name":"enterMarkets","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"lToken","type":"address"}],"name":"exitMarket","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_priceCalculator","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"initialized","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"keeper","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"labDistributor","outputs":[{"internalType":"contract ILABDistributor","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"leverager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"lTokenBorrowed","type":"address"},{"internalType":"address","name":"lTokenCollateral","type":"address"},{"internalType":"address","name":"borrower","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"liquidateBorrow","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"liquidationIncentive","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address payable","name":"lToken","type":"address"},{"internalType":"uint256","name":"supplyCap","type":"uint256"},{"internalType":"uint256","name":"borrowCap","type":"uint256"},{"internalType":"uint256","name":"collateralFactor","type":"uint256"}],"name":"listMarket","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"lToken","type":"address"}],"name":"marketInfoOf","outputs":[{"components":[{"internalType":"bool","name":"isListed","type":"bool"},{"internalType":"uint256","name":"supplyCap","type":"uint256"},{"internalType":"uint256","name":"borrowCap","type":"uint256"},{"internalType":"uint256","name":"collateralFactor","type":"uint256"}],"internalType":"struct Constant.MarketInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"marketInfos","outputs":[{"internalType":"bool","name":"isListed","type":"bool"},{"internalType":"uint256","name":"supplyCap","type":"uint256"},{"internalType":"uint256","name":"borrowCap","type":"uint256"},{"internalType":"uint256","name":"collateralFactor","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"marketListOf","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"marketListOfUsers","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"markets","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"priceCalculator","outputs":[{"internalType":"contract IPriceCalculator","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rebateDistributor","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"lToken","type":"address"},{"internalType":"uint256","name":"lAmount","type":"uint256"}],"name":"redeemToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"lToken","type":"address"},{"internalType":"uint256","name":"uAmount","type":"uint256"}],"name":"redeemUnderlying","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"lToken","type":"address"}],"name":"removeMarket","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"lToken","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"repayBorrow","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newCloseFactor","type":"uint256"}],"name":"setCloseFactor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"lToken","type":"address"},{"internalType":"uint256","name":"newCollateralFactor","type":"uint256"}],"name":"setCollateralFactor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_keeper","type":"address"}],"name":"setKeeper","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_labDistributor","type":"address"}],"name":"setLABDistributor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_leverager","type":"address"}],"name":"setLeverager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newLiquidationIncentive","type":"uint256"}],"name":"setLiquidationIncentive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"lTokens","type":"address[]"},{"internalType":"uint256[]","name":"newBorrowCaps","type":"uint256[]"}],"name":"setMarketBorrowCaps","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"lTokens","type":"address[]"},{"internalType":"uint256[]","name":"newSupplyCaps","type":"uint256[]"}],"name":"setMarketSupplyCaps","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_priceCalculator","type":"address"}],"name":"setPriceCalculator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_rebateDistributor","type":"address"}],"name":"setRebateDistributor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_validator","type":"address"}],"name":"setValidator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"lToken","type":"address"},{"internalType":"uint256","name":"uAmount","type":"uint256"}],"name":"supply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"supplier","type":"address"},{"internalType":"address","name":"lToken","type":"address"},{"internalType":"uint256","name":"uAmount","type":"uint256"}],"name":"supplyBehalf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"address","name":"src","type":"address"},{"internalType":"address","name":"dst","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"usersOfMarket","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"validator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]')
ionic_abi = json.loads('[{"inputs":[{"internalType":"address","name":"underlying_","type":"address"},{"internalType":"contract IonicComptroller","name":"comptroller_","type":"address"},{"internalType":"address payable","name":"ionicAdmin_","type":"address"},{"internalType":"contract InterestRateModel","name":"interestRateModel_","type":"address"},{"internalType":"string","name":"name_","type":"string"},{"internalType":"string","name":"symbol_","type":"string"},{"internalType":"uint256","name":"reserveFactorMantissa_","type":"uint256"},{"internalType":"uint256","name":"adminFeeMantissa_","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"bytes4","name":"_functionSelector","type":"bytes4"},{"internalType":"address","name":"_currentImpl","type":"address"}],"name":"FunctionAlreadyAdded","type":"error"},{"inputs":[{"internalType":"bytes4","name":"_functionSelector","type":"bytes4"}],"name":"FunctionNotFound","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"cashPrior","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"interestAccumulated","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"borrowIndex","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalBorrows","type":"uint256"}],"name":"AccrueInterest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"borrower","type":"address"},{"indexed":false,"internalType":"uint256","name":"borrowAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accountBorrows","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalBorrows","type":"uint256"}],"name":"Borrow","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"liquidator","type":"address"},{"indexed":false,"internalType":"address","name":"borrower","type":"address"},{"indexed":false,"internalType":"uint256","name":"repayAmount","type":"uint256"},{"indexed":false,"internalType":"address","name":"cTokenCollateral","type":"address"},{"indexed":false,"internalType":"uint256","name":"seizeTokens","type":"uint256"}],"name":"LiquidateBorrow","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"minter","type":"address"},{"indexed":false,"internalType":"uint256","name":"mintAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"mintTokens","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"oldAdminFeeMantissa","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newAdminFeeMantissa","type":"uint256"}],"name":"NewAdminFee","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"oldImplementation","type":"address"},{"indexed":false,"internalType":"address","name":"newImplementation","type":"address"}],"name":"NewImplementation","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"oldIonicFeeMantissa","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newIonicFeeMantissa","type":"uint256"}],"name":"NewIonicFee","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"contract InterestRateModel","name":"oldInterestRateModel","type":"address"},{"indexed":false,"internalType":"contract InterestRateModel","name":"newInterestRateModel","type":"address"}],"name":"NewMarketInterestRateModel","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"oldReserveFactorMantissa","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newReserveFactorMantissa","type":"uint256"}],"name":"NewReserveFactor","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"redeemer","type":"address"},{"indexed":false,"internalType":"uint256","name":"redeemAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"redeemTokens","type":"uint256"}],"name":"Redeem","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"payer","type":"address"},{"indexed":false,"internalType":"address","name":"borrower","type":"address"},{"indexed":false,"internalType":"uint256","name":"repayAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accountBorrows","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"totalBorrows","type":"uint256"}],"name":"RepayBorrow","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"benefactor","type":"address"},{"indexed":false,"internalType":"uint256","name":"addAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newTotalReserves","type":"uint256"}],"name":"ReservesAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"admin","type":"address"},{"indexed":false,"internalType":"uint256","name":"reduceAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newTotalReserves","type":"uint256"}],"name":"ReservesReduced","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Transfer","type":"event"},{"stateMutability":"nonpayable","type":"fallback"},{"inputs":[],"name":"_listExtensions","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract DiamondExtension","name":"extensionToAdd","type":"address"},{"internalType":"contract DiamondExtension","name":"extensionToReplace","type":"address"}],"name":"_registerExtension","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"implementation_","type":"address"},{"internalType":"bytes","name":"becomeImplementationData","type":"bytes"}],"name":"_setImplementationSafe","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"_upgrade","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"accrualBlockNumber","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"adminFeeMantissa","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"borrowIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"comptroller","outputs":[{"internalType":"contract IonicComptroller","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feeSeizeShareMantissa","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"interestRateModel","outputs":[{"internalType":"contract InterestRateModel","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ionicAdmin","outputs":[{"internalType":"address payable","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ionicFeeMantissa","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"protocolSeizeShareMantissa","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"reserveFactorMantissa","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalAdminFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalBorrows","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalIonicFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalReserves","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"underlying","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]')
swapmode_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]')
supswap_router_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_factoryV2","type":"address"},{"internalType":"address","name":"_deployer","type":"address"},{"internalType":"address","name":"_factoryV3","type":"address"},{"internalType":"address","name":"_positionManager","type":"address"},{"internalType":"address","name":"_stableFactory","type":"address"},{"internalType":"address","name":"_stableInfo","type":"address"},{"internalType":"address","name":"_WETH9","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"factory","type":"address"},{"indexed":true,"internalType":"address","name":"info","type":"address"}],"name":"SetStableSwap","type":"event"},{"inputs":[],"name":"WETH9","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"approveMax","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"approveMaxMinusOne","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"approveZeroThenMax","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"approveZeroThenMaxMinusOne","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes","name":"data","type":"bytes"}],"name":"callPositionManager","outputs":[{"internalType":"bytes","name":"result","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"paths","type":"bytes[]"},{"internalType":"uint128[]","name":"amounts","type":"uint128[]"},{"internalType":"uint24","name":"maximumTickDivergence","type":"uint24"},{"internalType":"uint32","name":"secondsAgo","type":"uint32"}],"name":"checkOracleSlippage","outputs":[],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"uint24","name":"maximumTickDivergence","type":"uint24"},{"internalType":"uint32","name":"secondsAgo","type":"uint32"}],"name":"checkOracleSlippage","outputs":[],"stateMutability":"view","type":"function"},{"inputs":[],"name":"deployer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"}],"internalType":"struct IV3SwapRouter.ExactInputParams","name":"params","type":"tuple"}],"name":"exactInput","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct IV3SwapRouter.ExactInputSingleParams","name":"params","type":"tuple"}],"name":"exactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"uint256[]","name":"flag","type":"uint256[]"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"}],"name":"exactInputStableSwap","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"}],"internalType":"struct IV3SwapRouter.ExactOutputParams","name":"params","type":"tuple"}],"name":"exactOutput","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct IV3SwapRouter.ExactOutputSingleParams","name":"params","type":"tuple"}],"name":"exactOutputSingle","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"uint256[]","name":"flag","type":"uint256[]"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address","name":"to","type":"address"}],"name":"exactOutputStableSwap","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"factoryV2","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getApprovalType","outputs":[{"internalType":"enum IApproveAndCall.ApprovalType","name":"","type":"uint8"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256","name":"amount1Min","type":"uint256"}],"internalType":"struct IApproveAndCall.IncreaseLiquidityParams","name":"params","type":"tuple"}],"name":"increaseLiquidity","outputs":[{"internalType":"bytes","name":"result","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256","name":"amount1Min","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"internalType":"struct IApproveAndCall.MintParams","name":"params","type":"tuple"}],"name":"mint","outputs":[{"internalType":"bytes","name":"result","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"previousBlockhash","type":"bytes32"},{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"positionManager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"pull","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"refundETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowed","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowedIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_info","type":"address"}],"name":"setStableSwap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stableSwapFactory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stableSwapInfo","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int256","name":"amount0Delta","type":"int256"},{"internalType":"int256","name":"amount1Delta","type":"int256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"supV3SwapCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"sweepToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"}],"name":"sweepToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"sweepTokenWithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"sweepTokenWithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"unwrapWETH9","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"unwrapWETH9WithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"unwrapWETH9WithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"wrapETH","outputs":[],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]')
kimswap_router_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WNativeToken","type":"address"},{"internalType":"address","name":"_poolDeployer","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WNativeToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"int256","name":"amount0Delta","type":"int256"},{"internalType":"int256","name":"amount1Delta","type":"int256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"algebraSwapCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"}],"internalType":"struct ISwapRouter.ExactInputParams","name":"params","type":"tuple"}],"name":"exactInput","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},{"internalType":"uint160","name":"limitSqrtPrice","type":"uint160"}],"internalType":"struct ISwapRouter.ExactInputSingleParams","name":"params","type":"tuple"}],"name":"exactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},{"internalType":"uint160","name":"limitSqrtPrice","type":"uint160"}],"internalType":"struct ISwapRouter.ExactInputSingleParams","name":"params","type":"tuple"}],"name":"exactInputSingleSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"}],"internalType":"struct ISwapRouter.ExactOutputParams","name":"params","type":"tuple"}],"name":"exactOutput","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"},{"internalType":"uint160","name":"limitSqrtPrice","type":"uint160"}],"internalType":"struct ISwapRouter.ExactOutputSingleParams","name":"params","type":"tuple"}],"name":"exactOutputSingle","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"poolDeployer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"refundNativeToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowed","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowedIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"sweepToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"sweepTokenWithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"unwrapWNativeToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"unwrapWNativeTokenWithFee","outputs":[],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]')

switch_cex = "okx"
proxy_server = ""
proxies = {
  "http": proxy_server,
  "https": proxy_server,
}

class Claim_airdrop(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.session = Session()
        self.session.headers['user-agent'] = random_ua()
        self.proxy = proxy
        if self.proxy != None:
            self.session.proxies.update({'http': self.proxy})

    @retry
    def claim(self):
        global send_list
        send_list = ''
        try:
            response = self.session.get(
                f'https://airdrop-data-mode.s3.us-west-2.amazonaws.com/{self.address}/0xe97bf25e34841f4cfad6bfd0212b3fe420e796da44e16ffee089ca33e48fd44e-{self.address}.json',
            ).json()
            if response['claimed']:
                logger.success(f'\n{SUCCESS}ClaimAirdrop: дроп уже заклеймлен...')
                return f'ClaimAirdrop: дроп уже заклеймлен...', 0
        except:
            logger.info(f'\n{SUCCESS}ClaimAirdrop: дроп уже заклеймлен...')
            return f'ClaimAirdrop: нотэллигбл бро...', 0

        available_claim = int(response['events'][0]['awardAmount'])
        available_claim_in_eth = available_claim / 10**18
        data_proofs = ''
        for data in response['events'][0]['proofs']:
            data_proofs += data[2:]
        data = (f'0x8132b32100000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000{self.address[2:]}0000000000000000000000000000000000000000000000000000000000000001{hex(int(available_claim))[2:].zfill(64)}0000000000000000000000000000000000000000000000000000000000000001{hex(int(available_claim))[2:].zfill(64)}000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000663a0d3400000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000012'
                f'{data_proofs}')


        tx_data = get_tx_data(self, to='0x042E609B2D5Aa6E815a44872131D8bbC6EdCeb55', value=0, data=data)

        logger.info(f'ClaimAirdrop: try claim {"{:0.2f}".format(available_claim_in_eth)} MODE')
        txstatus, tx_hash = sign_and_send_transaction(self, tx_data)

        if txstatus == 1:
            logger.success(f'ClaimAirdrop: claim {"{:0.2f}".format(available_claim_in_eth)} MODE : {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}ClaimAirdrop: claim {"{:0.2f}".format(available_claim_in_eth)} MODE - [tx hash]({self.scan + tx_hash})')
            return send_list, float("{:0.2f}".format(available_claim_in_eth))

        else:
            logger.error(f'ClaimAirdrop: claim {"{:0.2f}".format(available_claim_in_eth)} MODE : {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}ClaimAirdrop: claim {"{:0.2f}".format(available_claim_in_eth)} MODE - [tx hash]({self.scan + tx_hash})')
            return send_list, float("{:0.2f}".format(available_claim_in_eth))

class LayerBank(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.contract = self.get_contract(contract_address=self.w3.to_checksum_address("0x80980869D90A737aff47aBA6FbaA923012C1FF50"), abi=layerbank_abi)

    @retry
    def supply(self):
            global send_list

            balance_eth, balance_wei = self.get_value()
            tx_data = get_tx_data_withABI(self, balance_wei)
            transaction = self.contract.functions.supply(self.w3.to_checksum_address('0xe855b8018c22a05f84724e93693caf166912add5'), balance_wei).build_transaction(tx_data)

            logger.info(f'LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH')
            txstatus, tx_hash = sign_and_send_transaction(self, transaction)

            if txstatus == 1:
                logger.success(f'LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH : {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH - [tx hash]({self.scan + tx_hash})')

            else:
                logger.error(f'LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH : {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH - failed')


    @retry
    def collateral(self):
        global send_list
        tx_data = get_tx_data_withABI(self)
        transaction = self.contract.functions.enterMarkets([self.w3.to_checksum_address('0xe855b8018c22a05f84724e93693caf166912add5')]).build_transaction(tx_data)
        logger.info(f'LayerBank: Try enable collateral...')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)
        if txstatus == 1:
            logger.success(f'LayerBank: Collateral enable : {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}LayerBank: Collateral enable - [tx hash]({self.scan + tx_hash})')
            return True

        else:
            logger.error(f'LayerBank: Collateral enable : {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}LayerBank: Collateral enable - failed')

    def main(self):
        global send_list
        send_list = ''
        LayerBank.supply(self)
        sleeping_between_transactions()
        LayerBank.collateral(self)
        sleeping_between_transactions()

        return send_list

class SwapMode(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.contract = self.get_contract(contract_address=self.w3.to_checksum_address("0xc1e624C810D297FD70eF53B0E08F44FABE468591"), abi=swapmode_abi)

    @retry
    def swap_from_eth(self):
        global send_list
        token = random.choice(list(tokens))

        balance_eth, balance_wei = self.get_value()
        tx_data = get_tx_data_withABI(self, balance_wei)
        deadline = int(time.time() + 10000)

        transaction = self.contract.functions.swapExactETHForTokens(0, [self.w3.to_checksum_address('0x4200000000000000000000000000000000000006'), self.w3.to_checksum_address(tokens[token])], self.address, deadline).build_transaction(tx_data)
        logger.info(f'SwapMode: Swap {"{:0.9f}".format(balance_eth)} ETH to {token}')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)

        if txstatus == 1:
            logger.success(f'SwapMode: Swap {"{:0.9f}".format(balance_eth)} ETH to {token}: {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}SwapMode: Swap {"{:0.9f}".format(balance_eth)} ETH to {token} - [tx hash]({self.scan + tx_hash})')
            SwapMode.swap_from_token_to_eth(self, token)

        else:
            logger.error(f'SwapMode: Swap {"{:0.9f}".format(balance_eth)} ETH to {token}: {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}SwapMode: Swap {"{:0.9f}".format(balance_eth)} ETH to {token} - failed')

    @retry
    def swap_from_token_to_eth(self, token):
        global send_list
        send_list = ''


        balance = self.get_balance(tokens[token])
        balance_wei = balance['balance_wei']
        balance_eth = balance['balance']

        if self.check_allowance(tokens[token], '0xc1e624c810d297fd70ef53b0e08f44fabe468591') < balance_wei:
            logger.info(f'SwapMode: try approve token {token}...')
            send_list += self.approve(balance_wei, tokens[token], '0xc1e624c810d297fd70ef53b0e08f44fabe468591')
            sleeping_between_transactions()

        tx_data = get_tx_data_withABI(self)
        deadline = int(time.time() + 10000)

        transaction = self.contract.functions.swapExactTokensForETH(balance_wei, 0, [self.w3.to_checksum_address(tokens[token]), self.w3.to_checksum_address('0x4200000000000000000000000000000000000006')], self.address, deadline).build_transaction(tx_data)
        logger.info(f'SwapMode: Swap {"{:0.9f}".format(balance_eth)} {token} to ETH')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)

        if txstatus == 1:
            logger.success(f'SwapMode: Swap {"{:0.9f}".format(balance_eth)} {token} to ETH: {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}SwapMode: Swap {"{:0.9f}".format(balance_eth)} {token} to ETH - [tx hash]({self.scan + tx_hash})')


        else:
            logger.error(f'SwapMode: Swap {"{:0.9f}".format(balance_eth)} {token} to ETH: {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}SwapMode: Swap {"{:0.9f}".format(balance_eth)} {token} to ETH - failed')


    @retry
    def swap_to_eth(self):
        global send_list
        send_list = ''
        random.shuffle(swap_list)
        for token in swap_list:
            balance = self.get_balance(tokens[token])
            balance_wei = balance['balance_wei']
            balance_eth = balance['balance']
            if balance_wei == 0:
                logger.info(f'0 {token} на аккаунте...')
                continue

            if self.check_allowance(tokens[token], '0xc1e624c810d297fd70ef53b0e08f44fabe468591') < balance_wei:
                logger.info(f'SwapMode: try approve token {token}...')
                send_list += self.approve(balance_wei, tokens[token], '0xc1e624c810d297fd70ef53b0e08f44fabe468591')
                sleeping_between_transactions()

            tx_data = get_tx_data_withABI(self)
            deadline = int(time.time() + 10000)

            transaction = self.contract.functions.swapExactTokensForETH(balance_wei, 0, [self.w3.to_checksum_address(tokens[token]), self.w3.to_checksum_address('0x4200000000000000000000000000000000000006')], self.address, deadline).build_transaction(tx_data)
            logger.info(f'SwapMode: Swap {"{:0.9f}".format(balance_eth)} {token} to ETH')
            txstatus, tx_hash = sign_and_send_transaction(self, transaction)

            if txstatus == 1:
                logger.success(f'SwapMode: Swap {"{:0.9f}".format(balance_eth)} {token} to ETH: {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}SwapMode: Swap {"{:0.9f}".format(balance_eth)} {token} to ETH - [tx hash]({self.scan + tx_hash})')
                sleeping_between_transactions()

            else:
                logger.error(f'SwapMode: Swap {"{:0.9f}".format(balance_eth)} {token} to ETH: {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}SwapMode: Swap {"{:0.9f}".format(balance_eth)} {token} to ETH - failed')
        return send_list

    def main(self):
        global send_list
        send_list = ''
        count_swap = random.randint(count_swaps[0], count_swaps[1])
        for i in range(count_swap):
            SwapMode.swap_from_eth(self)
            sleeping_between_transactions()
        return send_list

class IONIC(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)

    @retry
    def wrap(self):
            global send_list

            balance_eth, balance_wei = self.get_value()
            tx_data = get_tx_data(self, value=balance_wei, data='0xd0e30db0', to='0x4200000000000000000000000000000000000006')

            logger.info(f'IONIC: Wrap {"{:0.9f}".format(balance_eth)} ETH')
            txstatus, tx_hash = sign_and_send_transaction(self, tx_data)

            if txstatus == 1:
                logger.success(f'IONIC: Wrap {"{:0.9f}".format(balance_eth)} ETH: {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}IONIC: Wrap {"{:0.9f}".format(balance_eth)} ETH - [tx hash]({self.scan + tx_hash})')

            else:
                logger.error(f'IONIC: Wrap {"{:0.9f}".format(balance_eth)} ETH: {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}IONIC: Wrap {"{:0.9f}".format(balance_eth)} ETH - [tx hash]({self.scan + tx_hash})')

    @retry
    def approve_and_supply(self):
            global send_list

            if self.check_allowance('0x4200000000000000000000000000000000000006', '0x71ef7eda2be775e5a7aa8afd02c45f059833e9d2') < 10:
                logger.info(f'IONIC: try approve token WETH...')
                send_list += self.approve(115792089237316195423570985008687907853269984665640564039457584007913129639935, '0x4200000000000000000000000000000000000006', '0x71ef7eda2be775e5a7aa8afd02c45f059833e9d2')
                sleeping_between_transactions()

            balance = self.get_balance(contract_address='0x4200000000000000000000000000000000000006')
            balance_wei = balance['balance_wei']
            balance_eth = balance['balance']
            data = '0xa0712d68' + self.w3.to_bytes(int(balance_wei)).hex().zfill(64)
            tx_data = get_tx_data(self, to='0x71ef7EDa2Be775E5A7aa8afD02C45F059833e9d2', data=data)

            logger.info(f'IONIC: Supply {"{:0.9f}".format(balance_eth)} WETH')
            txstatus, tx_hash = sign_and_send_transaction(self, tx_data)

            if txstatus == 1:
                logger.success(f'IONIC: Supply {"{:0.9f}".format(balance_eth)} WETH : {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}IONIC: Supply {"{:0.9f}".format(balance_eth)} WETH - [tx hash]({self.scan + tx_hash})')

            else:
                logger.error(f'IONIC: Supply {"{:0.9f}".format(balance_eth)} WETH : {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}IONIC: Supply {"{:0.9f}".format(balance_eth)} WETH - [tx hash]({self.scan + tx_hash})')


    def main(self):
        global send_list
        send_list = ''
        IONIC.wrap(self)
        sleeping_between_transactions()
        IONIC.approve_and_supply(self)
        sleeping_between_transactions()

        return send_list

class Ironclad(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)

    @retry
    def supply(self):
            global send_list

            balance_eth, balance_wei = self.get_value()
            tx_data = get_tx_data(self, value=balance_wei, data=f'0x474cf53d000000000000000000000000b702ce183b4e1faa574834715e5d4a6378d0eed3000000000000000000000000{self.address[2:]}0000000000000000000000000000000000000000000000000000000000000000', to='0x6387c7193B5563DD17d659b9398ACd7b03FF0080')

            logger.info(f'Ironclad: DepositETH {"{:0.9f}".format(balance_eth)} ETH')
            txstatus, tx_hash = sign_and_send_transaction(self, tx_data)

            if txstatus == 1:
                logger.success(f'Ironclad: DepositET {"{:0.9f}".format(balance_eth)} ETH: {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}Ironclad: DepositET {"{:0.9f}".format(balance_eth)} ETH - [tx hash]({self.scan + tx_hash})')

            else:
                logger.error(f'Ironclad: DepositET {"{:0.9f}".format(balance_eth)} ETH: {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}Ironclad: DepositET {"{:0.9f}".format(balance_eth)} ETH - [tx hash]({self.scan + tx_hash})')

    @retry
    def borrow(self):
        global send_list

        data = {
            'USDC': ['0xd988097fb8612cc24eec14542bc03424c656005f', random.randint(1000, 5000)],
            'USDT': ['0x8903dc1f4736d2fcb90c1497aebbaba133daac76', random.randint(100, 500)]
        }

        token = random.choice(list(data))
        borrow_value = data[token][1]

        tx_data = get_tx_data(self, value=0,
                              data=f'0xa415bcad000000000000000000000000d988097fb8612cc24eec14542bc03424c656005f000000000000000000000000000000000000000000000000000000000000{self.w3.to_bytes(int(borrow_value)).hex()}00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000{self.address[2:]}',
                              to='0xB702cE183b4E1Faa574834715E5D4a6378D0eEd3')

        balance_eth = borrow_value / 1000000

        logger.info(f'Ironclad: Borrow {"{:0.9f}".format(balance_eth)} {token} ETH')
        txstatus, tx_hash = sign_and_send_transaction(self, tx_data)

        if txstatus == 1:
            logger.success(f'Ironclad: Borrow {"{:0.9f}".format(balance_eth)} {token}: {self.scan + tx_hash}')
            send_list += (
                f'\n{SUCCESS}Ironclad: Borrow {"{:0.9f}".format(balance_eth)} {token} - [tx hash]({self.scan + tx_hash})')

        else:
            logger.error(f'Ironclad: Borrow {"{:0.9f}".format(balance_eth)} {token}: {self.scan + tx_hash}')
            send_list += (
                f'\n{FAILED}Ironclad: Borrow {"{:0.9f}".format(balance_eth)} {token} - [tx hash]({self.scan + tx_hash})')

    def main(self):
        global send_list
        send_list = ''
        Ironclad.supply(self)
        sleeping_between_transactions()
        Ironclad.borrow(self)
        sleeping_between_transactions()
        return send_list

class Nitro(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.session = Session()
        self.session.headers['user-agent'] = random_ua()
        self.proxy = proxy
        if self.proxy != None:
            self.session.proxies.update({'http': self.proxy, 'https': self.proxy})
        else:
            logger.warning('You are not using proxy')

    @retry
    def get_transaction_data(self, toChain):
        global send_list

        if type(value_nitro_bridge[0]) == str:
            percent = round(random.uniform(float(value_nitro_bridge[0]), float(value_nitro_bridge[1])), decimal_places) / 100
            balance = self.get_balance()
            value_eth = balance['balance'] * percent
            value_wei = int(balance['balance_wei'] * percent)
        else:
            value_eth = round(random.uniform(float(value_nitro_bridge[0]), float(value_nitro_bridge[1])), decimal_places)
            value_wei = self.w3.to_wei(value_eth, 'ether')

        url = "https://api-beta.pathfinder.routerprotocol.com/api/v2/quote"
        chain_ids = {
            "Ethereum": "1",
            "Arbitrum": "42161",
            "Optimism": "10",
            "zkSync": "324",
            "Scroll": "534352",
            "Base": "8453",
            "Linea": "59144",
            "Mode": "34443",
        }

        params = {
            "fromTokenAddress": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
            "toTokenAddress": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
            "amount": value_wei,
            "fromTokenChainId": self.w3.eth.chain_id,
            "toTokenChainId": chain_ids[toChain],
            "partnerId": 1,
        }

        transaction_data = self.session.get(url='https://api-beta.pathfinder.routerprotocol.com/api/v2/quote', params=params).json()
        transaction_data.update({"senderAddress": self.address, "receiverAddress": self.address})

        url = "https://api-beta.pathfinder.routerprotocol.com/api/v2/transaction"

        response = self.session.post(url=url, json=transaction_data)

        transaction_data = response.json()
        # print(transaction_data)

        tx_data = get_tx_data(self, to=transaction_data["txn"]["to"], value=int(transaction_data["txn"]["value"], 16),
                              data=transaction_data["txn"]["data"])

        balance_eth = self.w3.from_wei(tx_data['value'], 'ether')
        logger.info(f'Nitro: Bridge {"{:0.9f}".format(balance_eth)} ETH from Base to Mode')
        txstatus, tx_hash = sign_and_send_transaction(self, tx_data)

        if txstatus == 1:
            logger.success(f'Nitro: Bridge {"{:0.9f}".format(balance_eth)} ETH from {self.ChainName} to {toChain} : {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}Nitro: Bridge {"{:0.4f}".format(balance_eth)} ETH lfrom {self.ChainName} to {toChain} - [tx hash]({self.scan + tx_hash})')
            self.wait_balance(tx_data['value'], toChain)
            return send_list

        else:
            logger.error(f'Nitro: Bridge {"{:0.9f}".format(balance_eth)} ETH from {self.ChainName} to {toChain} : {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}Nitro: Bridge {"{:0.4f}".format(balance_eth)} ETH from {self.ChainName} to {toChain} - [tx hash]({self.scan + tx_hash})')


    def main(self, toChain):
        global send_list
        send_list = ''
        Nitro.get_transaction_data(self, toChain)
        return send_list

class SupSwap(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.router_contract = self.get_contract(contract_address=self.w3.to_checksum_address("0x016e131C05fb007b5ab286A6D614A5dab99BD415"), abi=supswap_router_abi)

    @retry
    def swap(self):
            global send_list
            from_token_name = "ETH"
            from_token_address = tokens[from_token_name]
            to_token_name = random.choice(["USDC", "USDT"])
            to_token_address = tokens[to_token_name]
            balance_eth, balance_wei = self.get_value()
            min_amount = (float(balance_eth) / get_min_to_amount(from_token_name, to_token_name) * (1 - slippage / 100))
            min_amount_wei = int(min_amount * 10 ** self.get_decimals(to_token_address))
            data = (f'0x04e45aaf'
                    f'{from_token_address[2:].zfill(64)}'
                    f'{to_token_address[2:].zfill(64)}'
                    f'00000000000000000000000000000000000000000000000000000000000001f4'
                    f'{self.address[2:].lower().zfill(64)}'
                    f'{hex(balance_wei)[2:].zfill(64)}'
                    f'{hex(min_amount_wei)[2:].zfill(64)}'
                    f'0000000000000000000000000000000000000000000000000000000000000000')
            '''
            0xeea0d7b2
            000000000000000000000000000000000000000000000000000000000000000a
            000000000000000000000000eeeba9ab3668c2c8e3bdebf618a7eb985c6add76
            000000000000000000000000000000000000000000000000000a7c26d530e0bc value
            00000000000000000000000000000000000000000000000000004be3f502d5d3 fee
            000000000000000000000000000000000000000000000000000a1fc3cd8c46dc amount_out
            00000000000000000000000000000000000000000000000000000000663ffd45 
            000000000000000000000000000000000000000000000000000a205472344cb4 amount - fee
            00000000000000000000000000000000000000000000000000000000663ffd45 
            
            0xeea0d7b2
            000000000000000000000000000000000000000000000000000000000000000a
            000000000000000000000000677e93ec82ca00329cb525f9fbd88807020972d4
            000000000000000000000000000000000000000000000000000d2c4325789d13
            00000000000000000000000000000000000000000000000000004be821fc429b fee
            000000000000000000000000000000000000000000000000000ccba0ea593961
            00000000000000000000000000000000000000000000000000000000663ffebf
            000000000000000000000000000000000000000000000000000ccc56b4a322da
            00000000000000000000000000000000000000000000000000000000663ffebf
            '''

            deadline = int(time.time() + 10000)
            tx_data = get_tx_data_withABI(self, value=balance_wei)
            transaction = self.router_contract.functions.multicall(deadline, [HexBytes(data[2:])]).build_transaction(tx_data)

            logger.info(f'SupSwap: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.9f}".format(min_amount)} {to_token_name}')
            txstatus, tx_hash = sign_and_send_transaction(self, transaction)

            if txstatus == 1:
                logger.success(f'SupSwap: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.9f}".format(min_amount)} {to_token_name}: {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}SupSwap: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.9f}".format(min_amount)} {to_token_name} - [tx hash]({self.scan + tx_hash})')
                return to_token_name

            else:
                logger.error(f'SupSwap: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.9f}".format(min_amount)} {to_token_name}: {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}SupSwap: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.9f}".format(min_amount)} {to_token_name} - [tx hash]({self.scan + tx_hash})')

    @retry
    def swap_to_eth(self, from_token_name):
            global send_list
            to_token_name = "ETH"
            from_token_address = tokens[from_token_name]
            to_token_address = tokens[to_token_name]

            balance = self.get_balance(tokens[from_token_name])
            balance_wei = balance['balance_wei']
            balance_eth = balance['balance']
            min_amount = (float(balance_eth) / get_min_to_amount(from_token_name, to_token_name) * (1 - slippage / 100))
            min_amount_wei = int(min_amount * 10 ** self.get_decimals(to_token_address))
            if self.check_allowance(tokens[from_token_name], '0x016e131C05fb007b5ab286A6D614A5dab99BD415') < balance_wei:
                logger.info(f'SupSwap: try approve token {from_token_name}...')
                send_list += self.approve(balance_wei, tokens[from_token_name], '0x016e131C05fb007b5ab286A6D614A5dab99BD415')
                sleeping_between_transactions()

            deadline = int(time.time() + 10000)
            data = (f'0x04e45aaf'
                    f'{from_token_address[2:].zfill(64)}'
                    f'{to_token_address[2:].zfill(64)}'
                    f'00000000000000000000000000000000000000000000000000000000000001f4'
                    f'0000000000000000000000000000000000000000000000000000000000000002'
                    f'{hex(balance_wei)[2:].zfill(64)}'
                    f'{hex(min_amount_wei)[2:].zfill(64)}'
                    f'0000000000000000000000000000000000000000000000000000000000000000')
            data2 = (f'0x49404b7c'
                     f'{hex(min_amount_wei)[2:].zfill(64)}'
                     f'{self.address[2:].zfill(64)}')
            '''
            0x88316456
            0000000000000000000000004200000000000000000000000000000000000006
            000000000000000000000000d988097fb8612cc24eec14542bc03424c656005f
            00000000000000000000000000000000000000000000000000000000000001f4
            fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd009e
            fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd00b2
            0000000000000000000000000000000000000000000000000000037438bfc8b9
            00000000000000000000000000000000000000000000000000000000000052cb
            0000000000000000000000000000000000000000000000000000000000000000
            0000000000000000000000000000000000000000000000000000000000000000
            000000000000000000000000eeeba9ab3668c2c8e3bdebf618a7eb985c6add76
            000000000000000000000000000000000000000000000000000000006632bc7f
            0x12210e8a
            
            0x88316456
            0000000000000000000000004200000000000000000000000000000000000006
            000000000000000000000000d988097fb8612cc24eec14542bc03424c656005f
            00000000000000000000000000000000000000000000000000000000000001f4
            fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd00b2
            fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd00c6
            00000000000000000000000000000000000000000000000000000dbfe4fe847f
            0000000000000000000000000000000000000000000000000000000000007530
            0000000000000000000000000000000000000000000000000000000000000000
            0000000000000000000000000000000000000000000000000000000000000000
            000000000000000000000000eeeba9ab3668c2c8e3bdebf618a7eb985c6add76
            000000000000000000000000000000000000000000000000000000006632bec1
            0x12210e8a
            '''

            tx_data = get_tx_data_withABI(self, value=0)
            transaction = self.router_contract.functions.multicall(deadline, [HexBytes(data[2:]), HexBytes(data2[2:])]).build_transaction(tx_data)

            logger.info(f'SupSwap: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.9f}".format(min_amount)} {to_token_name}')
            txstatus, tx_hash = sign_and_send_transaction(self, transaction)

            if txstatus == 1:
                logger.success(f'SupSwap: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.9f}".format(min_amount)} {to_token_name}: {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}SupSwap: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.9f}".format(min_amount)} {to_token_name} - [tx hash]({self.scan + tx_hash})')

            else:
                logger.error(f'SupSwap: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {to_token_name}: {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}SupSwap: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.9f}".format(min_amount)} {to_token_name} - [tx hash]({self.scan + tx_hash})')

    def main(self):
        global send_list
        send_list = ''
        count_swap = random.randint(count_swaps[0], count_swaps[1])
        for i in range(count_swap):
            to_token_name = SupSwap.swap(self)
            sleeping_between_transactions()
            SupSwap.swap_to_eth(self, to_token_name)
            sleeping_between_transactions()
        return send_list

class KimExchange(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.router_contract = self.get_contract(contract_address=self.w3.to_checksum_address("0xAc48FcF1049668B285f3dC72483DF5Ae2162f7e8"), abi=supswap_router_abi)

    @retry
    def swap(self):
            global send_list
            from_token_name = "ETH"
            from_token_address = tokens[from_token_name]
            to_token_name = random.choice(["USDC", "USDT"])
            to_token_address = tokens[to_token_name]
            balance_eth, balance_wei = self.get_value()
            min_amount = ((get_min_to_amount(from_token_name, to_token_name) * float(balance_eth)) * (1 - slippage / 100))

            min_amount_wei = int(min_amount * 10 ** self.get_decimals(to_token_address))

            deadline = int(time.time() + 10000)
            data = (f'0xbc651188'
                    f'{from_token_address[2:].zfill(64)}'
                    f'{to_token_address[2:].zfill(64)}'
                    f'{self.address[2:].lower().zfill(64)}'
                    f'{hex(deadline)[2:].zfill(64)}'
                    f'{hex(balance_wei)[2:].zfill(64)}'
                    f'{hex(min_amount_wei)[2:].zfill(64)}'
                    f'0000000000000000000000000000000000000000000000000000000000000000')
            '''
            0x9cc1a283
            0000000000000000000000004200000000000000000000000000000000000006
            000000000000000000000000f0f161fda2712db8b566946122a5af183995e2ed
            fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd006c
            fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd00a8
            0000000000000000000000000000000000000000000000000000000000000000
            0000000000000000000000000000000000000000000000000000000000007530
            0000000000000000000000000000000000000000000000000000000000000000
            0000000000000000000000000000000000000000000000000000000000007530
            000000000000000000000000eeeba9ab3668c2c8e3bdebf618a7eb985c6add76
            0000000000000000000000000000000000000000000000000000018f362edd11
            
            0xb9303701
            00000000000000000000000000000000000000000000000000000000000000c0
            0000000000000000000000000000000000000000000000000000018f389ba06f
            0000000000000000000000000000000000000000000000000000000000000340
            00000000000000000000000000000000000000000000000000000000000012f2
            0000000000000000000000000000000000000000000000000000000000000360
            0000000000000000000000000000000000000000000000000000000000000380
            0000000000000000000000000000000000000000000000000000000000000000
            0000000000000000000000000000000000000000000000000004162d3c5d54b0
            0000000000000000000000000000000000000000000000000000000000000160
            00000000000000000000000000000000000000000000000000038ca86df4cd40
            0000000000000000000000000000000000000000000000000000000000002105
            00000000000000000000000000000000000000000000000000000000000001a0
            000000000000000000000000eeeba9ab3668c2c8e3bdebf618a7eb985c6add76
            00000000000000000000000000000000000000000000000000000000000001e0
            0000000000000000000000000000000000000000000000000000000000000220
            0000000000000000000000000000000000000000000000000000000000000240
            0000000000000000000000000000000000000000000000000000000000000260
            0000000000000000000000000000000000000000000000000000000000000014
            0000000000000000000000000000000000000000000000000000000000000000
            0000000000000000000000000000000000000000000000000000000000000014
            eeeba9ab3668c2c8e3bdebf618a7eb985c6add76000000000000000000000000
            0000000000000000000000000000000000000000000000000000000000000014
            eeeba9ab3668c2c8e3bdebf618a7eb985c6add76000000000000000000000000
            0000000000000000000000000000000000000000000000000000000000000000
            0000000000000000000000000000000000000000000000000000000000000000
            0000000000000000000000000000000000000000000000000000000000000000
            0000000000000000000000000000000000000000000000000000000000000000
            0000000000000000000000000000000000000000000000000000000000000000
            0000000000000000000000000000000000000000000000000000000000000041
            0101010000b0d49697ae88000000000000000000000000000040cdf46da88c03
            0000000000000000000000000000000000000000000000000000000000000000
            0000000000000000000000000000000000000000000000000000000000000000
            '''
            tx_data = get_tx_data_withABI(self, value=balance_wei)
            transaction = self.router_contract.functions.multicall([HexBytes(data[2:])]).build_transaction(tx_data)

            logger.info(f'KimExchange: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.4f}".format(min_amount)} {to_token_name}')
            txstatus, tx_hash = sign_and_send_transaction(self, transaction)

            if txstatus == 1:
                logger.success(f'KimExchange: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.4f}".format(min_amount)} {to_token_name}: {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}KimExchange: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {min_amount} {to_token_name} - [tx hash]({self.scan + tx_hash})')
                return to_token_name

            else:
                logger.error(f'KimExchange: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.4f}".format(min_amount)} {to_token_name}: {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}KimExchange: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.4f}".format(min_amount)} {to_token_name} - [tx hash]({self.scan + tx_hash})')

    @retry
    def swap_to_eth(self, from_token_name):
            global send_list
            to_token_name = "ETH"
            from_token_address = tokens[from_token_name]
            to_token_address = tokens[to_token_name]

            balance = self.get_balance(tokens[from_token_name])
            balance_wei = balance['balance_wei']
            balance_eth = balance['balance']

            min_amount = (float(balance_eth) / get_min_to_amount(from_token_name, to_token_name) * (1 - slippage / 100))
            min_amount_wei = int(min_amount * 10 ** self.get_decimals(to_token_address))

            if self.check_allowance(tokens[from_token_name], '0xac48fcf1049668b285f3dc72483df5ae2162f7e8') < balance_wei:
                logger.info(f'SwapMode: try approve token {from_token_name}...')
                send_list += self.approve(balance_wei, tokens[from_token_name], '0xac48fcf1049668b285f3dc72483df5ae2162f7e8')
                sleeping_between_transactions()

            deadline = int(time.time() + 10000)
            data = (f'0xbc651188'
                    f'{from_token_address[2:].zfill(64)}'
                    f'{to_token_address[2:].zfill(64)}'
                    f'0000000000000000000000000000000000000000000000000000000000000000'
                    f'{hex(deadline)[2:].zfill(64)}'
                    f'{hex(balance_wei)[2:].zfill(64)}'
                    f'{hex(min_amount_wei)[2:].zfill(64)}'
                    f'0000000000000000000000000000000000000000000000000000000000000000')

            data2 = (f'0x69bc35b2'
                     f'{hex(min_amount_wei)[2:].zfill(64)}'
                     f'{self.address[2:].zfill(64)}')

            tx_data = get_tx_data_withABI(self, value=0)
            transaction = self.router_contract.functions.multicall([HexBytes(data[2:]), HexBytes(data2[2:])]).build_transaction(tx_data)

            logger.info(f'KimExchange: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.4f}".format(min_amount)} {to_token_name}')
            txstatus, tx_hash = sign_and_send_transaction(self, transaction)

            if txstatus == 1:
                logger.success(f'KimExchange: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.4f}".format(min_amount)} {to_token_name}: {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}KimExchange: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.4f}".format(min_amount)} {to_token_name} - [tx hash]({self.scan + tx_hash})')

            else:
                logger.error(f'KimExchange: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.4f}".format(min_amount)} {to_token_name}: {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}KimExchange: Swap {"{:0.9f}".format(balance_eth)} {from_token_name} to {"{:0.4f}".format(min_amount)} {to_token_name} - [tx hash]({self.scan + tx_hash})')

    def main(self):
        global send_list
        send_list = ''
        count_swap = random.randint(count_swaps[0], count_swaps[1])
        for i in range(count_swap):
            to_token_name = KimExchange.swap(self)
            sleeping_between_transactions()
            KimExchange.swap_to_eth(self, to_token_name)
            sleeping_between_transactions()
        return send_list

class Okex(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.rpc = rpc

    @retry
    def deposit_to_okex(self, addressokx):
        stay_eth_in_network = round(random.uniform(stay_eth[0], stay_eth[1]), decimal_places)
        value_in_eth = self.get_balance()["balance"] - stay_eth_in_network
        value_in_wei = int(self.w3.to_wei(value_in_eth, "ether"))

        transaction = get_tx_data(self, self.w3.to_checksum_address(addressokx), value=value_in_wei)

        logger.info(f'OKx: Deposit {"{:0.9f}".format(value_in_eth)} ETH from {self.rpc}...')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)

        if txstatus == 1:
            logger.success(f'OKx: Deposit {"{:0.9f}".format(value_in_eth)} ETH from {self.rpc} : {self.scan + tx_hash}')
            return (
                f'\n{SUCCESS}OKx: Deposit {"{:0.4f}".format(value_in_eth)} ETH from {self.rpc} - [tx hash]({self.scan + tx_hash})')
        else:
            logger.error(f'OKx: Deposit {"{:0.9f}".format(value_in_eth)} ETH from {self.rpc} : {self.scan + tx_hash}')
            return (f'\n{FAILED}OKx: Deposit {"{:0.4f}".format(value_in_eth)} ETH from {self.rpc} - failed')

    def withdraw_from_okex(self):

        if transfer_subaccount:
            Okex.transfer_from_subaccount(self)
            print()
        delay = [3, 5]
        amount_to_withdrawal = round(random.uniform(amount[0], amount[1]), decimal_places)
        Okex.choose_cex(self.address, amount_to_withdrawal, 1)
        time.sleep(random.randint(delay[0], delay[1]))
        self.wait_balance(int(self.w3.to_wei(amount_to_withdrawal, 'ether') * 0.8), rpc=self.rpc)
        sleeping_between_transactions()
        return (f'\n{SUCCESS}OKx: Withdraw {"{:0.4f}".format(amount_to_withdrawal)} ETH')

    def transfer_from_subaccount(self):
        exchange = ccxt.okx({
            'apiKey': API.okx_apikey,
            'secret': API.okx_apisecret,
            'password': API.okx_passphrase,
            'enableRateLimit': True,
            'proxies': proxies,
        })

        list_sub = exchange.private_get_users_subaccount_list()
        for sub_data in list_sub['data']:
            name_sub = sub_data['subAcct']
            balance = exchange.private_get_asset_subaccount_balances({'subAcct': name_sub, 'ccy': symbolWithdraw})
            sub_balance = balance['data'][0]['bal']
            logger.info(f'OKx: {name_sub} balance : {sub_balance} {symbolWithdraw}')
            if float(sub_balance) > 0:
                transfer = exchange.private_post_asset_transfer(
                    {"ccy": symbolWithdraw, "amt": str(sub_balance), "from": '6', "to": '6', "type": "2",
                     "subAcct": name_sub})
                logger.success(f'OKx: transfer to main {sub_balance} {symbolWithdraw}')
            else:
                continue
        time.sleep(15)
        return True

    def okx_withdraw(address, amount_to_withdrawal, wallet_number):
        exchange = ccxt.okx({
            'apiKey': API.okx_apikey,
            'secret': API.okx_apisecret,
            'password': API.okx_passphrase,
            'enableRateLimit': True,
            'proxies': proxies,
        })

        try:
            chainName = symbolWithdraw + "-" + network_okex
            fee = Okex.get_withdrawal_fee(symbolWithdraw, chainName)
            exchange.withdraw(symbolWithdraw, amount_to_withdrawal, address,
                              params={
                                  "toAddress": address,
                                  "chainName": chainName,
                                  "dest": 4,
                                  "fee": fee,
                                  "pwd": '-',
                                  "amt": amount_to_withdrawal,
                                  "network": network_okex
                              }
                              )
            logger.success(f'OKx: Вывел {amount_to_withdrawal} {symbolWithdraw}')
            return amount_to_withdrawal
        except Exception as error:
            logger.error(f'OKx: Не удалось вывести {amount_to_withdrawal} {symbolWithdraw}: {error}')

    def choose_cex(address, amount_to_withdrawal, wallet_number):
        if switch_cex == "okx":
            Okex.okx_withdraw(address, amount_to_withdrawal, wallet_number)

    def get_withdrawal_fee(symbolWithdraw, chainName):
        exchange = ccxt.okx({
            'apiKey': API.okx_apikey,
            'secret': API.okx_apisecret,
            'password': API.okx_passphrase,
            'enableRateLimit': True,
            'proxies': proxies,
        })
        currencies = exchange.fetch_currencies()
        for currency in currencies:
            if currency == symbolWithdraw:
                currency_info = currencies[currency]
                network_info = currency_info.get('networks', None)
                if network_info:
                    for network in network_info:
                        network_data = network_info[network]
                        network_id = network_data['id']
                        if network_id == chainName:
                            withdrawal_fee = currency_info['networks'][network]['fee']
                            if withdrawal_fee == 0:
                                return 0
                            else:
                                return withdrawal_fee
        raise ValueError(f"не могу получить сумму комиссии, проверьте значения symbolWithdraw и network")



