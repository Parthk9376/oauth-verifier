
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import jwt

app = FastAPI()

ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-gaogjv7o.apps.exam.local"

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt2OkH0spNjgA+2rTLbeuY
cXip/HgC6Sb9iwg3y1LA4AHHCp1tCwCSeLbvYGuC3EbNy4xfY5Cbj5DHJMD
Ekry0gyd2g3iIIBOUBj8S63UgnRpOBh9NFatFnwHeKusPUnLdu6A9cNteNpXC
WyIjG2axYfmq7i6SkUr1jknW6Y7TTAvKPujS14Otsf03h5Nepzdfp2r8oZnF
wd+zclR6BCmN0/Wfj4xyCSLBf0GqdTgW6PdaChd1V9DEZJTCV3Gk5Kq7Xfsi
SI6iyrYbKRN0EBsGgq4XkdEjsCs4F1RncS4L1gniT7GKL9Mce3b0wGLs9/7ZIX
dQIDAQAB
-----END PUBLIC KEY-----"""


class TokenRequest(BaseModel):
    token: str


@app.post("/verify")
def verify_token(body: TokenRequest):
    try:
        claims = jwt.decode(
            body.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={"require": ["iss", "aud", "exp"]},
        )

        return {
            "valid": True,
            "email": claims.get("email"),
            "sub": claims.get("sub"),
            "aud": claims.get("aud"),
        }

    except Exception:
        return JSONResponse(
            status_code=401,
            content={"valid": False},
        )
