import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Evolution from "./pages/Evolution";
import Strategies from "./pages/Strategies";
import TraderDetail from "./pages/TraderDetail";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/traders/:id" element={<TraderDetail />} />
        <Route path="/evolution" element={<Evolution />} />
        <Route path="/strategies" element={<Strategies />} />
      </Route>
    </Routes>
  );
}
