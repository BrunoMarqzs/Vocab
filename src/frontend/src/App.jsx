import React, { useEffect, useMemo, useRef, useState } from "react";

const API_BASE = typeof window !== "undefined" && window.__TERMO_API__
  ? window.__TERMO_API__
  : "http://localhost:8000";

const MAX_COLS = 5;
const MAX_TENTATIVAS = 5;

export default function App() {
  const [estado, setEstado] = useState(null);
  const [linhas, setLinhas] = useState([]); // histórico avaliado
  const [linhaAtual, setLinhaAtual] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);
  const [showShare, setShowShare] = useState(false);
  const [shareText, setShareText] = useState("");
  const [copied, setCopied] = useState(false);
  const inputRef = useRef(null);

  // -------------------------------------------------------
  // Helpers
  // -------------------------------------------------------
  const normaliza = (s) => s.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ]/g, "").toUpperCase();
  const somenteLetras5 = (s) => /^[A-ZÀ-ÖØ-Þ]{5}$/.test(s);

  const mapFeedbackToRow = (fb) =>
    fb.slice(0, MAX_COLS).map((f) => ({ letra: f.letra?.toUpperCase() ?? "", status: f.status }));

  const placeholder = useMemo(() => {
    if (!estado) return "Digite 5 letras";
    if (estado.status === "venceu") return "Você venceu!";
    if (estado.status === "perdeu") return "Tente novamente (Nova partida)";
    return "Digite 5 letras e pressione Enter";
  }, [estado]);

  // -------------------------------------------------------
  // API calls
  // -------------------------------------------------------
  async function api(path, opts = {}) {
    const url = `${API_BASE}${path}`;
    const res = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...opts,
    });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`${res.status} ${res.statusText}: ${txt}`);
    }
    return res.json();
  }

  async function iniciar() {
    setCarregando(true);
    setErro("");
    try {
      const est = await api("/api/iniciar", { method: "POST" });
      setEstado(est);
      setLinhas([]);
      setLinhaAtual("");
      requestAnimationFrame(() => inputRef.current?.focus());
    } catch (e) {
      setErro("Não foi possível iniciar o jogo. " + (e?.message ?? ""));
    } finally {
      setCarregando(false);
    }
  }

  async function carregarEstado() {
    try {
      const est = await api("/api/estado", { method: "GET" });
      setEstado(est);
    } catch {
    }
  }

  async function enviarPalpite(palpite) {
    setCarregando(true);
    setErro("");
    try {
      const resp = await api("/api/palpite", {
        method: "POST",
        body: JSON.stringify({ palpite }),
      });
      const row = mapFeedbackToRow(resp.feedback || []);
      setLinhas((prev) => [...prev, row]);
      setEstado((prev) => ({ ...prev, ...resp }));
      setLinhaAtual("");
    } catch (e) {
      setErro("Não foi possível enviar o palpite. " + (e?.message ?? ""));
    } finally {
      setCarregando(false);
      requestAnimationFrame(() => inputRef.current?.focus());
    }
  }

  async function novaPartida() {
    setCarregando(true);
    setErro("");
    try {
      const est = await api("/api/nova-partida", { method: "POST" });
      setEstado(est);
      setLinhas([]);
      setLinhaAtual("");
    } catch (e) {
      setErro("Não foi possível iniciar nova partida. " + (e?.message ?? ""));
    } finally {
      setCarregando(false);
      requestAnimationFrame(() => inputRef.current?.focus());
    }
  }

  // -------------------------------------------------------
  // Lifecycle
  // -------------------------------------------------------
  useEffect(() => {
    iniciar().then(carregarEstado);
  }, []);

  // -------------------------------------------------------
  // Handlers
  // -------------------------------------------------------
  const onChange = (e) => {
    const value = normaliza(e.target.value).slice(0, MAX_COLS);
    setLinhaAtual(value);
    setErro("");
  };

  const onKeyDown = (e) => {
    if (!estado || estado.status !== "em_andamento") return;
    if (e.key === "Enter") {
      if (!somenteLetras5(linhaAtual)) {
        setErro("Digite exatamente 5 letras (A–Z).");
        return;
      }
      enviarPalpite(linhaAtual);
    }
  };

  const podeTentar = estado?.status === "em_andamento" && (estado?.tentativas_restantes ?? 0) > 0;

  // -------------------------------------------------------
  // UI helpers
  // -------------------------------------------------------
  const classPorStatus = (s) => {
    switch (s) {
      case "correto":
        return "bg-green-600 text-white border-green-700";
      case "posicao_errada":
        return "bg-yellow-500 text-white border-yellow-600";
      case "inexistente":
        return "bg-neutral-700 text-neutral-300 border-neutral-600";
      default:
        return "bg-neutral-900 text-neutral-100 border-neutral-800";
    }
  };

  const statusMensagem = useMemo(() => {
    if (!estado) return "";
    if (estado.status === "venceu") {
      const palavraTexto = estado.palavra_secreta ? `A palavra era: ${estado.palavra_secreta}` : "";
      const pontuacaoTexto = estado.pontuacao !== undefined ? ` | Pontuação: ${estado.pontuacao}` : "";
      return `🎉 Você acertou! ${palavraTexto}${pontuacaoTexto}`;
    }
    if (estado.status === "perdeu") {
      const palavraTexto = estado.palavra_secreta ? `A palavra era: ${estado.palavra_secreta}` : "Tente outra vez.";
      const pontuacaoTexto = estado.pontuacao !== undefined ? ` | Pontuação: ${estado.pontuacao}` : "";
      return `💀 Fim de jogo. ${palavraTexto}${pontuacaoTexto}`;
    }
    return `Tentativas restantes: ${estado.tentativas_restantes ?? "-"}`;
  }, [estado]);

  // cria “linhas vazias” para completar o grid visual com 5 tentativas
  const linhasCompletas = useMemo(() => {
    const faltam = Math.max(0, MAX_TENTATIVAS - linhas.length);
    const vazia = Array.from({ length: MAX_COLS }, () => ({ letra: "", status: "vazia" }));
    return [...linhas, ...Array.from({ length: faltam }, () => vazia)];
  }, [linhas]);

  // Função para converter linhas em quadradinhos
  const emojiPorStatus = (status) => {
    switch (status) {
      case "correto": return "🟩";
      case "posicao_errada": return "🟨";
      case "inexistente": return "⬛";
      default: return "⬛";
    }
  };

  const gerarShareText = () => {
    let texto = "Joguei vocab!\n";
    for (const row of linhas) {
      texto += row.map(cell => emojiPorStatus(cell.status)).join("") + "\n";
    }
    if (estado?.pontuacao !== undefined) {
      texto += `Pontuação: ${estado.pontuacao}`;
    }
    return texto.trim();
  };

  const compartilhar = () => {
    const texto = gerarShareText();
    setShareText(texto);
    setShowShare(true);
    navigator.clipboard.writeText(texto).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    });
  };

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Cabeçalho */}
        <header className="mb-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold tracking-wide">VOCAB</h1>
          <div className="text-xs opacity-80">Jogo de Palavras</div>
        </header>

        {/* Grid de tentativas */}
        <div className="grid grid-rows-5 gap-2 mb-4">
          {linhasCompletas.map((row, rIdx) => (
            <div key={rIdx} className="grid grid-cols-5 gap-2">
              {row.map((cell, cIdx) => (
                <div
                  key={cIdx}
                  className={`h-14 flex items-center justify-center rounded-xl border text-xl font-bold ${classPorStatus(cell.status)}`}
                >
                  {cell.letra}
                </div>
              ))}
            </div>
          ))}
        </div>

        {/* Campo de entrada */}
        <div className="mb-2">
          <input
            ref={inputRef}
            type="text"
            inputMode="latin"
            autoCapitalize="characters"
            autoCorrect="off"
            disabled={!podeTentar || carregando}
            value={linhaAtual}
            onChange={onChange}
            onKeyDown={onKeyDown}
            placeholder={placeholder}
            className="w-full h-12 px-4 rounded-xl bg-neutral-900 border border-neutral-700 focus:outline-none focus:ring-2 focus:ring-sky-600 disabled:opacity-60"
            maxLength={MAX_COLS}
          />
        </div>

        {/* Ações */}
        <div className="flex items-center gap-2 mb-2">
          <button
            onClick={() => {
              if (!somenteLetras5(linhaAtual)) {
                setErro("Digite exatamente 5 letras (A–Z).");
                return;
              }
              enviarPalpite(linhaAtual);
            }}
            disabled={!podeTentar || carregando}
            className="px-4 h-10 rounded-lg bg-sky-600 hover:bg-sky-500 active:bg-sky-700 transition disabled:opacity-60"
          >
            Enviar
          </button>
          <button
            onClick={novaPartida}
            className="px-4 h-10 rounded-lg bg-neutral-800 hover:bg-neutral-700 active:bg-neutral-900 transition"
          >
            Nova partida
          </button>
          <button
            onClick={compartilhar}
            className="ml-auto px-3 h-10 rounded-lg bg-neutral-800 hover:bg-neutral-700 active:bg-neutral-900 transition"
          >
            Compartilhar
          </button>
        </div>

        {/* Resultado Final (quando jogo termina) */}
        {estado && (estado.status === "venceu" || estado.status === "perdeu") && (
          <div className={`mb-4 p-4 rounded-xl border-2 text-center ${
            estado.status === "venceu" 
              ? "bg-green-900/30 border-green-600 text-green-100" 
              : "bg-red-900/30 border-red-600 text-red-100"
          }`}>
            <div className="text-lg font-bold mb-2">
              {estado.status === "venceu" ? "🎉 PARABÉNS!" : "💀 QUE PENA!"}
            </div>
            {estado.palavra_secreta && (
              <div className="text-base mb-2 font-mono tracking-wider">
                A palavra era: <span className="font-bold text-yellow-300">{estado.palavra_secreta}</span>
              </div>
            )}
            {estado.pontuacao !== undefined && (
              <div className="text-xl font-bold">
                Pontuação: <span className="text-yellow-300">{estado.pontuacao}</span> pontos
              </div>
            )}
          </div>
        )}

        {/* Mensagens */}
        {statusMensagem && !(estado && (estado.status === "venceu" || estado.status === "perdeu")) && (
          <div className="text-sm mb-1 opacity-90">{statusMensagem}</div>
        )}
        {erro && (
          <div className="text-sm text-red-400 mb-2">{erro}</div>
        )}

        {/* Rodapé */}
        <footer className="mt-4 text-xs opacity-60">
          Como jogar: use o teclado, digite 5 letras e pressione Enter.
        </footer>

        {/* Modal de compartilhamento */}
        {showShare && (
          <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
            <div className="bg-neutral-900 p-6 rounded-xl shadow-xl max-w-xs w-full text-center relative">
              <button
                className="absolute top-2 right-2 text-neutral-400 hover:text-neutral-200"
                onClick={() => setShowShare(false)}
              >✕</button>
              <div className="mb-2 font-bold text-lg">Compartilhe seu resultado!</div>
              <pre className="bg-neutral-800 rounded p-3 text-lg mb-2 whitespace-pre-wrap">{shareText}</pre>
              <div className="text-green-400 mb-2" style={{ opacity: copied ? 1 : 0 }}>
                Copiado!
              </div>
              <button
                className="px-4 py-2 rounded bg-sky-600 hover:bg-sky-500 text-white"
                onClick={() => {
                  navigator.clipboard.writeText(shareText);
                  setCopied(true);
                  setTimeout(() => setCopied(false), 1500);
                }}
              >Copiar novamente</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
