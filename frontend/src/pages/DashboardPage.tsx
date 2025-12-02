import { useEffect, useState } from "react";
import MainLayout from "../layouts/MainLayout";
import axiosClient from "../utils/axiosClient";
import {
  Zap,
  BadgeCheck,
  CheckCircle,
  Flame,
  ArrowRight,
} from "lucide-react";

interface TopicStat {
  topic: string;
  solved: number;
  total: number;
}

interface DashboardStats {
  xp: number;
  rank: string;
  progress_percentage: number;
  problems_solved: number;
  best_streak: number;
  topic_stats: TopicStat[];
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);

  useEffect(() => {
    axiosClient
      .get("/dashboard/stats")
      .then((res) => setStats(res.data))
      .catch((err) => console.error("Dashboard load error:", err));
  }, []);

  if (!stats) {
    return (
      <MainLayout>
        <div className="text-gray-300 text-xl mt-10">Loading dashboard...</div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-10">

        {/* HEADER */}
        <h1 className="text-3xl font-extrabold text-white drop-shadow-lg">
          Your Learning Dashboard
        </h1>

        {/* STATS GRID */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          
          {/* XP CARD */}
          <StatCard
            icon={<Zap size={28} className="text-yellow-300" />}
            label="Total XP"
            value={stats.xp}
          />

          {/* RANK */}
          <StatCard
            icon={<BadgeCheck size={28} className="text-cyan-300" />}
            label="Rank"
            value={stats.rank}
          />

          {/* SOLVED */}
          <StatCard
            icon={<CheckCircle size={28} className="text-green-300" />}
            label="Problems Solved"
            value={stats.problems_solved}
          />

          {/* STREAK */}
          <StatCard
            icon={<Flame size={28} className="text-orange-400" />}
            label="Best Streak"
            value={`${stats.best_streak}`}
          />
        </div>

        {/* XP PROGRESS BAR */}
        <div className="bg-gray-800/60 p-6 rounded-2xl border border-gray-700 shadow-xl">
          <h2 className="text-xl font-bold text-white mb-3">Progress to Next Rank</h2>

          <div className="h-4 bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-cyan-400 to-emerald-400"
              style={{ width: `${stats.progress_percentage}%` }}
            />
          </div>

          <p className="text-gray-300 mt-2 text-sm">
            {stats.progress_percentage}% complete
          </p>
        </div>

        {/* TOPIC STATS */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-white">Topic-Wise Progress</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {stats.topic_stats.map((t) => {
              const pct = t.total === 0 ? 0 : Math.round((t.solved / t.total) * 100);

              return (
                <div
                  key={t.topic}
                  className="bg-gray-800/60 p-6 rounded-2xl border border-gray-700 shadow-xl"
                >
                  <h3 className="text-lg font-semibold text-white mb-2">{t.topic}</h3>

                  <div className="h-3 bg-gray-700 rounded-full overflow-hidden mb-2">
                    <div
                      className="h-full bg-gradient-to-r from-purple-400 to-pink-400"
                      style={{ width: `${pct}%` }}
                    />
                  </div>

                  <p className="text-gray-300 text-sm">
                    {t.solved} / {t.total} solved
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* QUICK ACTION BUTTONS */}
        <div className="flex gap-4 mt-6">
          <QuickActionButton label="Start Practice" link="/practice" />
        </div>
      </div>
    </MainLayout>
  );
}

/* ------------------------------
   REUSABLE COMPONENTS
--------------------------------*/

function StatCard({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string | number;
}) {
  return (
    <div
      className="
        bg-gray-800/60 border border-gray-700
        rounded-2xl p-6 shadow-xl
        hover:scale-[1.03] hover:shadow-cyan-500/20
        transition-all duration-200
      "
    >
      <div className="flex items-center gap-3 mb-2">{icon}</div>
      <div className="text-3xl font-extrabold text-white">{value}</div>
      <p className="text-gray-400 text-sm">{label}</p>
    </div>
  );
}

function QuickActionButton({ label, link }: { label: string; link: string }) {
  return (
    <a
      href={link}
      className="
        flex items-center gap-2 px-5 py-3 rounded-xl
        bg-cyan-600 hover:bg-cyan-700
        text-white font-semibold text-lg
        shadow-lg shadow-cyan-700/40
        transition-all hover:scale-[1.05]
      "
    >
      {label}
      <ArrowRight size={20} />
    </a>
  );
}
