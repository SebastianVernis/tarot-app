/**
 * Sistema Esotérico Universal - JavaScript Profesional
 * Maneja todas las interacciones de la interfaz avanzada
 */

class SistemaEsotericoPro {
    constructor() {
        this.modalidadActual = null;
        this.configuracion = {
            tema: 'cosmic',
            velocidadAnimacion: 'normal',
            efectosSonido: false,
            efectosParticulas: true
        };
        this.historialLecturas = [];
        
        this.init();
    }

    init() {
        this.cargarConfiguracion();
        this.crearFondoCosmico();
        this.setupEventListeners();
        this.cargarHistorial();
        this.iniciarEfectosAmbientales();
    }

    /**
     * Configuración inicial y event listeners
     */
    setupEventListeners() {
        // Pestañas
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.cambiarPestana(e.target.dataset.tab);
            });
        });

        // Cards de modalidades
        document.querySelectorAll('.modalidad-card').forEach(card => {
            card.addEventListener('click', (e) => {
                this.seleccionarModalidad(e.currentTarget.dataset.modalidad);
            });
            
            // Efecto hover mejorado
            card.addEventListener('mouseenter', this.efectoHoverCard);
            card.addEventListener('mouseleave', this.removerEfectoHover);
        });

        // Formulario dinámico
        document.getElementById('startReading')?.addEventListener('click', this.iniciarLectura.bind(this));
        document.getElementById('cancelForm')?.addEventListener('click', this.cancelarFormulario.bind(this));

        // Configuración
        document.getElementById('saveConfig')?.addEventListener('click', this.guardarConfiguracion.bind(this));
        
        // Resultados
        document.getElementById('saveReading')?.addEventListener('click', this.guardarLectura.bind(this));
        document.getElementById('shareReading')?.addEventListener('click', this.compartirLectura.bind(this));
        document.getElementById('newReading')?.addEventListener('click', this.nuevaLectura.bind(this));

        // Eventos de teclado para accesibilidad
        document.addEventListener('keydown', this.manejarTeclado.bind(this));
    }

    /**
     * Cambia entre pestañas
     */
    cambiarPestana(pestana) {
        // Remover activo de botones
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
            btn.setAttribute('aria-selected', 'false');
        });

        // Activar botón seleccionado
        const btnActivo = document.querySelector(`[data-tab="${pestana}"]`);
        btnActivo.classList.add('active');
        btnActivo.setAttribute('aria-selected', 'true');

        // Cambiar contenido
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        document.getElementById(pestana).classList.add('active');

        // Efectos especiales por pestaña
        this.efectosPorPestana(pestana);
    }

    /**
     * Efectos especiales según la pestaña
     */
    efectosPorPestana(pestana) {
        if (pestana === 'modalidades') {
            this.animarCards();
        } else if (pestana === 'historial') {
            this.cargarHistorial();
        }
    }

    /**
     * Anima las cards de modalidades
     */
    animarCards() {
        const cards = document.querySelectorAll('.modalidad-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    /**
     * Selecciona una modalidad esotérica
     */
    seleccionarModalidad(modalidad) {
        this.modalidadActual = modalidad;
        this.mostrarFormularioModalidad(modalidad);
        this.efectoSeleccionModalidad();
    }

    /**
     * Muestra el formulario específico de cada modalidad
     */
    mostrarFormularioModalidad(modalidad) {
        const form = document.getElementById('dynamicForm');
        const title = document.getElementById('formTitle');
        const content = document.getElementById('formContent');

        // Configurar título y contenido según modalidad
        const configuraciones = {
            tarot: {
                titulo: '🎴 Configurar Lectura de Tarot',
                contenido: this.crearFormularioTarot()
            },
            numerologia: {
                titulo: '🔢 Configurar Análisis Numerológico',
                contenido: this.crearFormularioNumerologia()
            },
            runas: {
                titulo: '🔥 Configurar Lectura de Runas',
                contenido: this.crearFormularioRunas()
            },
            iching: {
                titulo: '🏛️ Configurar Consulta I Ching',
                contenido: this.crearFormularioIChing()
            },
            horoscopo: {
                titulo: '⭐ Configurar Horóscopo',
                contenido: this.crearFormularioHoroscopo()
            },
            oraculo: {
                titulo: '🔮 Configurar Oráculo Sí/No',
                contenido: this.crearFormularioOraculo()
            }
        };

        const config = configuraciones[modalidad];
        if (config) {
            title.textContent = config.titulo;
            content.innerHTML = config.contenido;
            form.style.display = 'block';
            
            // Scroll suave al formulario
            form.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        }
    }

    /**
     * Formularios específicos para cada modalidad
     */
    crearFormularioTarot() {
        return `
            <div class="form-group">
                <label class="form-label">Tipo de Tirada</label>
                <select class="form-select" id="tipoTirada" required>
                    <option value="">Selecciona un tipo de tirada</option>
                    <option value="una_carta">Una Carta del Día</option>
                    <option value="tres_cartas">Pasado, Presente y Futuro</option>
                    <option value="cruz_celta">Cruz Celta (10 cartas)</option>
                    <option value="herradura">Herradura (7 cartas)</option>
                    <option value="relacion">Lectura de Relación</option>
                    <option value="amor">Lectura de Amor</option>
                    <option value="anual">Lectura Anual</option>
                    <option value="decision">Lectura de Decisión</option>
                    <option value="chakras">Lectura de Chakras</option>
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">Tu Pregunta (opcional)</label>
                <input type="text" class="form-input" id="preguntaTarot" 
                       placeholder="¿Cuál es tu pregunta para las cartas?">
            </div>
            <div class="form-group">
                <label class="form-label">
                    <input type="checkbox" id="mostrarInvertidas" checked style="margin-right: 10px;">
                    Incluir cartas invertidas
                </label>
            </div>
        `;
    }

    crearFormularioNumerologia() {
        return `
            <div class="form-group">
                <label class="form-label">Nombre Completo *</label>
                <input type="text" class="form-input" id="nombreCompleto" 
                       placeholder="Tu nombre completo (tal como aparece en tu documento)" required>
            </div>
            <div class="form-group">
                <label class="form-label">Fecha de Nacimiento *</label>
                <input type="date" class="form-input" id="fechaNacimiento" required>
            </div>
            <div class="form-group">
                <label class="form-label">Pregunta Específica (opcional)</label>
                <input type="text" class="form-input" id="preguntaNumerologia" 
                       placeholder="¿Hay algo específico que quieras saber?">
            </div>
            <div class="form-group">
                <label class="form-label">Tipo de Análisis</label>
                <select class="form-select" id="tipoAnalisis">
                    <option value="completo">Análisis Completo</option>
                    <option value="personalidad">Solo Personalidad</option>
                    <option value="destino">Solo Número de Destino</option>
                    <option value="compatibilidad">Compatibilidad (nombre pareja requerido)</option>
                </select>
            </div>
        `;
    }

    crearFormularioRunas() {
        return `
            <div class="form-group">
                <label class="form-label">Tipo de Tirada Rúnica</label>
                <select class="form-select" id="tipoTiradaRunas" required>
                    <option value="">Selecciona un tipo de tirada</option>
                    <option value="una_runa">Runa del Día</option>
                    <option value="tres_runas">Pasado, Presente, Futuro</option>
                    <option value="cinco_runas">Cruz Rúnica (5 runas)</option>
                    <option value="siete_runas">Estrella de Siete</option>
                    <option value="nueve_runas">Cuadrado Mágico (9 runas)</option>
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">Tu Consulta</label>
                <textarea class="form-input" id="consultaRunas" rows="3" 
                         placeholder="¿Qué deseas consultar a la sabiduría nórdica?"></textarea>
            </div>
            <div class="form-group">
                <label class="form-label">Elemento de Enfoque</label>
                <select class="form-select" id="elementoEnfoque">
                    <option value="todos">Todos los elementos</option>
                    <option value="fuego">Fuego (Acción, energía)</option>
                    <option value="agua">Agua (Emociones, intuición)</option>
                    <option value="aire">Aire (Mente, comunicación)</option>
                    <option value="tierra">Tierra (Material, estabilidad)</option>
                </select>
            </div>
        `;
    }

    crearFormularioIChing() {
        return `
            <div class="form-group">
                <label class="form-label">Tu Pregunta para el I Ching *</label>
                <textarea class="form-input" id="preguntaIChing" rows="3" 
                         placeholder="Formúla una pregunta específica para el Libro de los Cambios..." required></textarea>
            </div>
            <div class="form-group">
                <label class="form-label">Método de Consulta</label>
                <select class="form-select" id="metodoConsulta">
                    <option value="tres_monedas">Tres Monedas (tradicional)</option>
                    <option value="varillas">50 Varillas (complejo)</option>
                    <option value="intuicivo">Método Intuitivo (moderno)</option>
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">Área de Consulta</label>
                <select class="form-select" id="areaConsulta">
                    <option value="general">General</option>
                    <option value="personal">Desarrollo Personal</option>
                    <option value="relaciones">Relaciones</option>
                    <option value="trabajo">Trabajo/Carrera</option>
                    <option value="salud">Salud</option>
                    <option value="espiritual">Crecimiento Espiritual</option>
                </select>
            </div>
        `;
    }

    crearFormularioHoroscopo() {
        const signos = [
            'aries', 'tauro', 'geminis', 'cancer', 'leo', 'virgo',
            'libra', 'escorpio', 'sagitario', 'capricornio', 'acuario', 'piscis'
        ];

        const opcionesSignos = signos.map(signo => 
            `<option value="${signo}">${signo.charAt(0).toUpperCase() + signo.slice(1)}</option>`
        ).join('');

        return `
            <div class="form-group">
                <label class="form-label">Tu Signo Zodiacal *</label>
                <select class="form-select" id="signoZodiacal" required>
                    <option value="">Selecciona tu signo</option>
                    ${opcionesSignos}
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">Área de Interés</label>
                <select class="form-select" id="areaInteres">
                    <option value="general">General</option>
                    <option value="amor">Amor y Relaciones</option>
                    <option value="trabajo">Trabajo y Dinero</option>
                    <option value="salud">Salud y Bienestar</option>
                    <option value="familia">Familia y Hogar</option>
                    <option value="amistad">Amistad y Social</option>
                    <option value="espiritualidad">Espiritualidad</option>
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">Período de Predicción</label>
                <select class="form-select" id="periodoPrediccion">
                    <option value="hoy">Hoy</option>
                    <option value="semana">Esta Semana</option>
                    <option value="mes">Este Mes</option>
                    <option value="trimestre">Próximos 3 Meses</option>
                </select>
            </div>
        `;
    }

    crearFormularioOraculo() {
        return `
            <div class="form-group">
                <label class="form-label">Tu Pregunta de Sí/No *</label>
                <textarea class="form-input" id="preguntaOraculo" rows="3" 
                         placeholder="Formúla una pregunta que pueda responderse con Sí o No..." required></textarea>
            </div>
            <div class="form-group">
                <label class="form-label">Contexto de la Pregunta</label>
                <select class="form-select" id="contextoOraculo">
                    <option value="general">General</option>
                    <option value="personal">Personal</option>
                    <option value="relaciones">Relaciones</option>
                    <option value="profesional">Profesional</option>
                    <option value="financiero">Financiero</option>
                    <option value="salud">Salud</option>
                    <option value="espiritual">Espiritual</option>
                </select>
            </div>
            <div class="form-group">
                <label class="form-label">Urgencia de la Decisión</label>
                <select class="form-select" id="urgenciaDecision">
                    <option value="normal">Normal</option>
                    <option value="urgente">Urgente (necesito decidir hoy)</option>
                    <option value="reflexion">Tengo tiempo para reflexionar</option>
                </select>
            </div>
        `;
    }

    /**
     * Inicia la lectura con los datos del formulario
     */
    async iniciarLectura() {
        const datosFormulario = this.recopilarDatosFormulario();
        
        if (!this.validarDatos(datosFormulario)) {
            this.mostrarError('Por favor completa todos los campos requeridos.');
            return;
        }

        this.mostrarCargando();
        
        try {
            // Simular procesamiento (en producción conectaría con backend)
            const resultado = await this.procesarLectura(datosFormulario);
            this.mostrarResultado(resultado);
        } catch (error) {
            this.mostrarError('Error al procesar la lectura. Intenta nuevamente.');
            console.error('Error:', error);
        } finally {
            this.ocultarCargando();
        }
    }

    /**
     * Recopila datos del formulario activo
     */
    recopilarDatosFormulario() {
        const datos = {
            modalidad: this.modalidadActual,
            timestamp: Date.now()
        };

        // Obtener todos los inputs del formulario
        const inputs = document.querySelectorAll('#dynamicForm input, #dynamicForm select, #dynamicForm textarea');
        
        inputs.forEach(input => {
            if (input.type === 'checkbox') {
                datos[input.id] = input.checked;
            } else {
                datos[input.id] = input.value;
            }
        });

        return datos;
    }

    /**
     * Valida los datos del formulario
     */
    validarDatos(datos) {
        // Validaciones específicas por modalidad
        switch (datos.modalidad) {
            case 'tarot':
                return datos.tipoTirada && datos.tipoTirada !== '';
            case 'numerologia':
                return datos.nombreCompleto && datos.fechaNacimiento;
            case 'runas':
                return datos.tipoTiradaRunas && datos.tipoTiradaRunas !== '';
            case 'iching':
                return datos.preguntaIChing && datos.preguntaIChing.trim() !== '';
            case 'horoscopo':
                return datos.signoZodiacal && datos.signoZodiacal !== '';
            case 'oraculo':
                return datos.preguntaOraculo && datos.preguntaOraculo.trim() !== '';
            default:
                return false;
        }
    }

    /**
     * Procesa la lectura (simulación)
     */
    async procesarLectura(datos) {
        // Simular delay de procesamiento
        await this.delay(2000 + Math.random() * 3000);
        
        // Generar resultado simulado basado en la modalidad
        return this.generarResultadoSimulado(datos);
    }

    /**
     * Genera resultado simulado
     */
    generarResultadoSimulado(datos) {
        const resultados = {
            tarot: {
                titulo: `Lectura de Tarot: ${this.obtenerNombreTirada(datos.tipoTirada)}`,
                subtitulo: datos.preguntaTarot ? `Pregunta: "${datos.preguntaTarot}"` : 'Lectura general',
                contenido: this.generarResultadoTarot(datos)
            },
            numerologia: {
                titulo: `Análisis Numerológico de ${datos.nombreCompleto}`,
                subtitulo: `Fecha de nacimiento: ${datos.fechaNacimiento}`,
                contenido: this.generarResultadoNumerologia(datos)
            },
            runas: {
                titulo: `Lectura de Runas: ${this.obtenerNombreTiradaRunas(datos.tipoTiradaRunas)}`,
                subtitulo: datos.consultaRunas ? `Consulta: "${datos.consultaRunas}"` : 'Consulta general',
                contenido: this.generarResultadoRunas(datos)
            },
            iching: {
                titulo: 'Consulta al I Ching',
                subtitulo: `Pregunta: "${datos.preguntaIChing}"`,
                contenido: this.generarResultadoIChing(datos)
            },
            horoscopo: {
                titulo: `Horóscopo para ${datos.signoZodiacal.charAt(0).toUpperCase() + datos.signoZodiacal.slice(1)}`,
                subtitulo: `Área: ${datos.areaInteres || 'General'} - ${datos.periodoPrediccion || 'Hoy'}`,
                contenido: this.generarResultadoHoroscopo(datos)
            },
            oraculo: {
                titulo: 'Respuesta del Oráculo',
                subtitulo: `Pregunta: "${datos.preguntaOraculo}"`,
                contenido: this.generarResultadoOraculo(datos)
            }
        };

        return resultados[datos.modalidad] || { titulo: 'Error', subtitulo: '', contenido: 'Error generando resultado' };
    }

    /**
     * Generadores de contenido específicos
     */
    generarResultadoTarot(datos) {
        const cartas = [
            { nombre: 'El Sol', significado: 'Éxito, alegría, vitalidad' },
            { nombre: 'La Luna', significado: 'Intuición, sueños, ilusiones' },
            { nombre: 'La Estrella', significado: 'Esperanza, inspiración, renovación' }
        ];

        let contenido = '<div class="resultado-cartas">';
        cartas.forEach((carta, index) => {
            contenido += `
                <div class="carta-resultado">
                    <h4 class="highlight">Posición ${index + 1}: ${carta.nombre}</h4>
                    <p>${carta.significado}</p>
                </div>
            `;
        });
        contenido += '</div>';

        contenido += `
            <div class="interpretacion-general">
                <h4 class="highlight">Interpretación General:</h4>
                <p>Las cartas revelan un momento de gran potencial y claridad. El Sol te invita a brillar con tu luz propia, mientras que La Luna te recuerda la importancia de tu intuición. La Estrella confirma que tus esperanzas se materializarán.</p>
            </div>
        `;

        return contenido;
    }

    generarResultadoNumerologia(datos) {
        return `
            <div class="numeros-principales">
                <h4 class="highlight">Tus Números Principales:</h4>
                <p><strong>Número de Vida:</strong> 7 - El Buscador de la Verdad</p>
                <p><strong>Número de Destino:</strong> 3 - El Comunicador Creativo</p>
                <p><strong>Número del Alma:</strong> 5 - El Aventurero Libre</p>
            </div>
            
            <div class="interpretacion-numerologica">
                <h4 class="highlight">Interpretación Completa:</h4>
                <p>Tu combinación numerológica revela una personalidad única y fascinante. Como número 7, tienes una inclinación natural hacia la búsqueda espiritual y el conocimiento profundo.</p>
                <p>Tu número de destino 3 te impulsa hacia la expresión creativa y la comunicación. Tienes un don natural para inspirar a otros.</p>
                <p>Tu número del alma 5 habla de tu necesidad de libertad y experiencias variadas. No te conformas con la rutina.</p>
            </div>
            
            <div class="recomendaciones">
                <h4 class="highlight">Recomendaciones:</h4>
                <ul>
                    <li>Dedica tiempo a la meditación y el estudio</li>
                    <li>Expresa tu creatividad a través del arte o la escritura</li>
                    <li>Mantén un balance entre aventura y responsabilidad</li>
                </ul>
            </div>
        `;
    }

    generarResultadoRunas(datos) {
        const runas = ['ᚠ Fehu', 'ᚢ Uruz', 'ᚦ Thurisaz'];
        
        return `
            <div class="runas-resultado">
                <h4 class="highlight">Runas Reveladas:</h4>
                ${runas.map(runa => `<div class="runa-individual"><p><strong>${runa}</strong></p></div>`).join('')}
            </div>
            
            <div class="interpretacion-runas">
                <h4 class="highlight">Mensaje de los Ancestros:</h4>
                <p>Las runas hablan de abundancia (Fehu), fuerza primordial (Uruz) y protección necesaria (Thurisaz). Los antepasados nórdicos te aconsejan que uses tu fuerza interior para proteger lo que has construido.</p>
                
                <p>Es un momento de prosperidad, pero requiere vigilancia y determinación para mantener lo logrado.</p>
            </div>
        `;
    }

    generarResultadoIChing(datos) {
        return `
            <div class="hexagrama">
                <h4 class="highlight">Hexagrama 11: La Paz</h4>
                <div style="font-size: 2rem; text-align: center; margin: 20px 0;">☷☰</div>
                <p><em>La Tierra sobre el Cielo</em></p>
            </div>
            
            <div class="interpretacion-iching">
                <h4 class="highlight">Interpretación:</h4>
                <p>El hexagrama de La Paz indica un período de armonía y equilibrio en tu vida. Las fuerzas del cielo y la tierra están en perfecta sincronía.</p>
                
                <p>Este es un tiempo favorable para tomar decisiones importantes. Tu pregunta encuentra una respuesta positiva en este momento de estabilidad cósmica.</p>
                
                <h4 class="highlight">Consejo del I Ching:</h4>
                <p>Mantén la humildad en el éxito. La paz verdadera viene del equilibrio entre la acción (cielo) y la receptividad (tierra).</p>
            </div>
        `;
    }

    generarResultadoHoroscopo(datos) {
        return `
            <div class="prediccion-principal">
                <h4 class="highlight">Tu Predicción Astrológica:</h4>
                <p>Los astros están especialmente favorables para ti hoy. Tu signo ${datos.signoZodiacal} recibe influencias positivas de Venus y Júpiter.</p>
            </div>
            
            <div class="areas-especificas">
                <h4 class="highlight">Área de Enfoque: ${datos.areaInteres || 'General'}</h4>
                <p>Las energías planetarias se alinean perfectamente para favorecer esta área de tu vida. Es un momento excelente para tomar iniciativas.</p>
            </div>
            
            <div class="numeros-suerte">
                <h4 class="highlight">Tus Números de la Suerte:</h4>
                <p>7, 14, 23, 31, 42, 55</p>
            </div>
            
            <div class="color-dia">
                <h4 class="highlight">Color del Día:</h4>
                <p>Azul Turquesa - Te traerá serenidad y claridad mental</p>
            </div>
        `;
    }

    generarResultadoOraculo(datos) {
        const respuestas = ['SÍ DEFINITIVO', 'SÍ', 'PROBABLEMENTE SÍ', 'NO DEFINITIVO', 'NO', 'PROBABLEMENTE NO', 'NEUTRAL'];
        const respuesta = respuestas[Math.floor(Math.random() * respuestas.length)];
        
        return `
            <div class="respuesta-oraculo" style="text-align: center; font-size: 2rem; margin: 30px 0;">
                <div class="highlight" style="font-size: 3rem; margin-bottom: 20px;">
                    ${respuesta.includes('SÍ') ? '✅' : respuesta.includes('NO') ? '❌' : '⚖️'}
                </div>
                <h2 class="highlight">${respuesta}</h2>
            </div>
            
            <div class="interpretacion-oraculo">
                <h4 class="highlight">Interpretación del Oráculo:</h4>
                <p>El universo ha hablado con claridad. Esta respuesta llega en el momento perfecto para guiar tu decisión.</p>
                
                <p>Recuerda que el oráculo no dicta tu futuro, sino que te muestra las energías presentes. Siempre tienes el poder de influir en los resultados con tus acciones.</p>
                
                <h4 class="highlight">Consejo Adicional:</h4>
                <p>Confía en tu intuición y mantente abierto a las señales que el universo te envía. La respuesta es solo el comienzo de tu camino hacia la claridad.</p>
            </div>
        `;
    }

    /**
     * Funciones auxiliares para nombres
     */
    obtenerNombreTirada(tipo) {
        const nombres = {
            'una_carta': 'Una Carta del Día',
            'tres_cartas': 'Pasado, Presente y Futuro',
            'cruz_celta': 'Cruz Celta',
            'herradura': 'Herradura',
            'relacion': 'Lectura de Relación',
            'amor': 'Lectura de Amor',
            'anual': 'Lectura Anual',
            'decision': 'Lectura de Decisión',
            'chakras': 'Lectura de Chakras'
        };
        return nombres[tipo] || tipo;
    }

    obtenerNombreTiradaRunas(tipo) {
        const nombres = {
            'una_runa': 'Runa del Día',
            'tres_runas': 'Pasado, Presente, Futuro',
            'cinco_runas': 'Cruz Rúnica',
            'siete_runas': 'Estrella de Siete',
            'nueve_runas': 'Cuadrado Mágico'
        };
        return nombres[tipo] || tipo;
    }

    /**
     * Muestra el resultado de la lectura
     */
    mostrarResultado(resultado) {
        document.getElementById('resultTitle').textContent = resultado.titulo;
        document.getElementById('resultSubtitle').textContent = resultado.subtitulo;
        document.getElementById('resultContent').innerHTML = resultado.contenido;
        
        // Mostrar área de resultados con animación
        const resultsArea = document.getElementById('resultsArea');
        resultsArea.style.display = 'block';
        resultsArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Ocultar formulario
        document.getElementById('dynamicForm').style.display = 'none';
        
        // Crear efecto de partículas
        if (this.configuracion.efectosParticulas) {
            this.crearParticulasResultado();
        }
        
        // Guardar en memoria para posible guardado
        this.ultimaLectura = {
            ...resultado,
            datos: this.recopilarDatosFormulario(),
            fecha: new Date().toISOString()
        };
    }

    /**
     * Efectos visuales
     */
    crearFondoCosmico() {
        const background = document.getElementById('cosmicBackground');
        
        // Crear partículas de fondo
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.width = Math.random() * 4 + 'px';
            particle.style.height = particle.style.width;
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 6 + 's';
            particle.style.animationDuration = (Math.random() * 4 + 6) + 's';
            
            background.appendChild(particle);
        }
    }

    crearParticulasResultado() {
        const container = document.getElementById('resultParticles');
        container.innerHTML = ''; // Limpiar partículas anteriores
        
        for (let i = 0; i < 10; i++) {
            const particle = document.createElement('div');
            particle.className = 'result-particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 2 + 's';
            container.appendChild(particle);
        }
    }

    efectoSeleccionModalidad() {
        // Efecto visual al seleccionar modalidad
        const cards = document.querySelectorAll('.modalidad-card');
        cards.forEach(card => {
            if (card.dataset.modalidad === this.modalidadActual) {
                card.style.transform = 'scale(1.05)';
                card.style.borderColor = 'var(--primary-gold)';
                card.style.boxShadow = 'var(--shadow-glow)';
            } else {
                card.style.opacity = '0.7';
            }
        });
        
        // Restaurar después de un tiempo
        setTimeout(() => {
            cards.forEach(card => {
                card.style.transform = '';
                card.style.opacity = '';
                if (card.dataset.modalidad !== this.modalidadActual) {
                    card.style.borderColor = '';
                    card.style.boxShadow = '';
                }
            });
        }, 2000);
    }

    efectoHoverCard(e) {
        const card = e.currentTarget;
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        card.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(212, 175, 55, 0.2), transparent)`;
    }

    removerEfectoHover(e) {
        const card = e.currentTarget;
        card.style.background = '';
    }

    /**
     * Estados de carga
     */
    mostrarCargando() {
        const overlay = document.getElementById('loadingOverlay');
        overlay.style.display = 'flex';
        
        const textos = [
            'Conectando con el universo...',
            'Interpretando las energías...',
            'Canalizando la sabiduría antigua...',
            'Alineando los astros...',
            'Preparando tu lectura...'
        ];
        
        let indiceTexto = 0;
        this.intervaloCarga = setInterval(() => {
            document.getElementById('loadingText').textContent = textos[indiceTexto];
            indiceTexto = (indiceTexto + 1) % textos.length;
        }, 1000);
    }

    ocultarCargando() {
        document.getElementById('loadingOverlay').style.display = 'none';
        if (this.intervaloCarga) {
            clearInterval(this.intervaloCarga);
        }
    }

    /**
     * Gestión de configuración
     */
    cargarConfiguracion() {
        const configGuardada = localStorage.getItem('configuracionEsoterica');
        if (configGuardada) {
            this.configuracion = { ...this.configuracion, ...JSON.parse(configGuardada) };
        }
        this.aplicarConfiguracion();
    }

    guardarConfiguracion() {
        // Obtener valores del formulario de configuración
        this.configuracion.tema = document.getElementById('themeSelect')?.value || this.configuracion.tema;
        this.configuracion.velocidadAnimacion = document.getElementById('animationSpeed')?.value || this.configuracion.velocidadAnimacion;
        this.configuracion.efectosSonido = document.getElementById('soundEffects')?.checked || this.configuracion.efectosSonido;
        this.configuracion.efectosParticulas = document.getElementById('particleEffects')?.checked ?? this.configuracion.efectosParticulas;
        
        localStorage.setItem('configuracionEsoterica', JSON.stringify(this.configuracion));
        this.aplicarConfiguracion();
        
        this.mostrarNotificacion('Configuración guardada correctamente', 'success');
    }

    aplicarConfiguracion() {
        // Aplicar tema
        document.body.className = `theme-${this.configuracion.tema}`;
        
        // Aplicar velocidad de animación
        const root = document.documentElement;
        const velocidades = {
            'fast': '0.2s',
            'normal': '0.4s',
            'slow': '0.8s'
        };
        root.style.setProperty('--animation-speed', velocidades[this.configuracion.velocidadAnimacion] || '0.4s');
        
        // Actualizar controles de configuración si existen
        const themeSelect = document.getElementById('themeSelect');
        const animationSpeed = document.getElementById('animationSpeed');
        const soundEffects = document.getElementById('soundEffects');
        const particleEffects = document.getElementById('particleEffects');
        
        if (themeSelect) themeSelect.value = this.configuracion.tema;
        if (animationSpeed) animationSpeed.value = this.configuracion.velocidadAnimacion;
        if (soundEffects) soundEffects.checked = this.configuracion.efectosSonido;
        if (particleEffects) particleEffects.checked = this.configuracion.efectosParticulas;
    }

    /**
     * Gestión de historial
     */
    cargarHistorial() {
        const historialGuardado = localStorage.getItem('historialLecturas');
        if (historialGuardado) {
            this.historialLecturas = JSON.parse(historialGuardado);
        }
        this.mostrarHistorial();
    }

    mostrarHistorial() {
        const container = document.getElementById('historialList');
        if (!container) return;
        
        if (this.historialLecturas.length === 0) {
            container.innerHTML = `
                <p style="color: var(--silver); text-align: center; padding: 40px;">
                    No hay lecturas guardadas aún. ¡Realiza tu primera consulta!
                </p>
            `;
            return;
        }
        
        const historialHTML = this.historialLecturas
            .sort((a, b) => new Date(b.fecha) - new Date(a.fecha))
            .slice(0, 10) // Mostrar solo las últimas 10
            .map(lectura => `
                <div class="historial-item" style="background: rgba(255,255,255,0.05); padding: 15px; margin: 10px 0; border-radius: 10px; border-left: 3px solid var(--primary-gold);">
                    <h4 style="color: var(--primary-gold); margin-bottom: 5px;">${lectura.titulo}</h4>
                    <p style="color: var(--silver); font-size: 0.9rem; margin-bottom: 5px;">${lectura.subtitulo}</p>
                    <p style="color: #aaa; font-size: 0.8rem;">${new Date(lectura.fecha).toLocaleString()}</p>
                    <button class="btn-secondary" onclick="sistema.verLecturaHistorial('${lectura.id}')" style="margin-top: 10px; padding: 5px 15px; font-size: 0.9rem;">
                        Ver Detalles
                    </button>
                </div>
            `).join('');
        
        container.innerHTML = historialHTML;
    }

    guardarLectura() {
        if (!this.ultimaLectura) {
            this.mostrarError('No hay lectura para guardar');
            return;
        }
        
        const lecturaParaGuardar = {
            ...this.ultimaLectura,
            id: Date.now().toString()
        };
        
        this.historialLecturas.unshift(lecturaParaGuardar);
        
        // Mantener solo las últimas 50 lecturas
        if (this.historialLecturas.length > 50) {
            this.historialLecturas = this.historialLecturas.slice(0, 50);
        }
        
        localStorage.setItem('historialLecturas', JSON.stringify(this.historialLecturas));
        this.mostrarNotificacion('Lectura guardada correctamente', 'success');
    }

    verLecturaHistorial(id) {
        const lectura = this.historialLecturas.find(l => l.id === id);
        if (lectura) {
            this.mostrarResultado(lectura);
            this.cambiarPestana('modalidades'); // Cambiar a la pestaña de modalidades para ver el resultado
        }
    }

    compartirLectura() {
        if (!this.ultimaLectura) {
            this.mostrarError('No hay lectura para compartir');
            return;
        }
        
        const textoCompartir = `${this.ultimaLectura.titulo}\n\n${this.ultimaLectura.subtitulo}\n\nConsulta realizada en: Sistema Esotérico Universal`;
        
        if (navigator.share) {
            navigator.share({
                title: this.ultimaLectura.titulo,
                text: textoCompartir,
                url: window.location.href
            });
        } else {
            // Fallback: copiar al portapapeles
            navigator.clipboard.writeText(textoCompartir).then(() => {
                this.mostrarNotificacion('Lectura copiada al portapapeles', 'success');
            });
        }
    }

    nuevaLectura() {
        document.getElementById('resultsArea').style.display = 'none';
        document.getElementById('dynamicForm').style.display = 'none';
        this.modalidadActual = null;
        
        // Restaurar apariencia de las cards
        document.querySelectorAll('.modalidad-card').forEach(card => {
            card.style.transform = '';
            card.style.borderColor = '';
            card.style.boxShadow = '';
            card.style.opacity = '';
        });
        
        this.mostrarNotificacion('¡Listo para una nueva consulta!', 'info');
    }

    cancelarFormulario() {
        document.getElementById('dynamicForm').style.display = 'none';
        this.modalidadActual = null;
        
        // Restaurar apariencia de las cards
        document.querySelectorAll('.modalidad-card').forEach(card => {
            card.style.transform = '';
            card.style.borderColor = '';
            card.style.boxShadow = '';
            card.style.opacity = '';
        });
    }

    /**
     * Funciones de utilidad
     */
    mostrarError(mensaje) {
        this.mostrarNotificacion(mensaje, 'error');
    }

    mostrarNotificacion(mensaje, tipo = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${tipo}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 10px;
            color: white;
            font-weight: bold;
            z-index: 2000;
            animation: slideInRight 0.3s ease-out;
            max-width: 300px;
        `;
        
        const colores = {
            'success': 'background: linear-gradient(135deg, #28a745, #20c997);',
            'error': 'background: linear-gradient(135deg, #dc3545, #fd7e14);',
            'info': 'background: linear-gradient(135deg, #17a2b8, #6f42c1);'
        };
        
        notification.style.cssText += colores[tipo] || colores.info;
        notification.textContent = mensaje;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    manejarTeclado(e) {
        // Navegación con teclado
        if (e.key === 'Escape') {
            if (document.getElementById('loadingOverlay').style.display === 'flex') {
                // No permitir cerrar durante carga
                return;
            }
            
            if (document.getElementById('dynamicForm').style.display === 'block') {
                this.cancelarFormulario();
            } else if (document.getElementById('resultsArea').style.display === 'block') {
                this.nuevaLectura();
            }
        }
    }

    iniciarEfectosAmbientales() {
        // Efectos ambientales sutiles
        if (this.configuracion.efectosParticulas) {
            setInterval(() => {
                this.crearParticulaAmbiental();
            }, 3000);
        }
    }

    crearParticulaAmbiental() {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: fixed;
            width: 2px;
            height: 2px;
            background: var(--primary-gold);
            border-radius: 50%;
            pointer-events: none;
            z-index: 1;
            opacity: 0;
        `;
        
        particle.style.left = Math.random() * window.innerWidth + 'px';
        particle.style.top = window.innerHeight + 'px';
        
        document.body.appendChild(particle);
        
        // Animar partícula
        particle.animate([
            { opacity: 0, transform: 'translateY(0)' },
            { opacity: 0.8, transform: 'translateY(-50px)' },
            { opacity: 0, transform: `translateY(-${window.innerHeight + 100}px)` }
        ], {
            duration: 8000,
            easing: 'linear'
        }).onfinish = () => {
            document.body.removeChild(particle);
        };
    }
}

// CSS dinámico para animaciones adicionales
const styleSheet = document.createElement('style');
styleSheet.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .resultado-cartas {
        display: grid;
        gap: 20px;
        margin: 20px 0;
    }
    
    .carta-resultado {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border-left: 3px solid var(--primary-gold);
    }
    
    .runa-individual {
        text-align: center;
        font-size: 1.5rem;
        margin: 10px 0;
        padding: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    .hexagrama {
        text-align: center;
        margin: 30px 0;
        padding: 20px;
        background: rgba(212, 175, 55, 0.1);
        border-radius: 15px;
    }
    
    .historial-item:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        transform: translateX(5px);
        transition: all 0.3s ease;
    }
`;

document.head.appendChild(styleSheet);

// Inicializar el sistema cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.sistema = new SistemaEsotericoPro();
});

// Exportar para uso global
window.SistemaEsotericoPro = SistemaEsotericoPro;