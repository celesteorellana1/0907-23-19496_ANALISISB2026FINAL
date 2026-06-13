import { useState } from "react";
import api from "../api/api";

function RegistrarTecnico() {
  const [form, setForm] = useState({
    nombre: "",
    especialidad: "fibra_optica",
  });

  const [mensaje, setMensaje] = useState("");

  const manejarCambio = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const guardarTecnico = async (e) => {
    e.preventDefault();

    try {
      await api.post("/tecnicos", form);
      setMensaje("Técnico registrado correctamente.");

      setForm({
        nombre: "",
        especialidad: "fibra_optica",
      });
    } catch (error) {
      setMensaje("Error al registrar técnico.");
    }
  };

  return (
    <div>
      <h1>Registrar Técnico</h1>

      <form style={styles.form} onSubmit={guardarTecnico}>
        <label>Nombre del técnico</label>
        <input
          style={styles.input}
          name="nombre"
          value={form.nombre}
          onChange={manejarCambio}
          required
        />

        <label>Especialidad</label>
        <select
          style={styles.input}
          name="especialidad"
          value={form.especialidad}
          onChange={manejarCambio}
        >
          <option value="fibra_optica">Fibra óptica</option>
          <option value="microondas">Microondas</option>
          <option value="sistemas_electricos">Sistemas eléctricos</option>
        </select>

        <button style={styles.button} type="submit">
          Guardar técnico
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
    maxWidth: "500px",
  },
  input: {
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #334155",
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

export default RegistrarTecnico;