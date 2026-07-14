import { Outlet } from "react-router-dom";

import { Header } from "./Header";
import { Sidebar } from "./Sidebar";

export function Layout() {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <Sidebar />
      <main style={{ flex: 1, padding: 24 }}>
        <Header />
        <Outlet />
      </main>
    </div>
  );
}
