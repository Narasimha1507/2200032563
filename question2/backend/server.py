from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import time
from collections import deque

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WINDOW_SIZE = 10

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzQ3ODk0MzU1LCJpYXQiOjE3NDc4OTQwNTUsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjllMjk3ZWUxLTcxZjUtNGMxYi05YzQzLWJiMTJlZTMwMzZhMyIsInN1YiI6IjIyMDAwMzI1NjNjc2VoQGdtYWlsLmNvbSJ9LCJlbWFpbCI6IjIyMDAwMzI1NjNjc2VoQGdtYWlsLmNvbSIsIm5hbWUiOiJzYWdpIHZlbmthdGEgc2FpIG5hcmFzaW1oYSByYWp1Iiwicm9sbE5vIjoiMjIwMDAzMjU2MyIsImFjY2Vzc0NvZGUiOiJiZVRKakoiLCJjbGllbnRJRCI6IjllMjk3ZWUxLTcxZjUtNGMxYi05YzQzLWJiMTJlZTMwMzZhMyIsImNsaWVudFNlY3JldCI6IlByTXNISHJwcXRBdEhFYUUifQ.hlrMaXKh_0MnKqYpxoa_Vy7WsNis_ME8a5Gkwjql-90"
windows = {
    "p": deque(maxlen=WINDOW_SIZE),
    "f": deque(maxlen=WINDOW_SIZE),
    "e": deque(maxlen=WINDOW_SIZE),
    "r": deque(maxlen=WINDOW_SIZE),
}
SOURCE_URLS = {
    "p": "http://20.244.56.144/evaluation-service/primes",
    "f": "http://20.244.56.144/evaluation-service/fibo",
    "e": "http://20.244.56.144/evaluation-service/even",
    "r": "http://20.244.56.144/evaluation-service/rand",
}
@app.get("/numbers/{numberid}")
async def get_numbers(numberid: str):
    if numberid not in windows:
        return JSONResponse(status_code=404, content={"error": "Invalid number ID"})

    prev_window = list(windows[numberid])
    url = SOURCE_URLS[numberid]

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    try:
        async with httpx.AsyncClient(timeout=0.5) as client:
            start = time.time()
            response = await client.get(url, headers=headers)
            duration = time.time() - start

            if response.status_code != 200:
                print(f"API error {response.status_code}: {response.text}")
                raise Exception("Bad response")

            if duration > 0.5:
                print("Request timeout exceeded 500ms")
                raise Exception("Timeout")

            data = response.json().get("numbers", [])

            for num in data:
                if num not in windows[numberid]:
                    windows[numberid].append(num)

    except Exception as e:
        print(f"Fetch failed for {numberid}: {str(e)}")
        return {
            "windowPrevState": prev_window,
            "windowCurrState": list(windows[numberid]),
            "numbers": list(windows[numberid]),
            "avg": round(sum(windows[numberid]) / len(windows[numberid]), 2) if windows[numberid] else 0
        }

    curr_window = list(windows[numberid])
    return {
        "windowPrevState": prev_window,
        "windowCurrState": curr_window,
        "numbers": curr_window,
        "avg": round(sum(curr_window) / len(curr_window), 2) if curr_window else 0
    }
