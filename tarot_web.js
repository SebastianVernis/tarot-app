// Sistema de Tarot Web - JavaScript
// Implementación completa con aleatorización mejorada

// Base de datos de cartas
const TAROT_DB = {
    arcanosMayores: [
        {
            nombre: "El Loco",
            numero: 0,
            significadoDerecho: "Nuevos comienzos, espontaneidad, inocencia, espíritu libre",
            significadoInvertido: "Imprudencia, riesgo innecesario, caos, falta de dirección",
            palabrasClave: ["inicio", "libertad", "aventura", "potencial"],
            elemento: "Aire"
        },
        {
            nombre: "El Mago",
            numero: 1,
            significadoDerecho: "Manifestación, poder personal, acción, habilidad",
            significadoInvertido: "Manipulación, engaño, talentos desperdiciados",
            palabrasClave: ["poder", "habilidad", "concentración", "recursos"],
            elemento: "Mercurio"
        },
        {
            nombre: "La Sacerdotisa",
            numero: 2,
            significadoDerecho: "Intuición, misterio, conocimiento oculto, subconsciente",
            significadoInvertido: "Secretos revelados, desconexión de la intuición",
            palabrasClave: ["intuición", "misterio", "sabiduría", "receptividad"],
            elemento: "Luna"
        },
        {
            nombre: "La Emperatriz",
            numero: 3,
            significadoDerecho: "Fertilidad, feminidad, belleza, abundancia, naturaleza",
            significadoInvertido: "Bloqueo creativo, dependencia, esterilidad",
            palabrasClave: ["creatividad", "abundancia", "nutrición", "madre"],
            elemento: "Venus"
        },
        {
            nombre: "El Emperador",
            numero: 4,
            significadoDerecho: "Autoridad, estructura, control, figura paterna",
            significadoInvertido: "Tiranía, rigidez, frialdad, abuso de poder",
            palabrasClave: ["autoridad", "estabilidad", "liderazgo", "padre"],
            elemento: "Aries"
        },
        {
            nombre: "El Hierofante",
            numero: 5,
            significadoDerecho: "Tradición, conformidad, moralidad, espiritualidad",
            significadoInvertido: "Rebelión, subversión, nuevos métodos, libertad",
            palabrasClave: ["tradición", "enseñanza", "creencias", "conformidad"],
            elemento: "Tauro"
        },
        {
            nombre: "Los Enamorados",
            numero: 6,
            significadoDerecho: "Amor, armonía, relaciones, valores, elección",
            significadoInvertido: "Desarmonía, desequilibrio, desalineación de valores",
            palabrasClave: ["amor", "elección", "unión", "valores"],
            elemento: "Géminis"
        },
        {
            nombre: "El Carro",
            numero: 7,
            significadoDerecho: "Control, fuerza de voluntad, éxito, victoria",
            significadoInvertido: "Falta de control, falta de dirección, agresión",
            palabrasClave: ["victoria", "control", "determinación", "viaje"],
            elemento: "Cáncer"
        },
        {
            nombre: "La Justicia",
            numero: 8,
            significadoDerecho: "Justicia, equidad, verdad, causa y efecto, ley",
            significadoInvertido: "Injusticia, deshonestidad, falta de responsabilidad",
            palabrasClave: ["equilibrio", "karma", "honestidad", "ley"],
            elemento: "Libra"
        },
        {
            nombre: "El Ermitaño",
            numero: 9,
            significadoDerecho: "Introspección, búsqueda interior, guía, soledad",
            significadoInvertido: "Aislamiento, soledad, rechazo de ayuda",
            palabrasClave: ["sabiduría", "introspección", "soledad", "guía"],
            elemento: "Virgo"
        },
        {
            nombre: "La Rueda de la Fortuna",
            numero: 10,
            significadoDerecho: "Buena suerte, karma, ciclos, destino, punto de inflexión",
            significadoInvertido: "Mala suerte, falta de control, revés del destino",
            palabrasClave: ["cambio", "ciclos", "destino", "suerte"],
            elemento: "Júpiter"
        },
        {
            nombre: "La Fuerza",
            numero: 11,
            significadoDerecho: "Fuerza interior, coraje, paciencia, control",
            significadoInvertido: "Debilidad, inseguridad, falta de confianza",
            palabrasClave: ["coraje", "paciencia", "control", "compasión"],
            elemento: "Leo"
        },
        {
            nombre: "El Colgado",
            numero: 12,
            significadoDerecho: "Suspensión, restricción, sacrificio, nueva perspectiva",
            significadoInvertido: "Estancamiento, resistencia al cambio, indecisión",
            palabrasClave: ["sacrificio", "paciencia", "perspectiva", "suspensión"],
            elemento: "Agua"
        },
        {
            nombre: "La Muerte",
            numero: 13,
            significadoDerecho: "Fin, transformación, transición, liberación",
            significadoInvertido: "Resistencia al cambio, estancamiento personal",
            palabrasClave: ["transformación", "final", "renovación", "transición"],
            elemento: "Escorpio"
        },
        {
            nombre: "La Templanza",
            numero: 14,
            significadoDerecho: "Balance, moderación, paciencia, propósito",
            significadoInvertido: "Desequilibrio, exceso, falta de armonía",
            palabrasClave: ["equilibrio", "moderación", "paciencia", "alquimia"],
            elemento: "Sagitario"
        },
        {
            nombre: "El Diablo",
            numero: 15,
            significadoDerecho: "Ataduras, adicción, sexualidad, materialismo",
            significadoInvertido: "Liberación, ruptura de cadenas, poder recuperado",
            palabrasClave: ["tentación", "atadura", "materialismo", "sombra"],
            elemento: "Capricornio"
        },
        {
            nombre: "La Torre",
            numero: 16,
            significadoDerecho: "Destrucción súbita, revelación, cambio drástico",
            significadoInvertido: "Desastre evitado, miedo al cambio, retraso inevitable",
            palabrasClave: ["caos", "revelación", "destrucción", "liberación"],
            elemento: "Marte"
        },
        {
            nombre: "La Estrella",
            numero: 17,
            significadoDerecho: "Esperanza, fe, propósito, renovación, espiritualidad",
            significadoInvertido: "Falta de fe, desesperación, desconexión",
            palabrasClave: ["esperanza", "inspiración", "serenidad", "renovación"],
            elemento: "Acuario"
        },
        {
            nombre: "La Luna",
            numero: 18,
            significadoDerecho: "Ilusión, miedo, ansiedad, subconsciente, intuición",
            significadoInvertido: "Liberación del miedo, verdad revelada, claridad",
            palabrasClave: ["ilusión", "intuición", "sueños", "subconsciente"],
            elemento: "Piscis"
        },
        {
            nombre: "El Sol",
            numero: 19,
            significadoDerecho: "Alegría, éxito, celebración, positividad",
            significadoInvertido: "Tristeza temporal, nubes pasajeras, ego",
            palabrasClave: ["alegría", "éxito", "vitalidad", "iluminación"],
            elemento: "Sol"
        },
        {
            nombre: "El Juicio",
            numero: 20,
            significadoDerecho: "Juicio, renacimiento, llamada interior, absolución",
            significadoInvertido: "Autocrítica, duda, incapacidad de perdonar",
            palabrasClave: ["renacimiento", "evaluación", "despertar", "llamada"],
            elemento: "Fuego"
        },
        {
            nombre: "El Mundo",
            numero: 21,
            significadoDerecho: "Completitud, logro, viaje completado, plenitud",
            significadoInvertido: "Falta de cierre, búsqueda externa, incompletitud",
            palabrasClave: ["completitud", "logro", "integración", "cumplimiento"],
            elemento: "Saturno"
        }
    ]
};

// Configuración de tiradas
const TIRADAS = {
    una_carta: {
        nombre: "Una Carta del Día",
        posiciones: ["Mensaje del día"],
        descripcion: "Una sola carta para guía o reflexión diaria"
    },
    tres_cartas: {
        nombre: "Pasado, Presente y Futuro",
        posiciones: ["Pasado", "Presente", "Futuro"],
        descripcion: "Visión general de una situación en el tiempo"
    },
    cruz_celta: {
        nombre: "Cruz Celta",
        posiciones: [
            "Situación actual",
            "Desafío o Cruz",
            "Pasado distante",
            "Pasado reciente",
            "Futuro posible",
            "Futuro inmediato",
            "Tu enfoque",
            "Influencias externas",
            "Esperanzas y miedos",
            "Resultado final"
        ],
        descripcion: "Lectura completa y detallada de una situación"
    },
    herradura: {
        nombre: "Herradura",
        posiciones: [
            "Pasado",
            "Presente",
            "Influencias ocultas",
            "Obstáculos",
            "Ambiente",
            "Mejor curso de acción",
            "Resultado probable"
        ],
        descripcion: "Análisis de una situación con consejo"
    },
    relacion: {
        nombre: "Lectura de Relación",
        posiciones: [
            "Cómo te ves a ti mismo",
            "Cómo ves a la otra persona",
            "Cómo te ve la otra persona",
            "Lo que necesitas de la relación",
            "Lo que la otra persona necesita",
            "Dónde va la relación"
        ],
        descripcion: "Análisis de una relación entre dos personas"
    }
};

// Clase para generar aleatorización mejorada
class GeneradorAleatorio {
    constructor() {
        this.poolEntropia = new Uint8Array(256);
        this.indice = 0;
        this.inicializarEntropia();
    }

    inicializarEntropia() {
        // Usar crypto API del navegador para máxima aleatoriedad
        if (window.crypto && window.crypto.getRandomValues) {
            window.crypto.getRandomValues(this.poolEntropia);
        } else {
            // Fallback con múltiples fuentes
            for (let i = 0; i < this.poolEntropia.length; i++) {
                this.poolEntropia[i] = Math.floor(Math.random() * 256);
            }
        }
        
        // Agregar más entropía con eventos del usuario
        this.agregarEntropiaUsuario();
    }

    agregarEntropiaUsuario() {
        let entropia = 0;
        
        // Tiempo actual
        entropia ^= Date.now() & 0xFF;
        
        // Posición del mouse si está disponible
        if (window.event) {
            entropia ^= (window.event.clientX || 0) & 0xFF;
            entropia ^= (window.event.clientY || 0) & 0xFF;
        }
        
        // Performance timing
        if (performance && performance.now) {
            entropia ^= Math.floor(performance.now() * 1000) & 0xFF;
        }
        
        this.poolEntropia[this.indice] ^= entropia;
        this.indice = (this.indice + 1) % this.poolEntropia.length;
    }

    obtenerNumero(max) {
        // Usar crypto API si está disponible
        if (window.crypto && window.crypto.getRandomValues) {
            const array = new Uint32Array(1);
            window.crypto.getRandomValues(array);
            return array[0] % max;
        }
        
        // Fallback con pool de entropía
        this.agregarEntropiaUsuario();
        
        let resultado = 0;
        for (let i = 0; i < 4; i++) {
            resultado = (resultado << 8) | this.poolEntropia[this.indice];
            this.indice = (this.indice + 1) % this.poolEntropia.length;
        }
        
        return Math.abs(resultado) % max;
    }

    obtenerBoolean() {
        return this.obtenerNumero(2) === 1;
    }

    mezclarArray(array) {
        const copia = [...array];
        
        // Fisher-Yates con nuestro generador
        for (let i = copia.length - 1; i > 0; i--) {
            const j = this.obtenerNumero(i + 1);
            [copia[i], copia[j]] = [copia[j], copia[i]];
        }
        
        return copia;
    }
}

// Estado global de la aplicación
let estadoApp = {
    tipoTiradaSeleccionada: null,
    mazo: [],
    cartasSacadas: [],
    pregunta: "",
    generador: new GeneradorAleatorio(),
    lecturaActual: null
};

// Inicialización cuando carga la página
document.addEventListener('DOMContentLoaded', function() {
    inicializarApp();
});

function inicializarApp() {
    // Crear estrellas de fondo
    crearEstrellas();
    
    // Inicializar mazo
    estadoApp.mazo = [...TAROT_DB.arcanosMayores];
    
    // Agregar arcanos menores simplificados
    const palos = ["Bastos", "Copas", "Espadas", "Oros"];
    const elementosPalos = {
        "Bastos": "Fuego",
        "Copas": "Agua",
        "Espadas": "Aire",
        "Oros": "Tierra"
    };
    
    for (let palo of palos) {
        for (let num = 1; num <= 14; num++) {
            let nombre;
            if (num === 1) nombre = `As de ${palo}`;
            else if (num === 11) nombre = `Sota de ${palo}`;
            else if (num === 12) nombre = `Caballo de ${palo}`;
            else if (num === 13) nombre = `Reina de ${palo}`;
            else if (num === 14) nombre = `Rey de ${palo}`;
            else nombre = `${num} de ${palo}`;
            
            estadoApp.mazo.push({
                nombre: nombre,
                numero: num,
                palo: palo,
                significadoDerecho: `Energía de ${palo} en su expresión positiva`,
                significadoInvertido: `Energía de ${palo} bloqueada o en desequilibrio`,
                palabrasClave: [palo.toLowerCase(), elementosPalos[palo].toLowerCase()],
                elemento: elementosPalos[palo]
            });
        }
    }
    
    // Event listeners
    document.querySelectorAll('.tirada-option').forEach(opcion => {
        opcion.addEventListener('click', seleccionarTirada);
    });
    
    document.getElementById('btnIniciarLectura').addEventListener('click', iniciarLectura);
    
    // Agregar entropía con movimiento del mouse
    document.addEventListener('mousemove', function(e) {
        estadoApp.generador.agregarEntropiaUsuario();
    });
}

function crearEstrellas() {
    const starsContainer = document.getElementById('stars');
    const numEstrellas = 100;
    
    for (let i = 0; i < numEstrellas; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.width = Math.random() * 3 + 'px';
        star.style.height = star.style.width;
        star.style.animationDelay = Math.random() * 3 + 's';
        star.style.animationDuration = (Math.random() * 3 + 2) + 's';
        starsContainer.appendChild(star);
    }
}

function seleccionarTirada(e) {
    // Quitar selección previa
    document.querySelectorAll('.tirada-option').forEach(opt => {
        opt.classList.remove('selected');
    });
    
    // Agregar selección actual
    e.currentTarget.classList.add('selected');
    estadoApp.tipoTiradaSeleccionada = e.currentTarget.dataset.tipo;
    
    // Habilitar botón
    document.getElementById('btnIniciarLectura').disabled = false;
}

async function iniciarLectura() {
    if (!estadoApp.tipoTiradaSeleccionada) return;
    
    // Guardar pregunta
    estadoApp.pregunta = document.getElementById('pregunta').value;
    
    // Mostrar animación de barajado
    document.getElementById('menuPrincipal').style.display = 'none';
    document.getElementById('barajando').style.display = 'block';
    
    // Barajar el mazo con animación
    await barajarMazo();
    
    // Realizar la lectura
    realizarLectura();
}

async function barajarMazo() {
    // Simular barajado múltiple para máxima aleatoriedad
    for (let i = 0; i < 7; i++) {
        estadoApp.mazo = estadoApp.generador.mezclarArray(estadoApp.mazo);
        await esperar(300);
    }
    
    // Espera adicional para efecto dramático
    await esperar(1000);
}

function esperar(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function realizarLectura() {
    const tirada = TIRADAS[estadoApp.tipoTiradaSeleccionada];
    estadoApp.cartasSacadas = [];
    
    // Sacar las cartas necesarias
    for (let i = 0; i < tirada.posiciones.length; i++) {
        const indiceCarta = estadoApp.generador.obtenerNumero(estadoApp.mazo.length - i);
        const carta = estadoApp.mazo.splice(indiceCarta, 1)[0];
        const invertida = estadoApp.generador.obtenerBoolean();
        
        estadoApp.cartasSacadas.push({
            carta: carta,
            invertida: invertida,
            posicion: tirada.posiciones[i]
        });
    }
    
    // Ocultar animación y mostrar resultados
    document.getElementById('barajando').style.display = 'none';
    mostrarResultados();
}

function mostrarResultados() {
    document.getElementById('lecturaArea').style.display = 'block';
    const container = document.getElementById('cartasContainer');
    container.innerHTML = '';
    
    // Título de la lectura
    const titulo = document.createElement('h2');
    titulo.style.textAlign = 'center';
    titulo.style.color = '#ffd700';
    titulo.style.marginBottom = '30px';
    titulo.textContent = TIRADAS[estadoApp.tipoTiradaSeleccionada].nombre;
    container.appendChild(titulo);
    
    if (estadoApp.pregunta) {
        const preguntaDiv = document.createElement('div');
        preguntaDiv.style.textAlign = 'center';
        preguntaDiv.style.marginBottom = '30px';
        preguntaDiv.style.fontStyle = 'italic';
        preguntaDiv.innerHTML = `<strong>Pregunta:</strong> ${estadoApp.pregunta}`;
        container.appendChild(preguntaDiv);
    }
    
    // Mostrar cada carta con retraso
    estadoApp.cartasSacadas.forEach((cartaInfo, index) => {
        setTimeout(() => {
            mostrarCarta(cartaInfo, index);
            
            // Mostrar interpretación al final
            if (index === estadoApp.cartasSacadas.length - 1) {
                setTimeout(() => {
                    mostrarInterpretacion();
                }, 500);
            }
        }, index * 600);
    });
}

function mostrarCarta(cartaInfo, index) {
    const container = document.getElementById('cartasContainer');
    
    const cartaDiv = document.createElement('div');
    cartaDiv.className = 'carta-container';
    
    const significado = cartaInfo.invertida ? 
        cartaInfo.carta.significadoInvertido : 
        cartaInfo.carta.significadoDerecho;
    
    cartaDiv.innerHTML = `
        <div class="carta-header">
            <div class="posicion-nombre">
                Posición ${index + 1}: ${cartaInfo.posicion}
            </div>
        </div>
        <div class="carta-nombre">
            📌 ${cartaInfo.carta.nombre}
            <span class="carta-estado ${cartaInfo.invertida ? 'invertida' : 'derecha'}">
                ${cartaInfo.invertida ? '↓ Invertida' : '↑ Derecha'}
            </span>
        </div>
        <div class="significado">
            ✨ ${significado}
        </div>
        <div class="palabras-clave">
            🔑 ${cartaInfo.carta.palabrasClave.map(palabra => 
                `<span class="palabra-clave">${palabra}</span>`
            ).join(' ')}
        </div>
        ${cartaInfo.carta.elemento ? 
            `<div style="margin-top: 10px; color: #a0a0a0;">
                🌀 Elemento: ${cartaInfo.carta.elemento}
            </div>` : ''}
    `;
    
    container.appendChild(cartaDiv);
}

function mostrarInterpretacion() {
    const interpretacion = generarInterpretacion();
    
    document.getElementById('interpretacionTexto').innerHTML = interpretacion;
    document.getElementById('interpretacionGeneral').style.display = 'block';
    
    // Guardar lectura actual
    estadoApp.lecturaActual = {
        fecha: new Date().toISOString(),
        tipo: estadoApp.tipoTiradaSeleccionada,
        pregunta: estadoApp.pregunta,
        cartas: estadoApp.cartasSacadas,
        interpretacion: interpretacion
    };
}

function generarInterpretacion() {
    const tipo = estadoApp.tipoTiradaSeleccionada;
    const cartas = estadoApp.cartasSacadas;
    
    let interpretacion = "";
    
    if (tipo === 'una_carta') {
        const c = cartas[0];
        interpretacion = `La carta ${c.carta.nombre} `;
        if (c.invertida) {
            interpretacion += "aparece invertida, sugiriendo que debes prestar atención a los aspectos ocultos o bloqueados relacionados con ";
        } else {
            interpretacion += "te invita a embracar ";
        }
        interpretacion += `${c.carta.significadoDerecho.toLowerCase()}. `;
        interpretacion += `Las energías de ${c.carta.palabrasClave.slice(0, 2).join(' y ')} están presentes en este momento.`;
    } 
    else if (tipo === 'tres_cartas') {
        const [pasado, presente, futuro] = cartas;
        
        interpretacion = `<strong>Pasado:</strong> ${pasado.carta.nombre} `;
        interpretacion += pasado.invertida ? 
            `invertida nos habla de desafíos pasados relacionados con ${pasado.carta.palabrasClave[0]}. ` :
            `indica que ${pasado.carta.palabrasClave[0]} ha sido una influencia importante. `;
        
        interpretacion += `<br><br><strong>Presente:</strong> ${presente.carta.nombre} `;
        interpretacion += presente.invertida ?
            `invertida sugiere que actualmente enfrentas ${presente.carta.significadoInvertido.toLowerCase()}. ` :
            `muestra que ${presente.carta.significadoDerecho.toLowerCase()}. `;
        
        interpretacion += `<br><br><strong>Futuro:</strong> ${futuro.carta.nombre} `;
        interpretacion += futuro.invertida ?
            `invertida advierte sobre posibles obstáculos, pero también ofrece la oportunidad de transformación. ` :
            `promete ${futuro.carta.significadoDerecho.toLowerCase()}.`;
    }
    else {
        // Para tiradas más complejas
        const numInvertidas = cartas.filter(c => c.invertida).length;
        const numMayores = cartas.filter(c => c.carta.numero <= 21).length;
        
        interpretacion = `Esta lectura de ${cartas.length} cartas revela un panorama complejo. `;
        
        if (numMayores >= 3) {
            interpretacion += `La presencia de ${numMayores} Arcanos Mayores indica que estás atravesando un período de importantes lecciones espirituales y transformaciones profundas. `;
        }
        
        if (numInvertidas > cartas.length * 0.5) {
            interpretacion += `Con ${numInvertidas} cartas invertidas, es momento de mirar hacia adentro y trabajar en los bloqueos internos. `;
        }
        
        // Analizar elementos
        const elementos = {};
        cartas.forEach(c => {
            if (c.carta.elemento) {
                elementos[c.carta.elemento] = (elementos[c.carta.elemento] || 0) + 1;
            }
        });
        
        const elementoDominante = Object.entries(elementos).sort((a, b) => b[1] - a[1])[0];
        if (elementoDominante && elementoDominante[1] >= 3) {
            interpretacion += `<br><br>El elemento ${elementoDominante[0]} domina esta lectura, sugiriendo un enfoque en `;
            
            const significadosElementos = {
                'Fuego': 'la acción, pasión y creatividad',
                'Agua': 'las emociones, intuición y relaciones',
                'Aire': 'la comunicación, ideas y decisiones',
                'Tierra': 'lo práctico, material y la estabilidad'
            };
            
            interpretacion += significadosElementos[elementoDominante[0]] || 'sus cualidades asociadas';
            interpretacion += '.';
        }
    }
    
    return interpretacion;
}

// Funciones de acciones
function guardarLectura() {
    if (!estadoApp.lecturaActual) return;
    
    // Obtener lecturas guardadas
    let lecturasGuardadas = JSON.parse(localStorage.getItem('lecturasТаrot') || '[]');
    
    // Agregar nueva lectura
    lecturasGuardadas.push(estadoApp.lecturaActual);
    
    // Guardar
    localStorage.setItem('lecturasТаrot', JSON.stringify(lecturasGuardadas));
    
    alert('✅ Lectura guardada exitosamente');
}

function nuevaLectura() {
    // Reiniciar estado
    estadoApp.tipoTiradaSeleccionada = null;
    estadoApp.cartasSacadas = [];
    estadoApp.pregunta = "";
    estadoApp.lecturaActual = null;
    
    // Reinicializar mazo
    estadoApp.mazo = [...TAROT_DB.arcanosMayores];
    
    // Volver al menú
    document.getElementById('lecturaArea').style.display = 'none';
    document.getElementById('menuPrincipal').style.display = 'block';
    document.getElementById('pregunta').value = '';
    document.getElementById('btnIniciarLectura').disabled = true;
    
    // Quitar selecciones
    document.querySelectorAll('.tirada-option').forEach(opt => {
        opt.classList.remove('selected');
    });
}

function compartirLectura() {
    if (!estadoApp.lecturaActual) return;
    
    let texto = `🔮 Mi lectura de Tarot - ${TIRADAS[estadoApp.tipoTiradaSeleccionada].nombre}\n\n`;
    
    if (estadoApp.pregunta) {
        texto += `Pregunta: ${estadoApp.pregunta}\n\n`;
    }
    
    estadoApp.cartasSacadas.forEach((c, i) => {
        texto += `${i + 1}. ${c.posicion}: ${c.carta.nombre}`;
        texto += c.invertida ? ' (Invertida)\n' : '\n';
    });
    
    // Copiar al portapapeles
    navigator.clipboard.writeText(texto).then(() => {
        alert('📋 Lectura copiada al portapapeles. ¡Puedes compartirla donde quieras!');
    }).catch(() => {
        // Fallback
        alert('No se pudo copiar. Puedes hacer una captura de pantalla para compartir.');
    });
}