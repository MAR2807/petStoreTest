
# create directory, create initial pytest file, inside directory install python, pytest and requests
# run tests like this: python -m pytest swaggerTest.py
# find out what each end point returns, validate response code, if it returns data validate the data, if it deletes, validate the delete by hitting get, if it updates validate the updated using get endpoint and etc.


# import requests

import pytest


BASE_URL = "https://petstore.swagger.io/v2"


## Testing POST endpoint 3 tests ##

def test_create_pet( random_id, pet_client):

    # new pet info
    pet_id = random_id
    pet_name = "Luna"
    pet_status = "available"
    pet_tag_name = "shy"

    # create a pet dict to use in post req
    new_pet = pet_client.make_pet_dict(
        id = pet_id,
        name = pet_name,
        status = pet_status,
        tag_name = pet_tag_name
    )

    try:
        # make post req
        response = pet_client.post_pet(new_pet)

        # validate 200 response
        assert response.status_code == 200

        # do another get to verify addition persisted
        response = pet_client.get_pet_by_id(pet_id)
        # validate response code
        assert response.status_code == 200

        created_pet = response.json()

        # validate all new fields
        assert created_pet["id"] == pet_id
        assert created_pet["name"] == pet_name
        assert created_pet["status"] == pet_status

        # delete created pet
        response = pet_client.delete_pet(pet_id)
        assert response.status_code == 200

        # verify its gone
        response = pet_client.get_pet_by_id(pet_id)
        assert response.status_code == 404
    finally:
        pet_client.delete_pet(pet_id)

    


@pytest.mark.xfail(
    reason="Live Petstore API accepts missing name and returns 200",
    strict=False,
)
def test_creating_pet_with_missing_fields(random_id, pet_client):
    # This test will fail on purpose!
    # This test should assert that we recieve a 400 series error according to the documentation it should not allow a body with a missing field like name, 
    # however in reality the api actually allows for missing fields and returns a 200, not sure why.

    # new pet fields
    pet_id = random_id
    # pet_name = "Garfield"  This field will be missing(commented out on purpose)
    pet_status = "pending"
    pet_tags = "chunky"

    try:
        # create pet dict
        new_pet = {
            "id": pet_id,
            "status": pet_status,
            "photoUrls": [],
            "tags": [
                {"id": 1, "name": pet_tags}
            ],
        }

        response = pet_client.post_pet(new_pet)

        # verify 400 response (bad request)
        assert response.status_code == 400

        # make get request with ID, make sure it did not create a pet with missing name
        response = pet_client.get_pet_by_id(pet_id)

        assert response.status_code == 404

    finally:
        # cleanup runs whether an assertion passes or fails
        pet_client.delete_pet(pet_id)


@pytest.mark.xfail(
    reason="Live Petstore API returns 500 for a string pet ID",
    strict=False,
)
def test_invalid_body_argument(pet_client):
    # this test will also fail, due to another bug
    # this test expects the API to return a 400 or 405 for invalid input, however the api returns 500 error
    # create pet with invalid data in a field
    pet_id = "wrong_input"
    pet_name = "garfield"
    pet_status = "available"
    pet_tags = "cool"

    new_pet_dict = pet_client.make_pet_dict(
        id = pet_id,
        name = pet_name,
        status = pet_status,
        tag_name = pet_tags
    )

    response = pet_client.post_pet(new_pet_dict)

    #validate 400 or 405 response
    assert response.status_code == 400 or response.status_code == 405



    
## Testing GET endpoint n tests ##

# 2 endpoints to test:
# 1. /pet/findByStatus
# 2. /pet{petID}

# for pet/{petID}:
# create a test validate correct pet is returned
# create a test make sure invalid pet_id returns an error like 404
# create a test make sure invalid pet_id argument returns an error

def test_get_pet_by_id(created_pet,pet_client):
    pet_id = created_pet

    # get the created pet
    response = pet_client.get_pet_by_id(pet_id)
    # verify 200 response
    assert response.status_code == 200

    # verify other fields(idk if this is necessary, could also just check they are not blank)
    original_pet = response.json()
    assert original_pet["name"] == "Tesla"
    assert original_pet["status"] == "available"
    assert original_pet["tags"][0]["name"] == "friendly"


def test_get_invalid_pet_id(pet_client, random_id):
    # make get call
    response = pet_client.get_pet_by_id(random_id)
    # assert 404
    assert response.status_code == 404


def test_invalid_pet_id(pet_client):
    invalid_pet_id = "wrong_format"

    response = pet_client.get_pet_by_id(invalid_pet_id)
   
    # The live API classifies this route format as not found.
    assert response.status_code == 404

# for get /pet/findByStatus
def test_pet_by_status(pet_client):
    statuses = ["available", "pending", "sold"]

    for status in statuses:
        response = pet_client.get_pet_by_status(status)
        assert response.status_code == 200

        pets = response.json()

        assert isinstance(pets, list), (
            f"Expected a list of pets, but got {type(pets).__name__}"
        )

        #verify all pets have correct status
        assert all(pet["status"] == status for pet in pets), (
            f'Expected every pet to have status "{status}", but got '
            f"{[pet.get('status') for pet in pets]}"
        )



## Testing PUT endpoint n tests ##

def test_update_pet_name(pet_client, created_pet):

    # use fixture to get an existing pet supplied by DI at runtime
    pet_id = created_pet
    response = pet_client.get_pet_by_id(pet_id)
    assert response.status_code == 200, (
        f"Expected pet lookup status 200, but got "
        f"{response.status_code}: {response.text}"
    )

    original_pet = response.json()
    # save original pet info so we can verify later
    original_name = original_pet["name"]
    original_status = original_pet["status"]
    original_tags = original_pet["tags"]


    #modify the name:
    original_pet["name"] = "Yuki"

    # Send PUT request with updated pet name
    response = pet_client.update_pet(original_pet)
    assert response.status_code == 200, (
        f"Expected pet update status 200, but got "
        f"{response.status_code}: {response.text}"
    )

    # Get the pet again to verify changes persisted
    response = pet_client.get_pet_by_id(pet_id)
    assert response.status_code == 200, (
        f"Expected updated pet lookup status 200, but got "
        f"{response.status_code}: {response.text}"
    )

    updated_pet = response.json()

    # assert name is updated:
    assert updated_pet["name"] == "Yuki", (
        f'Expected pet name "Yuki", but got "{updated_pet["name"]}"'
    )
    assert updated_pet["name"] != original_name, (
        f'Expected pet name to change from "{original_name}", '
        f'but it remained "{updated_pet["name"]}"'
    )
    # now assert that the original values are not changed
    assert updated_pet["status"] == original_status, (
        f"Expected status {original_status}, but got {updated_pet['status']}"
    )
    assert updated_pet["tags"] == original_tags, (
        f"Expected tags {original_tags}, but got {updated_pet['tags']}"
    )

def test_update_pet_status(created_pet, pet_client):
    pet_id = created_pet

    # get original pet json
    response = pet_client.get_pet_by_id(pet_id)
    assert response.status_code == 200

    original_pet = response.json()
    # save original pet info so we can verify later
    original_id = original_pet["id"]
    original_name = original_pet["name"]
    original_status = original_pet["status"]
    original_tags = original_pet["tags"]


    new_pet_status = "pending"
    
    #modify the status:
    original_pet["status"] = new_pet_status


    response = pet_client.update_pet(original_pet)
    assert response.status_code == 200

    # assert
    response = pet_client.get_pet_by_id(pet_id)
    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code}: {response.text}"
    )
    new_updated_pet = response.json()

    # assert new ID
    assert new_updated_pet["id"] == original_id

    # assert other fields are unchanged
    assert new_updated_pet["name"] == original_name
    assert new_updated_pet["status"] == new_pet_status
    assert new_updated_pet["tags"] == original_tags


    # test delete endpoint

def test_delete_pet(pet_client, random_id):
    pet_id = random_id
    pet_name = "Jackson"
    pet_status = "pending"

    new_pet = pet_client.make_pet_dict(
        id = pet_id,
        name = pet_name,
        status = pet_status
    )

    try:
        # create the pet
        response = pet_client.post_pet(new_pet)
        assert response.status_code == 200

        # get the pet
        response = pet_client.get_pet_by_id(pet_id)
        assert response.status_code == 200

        # now delete it
        response = pet_client.delete_pet(pet_id)
        assert response.status_code == 200

        # assert pet is gone
        response = pet_client.get_pet_by_id(pet_id)
        assert response.status_code == 404
    finally:
        pet_client.delete_pet(pet_id)

def test_delete_nonexistent_pet(pet_client, random_id):
    pet_id = random_id

    response = pet_client.delete_pet(pet_id)

    assert response.status_code == 404, (
        f"Expected 404, got {response.status_code}: {response.text}"
    )

    assert response.text == "", (
        f"Expected an empty 404 response body, got {response.text!r}"
    )
    
    



    


