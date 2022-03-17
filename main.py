# Back End Packages
import json
from logging import exception
import pandas as pd
import sqlalchemy as sqa
import pymongo as pymgo
from mysqlaccessors import connectTo, executeQuery, readQuery
from recreatemysql import reimportDB
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from prepopulatemysql import (
    prepopulate_all,
    prepopulate_product,
    prepopulate_user,
    prepopulate_admin,
)
from warrantytest import setOld
# Front-end Packages
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

connection = connectTo("localhost", "root", "password", "oshes")


# Misc Packages
from dateutil.relativedelta import relativedelta
from datetime import date
from datetime import datetime

# Connecting to MongoDB
connectMongo = pymgo.MongoClient("localhost", 27017)
db = connectMongo["assignment1"]
collectionProduct = db["products"]
collectionItem = db["items"]

#################################################################################
# BACK END MANAGEMENT SITE
# Functions to implement
# 1. user and admin Schemas
# 2. Products Schemas
# 3. Service Management Schemas
#################################################################################
#################################################################################
# FRONT END MANAGEMENT SITE
# 1. Login Page                         [Done]
# 2. Home Page                          [Done]
# 3.1. Item Listings Page               [Done]
# 3. Product Catalogue                  [Done]
# 4. Item Information                   [Done]
# 5. Service Management Listings Page   [Done]
# 6. Sign-up Page [Create new user]     [Done]
#################################################################################
# Browser General Settings
root = Tk()
root.attributes("-fullscreen", True)

#################################################################################
# 1. Login Page
#################################################################################
def goToLogin():
    loginPage = Frame(
        root, highlightbackground="black", highlightthickness=1, bg="grey"
    )
    innerFrame = Frame(loginPage, highlightbackground = 'black', highlightthickness = 1)

    # Labels
    loginLabel = Label(
        loginPage,
        text="Smart Home Administration System",
        relief=SUNKEN,
        bg="orange",
    )
    loginLabel.place(relwidth=1, relheight=0.05)

    loginAsLabel = Label(innerFrame, text="Signing in As:")
    loginAsLabel.place(relx=0.10, rely=0.4)

    usernameLabel = Label(innerFrame, text="Username: ")
    usernameLabel.place(relx=0.1, rely=0.10)

    passwordLabel = Label(innerFrame, text="Password: ")
    passwordLabel.place(relx=0.1, rely=0.2)

    # Functions
    def ender():
        root.destroy()

    def navToSignUp():
        loginPage.destroy()
        goToSignUp()

    def clicker():
        userId = userField.get()
        password = passField.get()
        userType = useGroup.get()
        checkerQueue = []
        out = "Error: Login Credentials do not exist"
        # customer
        if userType == 0:
            validate_query = (
                "SELECT * FROM Customer WHERE customerId = '%s' AND password = '%s' "
                % (userId, password)
            )
            results = readQuery(connection, validate_query)
            for result in results:
                checkerQueue.append(result)
            if len(checkerQueue) == 0:
                return messagebox.showerror(title="Error", message=out)
            elif len(checkerQueue) != 0:
                person = checkerQueue[0]
                loginPage.destroy()
                return userHome(person)
            else:
                userField.delete(0, END)
                messagebox.askokcancel("Login Failure", out)
        # admin
        else:
            validate_query = (
                "SELECT * FROM Administrator WHERE adminID = '%s' AND password = '%s' "
                % (userId, password)
            )
            results = readQuery(connection, validate_query)
            for result in results:
                checkerQueue.append(result)
            if len(checkerQueue) == 0:
                return messagebox.showerror(title="Error", message=out)
            elif len(checkerQueue) != 0:
                person = checkerQueue[0]
                loginPage.destroy()
                return adminHome(person)
            else:
                userField.delete(0, END)
                messagebox.askokcancel("Login Failure", out)

    # Fields
    userId = IntVar()
    userField = Entry(innerFrame, textvariable=userId, width=50)
    userField.place(relx=0.4, rely=0.10)
    userField.delete(0, END)

    passField = Entry(innerFrame, width=50)
    passField.place(relx=0.4, rely=0.2)
    passField.config(show="*")

    # Buttons
    loginButton = Button(innerFrame, text="Login", width=50, command=clicker, bg="green")
    loginButton.place(relx=0.2, rely=0.6)

    quitButton = Button(
        innerFrame, text="End Program", width=50, command=ender, bg="red"
    )
    quitButton.place(relx=0.2, rely=0.9)

    signUpButton = Button(
        innerFrame, text="Sign Up", width=50, command=navToSignUp, bg="blue"
    )
    signUpButton.place(relx=0.2, rely=0.7)

    useGroup = IntVar()
    CustomerButton = Radiobutton(
        innerFrame, text="Customer", variable=useGroup, value=0, font=("Mincho", 10)
    )
    CustomerButton.place(relx=0.4, rely=0.4)

    AdminButton = Radiobutton(
        innerFrame, text="Admin", variable=useGroup, value=1, font=("Mincho", 10)
    )
    AdminButton.place(relx=0.6, rely=0.4)

    # Initialise
    loginPage.place(relwidth=1.0, relheight=1.0)
    innerFrame.place(relwidth = 0.4, relheight = 0.5, relx = 0.3, rely = 0.2)


#################################################################################
# 2. Home Page
#################################################################################
def adminHome(person):
    # Frames
    homePage = Frame(root, bg="grey")
    userInventory = Frame(
        homePage, highlightbackground="black", highlightthickness=1, bg="grey"
    )
    serviceManagementFrame = Frame(
        homePage, highlightbackground="black", highlightthickness=1, bg="grey"
    )

    # Labels
    homeLabel = Label(
        homePage,
        text=f"Welcome, Administrator {person[1]}",
        bg="violet",
        relief=SUNKEN,
    )
    homeLabel2 = Label(homePage, text="Please select the service you wish to use:")
    inventoryLabel = Label(
        userInventory, text="Product Management/Search/Admin Functions", bg="yellow"
    )
    serviceLabel = Label(
        serviceManagementFrame, text="Handle Service requests", bg="yellow"
    )

    homeLabel.place(relwidth=1, relheight=0.05)
    homeLabel2.place(relwidth=1, relheight=0.05, rely=0.05)
    inventoryLabel.place(relwidth=1, relheight=0.2)
    serviceLabel.place(relwidth=1, relheight=0.2)

    # Functions
    def servButton():
        homePage.destroy()
        serviceManagement(person)

    def logOut():
        homePage.destroy()
        goToLogin()

    def stockButton():
        homePage.destroy()
        adminProducts(person)


    # Buttons
    purchaseButton = Button(
        userInventory, text="Product Search", command=stockButton, width=30, bg="green"
    )


    serviceButton = Button(
        serviceManagementFrame,
        text="Service Management",
        width=30,
        command=servButton,
        bg="green",
    )
    logOutButton = Button(homePage, text="Log out", width=50, command=logOut, bg="blue")

    purchaseButton.place(relx=0.32, rely=0.5)
    serviceButton.place(relx=0.32, rely=0.5)
    logOutButton.place(relx=0.38, rely=0.6)

    # Initialise
    homePage.place(relwidth=1.0, relheight=1.0)
    userInventory.place(relwidth=0.4, relheight=0.3, relx=0.05, rely=0.2)
    serviceManagementFrame.place(relwidth=0.4, relheight=0.3, relx=0.55, rely=0.2)


def userHome(person):
    # Frames
    homePage = Frame(root, bg="grey")
    userSearch = Frame(
        homePage, highlightbackground="black", highlightthickness=1, bg="grey"
    )
    requestManagementFrame = Frame(
        homePage, highlightbackground="black", highlightthickness=1, bg="grey"
    )

    # Labels
    homeLabel = Label(
        homePage, text=f"Welcome, User {person[1]} ", bg="lightblue", relief=SUNKEN
    )
    homeLabel2 = Label(homePage, text="Please select the service you wish to use:")

    searchLabel = Label(userSearch, text="View our products in stock", bg="yellow")

    requestLabel = Label(
        requestManagementFrame,
        text="Request Servicing for your owned items",
        bg="yellow",
    )

    homeLabel.place(relwidth=1, relheight=0.05)
    homeLabel2.place(relwidth=1, relheight=0.05, rely=0.05)
    searchLabel.place(relwidth=1, relheight=0.2)
    requestLabel.place(relwidth=1, relheight=0.2)

    # Functions
    def goRequest():
        homePage.destroy()
        requestManagement(person)

    def goProduct():
        homePage.destroy()
        userProducts(person)

    def logOut():
        homePage.destroy()
        goToLogin()


    # Buttons
    stockCheckButton = Button(
        userSearch,
        text="Product Search and Purchase",
        width=30,
        command=goProduct,
        bg="green",
    )
    requestButton = Button(
        requestManagementFrame,
        text="Request Management",
        width=30,
        command=goRequest,
        bg="green",
    )

    logOutButton = Button(homePage, text="Log out", width=50, command=logOut, bg="blue")

    stockCheckButton.place(relx=0.32, rely=0.5)
    requestButton.place(relx=0.32, rely=0.5)
    logOutButton.place(relx=0.38, rely=0.6)

    # Initialise
    homePage.place(relwidth=1.0, relheight=1.0)
    userSearch.place(relwidth=0.4, relheight=0.3, relx=0.05, rely=0.2)
    requestManagementFrame.place(relwidth=0.4, relheight=0.3, relx=0.55, rely=0.2)

#################################################################################
# 3.1 Item list page
#################################################################################
def userItemPage(person, allItems, deets):
    validID = []

    #Frames
    itemListingsPage = Frame(root, bg = "dark green")
    itemTablesPage = Frame(itemListingsPage,
                           highlightbackground = "black",
                           highlightthickness = 1)

    # Labels
    titleLabel = Label(
        itemListingsPage, text="Item Listing", relief=SUNKEN, bg="lightblue"
    )
    titleLabel.place(relwidth=1, relheight=0.05)

    idSearchBarLabel = Label(itemListingsPage, text = "Enter item ID: ")
    idSearchBarLabel.place(relx = 0.1, rely = 0.1)

    # Functions
    def singleItem():
        id = idSearchBarField.get()
        if id == "":
            messagebox.askokcancel("No ID detected", 'Please input ID.')
        elif (id not in validID):
            messagebox.askokcancel("Invalid ID", 'Item does not exist or already sold.')
        else:
            itemListingsPage.destroy()
            goToItem(person, id)


    def goHome():
        itemListingsPage.destroy()
        userProducts(person)
    
    def clearSearchBar():
        idSearchBarField.delete(0, END)

    def select_record(e):
        # delete current entry boxes
        clearSearchBar()
        selected = table.focus()
        attrs = table.item(selected)["values"]

        idSearchBarField.insert(0, attrs[0])


    # Fields
    idSearchBarField = Entry(itemListingsPage, width=100)
    idSearchBarField.place(relx=0.25, rely=0.1)
    idSearchBarField.delete(0, END)

    # Buttons
    homeButton = Button(
        itemListingsPage,
        text="Return to Products",
        width=20,
        command=goHome,
        bg="red"
    )
    homeButton.place(relx=0.1, rely=0.2)

    descriptionButton = Button(itemListingsPage,
                               text = "Details",
                               width = 20,
                               bg = "blue",
                               command = singleItem)
    descriptionButton.place(relx = 0.7, rely = 0.1)

    # Tables
    colNames = ["ID", "Category", "Model", "Sale Status"]
    table = ttk.Treeview(itemTablesPage,
                         column = colNames,
                         show = "headings",
                         height = 10,
                         selectmode ='browse')
    verscrlbar = ttk.Scrollbar(itemTablesPage,
                               orient="vertical",
                               command=table.yview)
    table.configure(yscrollcommand=verscrlbar.set)
    verscrlbar.pack(side=RIGHT, fill=Y)


    table.bind("<ButtonRelease-1>", select_record)

    theModel = deets[0]
    theCategory = deets[1]
    for item in allItems:
        if item["Category"] == theCategory and item["Model"] == theModel:
            validID.append(item["ItemID"])
            toInsert = (
                item["ItemID"],
                item["Category"],
                item["Model"],
                item["PurchaseStatus"],
            )
            table.insert("", "end", text=str(item), values=toInsert)
    for name in colNames:
        table.heading(name, text=name, anchor=CENTER)



    table.place(relwidth = 1, relheight = 1)

    # Initialise
    itemListingsPage.place(relwidth = 1, relheight = 1)
    itemTablesPage.place(relwidth = 1, relheight = 0.7, rely = 0.3)
    
def adminItemPage(person, allItems, deets):
    validID = []
    #Frames
    itemListingsPage = Frame(root, bg = "dark green")
    itemTablesPage = Frame(itemListingsPage,
                           highlightbackground = "black",
                           highlightthickness = 1)

    # Labels
    titleLabel = Label(
        itemListingsPage, text="Item Listing", relief=SUNKEN, bg="violet"
    )
    titleLabel.place(relwidth=1, relheight=0.05)

    idSearchBarLabel = Label(itemListingsPage, text = "Enter item ID: ")
    idSearchBarLabel.place(relx = 0.1, rely = 0.1)

    # Functions
    def singleItem():
        id = idSearchBarField.get()
        if id == "":
            messagebox.askokcancel("No ID detected", 'Please input ID.')
        elif (id not in validID):
            messagebox.askokcancel("Invalid ID", 'Item does not exist.')
        else:
            itemListingsPage.destroy()
            goToItem(person, id, True)

    def goHome():
        itemListingsPage.destroy()
        adminProducts(person)

    def clearSearchBar():
        idSearchBarField.delete(0,END)

    def select_record(e):
        # delete current entry boxes
        clearSearchBar()
        selected = table.focus()
        attrs = table.item(selected)["values"]

        idSearchBarField.insert(0, attrs[0])

    # Fields
    idSearchBarField = Entry(itemListingsPage, width=100)
    idSearchBarField.place(relx=0.25, rely=0.1)
    idSearchBarField.delete(0, END)

    # Buttons
    homeButton = Button(
        itemListingsPage,
        text="Return to Products",
        width=20,
        command=goHome,
        bg="red"
    )
    homeButton.place(relx=0.1, rely=0.2)

    descriptionButton = Button(itemListingsPage,
                               text = "Details",
                               width = 20,
                               bg = "blue",
                               command = singleItem)
    descriptionButton.place(relx = 0.7, rely = 0.1)

    # Tables
    colNames = ["ID", "Category", "Model", "Sale Status"]
    table = ttk.Treeview(itemTablesPage,
                         column = colNames,
                         show = "headings",
                         height = 10,
                         selectmode ='browse')
    verscrlbar = ttk.Scrollbar(itemTablesPage,
                               orient="vertical",
                               command=table.yview)
    table.configure(yscrollcommand=verscrlbar.set)
    verscrlbar.pack(side=RIGHT, fill=Y)

    table.bind("<ButtonRelease-1>", select_record)

    theModel = deets[0]
    theCategory = deets[1]

    for item in allItems:
        if item["Category"] == theCategory and item["Model"] == theModel:
            validID.append(item["ItemID"])
            toInsert = (
                item["ItemID"],
                item["Category"],
                item["Model"],
                item["PurchaseStatus"],
            )
            table.insert("", "end", text=str(item), values=toInsert)
    for name in colNames:
        table.heading(name, text=name, anchor=CENTER)



    table.place(relwidth = 1, relheight = 1)

    # Initialise
    itemListingsPage.place(relwidth = 1, relheight = 1)
    itemTablesPage.place(relwidth = 1, relheight = 0.7, rely = 0.3)
    
#################################################################################
# 3. Product Catalogue [Search page and listings]
# list all products
# search button
# note: Remember to update MongoDB with the new JSON files Dr Danny Poo Uploaded
#################################################################################
def userProducts(person):
    # Frames
    userProductPage = Frame(root)
    global listFrame
    searchFrame = Frame(
        userProductPage, highlightbackground="black", highlightthickness=1, bg="grey"
    )
    listFrame = Frame(
        userProductPage, highlightbackground="black", highlightthickness=1
    )
    inventoryFrame = Frame(userProductPage, highlightbackground = "black", highlightthickness= 1)

    # Search inner Frames
    categoryFrame = Frame(searchFrame, highlightbackground = "black",highlightthickness= 1)
    modelFrame = Frame(searchFrame, highlightbackground="black",highlightthickness= 1)
    filterFrame = Frame(searchFrame, highlightbackground = "black",highlightthickness= 1)

    # Labels
    instructionLabel = Label(searchFrame, text = "Double Click a row under Product Listings to see items",
                             fg = 'white', bg = 'grey', font = ('arial', 12))
    instructionLabel.place(relx = 0.05, rely = 0.65)

    productLabel = Label(
        userProductPage, text="Product Page", relief=SUNKEN, bg="lightblue"
    )
    productLabel.place(relwidth=1, relheight=0.05)

    listTitleLabel = Label(userProductPage, text="Listings", relief=SUNKEN, bg="pink")
    listTitleLabel.place(relheight = 0.05, relwidth = 0.7, relx = 0.3, rely = 0.05)

    priceLimitLabel = Label(filterFrame, text="Maximum Price")
    priceLimitLabel.place(relx=0.05, rely=0.2)

    colourLabel = Label(filterFrame, text="Colour")
    colourLabel.place(relx=0.05, rely=0.4)

    factoryLabel = Label(filterFrame, text="Factory")
    factoryLabel.place(relx=0.05, rely=0.6)

    yearLabel = Label(filterFrame, text="Year")
    yearLabel.place(relx=0.05, rely=0.8)

    categoryLabel = Label(categoryFrame, text="Category", relief=SUNKEN, bg="yellow")
    categoryLabel.place(relheight = 0.3, relwidth = 1)

    modelLabel = Label(modelFrame, text="Model", relief=SUNKEN, bg="yellow")
    modelLabel.place(relheight = 0.1, relwidth = 1)

    yourInventoryLabel = Label(inventoryFrame, text = "Your Inventory", relief=SUNKEN, bg="orange")
    yourInventoryLabel.place(relheight = 0.1, relwidth = 1)

    filterLabel =Label(filterFrame, text = "Filter", relief=SUNKEN, bg="yellow")
    filterLabel.place(relheight=0.15, relwidth=1)

    # Tables
    detailNames = ['ItemID', 'Color', 'Factory', 'PowerSupply', 'ProductionYear', 'Model','Service Status']
    myInventoryTable = ttk.Treeview(inventoryFrame, column=detailNames, show="headings", height=5)
    for name in detailNames:
        myInventoryTable.heading(name, text=name, anchor=CENTER)
        myInventoryTable.column(name, anchor=CENTER, stretch=NO, width=150)
    test_query = "SELECT * FROM Purchase WHERE customerID = '%s' " % (person[0])
    results = readQuery(connection, test_query)
    if results != []:
        for item in results:
            test_query2 = "SELECT * FROM Item WHERE purchaseID = '%s' " % (item[0])
            mydetails = readQuery(connection, test_query2)[0]
            myInventoryTable.insert("","end",text=str(item), values=(int(mydetails[0]),) + mydetails[1:4] + (int(mydetails[4]), mydetails[5], mydetails[6]))

    myInventoryTable.place(relheight = 0.9, relwidth = 1, rely = 0.1)

    # Functions
    def searchTings():
        selected = example.get()
        selectedPrice = priceField.get()
        if selectedPrice != "":
            selectedPrice = int(priceField.get())

        if selected == "Search by...":
            # Never specify search filter, display all unsold items
            cats = [lightVar.get(), locksVar.get()]
            sql = collectionItem.find({"PurchaseStatus": "Unsold"})
            createTable(sql, selectedPrice)
            # messagebox.askokcancel("Search Error", "Please input a Category")
        elif selected == "Category":
            cats = [lightVar.get(), locksVar.get()]
            selectedColor = colourBox.get()
            selectedFactory = factoryBox.get()
            selectedYear = yearBox.get()
            # if selectedYear != "":
            #     selectedYear = int(selectedYear)

            selections = [selectedColor, selectedFactory, selectedYear]
            selectionsSQL = [
                {"Color": selectedColor},
                {"Factory": selectedFactory},
                {"ProductionYear": selectedYear},
            ]
            and_query_arr = [
                {"$or": [{"Category": cats[0]}, {"Category": cats[1]}]},
                {"PurchaseStatus": "Unsold"},
            ]
            and_query_arr = and_query_arr + [
                selectionsSQL[i] for i in range(len(selections)) if selections[i] != ""
            ]
            sql = collectionItem.find({"$and": and_query_arr})
            createTable(sql, selectedPrice)

        elif selected == "Model":
            models = [
                light1Var.get(),
                light2Var.get(),
                safe1Var.get(),
                safe2Var.get(),
                safe3Var.get(),
                smartHome1Var.get(),
            ]
            selectedColor = colourBox.get()
            selectedFactory = factoryBox.get()
            selectedYear = yearBox.get()

            selections = [selectedColor, selectedFactory, selectedYear]
            selectionsSQL = [
                {"Color": selectedColor},
                {"Factory": selectedFactory},
                {"ProductionYear": selectedYear},
            ]
            and_query_arr = [
                {
                    "$or": [
                        {"Model": models[0]},
                        {"Model": models[1]},
                        {"Model": models[2]},
                        {"Model": models[3]},
                        {"Model": models[4]},
                        {"Model": models[5]},
                    ]
                },
                {"PurchaseStatus": "Unsold"},
            ]
            and_query_arr = and_query_arr + [
                selectionsSQL[i] for i in range(len(selections)) if selections[i] != ""
            ]
            sql = collectionItem.find({"$and": and_query_arr})
            createTable(sql, selectedPrice)

        else:
            messagebox.askokcancel("Search Error", "No such product")

    def createTable(items, selectedPrice):
        allItems = []
        global listFrame
        listFrame.destroy()
        listFrame = Frame(
            userProductPage, highlightbackground="black", highlightthickness=1
        )
        sql = ""
        categoryValues = []
        modelValues = []
        categoryModel = [
            "LightsLight1",
            "LightsLight2",
            "LightsSmartHome1",
            "LocksSafe1",
            "LocksSafe2",
            "LocksSafe3",
            "LocksSmartHome1",
        ]
        instockValues = [0, 0, 0, 0, 0, 0, 0]

        for item in items:
            allItems.append(item)
            index = 0
            categoryModelPair = item["Category"] + item["Model"]

            index = categoryModel.index(categoryModelPair)

            if item["Category"] not in categoryValues:
                categoryValues.append(item["Category"])
            if item["Model"] not in modelValues:
                modelValues.append(item["Model"])
                instockValues[index] = instockValues[index] + 1
            else:
                instockValues[index] = instockValues[index] + 1

        numModels = len(modelValues)
        # Test if there is value in category and model
        oneCat = False
        # Test if theres 2 catorgoires i.e user never select category
        twoCat = False
        try:
            numCat = len(categoryValues)
            if numCat == 2:
                twoCat = True
            oneCat = True
        except:
            print("No value on either category or model")
            print(len(categoryValues))
            print(len(modelValues))

        if twoCat:
            if selectedPrice == "":
                sql = collectionProduct.find(
                    {
                        "$or": [
                            {
                                "$and": [
                                    {"Model": modelValue},
                                ]
                            }
                            for modelValue in modelValues
                        ]
                    }
                )

            else:
                sql = collectionProduct.find(
                    {
                        "$or": [
                            {
                                "$and": [
                                    {"Model": modelValue},
                                    {"Price ($)": {"$lte": selectedPrice}},
                                ]
                            }
                            for modelValue in modelValues
                        ]
                    }
                )

        elif oneCat:

            if selectedPrice == "":
                sql = collectionProduct.find(
                    {
                        "$or": [
                            {
                                "$and": [
                                    {"Category": categoryValues[0]},
                                    {"Model": modelValue},
                                ]
                            }
                            for modelValue in modelValues
                        ]
                    }
                )
            else:
                sql = collectionProduct.find(
                    {
                        "$or": [
                            {
                                "$and": [
                                    {"Category": categoryValues[0]},
                                    {"Model": modelValue},
                                    {"Price ($)": {"$lte": selectedPrice}},
                                ]
                            }
                            for modelValue in modelValues
                        ]
                    }
                )

        columnNames = (
            "Category",
            "Model",
            "Price ($)",
            "Warranty (months)",
            "In Stock",
        )
        
        table = ttk.Treeview(listFrame, column=columnNames, show="headings", height=10)
        for name in columnNames:
            table.heading(name, text=name, anchor=CENTER)

        for item in sql:
            categoryModelPair = item["Category"] + item["Model"]
            toInsert = (
                item["Category"],
                item["Model"],
                item["Price ($)"],
                item["Warranty (months)"],
                instockValues[categoryModel.index(categoryModelPair)],
            )
            table.insert("", "end", text=str(item), values=toInsert)

        table.place(relwidth=1, relheight=1)
        listFrame.place(relwidth=0.7, relheight=0.6, relx=0.3, rely=0.1)

        #Binding Click
        def clicking(e):
            selected = table.focus()
            theCategory = table.set(selected, 'Model')
            theModel = table.set(selected, 'Category')

            userProductPage.destroy()
            userItemPage(person, allItems, [theCategory, theModel])


        #Binding
        table.bind("<Double-1>", clicking)

    def goHome():
        userProductPage.destroy()
        userHome(person)

    # Fields
    priceValues = ["", "50", "70", "100", "120", "200"]
    priceField = ttk.Combobox(filterFrame, values=priceValues)
    priceField.place(relx=0.5, rely=0.2)

    # Combobox
    example = ttk.Combobox(searchFrame, values=["Search by...", "Category", "Model"])
    example.current(0)
    example.place(relx=0.05, rely=0.70)

    colourValues = []
    colourValues.append("")
    factoryValues = []
    factoryValues.append("")
    yearValues = []
    yearValues.append("")
    all = collectionItem.find()
    for item in all:
        if item["Color"] not in colourValues:
            colourValues.append(item["Color"])
        if item["Factory"] not in factoryValues:
            factoryValues.append(item["Factory"])
        if item["ProductionYear"] not in yearValues:
            yearValues.append(item["ProductionYear"])
    colourBox = ttk.Combobox(filterFrame, values=colourValues)
    factoryBox = ttk.Combobox(filterFrame, values=factoryValues)
    yearBox = ttk.Combobox(filterFrame, values=yearValues)

    colourBox.place(relx=0.5, rely=0.4)
    factoryBox.place(relx=0.5, rely=0.6)
    yearBox.place(relx=0.5, rely=0.8)

    # Checkboxes for Category
    lightVar = StringVar()
    locksVar = StringVar()

    lightBox = Checkbutton(
        categoryFrame, text="Lights", variable=lightVar, onvalue="Lights", offvalue=""
    )
    locksBox = Checkbutton(
        categoryFrame, text="Locks", variable=locksVar, onvalue="Locks", offvalue=""
    )

    lightBox.place(relx=0.1, rely=0.4)
    locksBox.place(relx=0.5, rely=0.4)

    # Checkboxes for Models
    light1Var = StringVar()
    light2Var = StringVar()
    safe1Var = StringVar()
    safe2Var = StringVar()
    safe3Var = StringVar()
    smartHome1Var = StringVar()

    light1Box = Checkbutton(
        modelFrame, text="Light 1", variable=light1Var, onvalue="Light1", offvalue=""
    )
    light2Box = Checkbutton(
        modelFrame, text="Light 2", variable=light2Var, onvalue="Light2", offvalue=""
    )
    safe1Box = Checkbutton(
        modelFrame, text="Safe 1", variable=safe1Var, onvalue="Safe1", offvalue=""
    )
    safe2Box = Checkbutton(
        modelFrame, text="Safe 2", variable=safe2Var, onvalue="Safe2", offvalue=""
    )
    safe3Box = Checkbutton(
        modelFrame, text="Safe 3", variable=safe3Var, onvalue="Safe3", offvalue=""
    )
    smartHome1Box = Checkbutton(
        modelFrame,
        text="Smart Home 1",
        variable=smartHome1Var,
        onvalue="SmartHome1",
        offvalue="",
    )

    light1Box.place(relx=0.1, rely=0.35)
    light2Box.place(relx=0.4, rely=0.35)
    safe1Box.place(relx=0.7, rely=0.35)
    safe2Box.place(relx=0.1, rely=0.6)
    safe3Box.place(relx=0.4, rely=0.6)
    smartHome1Box.place(relx=0.7, rely=0.6)

    # Buttons
    searchButton = Button(
        searchFrame,
        text="Search",
        width=10,
        height=3,
        command=lambda: searchTings(),
        bg="green",
    )
    homeButton = Button(
        searchFrame, text="Return to Home", width=30, command=goHome, bg="red"
    )
    searchButton.place(relx=0.75, rely=0.7)
    homeButton.place(relx=0.2, rely=0.9)

    # Initialise
    userProductPage.place(relwidth=1, relheight=1)
    searchFrame.place(relwidth=0.3, relheight=0.95, relx=0, rely=0.05)
    listFrame.place(relwidth=0.7, relheight=0.6, relx=0.3, rely=0.1)
    inventoryFrame.place(relwidth=0.7, relheight=0.3, relx=0.3, rely=0.7)
    categoryFrame.place(rely = 0.2, relx= 0.05, relwidth = 0.9, relheight = 0.1)
    modelFrame.place(rely = 0.35, relx=0.05, relwidth=0.9, relheight=0.25)
    filterFrame.place(relx = 0.05, rely = 0.02, relwidth = 0.9, relheight = 0.15)


def adminProducts(person):
    # Frames
    adminProductPage = Frame(root)
    global listFrame
    searchFrame = Frame(
        adminProductPage, highlightbackground="black", highlightthickness=1, bg="grey"
    )
    listFrame = Frame(
        adminProductPage, highlightbackground="black", highlightthickness=1
    )

    # Search inner Frames
    categoryFrame = Frame(searchFrame, highlightbackground = "black",highlightthickness= 1)
    modelFrame = Frame(searchFrame, highlightbackground="black",highlightthickness= 1)
    filterFrame = Frame(searchFrame, highlightbackground = "black",highlightthickness= 1)

    # Labels
    instructionLabel = Label(searchFrame, text = "Double Click a row under Product Listings to see items",
                             fg = 'white', bg = 'grey', font = ('arial', 12))
    instructionLabel.place(relx = 0.05, rely = 0.65)
    productLabel = Label(
        adminProductPage, text="Product Page", relief=SUNKEN, bg="violet"
    )
    productLabel.place(relwidth=1, relheight=0.05)

    listTitleLabel = Label(adminProductPage, text="Listings", relief=SUNKEN, bg="pink")
    listTitleLabel.place(relheight = 0.05, relwidth = 0.7, relx = 0.3, rely = 0.05)

    priceLimitLabel = Label(filterFrame, text="Maximum Price")
    priceLimitLabel.place(relx=0.05, rely=0.2)

    colourLabel = Label(filterFrame, text="Colour")
    colourLabel.place(relx=0.05, rely=0.4)

    factoryLabel = Label(filterFrame, text="Factory")
    factoryLabel.place(relx=0.05, rely=0.6)

    yearLabel = Label(filterFrame, text="Year")
    yearLabel.place(relx=0.05, rely=0.8)

    categoryLabel = Label(categoryFrame, text="Category", relief=SUNKEN, bg="yellow")
    categoryLabel.place(relheight=0.3, relwidth=1)

    modelLabel = Label(modelFrame, text="Model", relief=SUNKEN, bg="yellow")
    modelLabel.place(relheight=0.1, relwidth=1)

    filterLabel = Label(filterFrame, text="Filter", relief=SUNKEN, bg="yellow")
    filterLabel.place(relheight=0.15, relwidth=1)

    def searchTings():
        selected = example.get()
        selectedPrice = priceField.get()
        if selectedPrice != "":
            selectedPrice = int(priceField.get())

        if selected == "Search by...":
            # Never specify search filter, display all unsold items
            cats = [lightVar.get(), locksVar.get()]
            sql = collectionItem.find({})
            createTable(sql, selectedPrice)
            # messagebox.askokcancel("Search Error", "Please input a Category")
        elif selected == "Category":
            cats = [lightVar.get(), locksVar.get()]
            selectedColor = colourBox.get()
            selectedFactory = factoryBox.get()
            selectedYear = yearBox.get()

            selections = [selectedColor, selectedFactory, selectedYear]
            selectionsSQL = [
                {"Color": selectedColor},
                {"Factory": selectedFactory},
                {"ProductionYear": selectedYear},
            ]
            and_query_arr = [
                {"$or": [{"Category": cats[0]}, {"Category": cats[1]}]}
            ]
            and_query_arr = and_query_arr + [
                selectionsSQL[i] for i in range(len(selections)) if selections[i] != ""
            ]
            sql = collectionItem.find({"$and": and_query_arr})

            createTable(sql, selectedPrice)

        elif selected == "Model":
            models = [
                light1Var.get(),
                light2Var.get(),
                safe1Var.get(),
                safe2Var.get(),
                safe3Var.get(),
                smartHome1Var.get(),
            ]
            selectedColor = colourBox.get()
            selectedFactory = factoryBox.get()
            selectedYear = yearBox.get()

            selections = [selectedColor, selectedFactory, selectedYear]
            selectionsSQL = [
                {"Color": selectedColor},
                {"Factory": selectedFactory},
                {"ProductionYear": selectedYear},
            ]
            and_query_arr = [
                {
                    "$or": [
                        {"Model": models[0]},
                        {"Model": models[1]},
                        {"Model": models[2]},
                        {"Model": models[3]},
                        {"Model": models[4]},
                        {"Model": models[5]},
                    ]
                }
            ]
            and_query_arr = and_query_arr + [
                selectionsSQL[i] for i in range(len(selections)) if selections[i] != ""
            ]
            sql = collectionItem.find({"$and": and_query_arr})

            createTable(sql, selectedPrice)

        else:
            messagebox.askokcancel("Search Error", "No such product")

    def createTable(items, selectedPrice):
        allItems = []
        global listFrame
        listFrame.destroy()
        listFrame = Frame(
            adminProductPage, highlightbackground="black", highlightthickness=1
        )
        sql = ""
        categoryValues = []
        modelValues = []
        categoryModel = [
            "LightsLight1",
            "LightsLight2",
            "LightsSmartHome1",
            "LocksSafe1",
            "LocksSafe2",
            "LocksSafe3",
            "LocksSmartHome1",
        ]
        instockValues = [0, 0, 0, 0, 0, 0, 0]
        totalStocks = [0, 0, 0, 0, 0, 0, 0]

        for item in items:
            allItems.append(item)
            index = 0
            categoryModelPair = item["Category"] + item["Model"]

            index = categoryModel.index(categoryModelPair)

            if item["Category"] not in categoryValues:
                categoryValues.append(item["Category"])
            if item["Model"] not in modelValues:
                modelValues.append(item["Model"])
                totalStocks[index] = totalStocks[index] + 1
                if item["PurchaseStatus"] == "Unsold":
                    instockValues[index] = instockValues[index] + 1
            else:
                totalStocks[index] = totalStocks[index] + 1
                if item["PurchaseStatus"] == "Unsold":
                    instockValues[index] = instockValues[index] + 1

        # Test if there is value in category and model
        oneCat = False
        # Test if theres 2 catorgoires i.e user never select category
        twoCat = False
        try:
            numCat = len(categoryValues)
            if numCat == 2:
                twoCat = True
            oneCat = True
        except:
            print("No value on either category or model")
            print(len(categoryValues))
            print(len(modelValues))

        if twoCat:

            if selectedPrice == "":
                sql = collectionProduct.find(
                    {
                        "$or": [
                            {
                                "$and": [
                                    {"Model": modelValue},
                                ]
                            }
                            for modelValue in modelValues
                        ]
                    }
                )

            else:
                sql = collectionProduct.find(
                    {
                        "$or": [
                            {
                                "$and": [
                                    {"Model": modelValue},
                                    {"Price ($)": {"$lte": selectedPrice}},
                                ]
                            }
                            for modelValue in modelValues
                        ]
                    }
                )

        elif oneCat:

            if selectedPrice == "":
                sql = collectionProduct.find(
                    {
                        "$or": [
                            {
                                "$and": [
                                    {"Category": categoryValues[0]},
                                    {"Model": modelValue},
                                ]
                            }
                            for modelValue in modelValues
                        ]
                    }
                )
            else:
                sql = collectionProduct.find(
                    {
                        "$or": [
                            {
                                "$and": [
                                    {"Category": categoryValues[0]},
                                    {"Model": modelValue},
                                    {"Price ($)": {"$lte": selectedPrice}},
                                ]
                            }
                            for modelValue in modelValues
                        ]
                    }
                )

        columnNames = (
            "Category",
            "Model",
            "Price ($)",
            "Warranty (months)",
            "In Stock",
            "Cost",
            "Items Sold")
        table = ttk.Treeview(listFrame, column=columnNames, show="headings", height=10)
        for name in columnNames:
            table.heading(name, text=name, anchor=CENTER)
            table.column(name, anchor=CENTER, stretch=NO, width=150)

        for item in sql:
            categoryModelPair = item["Category"] + item["Model"]
            toInsert = (
                item["Category"],
                item["Model"],
                item["Price ($)"],
                item["Warranty (months)"],
                instockValues[categoryModel.index(categoryModelPair)],
                item["Cost ($)"],
                totalStocks[categoryModel.index(categoryModelPair)]
                - instockValues[categoryModel.index(categoryModelPair)],
            )
            table.insert("", "end", text=str(item), values=toInsert)

        table.place(relwidth=1, relheight=1)
        listFrame.place(relwidth=0.7, relheight=0.9, relx=0.3, rely=0.1)

        #Binding Click
        def clicking(e):
            selected = table.focus()
            theCategory = table.set(selected, 'Model')
            theModel = table.set(selected, 'Category')

            adminProductPage.destroy()
            adminItemPage(person, allItems, [theCategory, theModel])

        #Binding
        table.bind("<Double-1>", clicking)


    def goHome():
        adminProductPage.destroy()
        adminHome(person)

    def resetDB():
        # SQL
        try:
            dbCursor = connection.cursor()
            sql = "DROP DATABASE " + "oshes"
            dbCursor.execute(sql)
            databaseCollection = dbCursor.fetchall()

        except Exception as e:
            print("Exeception occured:{}".format(e))

        reimportDB()
        prepopulate_all()

        # MongoDB
        collectionItem.delete_many({})
        with open('items.json') as f:
            file_data = json.load(f)
        collectionItem.insert_many(file_data)

        collectionProduct.delete_many({})
        with open('products.json') as f:
            file_data2 = json.load(f)
        collectionProduct.insert_many(file_data2)
        setOld()
        root.destroy()

    # Combobox
    example = ttk.Combobox(searchFrame, values=["Search by...", "Category", "Model"])
    example.current(0)
    example.place(relx=0.05, rely=0.70)

    priceValues = ["", "50", "70", "100", "120", "200"]
    priceField = ttk.Combobox(filterFrame, values=priceValues)
    priceField.place(relx=0.5, rely=0.2)

    colourValues = []
    colourValues.append("")
    factoryValues = []
    factoryValues.append("")
    yearValues = []
    yearValues.append("")
    all = collectionItem.find()

    for item in all:
        if item["Color"] not in colourValues:
            colourValues.append(item["Color"])
        if item["Factory"] not in factoryValues:
            factoryValues.append(item["Factory"])
        if item["ProductionYear"] not in yearValues:
            yearValues.append(item["ProductionYear"])
    colourBox = ttk.Combobox(filterFrame, values=colourValues)
    factoryBox = ttk.Combobox(filterFrame, values=factoryValues)
    yearBox = ttk.Combobox(filterFrame, values=yearValues)

    colourBox.place(relx=0.5, rely=0.4)
    factoryBox.place(relx=0.5, rely=0.6)
    yearBox.place(relx=0.5, rely=0.8)

    # Checkboxes for Category
    lightVar = StringVar()
    locksVar = StringVar()

    lightBox = Checkbutton(
        categoryFrame, text="Lights", variable=lightVar, onvalue="Lights", offvalue=""
    )
    locksBox = Checkbutton(
        categoryFrame, text="Locks", variable=locksVar, onvalue="Locks", offvalue=""
    )

    lightBox.place(relx=0.1, rely=0.4)
    locksBox.place(relx=0.5, rely=0.4)

    # Checkboxes for Models
    light1Var = StringVar()
    light2Var = StringVar()
    safe1Var = StringVar()
    safe2Var = StringVar()
    safe3Var = StringVar()
    smartHome1Var = StringVar()

    light1Box = Checkbutton(
        modelFrame, text="Light 1", variable=light1Var, onvalue="Light1", offvalue=""
    )
    light2Box = Checkbutton(
        modelFrame, text="Light 2", variable=light2Var, onvalue="Light2", offvalue=""
    )
    safe1Box = Checkbutton(
        modelFrame, text="Safe 1", variable=safe1Var, onvalue="Safe1", offvalue=""
    )
    safe2Box = Checkbutton(
        modelFrame, text="Safe 2", variable=safe2Var, onvalue="Safe2", offvalue=""
    )
    safe3Box = Checkbutton(
        modelFrame, text="Safe 3", variable=safe3Var, onvalue="Safe3", offvalue=""
    )
    smartHome1Box = Checkbutton(
        modelFrame,
        text="Smart Home 1",
        variable=smartHome1Var,
        onvalue="SmartHome1",
        offvalue="",
    )

    light1Box.place(relx=0.1, rely=0.35)
    light2Box.place(relx=0.4, rely=0.35)
    safe1Box.place(relx=0.7, rely=0.35)
    safe2Box.place(relx=0.1, rely=0.6)
    safe3Box.place(relx=0.4, rely=0.6)
    smartHome1Box.place(relx=0.7, rely=0.6)

    # Buttons
    searchButton = Button(
        searchFrame,
        text="Search",
        width=10,
        height=1,
        command=lambda: searchTings(),
        bg="green",
    )

    homeButton = Button(
        searchFrame, text="Return to Home", width=30, command=goHome, bg="red"
    )
    searchButton.place(relx=0.75, rely=0.7)
    homeButton.place(relx=0.2, rely=0.9)
    dataResetButton = Button(
        searchFrame, text="Reset database", width=30, bg="red", command=resetDB
    )
    dataResetButton.place(relx=0.2, rely=0.8)

    # Initialise
    adminProductPage.place(relwidth=1, relheight=1)
    searchFrame.place(relwidth=0.3, relheight=0.95, relx=0, rely=0.05)
    listFrame.place(relwidth=0.7, relheight=0.9, relx=0.3, rely=0.1)
    categoryFrame.place(rely = 0.2, relx= 0.05, relwidth = 0.9, relheight = 0.1)
    modelFrame.place(rely = 0.35, relx=0.05, relwidth=0.9, relheight=0.25)
    filterFrame.place(relx = 0.05, rely = 0.02, relwidth = 0.9, relheight = 0.15)


#################################################################################
# 4. Item Information
#################################################################################
def goToItem(person, id, admin=False):

    # Functions
    def getItemInfo(itemID):
        item = collectionItem.find({"ItemID": {"$eq": itemID}})
        item = item[0]
        return (
            item["Category"],
            item["Color"],
            item["Factory"],
            item["PowerSupply"],
            item["PurchaseStatus"],
            item["ProductionYear"],
            item["Model"],
            item["ServiceStatus"],
        )

    def getProductInfo(category, model):
        product = collectionProduct.find(
            {"$and": [{"Category": {"$eq": category}}, {"Model": {"$eq": model}}]}
        )
        product = product[0]
        return (
            product["Cost ($)"],
            product["Price ($)"],
            product["Warranty (months)"],
            product["ProductID"],
        )

    def getSimilarItems(category, model, admin):

        items = collectionItem.find(
            {
                "$and": [
                    {"Category": {"$eq": category}},
                    {"Model": {"$eq": model}},
                    {"PurchaseStatus": {"$eq": "Unsold"}} if not admin else {},
                ]
            },
            {
                "ItemID": 1,
                "Color": 1,
                "Factory": 1,
                "PowerSupply": 1,
                "ProductionYear": 1,
                "PurchaseStatus": 1,
            },
        )

        return items

    def clearEntries():
        # clear entry boxes
        attrEntry0.delete(0, END)
        attrEntry1.delete(0, END)
        attrEntry2.delete(0, END)
        attrEntry3.delete(0, END)
        attrEntry4.delete(0, END)
        attrEntry5.delete(0, END)

    def select_record(e):
        # delete current entry boxes
        clearEntries()
        selected = table.focus()
        attrs = table.item(selected)["values"]

        attrEntry0.insert(0, attrs[0])
        attrEntry1.insert(0, attrs[1])
        attrEntry2.insert(0, attrs[2])
        attrEntry3.insert(0, attrs[3])
        attrEntry4.insert(0, attrs[4])
        attrEntry5.insert(0, attrs[5])

    def goItem():
        try:
            itemID = str(attrEntry0.get())
            itemPage.destroy()
            goToItem(person, itemID, admin)
        except:
            goToItem(person, id, admin)
            messagebox.askokcancel(title="Error", message="Invalid Item ID")

    def buyItem():
        # UPDATES MYSQL
        numQuery = "SELECT MAX(purchaseID) FROM Purchase"
        if readQuery(connection, numQuery)[0][0] != None:
            purchaseID = str(int(readQuery(connection, numQuery)[0][0]) + 1)
        else:
            purchaseID = 0
        purchaseDate = datetime.now().strftime("%Y-%m-%d")
        sql_query = "INSERT INTO Purchase VALUES ('%s', '%s','%s'); " % (
            purchaseID,
            purchaseDate,
            person_id,
        )
        executeQuery(connection, sql_query)
        temp = collectionItem.find_one({ "ItemID": id })
        productID = collectionProduct.find_one({"Model":temp["Model"], "Category":temp["Category"]})["ProductID"]
        sql_query = "INSERT INTO Item VALUES ('%s', '%s','%s', '%s', '%s','%s', '%s', %s, %s); " % (
            id,
            color,
            factory,
            power_supply,
            production_year,
            model,
            service_status,
            productID,
            purchaseID,
        )
        executeQuery(connection, sql_query)

        # UPDATES MONGODB
        collectionItem.find_one_and_update(
            {"ItemID": id}, {"$set": {"PurchaseStatus": "Sold"}}
        )

        goToItem(person, id, admin)

        return messagebox.showinfo(title="success", message="Update successful!")

    def goHome():
        itemPage.destroy()
        if admin:
            adminHome(person)
        else:
            userHome(person)

    def refresh():
        itemPage.destroy()
        goToItem(person, id, admin)
 
    def back():
        itemPage.destroy()
        if admin:
            adminProducts(person)
        else:
            userProducts(person)

    def backMainte():
        itemPage.destroy()
        if admin:
            serviceManagement(person)
        else:
            requestManagement(person)

    person_id = person[0]
    (
        category,
        color,
        factory,
        power_supply,
        purchase_status,
        production_year,
        model,
        service_status,
    ) = getItemInfo(id)

    
    cost, price, warranty, productId = getProductInfo(category, model)

    # Frames
    itemPage = Frame(root)
    outerFrame1 = Frame(itemPage, bg="blue")
    outerFrame2 = Frame(itemPage, bg="yellow")
    outerTableFrame = Frame(outerFrame2)

    Frame1 = Frame(outerFrame1)
    Frame2 = Frame(outerFrame1)

    tableFrame = Frame(outerTableFrame)
    selectionFrame = LabelFrame(outerTableFrame, text="Record")
    goItemFrame = Frame(outerFrame2)

    keyInfoFrame = Frame(Frame1, highlightbackground="black", highlightthickness=1)

    purchaseFrame = Frame(Frame1, highlightbackground="black", highlightthickness=1)

    infoFrame = LabelFrame(
        Frame2,
        text=f"Item Information",
        highlightbackground="black",
        highlightthickness=1,
    )

    buttonsFrame = Frame(
        outerFrame1,
        highlightbackground="black",
        highlightthickness=1,
    )

    # Labels
    bannerLabel = Label(
        itemPage,
        text=f"Item #{id} : {category} / {model}",
        bg="lightblue",
        relief=SUNKEN,
        height=2,
    )
    
    if admin:
        bannerLabel = Label(
        itemPage,
        text=f"Item #{id} : {category} / {model}",
        bg="violet",
        relief=SUNKEN,
        height=2,
        )

    similarItemsBannerLabel = Label(
        tableFrame,
        text=f"Similar Items ({category} : {model})",
        bg="yellow",
        relief=SUNKEN,
        height=2,
    )

    idLabel = Label(keyInfoFrame, text=f"Item ID:", bg="lightblue")
    categoryLabel = Label(keyInfoFrame, text=f"Category:", bg="lightblue")
    modelLabel = Label(keyInfoFrame, text=f"Model:", bg="lightblue")

    colorLabel = Label(infoFrame, text=f"Color:", bg="lightblue")
    factoryLabel = Label(infoFrame, text=f"Factory:", bg="lightblue")
    powerSupplyLabel = Label(infoFrame, text=f"Power Supply:", bg="lightblue")

    productionYearLabel = Label(infoFrame, text=f"Production Year:", bg="lightblue")

    warrantyLabel = Label(infoFrame, text=f"Warranty:", bg="lightblue")

    if admin:
        costLabel = Label(infoFrame, text=f"Cost:", bg="lightblue")

        serviceStatusLabel = Label(infoFrame, text=f"Service Status:", bg="lightblue")

    # Table
    similarItems = getSimilarItems(category, model, admin)
    columnNames = (
        "ID",
        "Color",
        "Factory",
        "Power Supply",
        "Production Year",
        "Purchase Status",
    )
    tableScroll = Scrollbar(tableFrame)
    tableScroll.pack(side=RIGHT, fill=Y)
    table = ttk.Treeview(
        tableFrame,
        yscrollcommand=tableScroll.set,
        columns=columnNames,
        show="headings",
        selectmode="extended",
    )
    tableScroll.config(command=table.yview)
    col_width = table.winfo_width() // 6
    for name in columnNames:
        table.heading(name, text=name, anchor=CENTER)
        table.column(name, width=col_width)
    for item in similarItems:
        toInsert = (
            item["ItemID"],
            item["Color"],
            item["Factory"],
            item["PowerSupply"],
            item["ProductionYear"],
            item["PurchaseStatus"],
        )
        table.insert("", "end", text=str(item), values=toInsert)

    # Event
    table.bind("<ButtonRelease-1>", select_record)

    # Entries
    attrLabel0 = Label(selectionFrame, text="ID")
    attrLabel0.grid(row=0, column=0, padx=10, pady=10)
    attrEntry0 = Entry(selectionFrame)
    attrEntry0.grid(row=0, column=1, padx=10, pady=10)

    attrLabel1 = Label(selectionFrame, text="Color")
    attrLabel1.grid(row=0, column=2, padx=10, pady=10)
    attrEntry1 = Entry(selectionFrame)
    attrEntry1.grid(row=0, column=3, padx=10, pady=10)

    attrLabel2 = Label(selectionFrame, text="Factory")
    attrLabel2.grid(row=0, column=4, padx=10, pady=10)
    attrEntry2 = Entry(selectionFrame)
    attrEntry2.grid(row=0, column=5, padx=10, pady=10)

    attrLabel3 = Label(selectionFrame, text="Power Supply")
    attrLabel3.grid(row=1, column=0, padx=10, pady=10)
    attrEntry3 = Entry(selectionFrame)
    attrEntry3.grid(row=1, column=1, padx=10, pady=10)

    attrLabel4 = Label(selectionFrame, text="Production Year")
    attrLabel4.grid(row=1, column=2, padx=10, pady=10)
    attrEntry4 = Entry(selectionFrame)
    attrEntry4.grid(row=1, column=3, padx=10, pady=10)

    attrLabel5 = Label(selectionFrame, text="Purchase Status")
    attrLabel5.grid(row=1, column=4, padx=10, pady=10)
    attrEntry5 = Entry(selectionFrame)
    attrEntry5.grid(row=1, column=5, padx=10, pady=10)

    # Fields
    idValue = Label(keyInfoFrame, text=f"{id}", bg="lightblue")
    categoryValue = Label(keyInfoFrame, text=f"{category}", bg="lightblue")
    modelValue = Label(keyInfoFrame, text=f"{model}", bg="lightblue")

    colorValue = Label(infoFrame, text=f"{color}", bg="lightblue")
    factoryValue = Label(infoFrame, text=f"{factory}", bg="lightblue")
    powerSupplyValue = Label(infoFrame, text=f"{power_supply}", bg="lightblue")

    productionYearValue = Label(infoFrame, text=f"{production_year}", bg="lightblue")

    warrantyValue = Label(infoFrame, text=f"{warranty} month(s)", bg="lightblue")

    if admin:
        costValue = Label(infoFrame, text=f"${cost}", bg="lightblue")
        serviceStatusText = 'N/A' if service_status == "" else service_status

        serviceStatusValue = Label(infoFrame, text=f"{serviceStatusText}", bg="lightblue")

    # Buttons
    if not admin and purchase_status == "Unsold":
        buyButton = Button(
            purchaseFrame,
            text=f"Buy (${price})",
            command=buyItem,
            bg="green",
            font=(None, 16),
            fg="#ffffff",
        )

    elif purchase_status == "Unsold":
        buyButton = Button(
            purchaseFrame,
            text=f"Unsold (${price})",
            state=DISABLED,
            bg="orange",
            font=(None, 16),
            fg="#ffffff",
        )

    else:  # sold
        buyButton = Button(
            purchaseFrame,
            text=f"Sold (${price})",
            state=DISABLED,
            bg="red",
            font=(None, 16),
            fg="#ffffff",
        )

    homeButton = Button(
        buttonsFrame,
        text="Home",
        command=goHome,
        bg="blue",
        font=(None, 16),
        fg="#ffffff",
    )
    refreshButton = Button(
        buttonsFrame,
        text="Refresh",
        command=refresh,
        bg="green",
        font=(None, 16),
        fg="#ffffff",
    )

    goItemButton = Button(
        goItemFrame,
        text="Go to Item",
        command=goItem,
        bg="green",
        font=(None, 16),
        fg="#ffffff",
    )
    
    backButton = Button(
        outerFrame1,
        text="Products Page",
        command=back, bg="white",
        font=12
    )

    maintenanceButton = Button(
        outerFrame1,
        text="Maintenance Page",
        command=backMainte, bg="white",
        font=12
    )

    # Initialise
    itemPage.place(relwidth=1, relheight=1)
    outerFrame1.place(relx=0, rely=0.05, relwidth=0.4, relheight=0.95)
    outerFrame2.place(relx=0.4, rely=0.05, relwidth=0.6, relheight=0.95)

    bannerLabel.place(relheight=0.05, relwidth=1)
    Frame1.place(relx=0.05, rely=0.5, anchor=W)
    Frame2.place(relx=0.95, rely=0.5, anchor=E)

    outerTableFrame.pack(fill="x")
    tableFrame.pack(fill="x")
    selectionFrame.pack(fill="x", expand="yes")
    goItemFrame.pack(fill="y", pady=20)

    maintenanceButton.place(relx = 0.5, rely = 0.85)
    backButton.place(relx = 0.5, rely = 0.9)
    buttonsFrame.place(relx=0.05, rely=0.95, anchor=SW)
    homeButton.grid(row=0, column=0, padx=10, pady=10)
    refreshButton.grid(row=0, column=1, padx=(0, 10), pady=10)
    goItemButton.pack()
    keyInfoFrame.pack(fill=X)
    purchaseFrame.pack(fill=X)
    infoFrame.pack(fill=BOTH)
    similarItemsBannerLabel.pack(fill="x")
    table.pack(fill="x")

    idLabel.grid(row=0, column=0, sticky=W, padx=20, pady=20)
    idValue.grid(row=0, column=1, padx=20, pady=20)
    categoryLabel.grid(row=1, column=0, sticky=W, padx=20, pady=(0, 20))
    categoryValue.grid(row=1, column=1, padx=20, pady=(0, 20))
    modelLabel.grid(row=2, column=0, sticky=W, padx=20, pady=(0, 20))
    modelValue.grid(row=2, column=1, padx=20, pady=20)
    idLabel.grid(row=0, column=0, sticky=W)

    colorLabel.grid(row=0, column=0, sticky=W, padx=20, pady=10)
    colorValue.grid(row=0, column=1, padx=20, pady=10)
    factoryLabel.grid(row=1, column=0, sticky=W, padx=20, pady=10)
    factoryValue.grid(row=1, column=1, padx=20, pady=10)
    powerSupplyLabel.grid(row=2, column=0, sticky=W, padx=20, pady=10)
    powerSupplyValue.grid(row=2, column=1, padx=20, pady=10)
    productionYearLabel.grid(row=3, column=0, sticky=W, padx=20, pady=10)
    productionYearValue.grid(row=3, column=1, padx=20, pady=10)
    warrantyLabel.grid(row=4, column=0, sticky=W, padx=20, pady=10)
    warrantyValue.grid(row=4, column=1, padx=20, pady=10)

    if admin:
        costLabel.grid(row=5, column=0, sticky=W, padx=20, pady=10)
        costValue.grid(row=5, column=1, padx=20, pady=10)
        serviceStatusLabel.grid(row=6, column=0, sticky=W, padx=20, pady=10)
        serviceStatusValue.grid(row=6, column=1, padx=20, pady=10)

    buyButton.pack(fill=X, padx=10, pady=10)


#################################################################################
# 5. Request Management Page (User)
#################################################################################
def requestManagement(person):
    global requestListFrame

    # Frames
    requestPage = Frame(root)
    requestListFrame = Frame(
        requestPage, highlightbackground="black", highlightthickness=1, bg="grey"
    )

    selectionFrame = LabelFrame(requestPage, text="Record")
    buttonsFrame = LabelFrame(
        requestPage,
        text="Options",
        highlightbackground="black",
        highlightthickness=1,
        bg="grey",
    )
    requestFormFrame = LabelFrame(
        requestPage,
        text="New Request",
        highlightbackground="black",
        highlightthickness=1,
    )

    # Labels
    requestLabel = Label(
        requestPage, text=f"Request Management", bg="lightblue", relief=SUNKEN
    )

    requestLabel.place(relwidth = 1, relheight = 0.05)

    # Entries
    attrLabel0 = Label(selectionFrame, text="ID")
    attrLabel0.grid(row=0, column=0, padx=10, pady=10)
    attrEntry0 = Entry(selectionFrame)
    attrEntry0.grid(row=0, column=1, padx=10, pady=10)

    attrLabel1 = Label(selectionFrame, text="Fee ($)")
    attrLabel1.grid(row=0, column=2, padx=10, pady=10)
    attrEntry1 = Entry(selectionFrame)
    attrEntry1.grid(row=0, column=3, padx=10, pady=10)

    attrLabel2 = Label(selectionFrame, text="Date")
    attrLabel2.grid(row=0, column=4, padx=10, pady=10)
    attrEntry2 = Entry(selectionFrame)
    attrEntry2.grid(row=0, column=5, padx=10, pady=10)

    attrLabel3 = Label(selectionFrame, text="Status")
    attrLabel3.grid(row=1, column=0, padx=10, pady=10)
    attrEntry3 = Entry(selectionFrame)
    attrEntry3.grid(row=1, column=1, padx=10, pady=10)

    attrLabel4 = Label(selectionFrame, text="Item ID")
    attrLabel4.grid(row=1, column=2, padx=10, pady=10)
    attrEntry4 = Entry(selectionFrame)
    attrEntry4.grid(row=1, column=3, padx=10, pady=10)

    formLabel0 = Label(requestFormFrame, text="Item ID")
    formLabel0.grid(row=0, column=0, padx=10, pady=10)
    formEntry0 = Entry(requestFormFrame)
    formEntry0.grid(row=0, column=1, padx=10, pady=10)

    # Variables
    userID = person[0]

    # Helpers

    def displayTable():
        requests = getUserRequests(userID)
        createTable(requests)

    def createTable(requests):
        global requestListFrame
        requestListFrame.destroy()
        requestListFrame = Frame(
            requestPage, highlightbackground="black", highlightthickness=1, bg="grey"
        )
        requestListFrame.place(relx = 0.05, rely = 0.4, relwidth = 0.9, relheight = 0.55)

        columnNames = ("ID", "Fee ($)", "Date", "Status", "Item ID")
        tableScroll = Scrollbar(requestListFrame)
        tableScroll.pack(side=RIGHT, fill=Y)
        table = ttk.Treeview(
            requestListFrame,
            yscrollcommand=tableScroll.set,
            column=columnNames,
            show="headings",
            selectmode="extended",
        )
        table.place(relwidth = 1, relheight = 1)
        tableScroll.config(command=table.yview)
        for name in columnNames:
            table.heading(name, text=name, anchor=CENTER)
        if requests:
            for r in requests:
                toInsert = (r[0], r[1], r[2], r[3], int(r[4]))
                table.insert("", "end", text=str(r), values=toInsert)

        # Function
        def select_record(e):
            # delete current entry boxes
            clearEntries()
            selected = table.focus()
            attrs = table.item(selected)["values"]

            attrEntry0.insert(0, attrs[0])
            attrEntry1.insert(0, attrs[1])
            attrEntry2.insert(0, attrs[2])
            attrEntry3.insert(0, attrs[3])
            attrEntry4.insert(0, attrs[4])
        # Event
        table.bind("<ButtonRelease-1>", select_record)

    def goHome():
        requestPage.destroy()
        userHome(person)

    def getUserRequests(userID):
        query_string = f"SELECT requestID, requestFee, requestDate, requestStatus, itemID FROM Request WHERE customerID = {userID}"
        return readQuery(connection, query_string)

    def clearEntries():
        # clear entry boxes
        attrEntry0.delete(0, END)
        attrEntry1.delete(0, END)
        attrEntry2.delete(0, END)
        attrEntry3.delete(0, END)
        attrEntry4.delete(0, END)

    def makePayment():
        try:
            requestID = attrEntry0.get()
            requestFee = attrEntry1.get()
            requestStatus = attrEntry3.get()
            itemID = attrEntry4.get()
            if requestStatus == "Submitted and Waiting for payment" and float(requestFee) > 0:
                response = messagebox.askokcancel("Request payment",
                    message=f"Request Fee: ${requestFee}. Proceed to payment?"
                )
                if response:
                    date_attr = date.today().strftime('%Y-%m-%d')
                    query_string_1 = f"INSERT INTO Payment VALUES({requestID},'{date_attr}',requestFee)"

                    query_string_2 = f"UPDATE Request SET requestStatus='In progress' WHERE requestID = {requestID}"
                    executeQuery(connection, query_string_1)
                    executeQuery(connection, query_string_2)

                    collectionItem.find_one_and_update({"ItemID":{"$eq":itemID}}, {
                        "$set":{"ServiceStatus": "Waiting for approval"}
                    })
                    
                    clearEntries()
                    displayTable()

            else:
                return messagebox.showerror(title="Error", message="Payment not needed")
        except:
            return messagebox.showerror(title="Error", message="An error has occurred")

    def cancelRequest():
        try:
            requestID = attrEntry0.get()
            requestStatus = attrEntry3.get()
            itemID = attrEntry4.get()
            if requestStatus != "Approved" and requestStatus != "Canceled":
                response = messagebox.askokcancel(
                    "Cancel Request",
                    message=f"Are you sure you want to cancel request '{requestID}'?",
                )

                if response:
                    query_string_1 = f"UPDATE Request SET requestStatus='Canceled' WHERE requestID = {requestID}"
                    executeQuery(connection, query_string_1)

                    query_string_2 = f"UPDATE Item SET serviceStatus='' WHERE itemID = {itemID}"
                    executeQuery(connection, query_string_2)

                    collectionItem.find_one_and_update({"ItemID":{"$eq":itemID}}, {
                        "$set":{"ServiceStatus": ""}
                    })

                    clearEntries()
                    displayTable()
            else:
                return messagebox.showerror(
                    title="Error", message="Request cannot be canceled"
                )
        except:
            return messagebox.showerror(title="Error", message="An error has occurred")

    def viewItem():
        itemID = attrEntry4.get()
        return goToItem(person,itemID)

    def getRequestItemID():
        try:
            itemID = formEntry0.get()
            return itemID
        except:
            return messagebox.showerror(
                title="Error", message="Invalid input/data type"
            )

    def submitForm():
        itemID = getRequestItemID()
        requestForm(itemID, person)
        displayTable()
        

    # Buttons
    displayButton = Button(
        buttonsFrame, text="Refresh Table", command=displayTable, bg="white"
    )
    displayButton.grid(row=0, column=0, padx=10, pady=10)

    homeButton = Button(buttonsFrame, text="Return to Home", command=goHome, bg="blue")
    homeButton.grid(row=0, column=1, padx=10, pady=10)

    viewItemButton = Button(buttonsFrame, text="View Item", command=viewItem, bg="blue")
    viewItemButton.grid(row=0, column=2, padx=10, pady=10)

    clearEntryButton = Button(
        buttonsFrame, text="Clear Entry", command=clearEntries, bg="blue"
    )
    clearEntryButton.grid(row=0, column=3, padx=10, pady=10)

    cancelRequestButton = Button(
        buttonsFrame, text="Cancel request", command=cancelRequest, bg="red"
    )
    cancelRequestButton.grid(row=0, column=4, padx=10, pady=10)

    requestPaymentButton = Button(
        buttonsFrame, text="Make Payment", command=makePayment, bg="green"
    )
    requestPaymentButton.grid(row=0, column=5, padx=10, pady=10)

    requestFormSubmitButton = Button(
        requestFormFrame, text="Submit", command=submitForm, bg="green"
    )
    requestFormSubmitButton.grid(row=0, column=2, padx=10, pady=10)

    # Inventory Table
    def getInventoryRow(purchaseID):
        query = f"SELECT itemID, productID FROM Item WHERE purchaseID = {purchaseID}"
        res = readQuery(connection, query)[0]
        itemID, productID = int(res[0]),int(res[1])
        query_1 = f"SELECT category, model FROM Product WHERE productID = {productID}"
        res_1 = readQuery(connection, query_1)[0]
        category, model = res_1

        requiresPayment = requestRequiresPaymentValidation(itemID)
        fee = getRequestFee(itemID) if requiresPayment else 0

        return (itemID,category,model,fee)
    
    def clearFormEntry():
        formEntry0.delete(0, END)

    def select_record(e):
        # delete current entry boxes
        clearFormEntry()
        selected = myInventoryTable.focus()
        attrs = myInventoryTable.item(selected)["values"]

        formEntry0.insert(0, attrs[0])


    inventoryFrame = Frame(requestPage, highlightbackground = 'black', highlightthickness = 1)
    inventoryLabel = Label(inventoryFrame, text = "Your Items", relief = SUNKEN, bg = "orange")
    inventoryLabel.place(relwidth = 1, relheight = 0.1)
    detailNames = ['Item ID', 'Category', 'Model', 'Service Fee']
    myInventoryTable = ttk.Treeview(inventoryFrame, column=detailNames, show="headings", height=5)
    for name in detailNames:
        myInventoryTable.heading(name, text=name, anchor=CENTER)
        myInventoryTable.column(name, anchor=CENTER, stretch=NO, width=150)
    test_query = "SELECT * FROM Purchase WHERE customerID = '%s' " % (person[0])
    results = readQuery(connection, test_query)
    if len(results) != 0:
        for ele in results:
            tup = getInventoryRow(ele[0]) #ele[0] -> purchase_id
            myInventoryTable.insert("","end",text=str(ele), values=tup)
    myInventoryTable.place(relheight = 0.9, relwidth = 1, rely = 0.1)
    inventoryFrame.place(relx = 0.55, rely = 0.05, relwidth = 0.4, relheight = 0.32)
    
    myInventoryTable.bind("<ButtonRelease-1>", select_record)


    # Init
    requestPage.place(relwidth = 1, relheight = 1)
    selectionFrame.place(relx = 0.05, rely = 0.05, relwidth = 0.45)
    buttonsFrame.place(relx = 0.05, rely = 0.2, relwidth = 0.45)
    requestFormFrame.place(relx = 0.05, rely = 0.3, relwidth = 0.45)
    displayTable()


def requestForm(itemID, person):

    # variables
    userID = person[0]
    request_status = [
        "Submitted",
        "Submitted and Waiting for payment",
        "In progress",
        "Approved",
        "Canceled",
        "Completed",
    ]

    # Functions
    def itemExistsValidation(itemID):
        query_string = f"SELECT * FROM Purchase INNER JOIN Item USING(purchaseID) WHERE customerID = {userID} AND itemID = '{itemID}'"
        res = readQuery(connection, query_string)
        return len(res) != 0

    def itemHasNoPendingRequestValidation(itemID):
        query_string = f"SELECT * FROM Request WHERE requestStatus \
             IN ('Submitted', 'Submitted and Waiting for payment', 'In progress', 'Approved') AND itemID='{itemID}'"
        res = readQuery(connection, query_string)
        return len(res) == 0

    def getRequestStatus(itemID):
        requires_payment = requestRequiresPaymentValidation(itemID)
        if requires_payment:
            return request_status[1]
        else:
            return request_status[0]

    def getAdminWithLeastRequests():
        query_string = (
            f"SELECT adminID, COUNT(adminID) FROM Administrator LEFT JOIN Request USING(adminID) GROUP BY adminID ORDER BY COUNT(adminID)"
        )
        res = readQuery(connection, query_string)[0][0]
        return res

    def getNumOfRequests():
        query_string = "SELECT COUNT(*) FROM Request"
        res = readQuery(connection, query_string)[0][0]
        return res

    def commitData():
        print(itemID, userID)
        try:
            if not itemExistsValidation(itemID):
                return messagebox.showerror(
                    title="Error", message="Item does not exist or belong to user"
                )
            
            elif not itemHasNoPendingRequestValidation(itemID):
                return messagebox.showerror(
                    title="Error", message="Item has a pending request"
                )

            else:
                requestDate = date.today().strftime("%Y-%m-%d")
                requestFee = (
                    0
                    if not requestRequiresPaymentValidation(itemID)
                    else getRequestFee(itemID)
                )
                requestStatus = getRequestStatus(itemID)
                adminID = getAdminWithLeastRequests()
                requestID = getNumOfRequests() + 1

                query_string = f"INSERT INTO Request VALUES ({requestID}, {requestFee},'{requestDate}','{requestStatus}',{userID},{adminID},'{itemID}')"
                executeQuery(connection, query_string)

                collectionItem.find_one_and_update({"ItemID":{"$eq":itemID}}, {
                        "$set":{"ServiceStatus": "Waiting for approval"}
                    })
                return messagebox.showinfo(
                    title="success", message=f"Request Submitted!"
                )

        except exception as e:
            print(e)
            return messagebox.showerror(title="Error", message="System Error")

    # init
    commitData()

def requestRequiresPaymentValidation(itemID):
        def getEndDate(warranty, purchase_date):
            end_date = purchase_date + relativedelta(months=int(warranty))
            return end_date

        query_string_product_warranty = f"SELECT warranty FROM Product WHERE productID = (SELECT productID FROM Item WHERE itemID = '{itemID}')"
        query_string_purchase_date = f"SELECT purchaseDate FROM Purchase INNER JOIN Item ON Purchase.purchaseID = Item.purchaseID WHERE itemID = '{itemID}'"
        res1 = readQuery(connection, query_string_product_warranty)[0][0]
        res2 = readQuery(connection, query_string_purchase_date)[0][0]
        end_date = getEndDate(res1, res2)
        return end_date < date.today()

def getRequestFee(itemID):
        FLAT_FEE = 40
        RATE = 0.2

        query_string = f"SELECT price FROM Product INNER JOIN Item USING(productID) WHERE itemID = '{itemID}'"
        res = readQuery(connection, query_string)[0][0]

        return FLAT_FEE + RATE * res


#################################################################################
# 5. Service Management Page (Admin)
#################################################################################
def serviceManagement(person):
    global requestListFrame
    global SELECTED_ROWS

    # Frames
    requestPage = Frame(root)
    requestListFrame = Frame(
        requestPage, highlightbackground="black", highlightthickness=1, bg="grey"
    )

    selectionFrame = LabelFrame(requestPage, text="Record")
    buttonsFrame = LabelFrame(
        requestPage,
        text="Options",
        highlightbackground="black",
        highlightthickness=1,
        bg="grey",
    )
    requestFormFrame = LabelFrame(
        requestPage,
        text="New Request",
        highlightbackground="black",
        highlightthickness=1,
    )

    # Labels
    serviceLabel = Label(
        requestPage, text=f"Service Management", bg="violet", relief=SUNKEN
    )
    serviceLabel.place(relwidth = 1, relheight = 0.05)

    # Entries
    attrLabel0 = Label(selectionFrame, text="ID")
    attrLabel0.grid(row=0, column=0, padx=10, pady=10)
    attrEntry0 = Entry(selectionFrame)
    attrEntry0.grid(row=0, column=1, padx=10, pady=10)

    attrLabel1 = Label(selectionFrame, text="Fee ($)")
    attrLabel1.grid(row=0, column=2, padx=10, pady=10)
    attrEntry1 = Entry(selectionFrame)
    attrEntry1.grid(row=0, column=3, padx=10, pady=10)

    attrLabel2 = Label(selectionFrame, text="Date")
    attrLabel2.grid(row=0, column=4, padx=10, pady=10)
    attrEntry2 = Entry(selectionFrame)
    attrEntry2.grid(row=0, column=5, padx=10, pady=10)

    attrLabel3 = Label(selectionFrame, text="Status")
    attrLabel3.grid(row=1, column=0, padx=10, pady=10)
    attrEntry3 = Entry(selectionFrame)
    attrEntry3.grid(row=1, column=1, padx=10, pady=10)

    attrLabel4 = Label(selectionFrame, text="Item ID")
    attrLabel4.grid(row=1, column=2, padx=10, pady=10)
    attrEntry4 = Entry(selectionFrame)
    attrEntry4.grid(row=1, column=3, padx=10, pady=10)

    # Variables
    adminID = person[0]
    SELECTED_ROWS = []

    # Helpers

    def displayTable():
        requests = getAdminRequests(adminID)
        # requests = [{"ID":1,"Fee ($)":200.0,"Date":"31/12","Status":"no","Item ID":2}]
        createTable(requests)

    def createTable(requests):
        global requestListFrame
        global SELECTED_ROWS
        SELECTED_ROWS = []
        requestListFrame.destroy()
        requestListFrame = Frame(
            requestPage, highlightbackground="black", highlightthickness=1, bg="grey"
        )
        requestListFrame.place(relx = 0.05, rely = 0.4, relwidth = 0.9, relheight = 0.55)

        columnNames = ("ID", "Fee ($)", "Date", "Status", "Item ID")
        tableScroll = Scrollbar(requestListFrame)
        tableScroll.pack(side=RIGHT, fill=Y)
        table = ttk.Treeview(
            requestListFrame,
            yscrollcommand=tableScroll.set,
            column=columnNames,
            show="headings",
            selectmode="extended",
        )
        table.place(relwidth = 1, relheight = 1)
        tableScroll.config(command=table.yview)
        for name in columnNames:
            table.heading(name, text=name, anchor=CENTER)
        if requests:
            for r in requests:
                toInsert = (r[0], r[1], r[2], r[3], int(r[4]))
                table.insert("", "end", text=str(r), values=toInsert)

        # Function
        def select_record(e):
            global SELECTED_ROWS
            # delete current entry boxes
            clearEntries()
            SELECTED_ROWS = []
            selected = table.focus()
            attrs = table.item(selected)["values"]

            attrEntry0.insert(0, attrs[0])
            attrEntry1.insert(0, attrs[1])
            attrEntry2.insert(0, attrs[2])
            attrEntry3.insert(0, attrs[3])
            attrEntry4.insert(0, attrs[4])

        def select_records(e):
            global SELECTED_ROWS
            # delete current entry boxes
            clearEntries()
            selected = table.selection()

            # display values for first row
            attrs = table.item(selected[0])["values"]
            attrEntry0.insert(0, attrs[0])
            attrEntry1.insert(0, attrs[1])
            attrEntry2.insert(0, attrs[2])
            attrEntry3.insert(0, attrs[3])
            attrEntry4.insert(0, attrs[4])

            SELECTED_ROWS = [table.item(ele)["values"] for ele in selected]

        # Event
        table.bind("<ButtonRelease-1>", select_record)
        table.bind("<Return>", select_records)

    def goHome():
        requestPage.destroy()
        adminHome(person)

    def getAdminRequests(userID):
        query_string = f"SELECT requestID, requestFee, requestDate, requestStatus, itemID FROM Request WHERE adminID = {adminID}"
        return readQuery(connection, query_string)

    def clearEntries():
        # clear entry boxes
        attrEntry0.delete(0, END)
        attrEntry1.delete(0, END)
        attrEntry2.delete(0, END)
        attrEntry3.delete(0, END)
        attrEntry4.delete(0, END)

    def getServiceStatus(itemID):
        query_string = f"SELECT serviceStatus FROM Item WHERE itemID={itemID}"
        return readQuery(connection, query_string)[0][0]

    def approveRequest():
        try:
            if SELECTED_ROWS == []:  # only one entry
                requestID = attrEntry0.get()
                requestStatus = attrEntry3.get()
                itemID = attrEntry4.get()
                if requestStatus == "In progress" or requestStatus == "Submitted":
                    response = messagebox.askokcancel(
                        "Approve Request", message=f"Approve request #{requestID}?"
                    )
                    if response:
                        query_string_1 = f"UPDATE Request SET requestStatus='Approved' WHERE requestID = {requestID}"
                        query_string_2 = f"UPDATE Item SET serviceStatus='In progress' WHERE itemID = {itemID}"
                        executeQuery(connection, query_string_1)
                        executeQuery(connection, query_string_2)

                        collectionItem.find_one_and_update({"ItemID": {"$eq":itemID}}, {
                            "$set":{"ServiceStatus": "In progress"}
                        })

                        clearEntries()
                        displayTable()

                else:
                    return messagebox.showerror(
                        title="Error", message="Request cannot be approved"
                    )
            else:

                setOfRequestStatus = set([ele[3] for ele in SELECTED_ROWS])
                IDs = tuple(ele[0] for ele in SELECTED_ROWS)
                itemIDs = tuple(str(ele[4]) for ele in SELECTED_ROWS)
                
                #print(setOfRequestStatus)
                #print(IDs)
                #print(itemIDs)

                if setOfRequestStatus.issubset({"In progresss", "Submitted"}):
                    response = messagebox.askokcancel(
                        "Approve Requests",
                        message=f"Approve ({len(SELECTED_ROWS)}) selected requests?",
                    )
                    if response:
                        query_string_1 = f"UPDATE Request SET requestStatus='Approved' WHERE requestID IN {IDs}"
                        query_string_2 = f"UPDATE Item SET serviceStatus='In progress' WHERE itemID IN {itemIDs}"
                        executeQuery(connection, query_string_1)
                        executeQuery(connection, query_string_2)

                        collectionItem.update_many({"ItemID":{"$in":list(itemIDs)}},{
                            "$set":{"ServiceStatus": "In progress"}
                        } )

                        clearEntries()
                        displayTable()
                else:
                    return messagebox.showerror(
                        title="Error", message="Requests cannot be approved"
                    )

        except:
            return messagebox.showerror(title="Error", message="An error has occurred")

    def serviceRequest():
        try:
            if SELECTED_ROWS == []:  # only one entry
                requestID = attrEntry0.get()
                requestStatus = attrEntry3.get()
                itemID = attrEntry4.get()
                if (
                    requestStatus == "Approved"
                    and getServiceStatus(itemID) == "In progress"
                ):
                    response = messagebox.askokcancel(
                        "Service Request", message=f"Service request #{requestID}?"
                    )
                    if response:
                        query_string_1 = f"UPDATE Request SET requestStatus='Completed' WHERE requestID = {requestID}"
                        query_string_2 = f"UPDATE Item SET serviceStatus='Completed' WHERE itemID = {itemID}"
                        executeQuery(connection, query_string_1)
                        executeQuery(connection, query_string_2)

                        collectionItem.update_many({"ItemID":{"$eq":itemID}},{
                            "$set":{"ServiceStatus": "Completed"}
                        } )

                        clearEntries()
                        displayTable()

                else:
                    return messagebox.showerror(
                        title="Error", message="Request cannot be serviced"
                    )
            else:
                setOfRequestStatus = set([ele[3] for ele in SELECTED_ROWS])
                IDs = tuple(ele[0] for ele in SELECTED_ROWS)
                itemIDs = tuple(str(ele[4]) for ele in SELECTED_ROWS)
                setOfServiceStatus = set([getServiceStatus(id) for id in itemIDs])

                if setOfRequestStatus == {"Approved"} and setOfServiceStatus == {
                    "In progress"
                }:
                    response = messagebox.askokcancel(
                        "Service Requests",
                        message=f"Service ({len(SELECTED_ROWS)}) selected requests?",
                    )
                    if response:
                        query_string_1 = f"UPDATE Request SET requestStatus='Completed' WHERE requestID IN {IDs}"
                        query_string_2 = f"UPDATE Item SET serviceStatus='Completed' WHERE itemID IN {itemIDs}"
                        executeQuery(connection, query_string_1)
                        executeQuery(connection, query_string_2)

                        collectionItem.update_many({"ItemID":{"$in":list(itemIDs)}},{
                            "$set":{"ServiceStatus": "Completed"}
                        } )

                        clearEntries()
                        displayTable()
                else:
                    return messagebox.showerror(
                        title="Error", message="Requests cannot be serviced"
                    )

        except:
            return messagebox.showerror(
                title="Error", message="Service cannot be completed"
            )

    def viewItem():
        try:
            itemID = attrEntry4.get()
            return goToItem(person, itemID,  True)
        except:
            return messagebox.showerror(title="Error", message="Invalid Item ID")

    def detailStats():
        requestPage.destroy()
        goToDetails(person)

    # Buttons

    displayButton = Button(
        buttonsFrame, text="Display/Refresh Table", command=displayTable, bg="white"
    )
    displayButton.grid(row=0, column=0, padx=10, pady=10)

    homeButton = Button(buttonsFrame, text="Return to Home", command=goHome, bg="blue")
    homeButton.grid(row=0, column=1, padx=10, pady=10)

    viewItemButton = Button(buttonsFrame, text="View Item", command=viewItem, bg="blue")
    viewItemButton.grid(row=0, column=2, padx=10, pady=10)

    approveRequestButton = Button(
        buttonsFrame, text="Approve Request(s)", command=approveRequest, bg="green"
    )
    approveRequestButton.grid(row=0, column=3, padx=10, pady=10)

    serviceRequestButton = Button(
        buttonsFrame, text="Service Request(s)", command=serviceRequest, bg="green"
    )
    serviceRequestButton.grid(row=0, column=4, padx=10, pady=10)

    allDetailsButton = Button(buttonsFrame, text="Administrator Functions",
                              command=detailStats, bg="pink")
    allDetailsButton.grid(row=0, column=5, padx=10, pady=10)

    # Init
    requestPage.place(relwidth = 1, relheight = 1)
    selectionFrame.place(relx = 0.05, rely = 0.05, relwidth = 0.60)
    buttonsFrame.place(relx = 0.05, rely = 0.2, relwidth = 0.60)
    requestFormFrame.place(relx = 0.05, rely = 0.3, relwidth = 0.45)
    displayTable()

#################################################################################
# 5.1 Details and Delinquents Page
#################################################################################
def goToDetails(person):
    detailsPage = Frame(root)

    # Labels
    titleLabel = Label(detailsPage, text = "Request Summary and Delinquents", relief = SUNKEN, bg = 'violet')
    titleLabel.place(relwidth = 1, relheight = 0.05)

    delinquentLabel = Label(detailsPage, text = "Delinquent Customers", relief = SUNKEN, bg = "orange")
    delinquentLabel.place(relwidth = 0.5, relheight = 0.05, rely = 0.05)

    detailsLabel = Label(detailsPage, text = "All Incomplete Service Requests", relief = SUNKEN, bg = "Yellow")
    detailsLabel.place(relwidth=0.5, relheight=0.05, rely=0.05, relx = 0.5)

    # Delinquent Table
    delinquentFrame = Frame(detailsPage, highlightbackground = 'black', highlightthickness = 1)
    detailNames = ['customerID', 'Name', 'requestID', 'requestFee']
    dqTable = ttk.Treeview(delinquentFrame, column=detailNames, show="headings", height=5)
    for name in detailNames:
        dqTable.heading(name, text=name, anchor=CENTER)
        dqTable.column(name, anchor=CENTER, stretch=NO, width=170)
    test_query = "SELECT * FROM Request WHERE requestStatus = 'Submitted and Waiting for payment'"
    results = readQuery(connection, test_query)
    if len(results) != 0:
        for item in results:
            test_query2 = "SELECT * FROM Customer WHERE customerID = '%s' " % (item[4])
            mydetails = readQuery(connection, test_query2)[0]
            customerName = mydetails[1]
            dqTable.insert("","end",text=str(item), values=(int(item[4]),customerName, item[0],item[1]))
    dqTable.place(relheight = 1, relwidth = 1)
    delinquentFrame.place(rely = 0.1, relwidth = 0.5, relheight = 0.8)

    # Service Request Table
    serviceFrame = Frame(detailsPage, highlightbackground = 'black', highlightthickness = 1)
    serviceName = ['requestID', 'requestStatus']
    servTable = ttk.Treeview(serviceFrame, column=serviceName, show="headings", height=5)
    for name in serviceName:
        servTable.heading(name, text=name, anchor=CENTER)
        servTable.column(name, anchor=CENTER, stretch=NO, width=350)
    test_query = "SELECT * FROM Request WHERE requestStatus NOT IN ('Canceled', 'Completed')"
    results = readQuery(connection, test_query)
    if len(results) != 0:
        for item in results:
            servTable.insert("","end",text=str(item), values=(item[0], item[3]))
    servTable.place(relheight = 1, relwidth = 1)
    serviceFrame.place(rely = 0.1, relx = 0.5, relwidth = 0.5, relheight = 0.8)

    # Functions
    def back():
        detailsPage.destroy()
        serviceManagement(person)

    # Buttons
    backButton = Button(detailsPage, text = "Back to Service Management", bg = "blue", command = back, fg = "white")
    backButton.place(relx = 0.05, rely = 0.95)

    # Initialise
    detailsPage.place(relwidth = 1, relheight = 1)

#################################################################################
# 6. Sign up Page
#################################################################################
def goToSignUp():
    signUpPage = Frame(root, bg="grey")

    # Labels
    signUpLabel = Label(signUpPage, text="New User Page", bg="lightblue", relief=SUNKEN)
    signUpLabel2 = Label(signUpPage, text="Please select the user type:")

    signUpLabel.place(relwidth=1, relheight=0.05)
    signUpLabel2.place(relwidth=1, relheight=0.05, rely=0.05)

    # Functions
    def transitionPages(state):
        signUpPage.destroy()
        if state == "admin":
            adminForm()
        elif state == "user":
            userForm()
        else:
            goToLogin()

    # Buttons
    userButton = Button(
        signUpPage,
        text="User Sign-up",
        width=50,
        command=lambda: transitionPages("user"),
        bg="green",
    )
    adminButton = Button(
        signUpPage,
        text="Admin Sign-up",
        width=50,
        command=lambda: transitionPages("admin"),
        bg="green",
    )
    goBackButton = Button(
        signUpPage,
        text="Return to Sign-in",
        width=50,
        command=lambda: transitionPages(""),
        bg="blue",
    )

    userButton.place(relx=0.38, rely=0.2)
    adminButton.place(relx=0.38, rely=0.3)
    goBackButton.place(relx=0.38, rely=0.6)

    # Initialise
    signUpPage.place(relwidth=1, relheight=1)


def userForm():
    formPage = Frame(root, bg="grey")

    # Labels
    title = Label(formPage, text="User Sign Up", relief=SUNKEN, bg="lightblue")

    formLabel0 = Label(formPage, text="Set User ID: ")
    formLabel1 = Label(formPage, text="Name: ")
    formLabel2 = Label(formPage, text="Email: ")
    formLabel3 = Label(formPage, text="Phone: ")
    formLabel4 = Label(formPage, text="Address: ")
    formLabel5 = Label(formPage, text="Password: ")
    formLabel6 = Label(formPage, text="Gender: ")

    title.place(relwidth=1, relheight=0.05)
    formLabel0.place(relx=0.2, rely=0.3)
    formLabel1.place(relx=0.2, rely=0.35)
    formLabel2.place(relx=0.2, rely=0.4)
    formLabel3.place(relx=0.2, rely=0.45)
    formLabel4.place(relx=0.2, rely=0.5)
    formLabel5.place(relx=0.2, rely=0.55)
    formLabel6.place(relx=0.2, rely=0.6)

    # Functions
    def renewFields():
        formPage.destroy()
        userForm()

    def commitData():
        try:
            customerId = customerIdField.get()
            name = nameField.get()
            emailAddress = emailAddressField.get()
            phoneNumber = phoneNumberField.get()
            address = addressField.get()
            password = passwordField.get()
            gender = genderField.get()
        except:
            return messagebox.showerror(title="Error", message="Invalid type/Input")

        if customerId == "":
            return messagebox.showerror(
                title="Error", message="Customer ID cannot be empty"
            )
        if name == "":
            return messagebox.showerror(title="Error", message="Name cannot be empty")
        if emailAddress == "":
            return messagebox.showerror(
                title="Error", message="Email address cannot be empty"
            )
        if phoneNumber == "":
            return messagebox.showerror(
                title="Error", message="phoneNumber cannot be empty"
            )
        if address == "":
            return messagebox.showerror(
                title="Error", message="Address cannot be empty"
            )
        if password == "":
            return messagebox.showerror(
                title="Error", message="Password cannot be empty"
            )

        test_query = "SELECT * FROM Customer WHERE customerID = '%s' " % (customerId)
        results = readQuery(connection, test_query)

        if len(results) == 0:
            sql_query = (
                "INSERT INTO Customer VALUES ('%s', '%s','%s','%s', '%s','%s','%s')"
                % (
                    customerId,
                    name,
                    gender,
                    emailAddress,
                    phoneNumber,
                    address,
                    password,
                )
            )
            test = executeQuery(connection, sql_query)
            if test:
                return messagebox.showinfo(
                    title="success", message="Registration successful!"
                )
            else:
                return messagebox.showerror(
                    title="Error",
                    message="Commit Error, some data may be invalid",
                )
        else:
            return messagebox.showerror(
                title="Error",
                message="There is an existing customer ID, please use another ID",
            )

    def cancelForm():
        formPage.destroy()
        goToSignUp()

    # Fields
    customerId = IntVar()
    customerIdField = Entry(formPage, textvariable=customerId, width=50)
    test_query = "SELECT MAX(customerID) FROM Customer"
    value = int(readQuery(connection, test_query)[0][0]) + 1
    customerIdField.delete(0, END)
    customerIdField.insert(0, value)
    customerIdField.place(relx=0.3, rely=0.3)

    name = StringVar()
    nameField = Entry(formPage, textvariable=name, width=50)
    nameField.place(relx=0.3, rely=0.35)

    emailAddress = StringVar()
    emailAddressField = Entry(formPage, textvariable=emailAddress, width=50)
    emailAddressField.place(relx=0.3, rely=0.4)

    phoneNumber = StringVar()
    phoneNumberField = Entry(formPage, textvariable=phoneNumber, width=50)
    phoneNumberField.place(relx=0.3, rely=0.45)

    address = StringVar()
    addressField = Entry(formPage, textvariable=address, width=50)
    addressField.place(relx=0.3, rely=0.5)

    password = StringVar()
    passwordField = Entry(formPage, textvariable=password, width=50)
    passwordField.place(relx=0.3, rely=0.55)

    # Buttons
    commitButton = Button(
        formPage, text="Confirm Details", width=50, command=commitData, bg="green"
    )
    resetButton = Button(
        formPage, text="Clear all fields", width=50, command=renewFields, bg="white"
    )
    cancelButton = Button(
        formPage,
        text="Return to User type Selection",
        width=50,
        command=cancelForm,
        bg="red",
    )

    commitButton.place(relx=0.3, rely=0.7)
    resetButton.place(relx=0.3, rely=0.75)
    cancelButton.place(relx=0.3, rely=0.8)

    genderField = StringVar()
    MaleButton = Radiobutton(
        formPage,
        text="Male",
        padx=20,
        variable=genderField,
        value="Male",
        font=("Mincho", 20),
    )
    FemaleButton = Radiobutton(
        formPage,
        text="Female",
        padx=20,
        variable=genderField,
        value="Female",
        font=("Mincho", 20),
    )

    MaleButton.place(relx=0.3, rely=0.6)
    FemaleButton.place(relx=0.4, rely=0.6)

    # Initialise
    formPage.place(relwidth=1, relheight=1)


def adminForm():
    formPage = Frame(root, bg="grey")

    # Labels
    title = Label(formPage, text="User Sign Up", relief=SUNKEN, bg="lightblue")

    formLabel0 = Label(formPage, text="Set Admin ID: ")
    formLabel1 = Label(formPage, text="Name: ")
    formLabel2 = Label(formPage, text="Phone: ")
    formLabel3 = Label(formPage, text="Set Password: ")
    formLabel4 = Label(formPage, text="Gender: ")

    title.place(relwidth=1, relheight=0.05)
    formLabel0.place(relx=0.2, rely=0.3)
    formLabel1.place(relx=0.2, rely=0.35)
    formLabel2.place(relx=0.2, rely=0.4)
    formLabel3.place(relx=0.2, rely=0.45)
    formLabel4.place(relx=0.2, rely=0.5)

    # Functions
    def renewFields():
        formPage.destroy()
        adminForm()

    def commitData():
        try:
            administratorId = administratorIdField.get()
            name = nameField.get()
            phoneNumber = phoneNumberField.get()
            password = passwordField.get()
            gender = genderField.get()
        except:
            return messagebox.showerror(title="Error", message="Invalid type/Input")

        if administratorId == "":
            return messagebox.showerror(
                title="Error", message="administrator ID cannot be empty"
            )
        if name == "":
            return messagebox.showerror(title="Error", message="Name cannot be empty")
        if phoneNumber == "":
            return messagebox.showerror(
                title="Error", message="phoneNumber cannot be empty"
            )
        if password == "":
            return messagebox.showerror(
                title="Error", message="Password cannot be empty"
            )

        test_query = "SELECT * FROM Administrator WHERE adminID = '%s' " % (
            administratorId
        )
        results = readQuery(connection, test_query)

        if len(results) == 0:
            sql_query = (
                "INSERT INTO Administrator VALUES ('%s','%s','%s','%s', '%s')"
                % (administratorId, name, gender, phoneNumber, password)
            )
            test = executeQuery(connection, sql_query)
            if test:
                return messagebox.showinfo(
                    title="success", message="Registration successful!"
                )
            else:
                return messagebox.showerror(
                    title="Error",
                    message="Commit Error, some data may be invalid",
                )
        else:
            return messagebox.showerror(
                title="Error",
                message="There is an existing administrator ID, please use another ID",
            )

    def cancelForm():
        formPage.destroy()
        goToSignUp()

    # Fields
    administratorId = IntVar()
    administratorIdField = Entry(formPage, textvariable=administratorId, width=50)
    test_query = "SELECT MAX(adminID) FROM Administrator"
    value = int(readQuery(connection, test_query)[0][0]) + 1
    administratorIdField.delete(0, END)
    administratorIdField.insert(0, value)
    administratorIdField.place(relx=0.3, rely=0.3)

    name = StringVar()
    nameField = Entry(formPage, textvariable=name, width=50)
    nameField.place(relx=0.3, rely=0.35)

    phoneNumber = StringVar()
    phoneNumberField = Entry(formPage, textvariable=phoneNumber, width=50)
    phoneNumberField.place(relx=0.3, rely=0.4)

    password = StringVar()
    passwordField = Entry(formPage, textvariable=password, width=50)
    passwordField.place(relx=0.3, rely=0.45)
    # Buttons
    commitButton = Button(
        formPage, text="Confirm Details", width=50, command=commitData, bg="green"
    )
    resetButton = Button(
        formPage, text="Clear all fields", width=50, command=renewFields, bg="white"
    )
    cancelButton = Button(
        formPage,
        text="Return to User type Selection",
        width=50,
        command=cancelForm,
        bg="red",
    )

    commitButton.place(relx=0.3, rely=0.7)
    resetButton.place(relx=0.3, rely=0.75)
    cancelButton.place(relx=0.3, rely=0.8)

    genderField = StringVar()
    MaleButton = Radiobutton(
        formPage,
        text="Male",
        padx=20,
        variable=genderField,
        value="Male",
        font=("Mincho", 20),
    )
    FemaleButton = Radiobutton(
        formPage,
        text="Female",
        padx=20,
        variable=genderField,
        value="Female",
        font=("Mincho", 20),
    )

    MaleButton.place(relx=0.3, rely=0.5)
    FemaleButton.place(relx=0.4, rely=0.5)

    # Initialise
    formPage.place(relwidth=1, relheight=1)

def updateRequestTable():
    #cancel requests with payment fee after more than 10 days
    today = date.today().strftime("%Y-%m-%d")
    query_string_1 = f"UPDATE Request SET requestStatus='Canceled' WHERE requestFee > 0 AND requestStatus='Submitted and Waiting for payment' AND DATE_ADD(requestDate, INTERVAL 10 DAY) < '{today}'"
    executeQuery(connection,query_string_1)

    query_string_2 = f"SELECT itemID FROM Request WHERE requestStatus='Canceled'"
    itemIDs = readQuery(connection, query_string_2)

    for i in itemIDs:
        query_string_3 = f"UPDATE Item SET serviceStatus='' WHERE itemID='{i[0]}'"
        executeQuery(connection,query_string_3)
        collectionItem.find_one_and_update({"ItemID":{"$eq":i[0]}},{"$set": {"ServiceStatus": ""}})

    print("Request table updated")



#################################################################################
# Execute Program
updateRequestTable()
goToLogin()
root.mainloop()
