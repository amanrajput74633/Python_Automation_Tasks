import requests

url = 'https://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf'

filename = 'downloaded_code_file.pdf'

try:
  
    response = requests.get(url)
    response.raise_for_status()  

    with open(filename, 'wb') as file:
        file.write(response.content)

    print(f"File downloaded successfully and saved as '{filename}'.")

except requests.exceptions.RequestException as e:
    print("Error downloading the file:",e)