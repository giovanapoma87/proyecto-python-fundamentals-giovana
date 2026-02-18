import streamlit as st
import pandas as pd
from functools import reduce

st.set_page_config(page_title="Proyecto Python Fundamentals", layout="centered")

# Guardar datos entre pantallas
if "actividades" not in st.session_state:
    st.session_state.actividades = []

# Menú lateral
menu = st.sidebar.selectbox(
    "Navegación",
    ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"]
)

# HOME
if menu == "Home":
    st.title("📊 Proyecto Aplicado – Python Fundamentals")
    st.caption("Aplicación desarrollada con Streamlit | Control simple de presupuesto y actividades")

    st.write("**Nombre del estudiante:** Giovana Felicitas Poma Garibay")
    st.write("**Curso / Módulo:** Especialización en Python for Analytics – Módulo 1 (Python Fundamentals)")
    st.write("**Año:** 2026")

    st.write(
        "Objetivo: Desarrollar una app sencilla en Streamlit para practicar variables, estructuras de datos, "
        "condicionales, funciones, programación funcional y POO."
    )

    st.subheader("Tecnologías utilizadas")
    st.write("- Python")
    st.write("- Streamlit")
    st.write("- Pandas")

    st.info("Usa el menú lateral para navegar por los ejercicios.")

# EJERCICIO 1
elif menu == "Ejercicio 1":
    st.title("🧾 Ejercicio 1 – Variables y Condicionales")
    st.write("Ingresa el presupuesto y gasto; el sistema calcula el saldo y valida si excede el presupuesto.")

    nombre = st.text_input("Nombre del proyecto/actividad")
    presupuesto_total = st.number_input("Presupuesto total", min_value=0.0, step=10.0, value=0.0, format="%.2f")
    gasto_mensual = st.number_input("Gasto mensual", min_value=0.0, step=10.0, value=0.0, format="%.2f")

    if st.button("Calcular"):
        if nombre.strip() == "":
            st.warning("⚠️ Ingresa el nombre del proyecto/actividad.")
        else:
            saldo = presupuesto_total - gasto_mensual
            st.subheader("Resultado")
            st.write(f"**Proyecto/Actividad:** {nombre.strip()}")
            st.write(f"**Saldo:** {saldo:.2f}")

            if gasto_mensual <= presupuesto_total:
                st.success("✅ Estás dentro del presupuesto.")
            else:
                st.warning("⚠️ El gasto excede el presupuesto.")

# EJERCICIO 2
elif menu == "Ejercicio 2":
    st.title("🗂️ Ejercicio 2 – Listas y Diccionarios")
    st.write("Registro de actividades usando una lista de diccionarios.")

    st.subheader("Registrar nueva actividad")

    with st.form("form_actividad", clear_on_submit=True):
        nombre = st.text_input("Nombre de la actividad", placeholder="Ej: Marketing, Publicidad, Operaciones")
        tipo = st.selectbox("Tipo", ["Operativa", "Comercial", "Administrativa", "Otro"])

        presupuesto = st.number_input("Presupuesto asignado", min_value=0.0, step=10.0, value=0.0, format="%.2f")
        gasto_real = st.number_input("Gasto real", min_value=0.0, step=10.0, value=0.0, format="%.2f")

        guardar = st.form_submit_button("Agregar actividad")

    if guardar:
        if nombre.strip() == "":
            st.warning("⚠️ Ingresa un nombre de actividad antes de agregar.")
        else:
            estado = "OK" if gasto_real <= presupuesto else "EXCEDIDO"
            st.session_state.actividades.append(
                {
                    "Actividad": nombre.strip(),
                    "Tipo": tipo,
                    "Presupuesto": float(presupuesto),
                    "Gasto Real": float(gasto_real),
                    "Estado": estado
                }
            )
            st.success("✅ Actividad agregada correctamente.")

    st.divider()
    st.subheader("Actividades registradas")

    if not st.session_state.actividades:
        st.info("Aún no hay actividades registradas. Agrega la primera usando el formulario.")
    else:
        df = pd.DataFrame(st.session_state.actividades)
        st.dataframe(df, use_container_width=True)

        st.subheader("Estado por actividad")

        for a in st.session_state.actividades:
            if float(a["Gasto Real"]) <= float(a["Presupuesto"]):
                st.write(f"✅ {a['Actividad']} — OK (dentro del presupuesto)")
            else:
                st.write(f"⚠️ {a['Actividad']} — EXCEDIDO (supera el presupuesto)")

        st.download_button(
            label="📥 Descargar actividades en CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="actividades.csv",
            mime="text/csv",
            key="download_ej2"
        )

        total_presupuesto = df["Presupuesto"].sum()
        total_gasto = df["Gasto Real"].sum()
        saldo = total_presupuesto - total_gasto

        st.subheader("Resumen")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Presupuesto", f"{total_presupuesto:.2f}")
        col2.metric("Total Gasto", f"{total_gasto:.2f}")
        col3.metric("Saldo", f"{saldo:.2f}")

        if total_gasto <= total_presupuesto:
            st.success("✅ En total, estás dentro del presupuesto.")
        else:
            st.error("❌ En total, estás excedida respecto al presupuesto.")

# EJERCICIO 3
elif menu == "Ejercicio 3":
    st.title("🧠 Ejercicio 3 – Funciones y Programación Funcional")
    st.write("Cálculo del retorno esperado por actividad usando map() y lambda.")

    if not st.session_state.actividades:
        st.info("Primero registra actividades en el Ejercicio 2 para poder calcular el retorno.")
    else:
        # Inputs
        tasa = st.slider("Tasa (ej: 0.05 = 5%)", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
        meses = st.number_input("Meses", min_value=1, value=1, step=1)

        # Función requerida
        def calcular_retorno(actividad: dict, tasa: float, meses: int) -> float:
            presupuesto = float(actividad["Presupuesto"])
            return presupuesto * tasa * meses

        if st.button("Calcular retorno"):
            actividades = st.session_state.actividades

            # map + lambda (requisito)
            retornos = list(map(lambda a: calcular_retorno(a, tasa, meses), actividades))

            # Mostrar resultados
            resultados = []
            for a, r in zip(actividades, retornos):
                resultados.append({
                    "Actividad": a["Actividad"],
                    "Tipo": a["Tipo"],
                    "Presupuesto": float(a["Presupuesto"]),
                    "Tasa": float(tasa),
                    "Meses": int(meses),
                    "Retorno esperado": float(r)
                })

            df_ret = pd.DataFrame(resultados)
            st.dataframe(df_ret, use_container_width=True)

            st.write("Fórmula aplicada: Retorno = Presupuesto × Tasa × Meses")

# EJERCICIO 4
elif menu == "Ejercicio 4":
    st.title("🏷️ Ejercicio 4 – Programación Orientada a Objetos (POO)")
    st.write("Modelando actividades como objetos usando una clase con métodos propios.")

    class Actividad:
        def __init__(self, nombre: str, tipo: str, presupuesto: float, gasto_real: float):
            self.nombre = nombre
            self.tipo = tipo
            self.presupuesto = float(presupuesto)
            self.gasto_real = float(gasto_real)

        # Método requerido
        def esta_en_presupuesto(self) -> bool:
            return self.gasto_real <= self.presupuesto

        # Método requerido
        def mostrar_info(self) -> str:
            return (
                f"Actividad: {self.nombre} | Tipo: {self.tipo} | "
                f"Presupuesto: {self.presupuesto:.2f} | Gasto real: {self.gasto_real:.2f}"
            )

        # (Opcional, útil para tabla)
        def saldo(self) -> float:
            return self.presupuesto - self.gasto_real

        def to_dict(self) -> dict:
            return {
                "Actividad": self.nombre,
                "Tipo": self.tipo,
                "Presupuesto": self.presupuesto,
                "Gasto Real": self.gasto_real,
                "Saldo": self.saldo(),
                "En presupuesto": self.esta_en_presupuesto()
            }

    if not st.session_state.actividades:
        st.info("Primero registra actividades en el Ejercicio 2 para convertirlas a objetos aquí.")
    else:
        # Convertir diccionarios a objetos
        objetos = []
        for a in st.session_state.actividades:
            objetos.append(
                Actividad(
                    a["Actividad"],
                    a["Tipo"],
                    a["Presupuesto"],
                    a["Gasto Real"]
                )
            )

        st.subheader("Actividades registradas (como objetos)")

        # Mostrar cada objeto como pide el profe
        for o in objetos:
            st.write(o.mostrar_info())
            if o.esta_en_presupuesto():
                st.success("✅ Cumple el presupuesto.")
            else:
                st.warning("⚠️ Excede el presupuesto.")

        # Tabla (opcional, pero ordena bien)
        df_obj = pd.DataFrame([o.to_dict() for o in objetos])
        st.subheader("Vista consolidada")
        st.dataframe(df_obj, use_container_width=True)

        st.download_button(
            label="📥 Descargar actividades (POO) en CSV",
            data=df_obj.to_csv(index=False).encode("utf-8"),
            file_name="actividades_poo.csv",
            mime="text/csv",
            key="download_poo"
        )