vfrom googlesearch import search

# Taking user input
query = input("Enter your search query: ")

# Performing search
results = []
print("\nTop 10 Google Search Results:\n")
for i, result in enumerate(search(query, num_results=10), start=1):
    print(f"{i}. {result}")
    results.append(result)

# Optional: Save results to a text file
with open("google_search_results.txt", "w") as file:
    for link in results:
        file.write(link + "\n")
