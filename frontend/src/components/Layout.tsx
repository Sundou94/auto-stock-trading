import { NavLink, Outlet } from "react-router-dom";

const navItems = [
  { to: "/", label: "대시보드" },
  { to: "/evolution", label: "진화 히스토리" },
  { to: "/strategies", label: "알고리즘 라이브러리" },
];

export default function Layout() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand">Auto Stock Trading</div>
        <nav>
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </header>
      <main className="app-main">
        <Outlet />
      </main>
    </div>
  );
}
