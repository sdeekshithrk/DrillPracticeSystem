import MainLayout from "../layouts/MainLayout";

export default function HomePage() {
  return (
    <MainLayout>
      <section className="space-y-4">
        <h1 className="text-3xl font-bold text-rose-300">
          Welcome to the Logic & Set Theory Drill System
        </h1>
        <p className="text-slate-200 max-w-2xl">
          This web app will give you small, focused practice problems in logic
          and set theory, check your answers automatically, and provide
          immediate feedback so you can spot and fix mistakes quickly.
        </p>
        <p className="text-sm text-slate-400">
          Use the <span className="font-semibold text-rose-300">Practice</span>{" "}
          tab to start solving problems once we hook up the backend.
        </p>
      </section>
    </MainLayout>
  );
}
