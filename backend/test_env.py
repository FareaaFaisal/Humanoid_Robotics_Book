from cohere import Client

co = Client("QvVF3yX1mjT7VGCQOwcmR6BMG8pxBFPn3P6toMDk")
resp = co.embed(model="embed-english-v2.0", texts=["Hello world!"])
print(resp.embeddings)
