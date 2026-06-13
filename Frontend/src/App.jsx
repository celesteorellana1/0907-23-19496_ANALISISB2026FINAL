import { Link, Route, Routes } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import RegistrarTecnico from "./pages/RegistrarTecnico";
import RegistrarIncidente from "./pages/RegistrarIncidente";
import ListaIncidentes from "./pages/ListaIncidentes";
import Reportes from "./pages/Reportes";

function App() {
  return (
    <div style={styles.app}>
      <nav style={styles.nav}>
        <h2 style={styles.logo}>NetGuard GT</h2>

        <div style={styles.links}>
          <Link style={styles.link} to="/">Dashboard</Link>
          <Link style={styles.link} to="/tecnicos">Técnicos</Link>
          <Link style={styles.link} to="/incidentes/nuevo">Nuevo incidente</Link>
          <Link style={styles.link} to="/incidentes">Incidentes</Link>
          <Link style={styles.link} to="/reportes">Reportes</Link>
        </div>
      </nav>

      <main style={styles.main}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/tecnicos" element={<RegistrarTecnico />} />
          <Route path="/incidentes/nuevo" element={<RegistrarIncidente />} />
          <Route path="/incidentes" element={<ListaIncidentes />} />
          <Route path="/reportes" element={<Reportes />} />
        </Routes>
      </main>
    </div>
  );
}

const styles = {
  app: {
    minHeight: "100vh",
    background: "#0f172a",
    color: "white",
    fontFamily: "Arial, sans-serif",
  },
  nav: {
    background: "#020617",
    padding: "18px 30px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    borderBottom: "1px solid #334155",
  },
  logo: {
    margin: 0,
    color: "#38bdf8",
  },
  links: {
    display: "flex",
    gap: "15px",
  },
  link: {
    color: "white",
    textDecoration: "none",
    fontWeight: "bold",
  },
  main: {
    padding: "30px",
  },
};

export default App;