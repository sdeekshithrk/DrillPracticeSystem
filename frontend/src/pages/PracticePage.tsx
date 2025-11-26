import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import { ListChecks, Code, Search } from "lucide-react";
import axiosClient from "../utils/axiosClient";

interface Problem {
  id: string;
  title: string;
  topic: string;
  difficulty: string;
  status: "UNATTEMPTED" | "ATTEMPTED" | "SOLVED";
}

export default function PracticePage() {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [filtered, setFiltered] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);

  const [search, setSearch] = useState("");
  const [topicFilter, setTopicFilter] = useState("ALL");
  const [difficultyFilter, setDifficultyFilter] = useState("ALL");
  const [statusFilter, setStatusFilter] = useState("ALL");

  const navigate = useNavigate();

  useEffect(() => {
    axiosClient
      .get("/problems/with-status")
      .then((res) => {
        setProblems(res.data);
        setFiltered(res.data);
      })
      .catch((err) => console.error("Error fetching problems:", err))
      .finally(() => setLoading(false));
  }, []);

  /** Filtering Logic */
  useEffect(() => {
    let list = [...problems];

    if (search.trim()) {
      const q = search.toLowerCase();
      list = list.filter(
        (p) =>
          p.title.toLowerCase().includes(q) ||
          p.topic.toLowerCase().includes(q)
      );
    }

    if (topicFilter !== "ALL") {
      list = list.filter((p) => p.topic === topicFilter);
    }

    if (difficultyFilter !== "ALL") {
      list = list.filter((p) => p.difficulty === difficultyFilter);
    }

    if (statusFilter !== "ALL") {
      list = list.filter((p) => p.status === statusFilter);
    }

    setFiltered(list);
  }, [search, topicFilter, difficultyFilter, statusFilter, problems]);

  if (loading) {
    return (
      <MainLayout>
        <div className="text-gray-300 text-xl mt-12">Loading problems...</div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* HEADER */}
        <div className="flex items-center gap-4">
          <ListChecks size={40} className="text-cyan-400 drop-shadow-md" />
          <h1 className="text-3xl font-extrabold text-white drop-shadow-lg">
            Practice Problems
          </h1>
        </div>

        {/* <p className="text-gray-400 max-w-2xl">
          Explore logic and set theory challenges. Filter, search and practice
          problems tailored to your learning.
        </p> */}

        {/* ===== SEARCH BAR ===== */}
        <div className="flex items-center gap-4 bg-gray-800/60 border border-gray-700 rounded-xl p-3 shadow-lg shadow-black/40">
          <Search className="text-gray-400" />
          <input
            type="text"
            placeholder="Search problems by title or topic..."
            className="w-full bg-transparent outline-none text-gray-200"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {/* ===== FILTERS ===== */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Topic */}
          <select
            className="bg-gray-800 border border-gray-700 rounded-xl p-3 text-gray-200 shadow-black/40 shadow"
            value={topicFilter}
            onChange={(e) => setTopicFilter(e.target.value)}
          >
            <option value="ALL">All Topics</option>
            <option value="Logic">Logic</option>
            <option value="Set Theory">Set Theory</option>
          </select>

          {/* Difficulty */}
          <select
            className="bg-gray-800 border border-gray-700 rounded-xl p-3 text-gray-200 shadow-black/40 shadow"
            value={difficultyFilter}
            onChange={(e) => setDifficultyFilter(e.target.value)}
          >
            <option value="ALL">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>

          {/* Status */}
          <select
            className="bg-gray-800 border border-gray-700 rounded-xl p-3 text-gray-200 shadow-black/40 shadow"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="ALL">All Statuses</option>
            <option value="UNATTEMPTED">Unattempted</option>
            <option value="ATTEMPTED">Attempted</option>
            <option value="SOLVED">Solved</option>
          </select>
        </div>

        {/* ===== PROBLEM LIST ===== */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filtered.map((p) => {
            const difficultyColor =
              p.difficulty === "Easy"
                ? "bg-green-600/20 text-green-400 border-green-500/40"
                : p.difficulty === "Medium"
                ? "bg-yellow-600/20 text-yellow-400 border-yellow-500/40"
                : "bg-red-600/20 text-red-400 border-red-500/40";

            const statusColor =
              p.status === "SOLVED"
                ? "text-green-400"
                : p.status === "ATTEMPTED"
                ? "text-yellow-300"
                : "text-gray-400";

            return (
              <div
                key={p.id}
                onClick={() => navigate(`/practice/${p.id}`)}
                className="
                  group
                  bg-gray-800/60 border border-gray-700/60
                  rounded-2xl p-6 cursor-pointer
                  shadow-lg shadow-black/40
                  hover:shadow-cyan-500/20 hover:border-cyan-600/40
                  hover:bg-gray-800/80
                  hover:scale-[1.03]
                  transition-all duration-200
                "
              >
                {/* TITLE */}
                <h2 className="text-xl font-bold text-white mb-1 group-hover:text-cyan-300">
                  {p.title}
                </h2>

                <p className="text-sm text-gray-400 mb-4 font-mono">
                  Topic: {p.topic}
                </p>

                <div className="flex justify-between items-center">
                  {/* Difficulty */}
                  <span
                    className={`px-3 py-1 text-xs font-semibold rounded-full border ${difficultyColor}`}
                  >
                    {p.difficulty}
                  </span>

                  {/* Status */}
                  <span className={`text-sm font-semibold ${statusColor}`}>
                    {p.status}
                  </span>

                  <Code
                    size={22}
                    className="text-gray-400 group-hover:text-cyan-300 transition"
                  />
                </div>
              </div>
            );
          })}
        </div>

        {filtered.length === 0 && (
          <div className="text-gray-400 text-center py-6">
            No problems match your filters.
          </div>
        )}
      </div>
    </MainLayout>
  );
}
