import MainLayout from "../layouts/MainLayout";
import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <MainLayout>
      <div className="space-y-3">
        <h1 className="text-2xl font-bold text-rose-300">Page not found</h1>
        <p className="text-slate-200">
          The page you&apos;re looking for doesn&apos;t exist.
        </p>
        <Link to="/" className="text-rose-300 underline">
          Go back home
        </Link>
      </div>
    </MainLayout>
  );
}
