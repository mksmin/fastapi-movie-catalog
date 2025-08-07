from redis import Redis
from core import config

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def main():
    print("Redis:", redis.ping())
    redis.set("Name", "Max")
    redis.set("Foo", "Bar")
    print("Name", redis.get("Name"))
    print("Foo", redis.getdel("Foo"))
    print("Foo", redis.get("Foo"))


if __name__ == "__main__":
    main()
