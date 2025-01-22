import requests

# GraphQL endpoint
url = "http://localhost:4012/api/graphql"

# Headers
headers = {
    "Content-Type": "application/json",
    "x-csrf-token": "15b8883a96e43d2cfb4c1ddc8239dda8cc1592b9b4b252c45e2e4f1e4cefdac7",
}

# Payload
payload = {
    "query": """
    mutation ContactCreate($input: ContactInput!) {
      contactCreate(input: $input)
    }
    """,
    "variables": {
        "input": {
            "reference": "test_reference",
            "companyName": "Test Company",
            "facilityType": "Test Facility",
            "facilityName": "Test Facility Name",
            "postCode": "123456",
            "prefectureName": "Test Prefecture",
            "email": "ab.sukhee@gmail.com",
            "phoneNumber": "1234567890",
            "chargeName": "Test Name",
            "serviceName": "Test Service",
            "detailQuestion": "This is a test question."
        }
    }
}

# Execute request
response = requests.post(url, json=payload, headers=headers, cookies={'CSRF-TOKEN': '<CSRF_TOKEN>'})

# Print response
print(response.status_code)
print(response.json())
