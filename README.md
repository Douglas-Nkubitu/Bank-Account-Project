# Bank Account Project

The goal of this mini project is to write a simple micro web service to mimic a “Bank Account”. Through this web service, one can query about the balance, deposit money, and withdraw money. Just like any Bank, there are restrictions on how many transactions/amounts it can handle. The details are described below.

  + Write a simple “Bank Account” web service using REST API design principles.
  + Program should have 3 REST API endpoints: Balance, Deposit, and Withdrawal
  + No requirement for authentication assume the web service is for one account only and is open to the world
  + No requirement for the backend store you can store it in a file or database (your decision)
  + Balance endpoint this will return the outstanding balance
  + Deposit endpoint credits the account with the specified amount
    - Max deposit for the day = Kes. 150K
    - Max deposit per transaction = Kes. 40K
    - Max deposit frequency = 4 transactions/day
  + Withdrawal endpoint deducts the account with the specified amount
    - Max withdrawal for the day = Kes. 50K
    - Max withdrawal per transaction = Kes. 20K
    - Max withdrawal frequency = 3 transactions/day
    - Cannot withdraw when balance is less than withdrawal amount
  + The service should handle all the error cases and return the appropriate error HTTP status code and error message (Eg. If an attempt is to withdraw greater than Kes. 20k in a single transaction, the error message should say “Exceeded Maximum Withdrawal Per Transaction”).

### Installation

+ Clone Repo
  
```sh
git clone https://github.com/Douglas-Nkubitu/Bank-Account-Project.git
```
+ Navigate to bankApp

```sh
cd Bank-Account-Project/bankApp
```

+ Activate the virtualenv

```sh
source bin/activate
```

+ Install flask

```sh
pip3 install flask
```

+ Run:

```sh
python3 bankapp.py
```

### Running unittest TestCase

+ Navigate to bankApp
  
```sh
cd Bank-Account-Project/bankApp
```
+ Run
  
```sh
python3 -m unittest discover -s tests
```
