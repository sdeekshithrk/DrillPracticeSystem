import { useEffect, useRef, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import { ArrowLeft, Loader2 } from "lucide-react";
import axiosClient from "../utils/axiosClient";

interface Problem {
  id: string;
  title: string;
  description: string;
  topic: string;
  difficulty: string;
  answer_type: string;

  // NEW FIELDS RETURNED BY /problems/:id (backend will include these)
  status?: string;
  last_answer?: string;
}

// Symbol → Token map
const SYMBOL_MAP: Record<string, string> = {
  "¬": "NOT",
  "∧": "AND",
  "∨": "OR",
  "→": "IMPLIES",
  "↔": "IFF",
};

// Reverse mapping (for displaying last attempt)
const TOKEN_TO_SYMBOL: Record<string, string> = {
  NOT: "¬",
  AND: "∧",
  OR: "∨",
  IMPLIES: "→",
  IFF: "↔",
};

// Convert symbolic → verbal
function toVerbal(expr: string): string {
  let out = expr;
  Object.entries(SYMBOL_MAP).forEach(([symbol, token]) => {
    out = out.replace(new RegExp(`\\${symbol}`, "g"), ` ${token} `);
  });
  return out.replace(/\s+/g, " ").trim().toUpperCase();
}

// Convert verbal tokens → logical symbols
function verbalToSymbols(expr: string): string {
  let out = expr.toUpperCase();

  // replace tokens with symbols
  Object.entries(TOKEN_TO_SYMBOL).forEach(([token, symbol]) => {
    out = out.replace(new RegExp(`\\b${token}\\b`, "g"), symbol);
  });

  return out.replace(/\s+/g, " ").trim();
}

export default function SolveProblemPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const textRef = useRef<HTMLTextAreaElement | null>(null);

  const [problem, setProblem] = useState<Problem | null>(null);

  const [displayExpr, setDisplayExpr] = useState(""); // UI symbols
  const [verbalExpr, setVerbalExpr] = useState(""); // backend tokens

  const [evaluation, setEvaluation] = useState<{
    correct: boolean;
    feedback: string;
  } | null>(null);

  const [isLoading, setIsLoading] = useState(false);

  // ------------------------------------------
  // Load problem with status + last_answer
  // ------------------------------------------
  useEffect(() => {
    async function load() {
      try {
        const res = await axiosClient.get(`/problems/${id}`);
        setProblem(res.data);

        // PREPARE last_answer → SYMBOLS
        if (res.data.last_answer) {
          console.log("Previous:", res.data.last_answer);
        }

      } catch (err) {
        console.error("Error loading problem:", err);
      }
    }
    load();
  }, [id]);

  // ------------------------------------------
  // Insert symbol at caret
  // ------------------------------------------
  function insertSymbol(symbol: string) {
    const textarea = textRef.current;
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;

    const newText =
      displayExpr.slice(0, start) + symbol + displayExpr.slice(end);

    setDisplayExpr(newText);

    // move cursor
    setTimeout(() => {
      textarea.selectionStart = textarea.selectionEnd = start + symbol.length;
    }, 0);

    setVerbalExpr(toVerbal(newText));
  }

  // ------------------------------------------
  // Submit answer
  // ------------------------------------------
  async function handleSubmit() {
    if (!verbalExpr.trim()) return;
    setIsLoading(true);
    setEvaluation(null);

    try {
      const payload = {
        problem_id: id,
        student_answer: verbalExpr.trim(),
      };

      const res = await axiosClient.post("/evaluate", payload);
      setEvaluation(res.data);
    } catch (err) {
      setEvaluation({
        correct: false,
        feedback: "Server error evaluating answer.",
      });
    }

    setIsLoading(false);
  }

  if (!problem) {
    return (
      <MainLayout>
        <div className="text-gray-300 text-lg">Loading...</div>
      </MainLayout>
    );
  }

  const LOGIC_KEYS = ["¬", "∧", "∨", "→", "↔"];

  return (
    <MainLayout>
      <div className="space-y-10">

        {/* HEADER */}
        <div className="flex flex-col gap-3">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate("/practice")}
              className="
                flex items-center gap-2 px-4 py-2 
                bg-gray-800 border border-gray-700
                rounded-xl text-cyan-300 font-semibold
                hover:bg-gray-700 hover:border-cyan-400
                shadow-lg shadow-black/40 transition-all
              "
            >
              <ArrowLeft size={20} />
              Back to Practice
            </button>

            <h1 className="text-3xl font-extrabold text-white drop-shadow-lg">
              {problem.title}
            </h1>
          </div>

          {/* Topic + Difficulty + Status */}
          <div className="flex flex-wrap gap-3 mt-1">

            <span className="
              px-3 py-1 text-sm font-semibold
              bg-purple-700/30 text-purple-300
              border border-purple-400/40
              rounded-full shadow-md
            ">
              Topic: {problem.topic}
            </span>

            <span className={`
              px-3 py-1 text-sm font-semibold rounded-full border shadow-md
              ${problem.difficulty === "Easy"
                ? "bg-green-700/30 text-green-300 border-green-500/40"
                : problem.difficulty === "Medium"
                  ? "bg-yellow-700/30 text-yellow-300 border-yellow-500/40"
                  : "bg-red-700/30 text-red-300 border-red-500/40"
              }
            `}>
              Difficulty: {problem.difficulty}
            </span>

            {problem.status && (
              <span className="
                px-3 py-1 text-sm font-semibold rounded-full shadow-md
                bg-cyan-700/30 text-cyan-300 border border-cyan-500/40
              ">
                Status: {problem.status}
              </span>
            )}

          </div>

          {/* Last attempt (converted to symbols) */}
          {problem.last_answer && (
            <div className="text-gray-400 font-mono text-sm mt-1">
              Last Attempt:{" "}
              <span className="text-gray-300 font-semibold">
                {verbalToSymbols(problem.last_answer)}
              </span>
            </div>
          )}

        </div>

        {/* PROBLEM STATEMENT */}
        {/* <div className="bg-gray-800/60 border border-gray-700 rounded-2xl p-6 shadow-xl shadow-black/40">
          <p className="text-gray-300 text-lg leading-relaxed">
            {problem.description}
          </p>
        </div> */}

        <div
          className="
    bg-gray-800/70 
    border border-cyan-600/40
    rounded-2xl 
    p-8 
    shadow-xl shadow-black/40
    relative
    overflow-hidden
  "
        >
          {/* subtle glow background */}
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-900/10 via-transparent to-purple-900/10 pointer-events-none" />

          <p className="relative text-gray-100 text-xl leading-relaxed tracking-wide font-medium">
            {problem.description}
          </p>

          {/* left accent bar */}
          <div className="absolute left-0 top-0 h-full w-1 bg-cyan-500 rounded-l-xl" />
        </div>


        {/* ANSWER INPUT */}
        <div className="space-y-4">

          <label className="text-gray-300 font-semibold text-lg">
            Your Answer
          </label>

          <textarea
            ref={textRef}
            value={displayExpr}
            onChange={(e) => {
              const raw = e.target.value;
              setDisplayExpr(raw);
              setVerbalExpr(toVerbal(raw));
            }}
            placeholder="Type or use keypad…"
            className="
              w-full h-40 p-4 rounded-xl font-mono text-white text-lg
              bg-gray-900 border border-gray-700
              focus:outline-none focus:border-cyan-500
            "
          />

          {/* SYMBOL KEYPAD */}
          <div className="grid grid-cols-7 gap-3">
            {LOGIC_KEYS.map((sym) => (
              <button
                key={sym}
                onClick={() => insertSymbol(sym)}
                className="
                  py-2 text-xl font-bold
                  bg-gray-800 text-cyan-300
                  border border-gray-700 rounded-xl
                  shadow-md shadow-black/40
                  hover:bg-gray-700 hover:border-cyan-400
                  transition
                "
              >
                {sym}
              </button>
            ))}
          </div>

          {/* SUBMIT */}
          <button
            onClick={handleSubmit}
            disabled={isLoading}
            className="
              w-full py-3 mt-4
              bg-cyan-600 hover:bg-cyan-700
              rounded-xl font-semibold text-white text-lg
              shadow-xl shadow-cyan-700/40
              transition disabled:opacity-50
            "
          >
            {isLoading ? (
              <div className="flex items-center justify-center gap-2">
                <Loader2 size={20} className="animate-spin" />
                Checking…
              </div>
            ) : (
              "Submit Answer"
            )}
          </button>
        </div>

        {/* FEEDBACK */}
        {evaluation && (
          <div
            className={`
              mt-8 p-6 rounded-xl border shadow-xl
              ${evaluation.correct
                ? "bg-green-800/40 border-green-500 text-green-300"
                : "bg-red-800/40 border-red-500 text-red-300"}
            `}
          >
            <h2 className="text-2xl font-bold mb-3">
              {evaluation.correct ? "Correct!" : "Incorrect"}
            </h2>
            <p className="text-lg leading-relaxed">{evaluation.feedback}</p>
          </div>
        )}
      </div>
    </MainLayout>
  );
}
