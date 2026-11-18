pet
Everything about your Pets

Find out more


POST
/pet
Add a new pet to the store

PUT
/pet
Update an existing pet

GET
/pet/findByStatus
Finds Pets by status

GET
/pet/findByTags
Finds Pets by tags

GET
/pet/{petId}
Find pet by ID

POST
/pet/{petId}
Updates a pet in the store with form data



DELETE
/pet/{petId}
Deletes a pet



POST
/pet/{petId}/uploadImage
uploads an image


store
Access to Petstore orders



GET
/store/inventory
Returns pet inventories by status



GET
/store/order/{orderId}
Find purchase order by ID


DELETE
/store/order/{orderId}
Delete purchase order by ID


POST
/store/order
Place an order for a pet

user
Operations about user

Find out more about our store


GET
/user/logout
Logs out current logged in user session


POST
/user/createWithArray
Creates list of users with given input array


POST
/user/createWithList
Creates list of users with given input array


GET
/user/{username}
Get user by user name


PUT
/user/{username}
Updated user


DELETE
/user/{username}
Delete user


GET
/user/login
Logs user into the system


POST
/user
Create user


