import requests

# GraphQL endpoint
url = "http://localhost:4012/api/graphql"

# Headers
headers = {
    "Content-Type": "application/json",
    "x-csrf-token": "64ce37142a3c4e31808e3f787c9a647ac0072df37997153d7aa799c9eb400f3c",
}

# Payload
payload = {
    "query": """
    query Posts($take: Int!, $skip: Int!) {
      posts(take: $take, skip: $skip) {
        count
        data {
          id
          title
          publishDate
          status
          privacy
        }
      }
    }
    """,
    "variables": {
        "take": 1100,
        "skip": 0
    }
}

# Execute request
response = requests.post(url, json=payload, headers=headers)

# Print response
print(response.status_code)
print(response.json())
