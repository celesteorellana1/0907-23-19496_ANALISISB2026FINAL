import { useEffect, useState } from "react";
import api from "../api/api";

function Reportes() {
  const [reporte, setReporte] = useState(null);

  const cargarReporte = async () => {
    try {
      const response = await api.get("/reportes/incidentes");
      setReporte(response.data);
    } catch (error) {
      alert("Error al cargar reporte.");
    }
  };

  useEffect(() => {
    cargarReporte();
  }, []);

  if (!reporte) {
    return <p>Cargando reporte...</p>;
  }

  return (
    <div>
      <h1>Reportes de Incidentes</h1>

      <div style={styles.card}>
        <h2>Resumen general</h2>
        <p>Total de incidentes: {reporte.total_incidentes}</p>
        <p>Incidentes escalados: {reporte.incidentes_escalados}</p>
      </div>

      <div style={styles.card}>
        <h2>Incidentes por estado</h2>
        {reporte.por_estado.map((item, index) => (
          <p key={index}>
            {item.estado}: <strong>{item.cantidad}</strong>
          </p>
        ))}
      </div>

      <div style={styles.card}>
        <h2>Incidentes por severidad</h2>
        {reporte.por_severidad.map((item, index) => (
          <p key={index}>
            {item.severidad}: <strong>{item.cantidad}</strong>
          </p>
        ))}
      </div>

      <div style={styles.card}>
        <h2>Incidentes por técnico</h2>

        {reporte.por_tecnico.length === 0 && (
          <p>No hay incidentes asignados todavía.</p>
        )}

        {reporte.por_tecnico.map((item, index) => (
          <p key={index}>
            {item.tecnico}: <strong>{item.cantidad}</strong>
          </p>
        ))}
      </div>

      <div style={styles.card}>
        <h2>SLA por severidad</h2>

        {Object.entries(reporte.sla_horas_por_severidad).map(
          ([severidad, horas]) => (
            <p key={severidad}>
              {severidad}: <strong>{horas} horas</strong>
            </p>
          )
        )}
      </div>
    </div>
  );
}

const styles = {
  card: {
    background: "#1e293b",
    padding: "20px",
    borderRadius: "12px",
    border: "1px solid #334155",
    marginBottom: "20px",
  },
};

export default Reportes;