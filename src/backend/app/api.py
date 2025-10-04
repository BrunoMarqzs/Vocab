# api.py — FastAPI do TERMO (com CORS)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ajuste o import conforme a sua estrutura
try:
    from vocab_game import VocabGame
except ImportError:
    try:
        from src.vocab_game import VocabGame
    except ImportError:
        from backend.app.vocab_game import VocabGame  # se estiver dentro de src/backend/app

app = FastAPI()

# >>> CORS: libera chamadas do React (localhost:3000) <<<
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",  # pode deixar * enquanto desenvolve
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game = VocabGame()

class Palpite(BaseModel):
    palpite: str

@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs", "api": "/api"}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/api/iniciar")
def iniciar():
    est = game.iniciar_jogo()
    return est if isinstance(est, dict) else game.obter_estado_jogo()

@app.get("/api/estado")
def estado():
    return game.obter_estado_jogo()

@app.post("/api/palpite")
def palpite(data: Palpite):
    return game.analisar_palpite(data.palpite)

@app.post("/api/nova-partida")
def nova_partida():
    est = game.iniciar_jogo()
    return est if isinstance(est, dict) else game.obter_estado_jogo()
