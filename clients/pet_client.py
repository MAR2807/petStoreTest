import requests

# POST
# /pet
# Add a new pet to the store

# PUT
# /pet
# Update an existing pet

# GET
# /pet/findByStatus
# Finds Pets by status

# GET
# /pet/findByTags
# Finds Pets by tags

# GET
# /pet/{petId}
# Find pet by ID

# POST
# /pet/{petId}
# Updates a pet in the store with form data

# DELETE
# /pet/{petId}
# Deletes a pet


class PetClient:
    BASE_URL = "https://petstore.swagger.io/v2"


# this will make it easier to just create a json object in the actual test, instead of having to make an entire json body in order to use the put endpoint for example and etc.
    @staticmethod
    def make_pet_dict(
            id,
            name ="Test Pet",
            status="available",
            tag_name = "friendly"
    ):
        return{
            "id": id,
            "name": name,
            "status": status,
            "photoUrls":[],
            "tags":[
                {"id":1, "name": tag_name}
            ]
        }
        

    def get_pet_by_id(self, pet_id):
        return requests.get(
            f"{self.BASE_URL}/pet/{pet_id}",
            timeout=10,
        )

    def get_pet_by_status(self, status):
        return requests.get(
            f"{self.BASE_URL}/pet/findByStatus?status={status}",
            timeout=10,
        )


    def post_pet(self, body):
        return requests.post(
            f"{self.BASE_URL}/pet",
            json=body,
            timeout = 10
    )

    def update_pet(self, body):
        pet_body = body.copy()
        return requests.put(
            f"{self.BASE_URL}/pet",
            json=pet_body,
            timeout=10,
        )

    def delete_pet(self, pet_id):
        return requests.delete(
            f"{self.BASE_URL}/pet/{pet_id}",
            timeout=10,
        )