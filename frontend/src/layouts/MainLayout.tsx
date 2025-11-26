import type { ReactNode } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Gauge, ListChecks, LogOut } from "lucide-react";

type MainLayoutProps = {
  children: ReactNode;
};

export default function MainLayout({ children }: MainLayoutProps) {
  const location = useLocation();
  const navigate = useNavigate();

  const isActive = (path: string) => location.pathname === path;

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login", { replace: true });
  };

  return (
    <div
      className="
        min-h-screen
        bg-gradient-to-br
        from-[#0b0f19] via-[#111827] to-[#0a0f1f]
        text-gray-200
      "
    >
      {/* ================= NAVBAR ================ */}
      <header
        className="
          sticky top-0 z-50
          bg-gray-900/80
          backdrop-blur-xl
          border-b border-gray-800/50
          shadow-[0_6px_30px_rgba(0,0,0,0.45)]
          shadow-cyan-500/20
        "
      >
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          
          {/* TITLE */}
          <span className="text-xl font-extrabold tracking-tight text-cyan-300 drop-shadow-lg">
            Logic Drill & Practice
          </span>

          {/* NAV BUTTONS */}
          <nav className="flex items-center gap-4">

            {/* DASHBOARD TAB */}
            <Link
              to="/"
              className={`
                flex items-center gap-3 px-4 py-2.5 rounded-xl
                text-base font-semibold
                transition-all duration-200 ease-out
                ${
                  isActive("/")
                    ? "bg-gray-800 text-white shadow-lg shadow-cyan-500/30 scale-[1.08]"
                    : "text-gray-300 hover:text-white hover:bg-gray-800/80 hover:shadow-lg hover:shadow-cyan-500/30 hover:scale-[1.05]"
                }
              `}
            >
              <Gauge size={22} className="text-cyan-300" />
              <span>Dashboard</span>
            </Link>

            {/* PRACTICE TAB */}
            <Link
              to="/practice"
              className={`
                flex items-center gap-3 px-4 py-2.5 rounded-xl
                text-base font-semibold
                transition-all duration-200 ease-out
                ${
                  isActive("/practice")
                    ? "bg-gray-800 text-white shadow-lg shadow-pink-500/30 scale-[1.08]"
                    : "text-gray-300 hover:text-white hover:bg-gray-800/80 hover:shadow-lg hover:shadow-pink-500/30 hover:scale-[1.05]"
                }
              `}
            >
              <ListChecks size={22} className="text-pink-300" />
              <span>Practice</span>
            </Link>

            {/* LOGOUT BUTTON - 3D Effect */}
            <button
              onClick={handleLogout}
              className="
                ml-4 flex items-center gap-2 px-4 py-2.5 
                bg-red-600/80 hover:bg-red-500
                text-white font-semibold rounded-xl
                shadow-md shadow-red-500/30
                hover:shadow-lg hover:shadow-red-500/40
                hover:scale-[1.07]
                transition-all duration-200 ease-out
              "
            >
              <LogOut size={20} className="text-white" />
              <span>Logout</span>
            </button>

          </nav>
        </div>
      </header>

      {/* ================= PAGE CONTENT ================ */}
      <main className="mx-auto max-w-7xl px-6 py-10">
        {children}
      </main>

    </div>
  );
}
