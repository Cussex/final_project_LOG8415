import requests
import argparse
import json

def insert_direct(query, gatekeeper_dns):
    try:
        response = requests.post("http://" + gatekeeper_dns + ":8080/direct", json={"query": query})
        return json.loads(response.content)
    except:
        return {"message": "Error in post direct request:" + query}
    
def select_direct(query, gatekeeper_dns):
    try:
        response = requests.get("http://" + gatekeeper_dns + ":8080/direct", json={"query": query})
        return json.loads(response.content)
    except:
        return {"message": "Error in get direct request:" + query}
    
def select_random(query, gatekeeper_dns):
    try:
        response = requests.get("http://" + gatekeeper_dns + ":8080/random", json={"query": query})
        return json.loads(response.content)
    except:
        return {"message": "Error in get random request:" + query}
    
def select_custom(query, gatekeeper_dns):
    try:
        response = requests.get("http://" + gatekeeper_dns + ":8080/custom", json={"query": query})
        return json.loads(response.content)
    except:
        return {"message": "Error in get custom request:" + query}
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("gatekeeper_dns", help="Public dns to reach the gatekeeper")
    args = parser.parse_args()
    gatekeeper_dns = args.gatekeeper_dns    

    select_actor_query = "SELECT * FROM actor WHERE first_name = 'Scarlett';"
    insert_actor_query = "INSERT INTO actor (first_name, last_name) VALUES ('John', 'Doe');"
    delete_actor_query = "DELETE FROM actor WHERE first_name = 'Scarlett' and last_name = 'Johansson';"

    print("\nSelecting from actor table using direct query")
    print(select_direct(select_actor_query, gatekeeper_dns))
    print("\nInserting into actor table using direct query")
    print(insert_direct(insert_actor_query, gatekeeper_dns))
    print("\nSelecting from actor table using random query")
    print(select_random(select_actor_query, gatekeeper_dns))
    print("\nSelecting from actor table using custom query")
    print(select_custom(select_actor_query, gatekeeper_dns))
    print("\nDeleting from actor table using direct query")
    print(insert_direct(delete_actor_query, gatekeeper_dns))

    print("\n Tests completed")

if __name__ == "__main__":
    main()


    
