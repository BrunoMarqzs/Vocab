import React, { useEffect, useMemo, useRef, useState } from "react";

/**
 * VOCAB — Frontend SPA
 * -------------------------------------------------------
 * ✔ Single-file React componen  //   // cria "linhas vazias" para completar o grid visual com 5 tentativasria "linhas vazias" para completar o grid visual com 5 tentativas
  const linhasCompletas = useMemo(() => {
    const faltam = Math.max(0, MAX_TENTATIVAS - linhas.length);
    const vazia = Array.from({ length: MAX_COLS }, () => ({ letra: "", status: "vazia" }));
    return [...linhas, ...Array.from({ length: faltam }, () => vazia)];
  }, [linhas]);.jsx)
 * ✔ Tailwind-only styling (no external UI libs)
 * ✔ Clean, keyboard-friendly UX (Enter/Backspace)
 * ✔ Works against a minimal REST API (spec below)
 * ✔ Graceful fallback messages & validations (5 letras A–Z)
 *
 * API EXPECTED (adapte ao seu backend Python):
 *   POST   /api/iniciar                 -> { tentativas_restantes:number, tabuleiro:[], status:"em_andamento" }
 *   GET    /api/estado                  -> { tentativas_restantes:number, tabuleiro:[Row], status:string }
 *   POST   /api/palpite { palpite }     -> {
 *                                           feedback: Array<{ letra:string, status:"correto"|"posicao_errada"|"inexistente" }>,
 *                                           tentativas_restantes:number,
 *                                           status:"em_andamento"|"venceu"|"perdeu"
 *                                         }
 *   POST   /api/nova-partida            -> { ...mesmo shape de /api/iniciar }
 *
 * Onde `tabuleiro` pode ser um array de arrays já avaliados (opcional). O frontend não depende disso; ele desenha
 * com base no que chega de `feedback` a cada palpite.
 *
 * Se quiser, você pode trocar o API_BASE para apontar pro seu backend local (ex.: http://localhost:8000).
 */

const API_BASE = typeof window !== "undefined" && window.__TERMO_API__
  ? window.__TERMO_API__
  : "http://localhost:8000"; // mude para o host do seu backend se necessário

const MAX_COLS = 5;           // 5 letras por palavra
const MAX_TENTATIVAS = 5;     // exibição (o backend devolve o valor real)

// Tipos para referência (remover se usar JSDoc):
// Celula = { letra: string; status: "correto" | "posicao_errada" | "inexistente" | "vazia" }
// FeedbackItem = { letra: string; status: "correto" | "posicao_errada" | "inexistente" }
// EstadoJogo = { tentativas_restantes: number; tabuleiro: FeedbackItem[][] | [], status: string }

export default function App() {
  const [estado, setEstado] = useState(null);
  const [linhas, setLinhas] = useState([]); // histórico avaliado
  const [linhaAtual, setLinhaAtual] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);
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
      // silencioso; a maioria dos backends devolve o estado já no /iniciar
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
      // resp esperado: { feedback, tentativas_restantes, status }
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
    if (estado.status === "venceu") return "🎉 Você acertou!";
    if (estado.status === "perdeu") return "💀 Fim de jogo. Tente outra vez.";
    return `Tentativas restantes: ${estado.tentativas_restantes ?? "-"}`;
  }, [estado]);

  // cria “linhas vazias” para completar o grid visual com 6 tentativas
  const linhasCompletas = useMemo(() => {
    const faltam = Math.max(0, MAX_TENTATIVAS - linhas.length);
    const vazia = Array.from({ length: MAX_COLS }, () => ({ letra: "", status: "vazia" }));
    return [...linhas, ...Array.from({ length: faltam }, () => vazia)];
  }, [linhas]);

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
            onClick={iniciar}
            className="ml-auto px-3 h-10 rounded-lg border border-neutral-700 hover:bg-neutral-900"
          >
            Reiniciar
          </button>
        </div>

        {/* Mensagens */}
        {statusMensagem && (
          <div className="text-sm mb-1 opacity-90">{statusMensagem}</div>
        )}
        {erro && (
          <div className="text-sm text-red-400 mb-2">{erro}</div>
        )}

        {/* Rodapé */}
        <footer className="mt-4 text-xs opacity-60">
          Dica: use o teclado — digite 5 letras e pressione Enter. Backspace edita.
        </footer>
      </div>
    </div>
  );
}
