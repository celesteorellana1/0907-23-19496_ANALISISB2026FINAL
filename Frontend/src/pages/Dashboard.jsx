import { useEffect, useState } from "react";
import api from "../api/api";

function Dashboard() {
  const [reporte, setReporte] = useState(null);
  const [error, setError] = useState("");

  const cargarReporte = async () => {
    try {
      const response = await api.get("/reportes/incidentes");
      setReporte(response.data);
    } catch (error) {
      setError("No se pudo cargar el reporte. Verifica que el backend esté encendido.");
    }
  };

  useEffect(() => {
    cargarReporte();
  }, []);

  return (
    <div>
      <h1>Dashboard de Incidentes</h1>
      <p>Sistema de gestión de incidentes de red para NetGuard GT.</p>

      {error && <p style={styles.error}>{error}</p>}

      {reporte && (
        <div style={styles.grid}>
          <div style={styles.card}>
            <h3>Total de incidentes</h3>
            <p style={styles.number}>{reporte.total_incidentes}</p>
          </div>

          <div style={styles.card}>
            <h3>Incidentes escalados</h3>
            <p style={styles.number}>{reporte.incidentes_escalados}</p>
          </div>

          <div style={styles.card}>
            <h3>Incidentes por estado</h3>
            {reporte.por_estado.map((item, index) => (
              <p key={index}>
                {item.estado}: <strong>{item.cantidad}</strong>
              </p>
            ))}
          </div>

          <div style={styles.card}>
            <h3>Incidentes por severidad</h3>
            {reporte.por_severidad.map((item, index) => (
              <p key={index}>
                {item.severidad}: <strong>{item.cantidad}</strong>
              </p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
    gap: "20px",
    marginTop: "25px",
  },
  card: {
    background: "#1e293b",
    padding: "20px",
    borderRadius: "12px",
    border: "1px solid #334155",
  },
  number: {
    fontSize: "40px",
    fontWeight: "bold",
    color: "#38bdf8",
  },
  error: {
    background: "#7f1d1d",
    padding: "12px",
    borderRadius: "8px",
  },
};

export default Dashboard;