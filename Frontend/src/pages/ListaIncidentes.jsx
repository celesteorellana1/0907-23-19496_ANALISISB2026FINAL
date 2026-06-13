import { useEffect, useState } from "react";
import api from "../api/api";

function ListaIncidentes() {
  const [incidentes, setIncidentes] = useState([]);
  const [tecnicos, setTecnicos] = useState([]);
  const [tecnicoSeleccionado, setTecnicoSeleccionado] = useState({});
  const [historial, setHistorial] = useState([]);
  const [incidenteHistorial, setIncidenteHistorial] = useState(null);

  const cargarDatos = async () => {
    try {
      const responseIncidentes = await api.get("/incidentes");
      const responseTecnicos = await api.get("/tecnicos");

      setIncidentes(responseIncidentes.data);
      setTecnicos(responseTecnicos.data);
    } catch (error) {
      alert("Error al cargar datos. Verifica que el backend esté encendido.");
    }
  };

  useEffect(() => {
    cargarDatos();
  }, []);

  const asignarIncidente = async (incidenteId) => {
    const tecnicoId = tecnicoSeleccionado[incidenteId];

    if (!tecnicoId) {
      alert("Seleccione un técnico.");
      return;
    }

    try {
      await api.put(`/incidentes/${incidenteId}/asignar`, {
        tecnico_id: Number(tecnicoId),
      });

      alert("Incidente asignado correctamente.");
      cargarDatos();
    } catch (error) {
      alert(error.response?.data?.detail || "Error al asignar incidente.");
    }
  };

  const cambiarEstado = async (incidenteId, nuevoEstado) => {
    try {
      await api.put(`/incidentes/${incidenteId}/estado`, {
        nuevo_estado: nuevoEstado,
      });

      alert("Estado actualizado correctamente.");
      cargarDatos();
    } catch (error) {
      alert(error.response?.data?.detail || "Error al cambiar estado.");
    }
  };

  const verHistorial = async (incidenteId) => {
    try {
      const response = await api.get(`/incidentes/${incidenteId}/historial`);
      setHistorial(response.data);
      setIncidenteHistorial(incidenteId);
    } catch (error) {
      alert("Error al cargar historial.");
    }
  };

  return (
    <div>
      <h1>Lista de Incidentes</h1>

      <table style={styles.table}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Sitio</th>
            <th>Tipo</th>
            <th>Severidad</th>
            <th>Estado</th>
            <th>Escalado</th>
            <th>Técnico</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>
          {incidentes.map((incidente) => (
            <tr key={incidente.id}>
              <td>{incidente.id}</td>
              <td>{incidente.sitio}</td>
              <td>{incidente.tipo_incidente}</td>
              <td>{incidente.severidad}</td>
              <td>{incidente.estado}</td>
              <td>{incidente.escalado ? "Sí" : "No"}</td>
              <td>{incidente.tecnico_id || "Sin asignar"}</td>
              <td>
                <select
                  style={styles.select}
                  value={tecnicoSeleccionado[incidente.id] || ""}
                  onChange={(e) =>
                    setTecnicoSeleccionado({
                      ...tecnicoSeleccionado,
                      [incidente.id]: e.target.value,
                    })
                  }
                >
                  <option value="">Seleccione técnico</option>

                  {tecnicos.map((tecnico) => (
                    <option key={tecnico.id} value={tecnico.id}>
                      {tecnico.nombre} - {tecnico.especialidad}
                    </option>
                  ))}
                </select>

                <button
                  style={styles.button}
                  onClick={() => asignarIncidente(incidente.id)}
                >
                  Asignar
                </button>

                <button
                  style={styles.button}
                  onClick={() => cambiarEstado(incidente.id, "En progreso")}
                >
                  En progreso
                </button>

                <button
                  style={styles.button}
                  onClick={() => cambiarEstado(incidente.id, "Resuelto")}
                >
                  Resuelto
                </button>

                <button
                  style={styles.button}
                  onClick={() => cambiarEstado(incidente.id, "Cerrado")}
                >
                  Cerrado
                </button>

                <button
                  style={styles.buttonSecondary}
                  onClick={() => verHistorial(incidente.id)}
                >
                  Historial
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {incidenteHistorial && (
        <div style={styles.historial}>
          <h2>Historial del incidente #{incidenteHistorial}</h2>

          {historial.map((item) => (
            <div key={item.id} style={styles.historialItem}>
              <strong>{item.accion}</strong>
              <p>{item.detalle}</p>
              <small>{new Date(item.fecha).toLocaleString()}</small>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  table: {
    width: "100%",
    borderCollapse: "collapse",
    background: "#1e293b",
    borderRadius: "12px",
    overflow: "hidden",
  },
  select: {
    padding: "8px",
    borderRadius: "6px",
    marginRight: "5px",
    marginBottom: "5px",
  },
  button: {
    padding: "8px",
    borderRadius: "6px",
    border: "none",
    background: "#38bdf8",
    fontWeight: "bold",
    marginRight: "5px",
    marginBottom: "5px",
    cursor: "pointer",
  },
  buttonSecondary: {
    padding: "8px",
    borderRadius: "6px",
    border: "none",
    background: "#22c55e",
    fontWeight: "bold",
    marginRight: "5px",
    cursor: "pointer",
  },
  historial: {
    marginTop: "30px",
    background: "#1e293b",
    padding: "20px",
    borderRadius: "12px",
  },
  historialItem: {
    borderBottom: "1px solid #334155",
    padding: "10px 0",
  },
};

export default ListaIncidentes;