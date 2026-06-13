import { useState } from "react";
import api from "../api/api";

function RegistrarIncidente() {
  const [form, setForm] = useState({
    sitio: "",
    tipo_incidente: "fibra_optica",
    severidad: "media",
    descripcion: "",
  });

  const [mensaje, setMensaje] = useState("");

  const manejarCambio = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const guardarIncidente = async (e) => {
    e.preventDefault();

    try {
      await api.post("/incidentes", form);
      setMensaje("Incidente registrado correctamente.");

      setForm({
        sitio: "",
        tipo_incidente: "fibra_optica",
        severidad: "media",
        descripcion: "",
      });
    } catch (error) {
      setMensaje("Error al registrar incidente.");
    }
  };

  return (
    <div>
      <h1>Registrar Incidente</h1>

      <form style={styles.form} onSubmit={guardarIncidente}>
        <label>Sitio afectado</label>
        <input
          style={styles.input}
          name="sitio"
          value={form.sitio}
          onChange={manejarCambio}
          placeholder="Ejemplo: POP Jalapa Centro"
          required
        />

        <label>Tipo de incidente</label>
        <select
          style={styles.input}
          name="tipo_incidente"
          value={form.tipo_incidente}
          onChange={manejarCambio}
        >
          <option value="fibra_optica">Fibra óptica</option>
          <option value="microondas">Microondas</option>
          <option value="sistemas_electricos">Sistemas eléctricos</option>
        </select>

        <label>Severidad</label>
        <select
          style={styles.input}
          name="severidad"
          value={form.severidad}
          onChange={manejarCambio}
        >
          <option value="baja">Baja</option>
          <option value="media">Media</option>
          <option value="alta">Alta</option>
          <option value="urgente">Urgente</option>
          <option value="critico">Crítico</option>
        </select>

        <label>Descripción</label>
        <textarea
          style={styles.textarea}
          name="descripcion"
          value={form.descripcion}
          onChange={manejarCambio}
          placeholder="Describa el problema reportado"
          required
        />

        <button style={styles.button} type="submit">
          Guardar incidente
        </button>
      </form>

      {mensaje && <p style={styles.message}>{mensaje}</p>}
    </div>
  );
}

const styles = {
  form: {
    background: "#1e293b",
    padding: "25px",
    borderRadius: "12px",
    display: "flex",
    flexDirection: "column",
    gap: "12px",
    maxWidth: "600px",
  },
  input: {
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #334155",
  },
  textarea: {
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #334155",
    minHeight: "100px",
  },
  button: {
    padding: "12px",
    borderRadius: "8px",
    border: "none",
    background: "#38bdf8",
    fontWeight: "bold",
    cursor: "pointer",
  },
  message: {
    marginTop: "15px",
    color: "#38bdf8",
  },
};

export default RegistrarIncidente;