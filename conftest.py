import random

import pytest
from clients.pet_client import PetClient

@pytest.fixture
def pet_client():
    return PetClient()

@pytest.fixture
def random_id():
    return random.randint(100000000000000000, 922337203685477580)

# This will create a new pet and supply it to the test at runtime, and then delete the pet with that ID when test ends
@pytest.fixture
def created_pet(pet_client, random_id):
    pet_id = random_id
    new_pet_body = pet_client.make_pet_dict(
            id=pet_id,
            name ="Tesla",
            status="available",
            tag_name = "friendly"
        )
    
    pet_client.post_pet(new_pet_body).raise_for_status()

    yield pet_id

    lookup_response = pet_client.get_pet_by_id(pet_id)
    if lookup_response.status_code == 200:
        cleanup_response = pet_client.delete_pet(pet_id)
        assert cleanup_response.status_code in (200, 404), (
            f"Expected cleanup to delete the pet or find it already deleted, "
            f"but got {cleanup_response.status_code}: {cleanup_response.text}"
        )

    

