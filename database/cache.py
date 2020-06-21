import redis

client = redis.Redis(host="localhost", port=6379)

client.set("test-key", "test-value")

# get a value
value = client.get("test-key")
print(value)

client.delete("test-key")

# get a value
value = client.get("test-key")
print(value)
