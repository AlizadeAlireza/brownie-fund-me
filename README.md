# brownie-fund-me
Smart Contract Application


### FundMe.sol

we want this contract to be able to accept some type of payment.

we want to know about who sent us some funding. - create a new mapping between addresses and value.

in fund() we want track of all the people who sent us money or all the addresses that
sent us some value. - msg.sender is the sender of the function call. - msg.value is how much they sent.

    when we send our funds to a contract means that this contract whereever this
    is deployed now is the owner of this amount of ether.

minimum value fot people to be able to fund.
we want accept eth as the token but i want it in the usd currency.
then i need to know what that conversion rate is.

    for our purposes we need to latest price.



    for implement this data feed into our fundme application we need to import
    the chainlink code.

anytime you want to interact with an already deployed smart contract you will need an ABI.

getVersion():
after we initialize interface we need to finding the priceFeed address. - in chainlink contract addresses. - the goerly chian has this address.

        we made a contract call to another contract from our contract.

getPrice():

    in this function that we're going to want to call on this contract.

for convertion our value we need function:

    getConvertion():

    - in this function we get the updated ethprice in the local variable and
    multiply in the ehtAmount that is a argument of this function.
    in the end divided by 1e18 to give us the number without decimal!

in the solidity prior the 0.8 if we added the maximum size it actually overflow.
for avoiding this problem we can use SafeMath from openzeppelin.

if they didn't send us enough ether and we call revert() that revert the transaction.
means the users get their money back as well as any unspend gas.

withdraw():
in this function we transfer all the money the user has.

we don't want to anybody can call withdraw so we can change the contract to ownable.

when we withdraw from this contract we are actually update the contract balance of people who funded this.
so we need to through all the funders in this mapping and reset their balances to zero.
we can loop through all of the keys in the mapping with creating a list of keys.
so we can push the funders address in this array and do our purposes.

and when withdraw everything we want to reset the balance of this contract.  
we want to reset everyone's balance in that mapping to zero.

the funder at the index of funders array.we use this as the key of the mapping.

at the end we need to reset our funder array.

### deploy by brownie

1 ) make brownie project

1,1 ) brownie init

1,2 ) in contracts ---> FundMe.sol

1,3 ) when we start $browmie compile is not same like the remix
the remix know imports of FundMe but brownie doesn't know.
brownie can donwload directly from Github
we have a package create for downloading chainlink contracts

1,4 ) tell brownie where to get these from is in our browning config ----> brownie-config.yaml

also need to brownie what this at chanilink thing means.
in dependencies after we declare organization and repo name with version.

2 ) remappings ---> is the first section of that import
when you see @chainlink = smartcontractkit/chainlink-brownie-contracts@1.1.1

3 ) helpful scripts in scripts dir

3,1 ) we can use it with **init**.py in scripts dir

with that python knows that it can import other scripts and other packages in this project

4 ) deploy to the kovan
go to it and verify and @ import does n't work in etherscan and we force to copy in the top of our contract
flattening = replacing imports with the actuall code is known as "flattening"

programatic way to verify

5 ) create an api key after signing up in etherscan.io that is enviroment variable

5,1 ) to verify this in our dictionary({"from: account}) we add publish_source=True

5,2 ) we are always going to want to be able to deploy to our own local blockchain or brownies built-in development chain

price feed contracts don't exist on a local ganache chain or ganache chain that brownie spins up;

1, forking: work on a forkchain

2, mocking: we can deploy a fake deploy contract and interacting with it as if
it's real

6 ) constructor parameters

is right when we deploy this contract we'll tell it what peice feed address it
should use right when we call our deploy function here instead of having hard coded.
so instead of creating aggrV3 interface in functions we can create a global one.

6,1 ) add this line to our constructor ----> address \_priceFeed(as an input parameter)

is going to be our global price feed address

6,2 ) instead of aggregator v3 interface contract we create a global one and
delete aggre in getVersion func ---> <= 0

6,3 ) still we have that issue with hard-code
we can do is in our browine config add different addresses for deifferent networks

- we can get this address from brownie config section

\*\* this way we can define different addresses for this priceFeed across different
networks

6,4 ) import config from brownie
6,5 ) we can pass variables to constructors we can pass from brownie in our deploy script here---> we can use it in deploy(,)

###MOCK
7 ) in contracts dir we made a dir ----> test
in this folder we create a new file ---> MockV3aggregator.sol

7,1 ) copy paste mocks from the chainlink-mix or the chainlink core repo
brownie compiles any contract in contracts dir

7,2 ) the same way we import FundMe we can import MockV3Aggregator

7,3 ) we can just deploy this contract the same way we deploy FundMe
add the parameteres the constructor takes.

7,4 ) published_source is going to pulled from our config

7, 5) for more readable number in our deploy.py
we can use web3.toWei()

8,1 ) we don't have need two mock so we can use if statement
and we say if the length is 0 can deploy the mock
otherwise we don't need anyother mock
8,2 ) we can deploying own function to helpful script
8,3 ) instead use of account in dictionary with "from" key
we can use get_account func

8,4 ) delete that code from deploy.py and import that from helpful script

9 ) deploying to persistant ganache
9,2 ) with open ganache program and test locally
for development networks brownie doesn't keep track of those

10 ) adding a network to brownie
$ brownie networks add (Ethereum | Development) ganache-local host=http://0.0.0.0:8545 chainid=1337

10,1 ) keep the ganache UI up!
ganache-local isn't development and go ahead and try to pull from our config file
and want to deploy the mock for our local ganache
we can create a list with development and ganache-local

10,2 ) if whatever network that we're on if it isn't development or ganache-local
then go ahead and use a config
if it one of these two we're gonna go ahead and deploy a mock here

10,3 ) in get_account() --> also looking directly for this development chain

10, 4) then we have now a new chain in build/deplpyments dir

11 ) if you delete this ganache chian all of your contrcats will be lost

RESETTING A NETWORK BUILD

11,1 ) make a script ---> fund_and_withdraw.py

12 ) create test_fund_me in tests dir
default network in yaml is set to everything

12,1 ) well we want this to happen we were expecting this to happen so how do we
test that we want this to happen
import from brownie exception

13 ) main net forking : powerful when we're working with smart contracts on
mainnet that we want to test locally

13,1 ) forked blockchain ---> takes a copy of an existing blockchain on the left
here and brings it into our local computer for us to work with ---> it is a simulated blockchain

13,2 ) we can take this whole kovan big section from config.yaml
and copy it and change this address to mainnet address

13,3 ) we need to tell brownie that when we're working with mainnet fork it should create us a fake account with a hundred eth
and we don't want it to deploy a mock because the price feed contract already exist so and get the price feed from our config

13,4 ) add another varialble here ---> FORKED_LOCAL_ENVIRONMENTS = ["mainnet_fork"]

14 ) custom mainnet-fork
brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.g.alchemy.com/v2/x20J5PZObPOfWdThHEGzpjmRhZ6vZOIS accounts=10 mnemonic=brownie port=8545

15 ) do not push your .env to github

16 ) authentication

17 ) where should i run my tests?

- brownie ganache chain with mocks: always
- testnet : always(but only for integration testing)
- brownie mainnet-fork: optional
- custom mainnet-fork: optional
