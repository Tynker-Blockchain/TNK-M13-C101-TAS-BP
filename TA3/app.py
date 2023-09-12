from flask import Flask, render_template, request, redirect, session
import os
from time import time
from wallet import Wallet
from wallet import Account
import firebase_admin
from firebase_admin import credentials
import json

STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, static_folder=STATIC_DIR)
app.use_static_for_root = True

myWallet =  Wallet()
account = None
allAccounts = []
user= None
isSignedIn = False

def firebaseInitialization():
    cred = credentials.Certificate("config/serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://blockchain-wallet-a2812-default-rtdb.firebaseio.com'})
    print("🔥🔥🔥🔥🔥 Firebase Connected! 🔥🔥🔥🔥🔥")

firebaseInitialization()

@app.route("/", methods= ["GET", "POST"])
def home():
    global myWallet, account, allAccounts, isSignedIn
    isConnected = myWallet.checkConnection()
   
    balance = "No Balance"
    transactions = None
    
    transactionData = {}

    if(isSignedIn):
        allAccounts = myWallet.getAccounts()
        if(account == None and allAccounts):
            account = allAccounts[0]

        if(account):
            address = 0
            if(type(account) == dict):
                balance = myWallet.getBalance(account['address'])
                transactions = myWallet.getTransactions(account['address'])
                address= account['address']
            else:
                balance = myWallet.getBalance(account.address)
                transactions = myWallet.getTransactions(account.address)
                address= account.address

            # TA3: Set amountList, colorList and indicesTransactions to empty
            amountList = [10, 20, 30]
            colorList=['red','blue','green']
            indicesTransactions = [0,1,2]
           

            # TA3: Reverse the transactions list in Python
            
            # TA3: Iterate over the reversed transactions list
            
                # TA3:  Append transaction amount to amountList after converting it to float
                
                # TA3:  Append 'red' or 'blue color based on whether  transaction['from'] matches the address i.e current user's address
                
                # TA3:  Append index to indicesTransactions
                
                
            traceTnx = {
                'x': indicesTransactions,
                'y': amountList,
                'name': 'Amount',
                'type': 'bar',
                'marker': { 'color' : colorList }
            }
    
            layoutTnx = {
                'title': 'Transaction History',
                'xaxis': { 'title': 'Transaction Index' },
                'yaxis': { 'title': 'Amount(ETH)' }
            }

            transactionData ={
                 'trace': [traceTnx], 
                 'layout': layoutTnx
                 }
            
            transactionData = json.dumps(transactionData)

    return render_template('index.html', 
                        isConnected=isConnected,  
                        account= account, 
                        balance = balance, 
                        transactions = transactions, 
                        allAccounts=allAccounts,
                        isSignedIn = isSignedIn,
                        transactionData = transactionData)



@app.route("/makeTransaction", methods = ["GET", "POST"])
def makeTransaction():
    global myWallet, account

    receiver = request.form.get("receiverAddress")
    amount = request.form.get("amount")

    privateKey = None
    if(type(account) == dict):
            privateKey = account['privateKey']
            sender= account['address']
    else:
            privateKey = account.privateKey
            sender= account.address

    privateKey = account['privateKey']

    tnxHash = myWallet.makeTransactions(sender, receiver, amount, privateKey)
    myWallet.addTransactionHash(tnxHash, sender, receiver,amount)
    return redirect("/")


@app.route("/createAccount", methods= ["GET", "POST"])
def createAccount(): 
    global account, myWallet
    username = myWallet.username
    account = Account(username)
    return redirect("/")

@app.route("/changeAccount", methods= ["GET", "POST"])
def changeAccount(): 
    global account, allAccounts
    
    newAccountAddress = int(request.args.get("address"))
    account = allAccounts[newAccountAddress]
    return redirect("/")

@app.route("/signIn", methods= ["GET", "POST"])
def signIn(): 
    global account, allAccounts, isSignedIn, myWallet
    isSignedIn = True
    
    username = request.form.get("user")
    password = request.form.get("password")
    
    isSignedIn = myWallet.addUser(username, password)
    return redirect("/")

@app.route("/signOut", methods= ["GET", "POST"])
def signOut(): 
    global account, allAccounts, isSignedIn
    isSignedIn = False
    return redirect("/")

if __name__ == '__main__':
    app.run(debug = True, port=4000)



