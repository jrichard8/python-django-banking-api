# Banking API

Dummy banking API

## TECH Stack

* Python 3.6+
* [Django](https://www.djangoproject.com/)

## Install Required Packages
```shell
 pip install -r requirements.txt
```

## Running the Application
Go to into the banking API app
```shell
cd banking_management
```
Before running the application we need to create the needed DB tables:
```shell
./manage.py migrate
```
Now you can run the development web server:
```shell
./manage.py runserver
```

## User Manual
* Register as a new user:
  ![](./asset/register.PNG)
  
* Login with your user
  
* Create some customers:
  ![alt text](./asset/Customer.PNG)
  
* Create an account attached to a customer:
  ![alt text](./asset/Account.PNG)
  
* Make some transfers between two accounts:
  * you have to follow some rules:
    * Account "from" and "to" should be different
    * The amount of the transfer should <= of the customer balance
  ![alt text](./asset/Transfer.PNG)

* You can now look at the transfer history for a given account:
  ![alt text](./asset/TransferHisto.PNG)
  
* And finally check balance for a given account:
  ![alt text](./asset/AccountBalance.PNG)
  