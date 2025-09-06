from redis import Redis

from core.config import settings

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.default,
    decode_responses=True,
)


def main() -> None:
    print("Redis:", redis.ping())
    redis.set("Name", "Max")
    redis.set("Foo", "Bar")
    print("Name", redis.get("Name"))
    print("Foo", redis.getdel("Foo"))
    print("Foo", redis.get("Foo"))


if __name__ == "__main__":
    main()
