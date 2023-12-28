import requests
import argparse
import json

# Post direct insert queries to the gatekeeper
def insert_direct(query, gatekeeper_dns):
    try:
        response = requests.post("http://" + gatekeeper_dns + ":8080/direct", json={"query": query})
        return json.loads(response.content)
    except:
        return {"message": "Error in post direct request:" + query}

# Get direct select queries from the gatekeeper
def select_direct(query, gatekeeper_dns):
    try:
        response = requests.get("http://" + gatekeeper_dns + ":8080/direct", json={"query": query})
        return json.loads(response.content)
    except:
        return {"message": "Error in get direct request:" + query}

# Get random select queries from the gatekeeper
def select_random(query, gatekeeper_dns):
    try:
        response = requests.get("http://" + gatekeeper_dns + ":8080/random", json={"query": query})
        return json.loads(response.content)
    except:
        return {"message": "Error in get random request:" + query}

# Get custom select queries from the gatekeeper
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

    select_actor_query = "SELECT * FROM actor WHERE first_name = 'JENNIFER' and last_name = 'DAVIS';"
    select_actor_query2 = "SELECT * FROM actor WHERE first_name = 'JOHN' and last_name = 'DOE';"
    insert_actor_query = "INSERT INTO actor (first_name, last_name) VALUES ('JOHN', 'DOE');"
    delete_actor_query = "DELETE FROM actor WHERE first_name = 'JENNIFER' and last_name = 'DAVIS';"

    # Should work
    print("\nSelecting from actor table using direct query (Should work : selecting JENNIFER DAVIS)")
    print(select_direct(select_actor_query, gatekeeper_dns))
    # Should work but empty response
    print("\nSelecting from actor table using direct query (Should work but empty response : selecting JOHN DOE)")
    print(select_direct(select_actor_query2, gatekeeper_dns))
    # Should work
    print("\nInserting into actor table using direct query (Should work : inserting JOHN DOE)")
    print(insert_direct(insert_actor_query, gatekeeper_dns))
    # Should work
    print("\nSelecting from actor table using random query (Should work : selecting JENNIFER DAVIS)")
    print(select_random(select_actor_query, gatekeeper_dns))
    # Should work
    print("\nSelecting from actor table using custom query (Should work : selecting JENNIFER DAVIS)")
    print(select_custom(select_actor_query, gatekeeper_dns))
    # Should work
    print("\nSelecting from actor table using custom query (Should work : selecting JOHN DOE)")
    print(select_custom(select_actor_query2, gatekeeper_dns))
    # Shouldn't work
    print("\nDeleting from actor table using direct query")
    print(insert_direct(delete_actor_query, gatekeeper_dns))

    print("\n Tests completed")

if __name__ == "__main__":
    main()


    
