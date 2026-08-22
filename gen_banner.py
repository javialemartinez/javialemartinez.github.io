"""
Fondo del banner: las industrias donde trabajo, disolviendose en bits.

La idea, que es la tesis: la materia fisica de once anios de trabajo
-- satelites, radares, torres de refrigeracion, plantas, robots, turbinas --
se desarma y se vuelve informacion, y esa informacion desemboca en el nombre.

Como se logra CONTINUIDAD (y no islas sueltas):

  1. Todo vive sobre CARRILES. Cinco corrientes que cruzan el banner de lado
     a lado con una ondulacion suave. Las figuras se apoyan en el carril, los
     bits corren por el mismo carril. El ojo sigue la linea.
  2. La figura no se borra ni se tapa: se DESARMA. El mismo trazo va abriendo
     huecos (stroke-dasharray creciente) hasta quedar en pedazos. Es la misma
     forma en todo momento, no dos dibujos distintos.
  3. Los bits nacen donde la figura se rompe y siguen por el carril. La
     densidad de bits sube justo cuando la figura baja, asi no hay corte.

Una sola variable `d` (0 = materia, 1 = informacion) gobierna todo:
opacidad, huecos del trazo, color, y cuantos bits salen.

Deterministico (semilla fija).
"""
import math
import random

random.seed(7)

W, H = 1584, 396
X_INI, X_FIN = 60.0, 618.0     # el recorrido de la disolucion
X_APAGA = 664.0                # los bits ya no llegan mas alla
GRIS = (0x8A, 0x99, 0xAD)      # materia
VERDE = (0x2F, 0xD3, 0xA0)     # informacion


def mezcla(t):
    t = max(0.0, min(1.0, t))
    return "#%02X%02X%02X" % tuple(
        round(GRIS[i] + (VERDE[i] - GRIS[i]) * t) for i in range(3))


def disolucion(x):
    t = max(0.0, min(1.0, (x - X_INI) / (X_FIN - X_INI)))
    return t * t * (3 - 2 * t)


# --- Carriles: las corrientes que dan continuidad -------------------
CARRILES = [
    {"y": 74,  "amp": 13, "fase": 0.4,  "frec": 0.0092},
    {"y": 146, "amp": 17, "fase": 2.1,  "frec": 0.0079},
    {"y": 214, "amp": 11, "fase": 3.7,  "frec": 0.0104},
    {"y": 282, "amp": 16, "fase": 1.2,  "frec": 0.0086},
    {"y": 342, "amp": 10, "fase": 5.0,  "frec": 0.0098},
]


def y_carril(c, x):
    return c["y"] + c["amp"] * math.sin(x * c["frec"] + c["fase"])


# --- Iconos en caja 0..24, solo trazo -------------------------------
def arco(x1, y1, r, x2, y2, barrido=1):
    return "M%s,%s A%s,%s 0 0 %d %s,%s" % (x1, y1, r, r, barrido, x2, y2)


ICONOS = {
    # --- espacio ---
    "satelite": ['<rect x="9.5" y="9.5" width="5" height="5" rx="0.6"/>',
                 '<rect x="1.5" y="10" width="6.5" height="4" rx="0.5"/>',
                 '<rect x="16" y="10" width="6.5" height="4" rx="0.5"/>',
                 '<path d="M4.7,10 L4.7,14 M19.3,10 L19.3,14"/>',
                 '<path d="M12,9.5 L12,6"/>',
                 '<path d="%s"/>' % arco(9, 5.5, 3.2, 15, 5.5)],
    "cohete":   ['<path d="M12,2.5 C15,6 16.2,10.5 16.2,14.5 L7.8,14.5'
                 ' C7.8,10.5 9,6 12,2.5 Z"/>',
                 '<circle cx="12" cy="9" r="1.9"/>',
                 '<path d="M7.8,12 L4.6,17.5 L7.8,16.4 M16.2,12 L19.4,17.5'
                 ' L16.2,16.4"/>',
                 '<path d="M10.4,14.5 L10.4,19.5 M13.6,14.5 L13.6,19.5"/>'],
    "orbita":   ['<circle cx="12" cy="12" r="4"/>',
                 '<ellipse cx="12" cy="12" rx="10.5" ry="4.6"'
                 ' transform="rotate(-26 12 12)"/>',
                 '<circle cx="20.2" cy="7.6" r="1.5"/>'],
    # --- defensa ---
    "radar":    ['<path d="M7,20.5 L17,20.5 M12,20.5 L12,15"/>',
                 '<path d="%s"/>' % arco(4.5, 15.5, 8.5, 15.5, 6.5),
                 '<path d="M4.5,15.5 L15.5,6.5"/>',
                 '<path d="%s"/>' % arco(16.5, 4.6, 3.4, 19.6, 7.7),
                 '<path d="%s"/>' % arco(18.4, 2.6, 5.6, 21.6, 8.2)],
    "antena":   ['<path d="M8,21 L12,4 L16,21"/>',
                 '<path d="M9.3,15.5 L14.7,15.5 M10.2,11.5 L13.8,11.5"/>',
                 '<path d="%s"/>' % arco(16.6, 6.5, 3.6, 16.6, 12.5),
                 '<path d="%s"/>' % arco(7.4, 6.5, 3.6, 7.4, 12.5, 0)],
    # --- nuclear ---
    "reactor":  ['<path d="M6.4,20.8 C8.1,16.6 9.3,13.6 9.5,10.6 L14.5,10.6'
                 ' C14.7,13.6 15.9,16.6 17.6,20.8 Z"/>',
                 '<path d="M9.5,10.6 L14.5,10.6"/>',
                 '<path d="M10.4,7.6 C10.4,5.9 13.6,5.9 13.6,4.2"/>',
                 '<path d="M14.6,7.9 C14.6,6.6 16.8,6.6 16.8,5.3"/>'],
    "atomo":    ['<circle cx="12" cy="12" r="2"/>',
                 '<ellipse cx="12" cy="12" rx="10" ry="4.2"/>',
                 '<ellipse cx="12" cy="12" rx="10" ry="4.2"'
                 ' transform="rotate(60 12 12)"/>',
                 '<ellipse cx="12" cy="12" rx="10" ry="4.2"'
                 ' transform="rotate(-60 12 12)"/>'],
    # --- industria ---
    "planta":   ['<path d="M2.5,20.5 L2.5,12.5 L9,12.5 L9,9.5 L15.5,12.5'
                 ' L15.5,9.5 L21.5,12.5 L21.5,20.5 Z"/>',
                 '<path d="M18,9.5 L18,4.5 L20.5,4.5 L20.5,10.6"/>',
                 '<path d="M6,16 L6,20.5 M12,16 L12,20.5"/>'],
    "engranaje":['<circle cx="12" cy="12" r="4.4"/>',
                 '<circle cx="12" cy="12" r="1.7"/>',
                 '<path d="M12,4.4 L12,7 M12,17 L12,19.6 M4.4,12 L7,12'
                 ' M17,12 L19.6,12 M6.6,6.6 L8.4,8.4 M15.6,15.6 L17.4,17.4'
                 ' M17.4,6.6 L15.6,8.4 M8.4,15.6 L6.6,17.4"/>'],
    "robot":    ['<rect x="7.5" y="19" width="9" height="2.6" rx="0.6"/>',
                 '<path d="M12,19 L7,13.5 M7,13.5 L14.5,8"/>',
                 '<circle cx="7" cy="13.5" r="1.5"/>',
                 '<circle cx="12" cy="19" r="1.2"/>',
                 '<path d="M14.5,8 L18,5.6 M14.5,8 L17.4,9.6"/>'],
    "cinta":    ['<path d="M3,15 L21,15"/>',
                 '<circle cx="5.5" cy="17.5" r="2.5"/>',
                 '<circle cx="18.5" cy="17.5" r="2.5"/>',
                 '<path d="M5.5,20 L18.5,20"/>',
                 '<rect x="8" y="10" width="4" height="4.5" rx="0.4"/>',
                 '<rect x="14" y="11.5" width="3.4" height="3" rx="0.4"/>'],
    "tablero":  ['<rect x="5" y="3.5" width="14" height="17" rx="1.2"/>',
                 '<path d="M5,8 L19,8"/>',
                 '<circle cx="8.2" cy="5.8" r="0.9"/>',
                 '<circle cx="11" cy="5.8" r="0.9"/>',
                 '<path d="M7.5,11 L16.5,11 M7.5,14 L16.5,14'
                 ' M7.5,17 L13,17"/>'],
    # --- energia ---
    "solar":    ['<path d="M3.5,15.5 L8,6.5 L21,6.5 L16.5,15.5 Z"/>',
                 '<path d="M6.6,15.5 L11.1,6.5 M11.1,15.5 L15.6,6.5"/>',
                 '<path d="M7.3,11 L18.8,11"/>',
                 '<path d="M10,15.5 L10,20.5 M10,20.5 L6,20.5'
                 ' M10,20.5 L14,20.5"/>'],
    "eolico":   ['<path d="M11,21 L13,21 L12.4,9 L11.6,9 Z"/>',
                 '<circle cx="12" cy="8" r="1.2"/>',
                 '<path d="M12,6.8 L12.6,1.5 M13.1,8.6 L18,10.6'
                 ' M10.9,8.6 L6,10.6"/>'],
    "torre":    ['<path d="M6,21 L9.5,3 L14.5,3 L18,21"/>',
                 '<path d="M8.2,12 L15.8,12 M7.2,17 L16.8,17"/>',
                 '<path d="M9.5,3 L14.5,3 M8.6,7.5 L15.4,7.5"/>',
                 '<path d="M8.2,12 L15.4,7.5 M15.8,12 L8.6,7.5"/>'],
    # --- software / IA ---
    "software": ['<path d="M8.5,7.5 L4,12 L8.5,16.5"/>',
                 '<path d="M15.5,7.5 L20,12 L15.5,16.5"/>',
                 '<path d="M13.6,5.6 L10.4,18.4"/>'],
    "chip":     ['<rect x="7" y="7" width="10" height="10" rx="1"/>',
                 '<rect x="10.2" y="10.2" width="3.6" height="3.6" rx="0.5"/>',
                 '<path d="M9.5,7 L9.5,4 M14.5,7 L14.5,4 M9.5,17 L9.5,20'
                 ' M14.5,17 L14.5,20 M7,9.5 L4,9.5 M7,14.5 L4,14.5'
                 ' M17,9.5 L20,9.5 M17,14.5 L20,14.5"/>'],
    "servidor": ['<rect x="4" y="4" width="16" height="5" rx="0.8"/>',
                 '<rect x="4" y="10.5" width="16" height="5" rx="0.8"/>',
                 '<rect x="4" y="17" width="16" height="5" rx="0.8"/>',
                 '<circle cx="7" cy="6.5" r="0.8"/>'
                 '<circle cx="7" cy="13" r="0.8"/>'
                 '<circle cx="7" cy="19.5" r="0.8"/>'],
    "red":      ['<circle cx="4.5" cy="12" r="1.8"/>',
                 '<circle cx="12" cy="5" r="1.8"/>',
                 '<circle cx="12" cy="19" r="1.8"/>',
                 '<circle cx="19.5" cy="12" r="1.8"/>',
                 '<circle cx="12" cy="12" r="1.8"/>',
                 '<path d="M6.2,12 L10.2,12 M13.8,12 L17.7,12'
                 ' M12,6.8 L12,10.2 M12,13.8 L12,17.2'
                 ' M6,10.4 L10.6,6.4 M13.4,17.6 L18,13.6"/>'],
    "datos":    ['<ellipse cx="12" cy="6" rx="7.5" ry="2.8"/>',
                 '<path d="M4.5,6 L4.5,18 C4.5,19.6 7.9,20.8 12,20.8'
                 ' C16.1,20.8 19.5,19.6 19.5,18 L19.5,6"/>',
                 '<path d="M4.5,12 C4.5,13.6 7.9,14.8 12,14.8'
                 ' C16.1,14.8 19.5,13.6 19.5,12"/>'],
}

# Que figura va en cada carril y a que altura del recorrido.
# Se ordena de materia pesada (izquierda) a informacion (derecha).
COMPOSICION = [
    # carril 0
    [("satelite", 74, 2.35), ("orbita", 196, 1.85), ("antena", 318, 1.60),
     ("chip", 436, 1.35), ("red", 548, 1.15)],
    # carril 1
    [("radar", 128, 2.45), ("robot", 262, 1.95), ("tablero", 384, 1.55),
     ("software", 498, 1.30), ("datos", 596, 1.05)],
    # carril 2
    [("reactor", 66, 2.30), ("atomo", 190, 1.90), ("engranaje", 308, 1.60),
     ("servidor", 424, 1.35), ("software", 536, 1.10)],
    # carril 3
    [("planta", 104, 2.30), ("cinta", 232, 1.85), ("torre", 352, 1.55),
     ("chip", 466, 1.30), ("red", 572, 1.05)],
    # carril 4
    [("cohete", 158, 2.05), ("solar", 280, 1.70), ("eolico", 396, 1.45),
     ("datos", 508, 1.20), ("servidor", 604, 1.00)],
]

partes = []
ap = partes.append

# ---- 1. la corriente: hilos continuos que atraviesan todo ----------
ap('<g fill="none" stroke-linecap="round">')
for c in CARRILES:
    pts = []
    for x in range(30, 700, 6):
        pts.append("%.1f,%.1f" % (x, y_carril(c, x)))
    # se dibuja en tramos para que la opacidad siga la disolucion
    for i in range(0, len(pts) - 1, 6):
        tramo = pts[i:i + 7]
        xm = 30 + (i + 3) * 6
        d = disolucion(xm)
        op = round(0.16 + 0.10 * d, 3) * max(0.0, 1 - max(0.0, xm - 560) / 140)
        if op < 0.015:
            continue
        ap('<polyline points="%s" stroke="%s" stroke-width="0.9" '
           'opacity="%.3f"/>' % (" ".join(tramo), mezcla(d), op))
ap('</g>')

# ---- 2. las figuras, desarmandose sobre su carril -------------------
bits_pendientes = []
for idx, carril in enumerate(COMPOSICION):
    c = CARRILES[idx]
    for nombre, cx, esc in carril:
        d = disolucion(cx)
        cy = y_carril(c, cx)
        lado = 24 * esc
        x0, y0 = cx - lado / 2, cy - lado / 2

        op = round(max(0.0, 1.00 * (1 - d) ** 0.92), 3)
        if op > 0.02:
            # el trazo se abre en huecos: la figura no se borra, se rompe
            hueco = 9.5 * d ** 1.6
            raya = max(0.6, 5.0 - 3.4 * d)
            dash = ('' if d < 0.06
                    else ' stroke-dasharray="%.2f %.2f"' % (raya / esc, hueco / esc))
            ap('<g transform="translate(%.1f,%.1f) scale(%.3f)" fill="none" '
               'stroke="%s" stroke-width="%.2f" stroke-linecap="round" '
               'stroke-linejoin="round" opacity="%.3f"%s>'
               % (x0, y0, esc, mezcla(d), 2.0 / esc, op, dash))
            for elem in ICONOS[nombre]:
                ap("  " + elem)
            ap("</g>")

        # los bits nacen donde la figura se rompe y siguen por el carril
        n = int(round(34 * d ** 1.05)) + 2
        for _ in range(n):
            avance = random.random() ** 0.55 * (215 * d + 30)
            bx = cx + lado * 0.30 + avance
            if bx > X_APAGA:
                continue
            desv = random.gauss(0, 3.4 + 5.6 * d)
            by = y_carril(c, bx) + desv
            db = disolucion(bx)
            cae = max(0.0, 1 - max(0.0, bx - 520) / (X_APAGA - 520))
            opb = round((0.30 + 0.42 * db) * (0.4 + random.random() * 0.7) * cae, 3)
            if opb < 0.03:
                continue
            bits_pendientes.append(
                (bx, by, random.choice("01"),
                 round(8.5 + random.random() * 4.5 - 3.2 * db, 1),
                 mezcla(min(1.0, db + 0.18)), opb))

# ---- 3. los bits, todos juntos para que queden por encima ----------
ap('<g font-family="Consolas,\'SF Mono\',Menlo,monospace" font-weight="600">')
for bx, by, ch, fs, col, opb in bits_pendientes:
    ap('<text x="%.1f" y="%.1f" font-size="%.1f" fill="%s" opacity="%.3f">%s</text>'
       % (bx, by, fs, col, opb, ch))
ap("</g>")

open("fondo_banner.svg", "w", encoding="utf-8").write("\n".join(partes))
print("  figuras: %d en %d carriles" % (sum(len(c) for c in COMPOSICION), len(CARRILES)))
print("  bits: %d   elementos: %d" % (len(bits_pendientes), len(partes)))
