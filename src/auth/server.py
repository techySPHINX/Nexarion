import jwt
import datetime
import os
from flask import Flask, request
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse

server = Flask(__name__)

NEON_DB_URL = os.environ.get("NEON_DB_URL")

parsed_url = urlparse(NEON_DB_URL)

server.config["PG_HOST"] = parsed_url.hostname
server.config["PG_USER"] = parsed_url.username
server.config["PG_PASSWORD"] = parsed_url.password
server.config["PG_DB"] = parsed_url.path[1:] 
server.config["PG_PORT"] = parsed_url.port or 5432 
server.config["SSL_MODE"] = "require" 
def get_db_connection():
    conn = psycopg2.connect(
        host=server.config["PG_HOST"],
        user=server.config["PG_USER"],
        password=server.config["PG_PASSWORD"],
        dbname=server.config["PG_DB"],
        port=server.config["PG_PORT"],
        sslmode=server.config["SSL_MODE"], 
    )
    return conn

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT email, password FROM \"user\" WHERE email=%s", (auth.username,))
    user_row = cur.fetchone()
    
    if user_row:
        email = user_row["email"]
        password = user_row["password"]
        
        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers.get("Authorization")
    
    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        return "Token has expired", 403
    except jwt.InvalidTokenError:
        return "Invalid token", 403

    return decoded, 200


def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
