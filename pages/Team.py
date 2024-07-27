import streamlit as st 
from menu import menu

markdown = """
**Dirección**: *Yudivián Almeida (Profesor)*

**Despliegue**: *Alejandro Piad (Profesor)*

**Programación**: *Yudivián Almeida (Profesor)*

**Modelos de Pronóstico**:

- Atletismo - *Yudivián Almeida (Profesor)*
- Badmington - *Anthuán Montes de Oca (Estudiante 4to año - Ciencia de la Computación)*
- Baloncesto - *Carlos M. Chang (Estudiante 3er año - Ciencia de la Computación)*
- Baloncesto 3x3 - *Carlos M. Chang (Estudiante 3er año - Ciencia de la Computación)*
- Balonmano - *Carlos M. Chang (Estudiante 3er año - Ciencia de la Computación)*
- Boxeo - *Edián Broche (Estudiante 3er año - Ciencia de la Computación)*
- Breakdance - *Massiel Paz (Estudiante 3er año - Ciencia de la Computación)*
- Ciclismo BMX - *Carlos M. García (Estudiante 3er año - Ciencia de la Computación)*
- Ciclismo Mountain Bike - *Carlos M. García (Estudiante 3er año - Ciencia de la Computación)*
- Ciclismo Ruta - *Carlos M. García (Estudiante 3er año - Ciencia de la Computación)*
- Escalada - *Alejandro Lamelas (Estudiante 3er año - Ciencia de la Computación)*
- Esgrima - *Manuel A. Gamboa (Estudiante 3er año - Ciencia de la Computación)*
- Fútbol  - *Yudivián Almeida (Profesor)*
- Gimnasia Artística - *Massiel Paz (Estudiante 3er año - Ciencia de la Computación)*
- Gimnasia con Trampolín - *Reinaldo Cánovas (Estudiante 2do año - Ciencia de Datos)*
- Gimnasia Rítmica - *Reinaldo Cánovas (Estudiante 2do año - Ciencia de Datos)*
- Golf - *Marco A. Ochill (Estudiante 4to año - Ciencia de la Computación)*
- Halterofilia - *Alex S. Bas (Estudiante 3er año - Ciencia de la Computación)*
- Hípica - *Sebastián Suárez (Estudiante 4to año - Ciencia de la Computación)*
- Hockey sobre Césped - *Daniel Polanco (Estudiante 3er año - Ciencia de la Computación)*
- Judo - *Francisco Préstamo (Estudiante 2do año - Ciencia de la Computación)*
- Lucha - *Manuel A. Gamboa (Estudiante 3er año - Ciencia de la Computación)*
- Natación - *Adrián Navarro (Estudiante 3er año - Ciencia de la Computación)*
- Natación Artística - *Carla S. Pérez (Estudiante 4to año - Ciencia de la Computación)*
- Natación Aguas Abiertas - *Adrián Navarro (Estudiante 3er año - Ciencia de la Computación)*
- Pentatlón Moderno - *Leonardo J. Ramírez (Estudiante 4to año - Ciencia de la Computación)*
- Piragüismo Slalom - *Darío López (Estudiante 2do año - Ciencia de la Computación)*
- Piragüismo Sprint - *Darío López (Estudiante 2do año - Ciencia de la Computación)*
- Remo - *Darío López (Estudiante 2do año - Ciencia de la Computación)*
- Rugby 7 - *Yudivián Almeida (Profesor)*
- Saltos - *Carla S. Pérez (Estudiante 4to año - Ciencia de la Computación)*
- Skateboarding - *Alejandro Ramírez (Estudiante 3er año - Ciencia de la Computación)*
- Surf - *Alejandro Ramírez (Estudiante 3er año - Ciencia de la Computación)*
- Taekwondo - *Glenda N. Ríos (Estudiante 2do año - Ciencia de la Computación)*
- Tenis - *Anthuán Montes de Oca (Estudiante 4to año - Ciencia de la Computación)*
- Tenis de Mesa - *Daniel Polanco (Estudiante 3er año - Ciencia de la Computación)*
- Tiro - *Eric L. López (Estudiante 4to año - Ciencia de la Computación)*
- Tiro con Arco - *Glenda N. Ríos (Estudiante 2do año - Ciencia de la Computación)*
- Triatlón - *Adrián Navarro (Estudiante 3er año - Ciencia de la Computación)*
- Vela - *Francisco Préstamo (Estudiante 2do año - Ciencia de la Computación)*
- Voleibol - *Ariel González (Estudiante 3er año - Ciencia de la Computación)*
- Voleibol de Playa - *Ariel González (Estudiante 3er año - Ciencia de la Computación)*
- Waterpolo - *Leonardo Artiles (Estudiante 3er año - Ciencia de la Computación)*

"""
st.header("Equipo de Desarrollo")

st.markdown(markdown)

menu()
