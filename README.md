# BT2102 Assignment 1
# Group 2

## Members:
1. Keltonn Lim Jing Feng  [E0560123]
2. Yu Shi Jie             [E0564882]
3. Reuben Ang Wen Zheng   [E0407386]
4. Aaron Tham Shun Cong   [E0544448]
5. Pui Yee Tong           [E0560031]
6. Angley Gan             [E0564603]


## Before Running:
1. Go to prepopulatemysql.py to set login details for MySQL
2. Go to recreatemysql.py to set login details for MySQL
3. Go to main.py and insert login details for both MySQL and MongoDB
4. Run setup.py
5. Done! Run main.py for the application.

## Registration and Login

### Registration:
1. After running main.py, click on the "Register" Button. You will be redirected to a selection screen to indicate if you are an Admin or User
2. Select 'Admin' if Admin. Select 'User' if user.
3. Complete the Sign in form and commit the data.

### Login
1. Insert the login information and click 'login'
2. You will be redirected to the Home Page.

## User's Features

### Product Search [Users]
1. Click on the left button "Product Search", from the Home Page.
2. Apply filters for (Price/Color/Factory/Year) on the left side.
3. Select EITHER category OR models to display. Can choose multiple.
4. Specify to the system whether Category or Model to be used as base filter.
5. Click Search.
6. System will display summary of available items per product category on the Right side. At the bottom right, if any items are owned by the user, a summary will be displayed for each of their owned items.
7. To see detailed information on the items in each entry, double-click on any entry in the "Products Listing" table.

### Item Details [Users] + Purchase Items
1. Once in the Items Table page, accessed through Product Search Page, type in the itemID of the desired item into the input field at the top of the page.
2. Click on the "Details" button, on the right of the field,
3. You will be brought to the Item Description Page. From here, you can view details on the item on the left, and all similar items on the right.
4. If you like the item, click on "Buy".
5. You may choose to return to any pages you like by clicking on any of the redirection buttons on the bottom left.

### Making Service Requests
1. From the "Home page", click on the right button for service management.
2. On the top right of the Service Management Page, the user's inventory of owned items will be displayed, along with the costs of servicing.
3. To service an item, double-click on the item in the inventory table at the top right and then click on "Submit" button under "New Request" at the left side of the table.
4. Your Request will now be processed by an administrator.The Request will be displayed in the "Request Listings" table at the bottom half of the screen. To make payment, double click the entry in the "Request Listings" table and then click "Make Payment" under "Options" at the top left side of the screen.

## Admin Features
### Product Search [Admin] + Database Reset
1. Click on the left button "Product Search", from the Home Page.
2. Apply filters for (Price/Color/Factory/Year) on the left side.
3. Select EITHER category OR models to display. Can choose multiple.
4. Specify to the system whether Category or Model to be used as base filter.
5. Click Search.
6. System will display summary of available items per product category on the Right side, along with detailed information on how many items are in stock, and how many items have been sold.
7. To see detailed information on the items in each entry, double-click on any entry in the "Products Listing" table.
8. To reset the database, click the "Reset Database" red button at the bottom left of the screen. This will terminate the system and reset the database.

### Item Details [Admin]
1. Once in the Items Table page, accessed through Product Search Page, type in the itemID of the desired item into the input field at the top of the page.
2. Click on the "Details" button, on the right of the field,
3. You will be brought to the Item Description Page. From here, you can view details on the item on the left, and all similar items on the right.
4. You may choose to return to any pages you like by clicking on any of the redirection buttons on the bottom left.

### Dealing with Service Requests + Check all Service Request Details
1. Service Requests are distributed equally to all administrators. An administrator can only deal with whatever service requests that has been issued to him/her.
2. To approve a request, select any of the assigned requests in the "Requests" table at the bottom of the screen, and then select "Approve Requests" under "Options" at the top left of the screen.
3. Once servicing is complete, click on the "Service Requests" button under options at the top left of the screen and the request will be marked as completed.
4. To view all requests in the organisation, click on "Administrator Functions" under Options. You will be redirected to the "Requests Summary and Delinquents" page.
5. Once in the Request Summary page, you can view all incomplete requests in the entire organisation on the right side of the screen. You can also view all requests that have yet to receive payment on the left side of the screen.

