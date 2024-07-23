import streamlit as st 
from menu import menu

markdown = """
Dirección: Yudivián Almeida (Profesor)
Despliegue: Alejandro Piad (Profesor)
Programación: Yudivián Almeida (Profesor)

Modelos:

- Atletismo | Yudivián Almeida (Profesor)
- Badmington
- Baloncesto 3x3
- Balonmano
- Boxeo
- Breakdance
- Ciclismo BMX
- Ciclismo Mountain Bike
- Ciclismo Ruta
- Escalada
- Esgrima
- Fútbol  | Yudivián Almeida (Profesor)
- Gimnasia Artística
- Gimnasia con Trampolín
- Gimnsaia Rítmica
- Golf
- Halterofilia
- Hípica
- Hockey sobre Césped
- Judo
- Lucha
- Natación
- Natación Artística
- Natación Aguas Abiertas
- Pentatlón Moderno
- Piragüismo Slalom
- Piragüismo Sprint
- Remo
- Rugby 7 | Yudivián Almeida (Profesor)
- Saltos
- Skateboarding
- Surf 
- Taekwondo
- Tenis
- Tenis de Mesa
- Tiro
- Tiro con Arco
- Triatlón
- Vela
- Voleibol
- Voleibol de Playa
- Waterpolo 

"""

st.markdown(markdown)

menu()
