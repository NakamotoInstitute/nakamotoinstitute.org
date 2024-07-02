La Prueba de Trabajo Reutilizable (RPOW) fue inventada por Hal Finney como un prototipo de dinero efectivo digital basado en la [teoría de los coleccionables de Nick Szabo](/library/shelling-out/). RPOW fue un importante paso temprano en la historia del dinero digital y fue un precursor de Bitcoin. Aunque nunca pretendió ser más que un prototipo, RPOW fue un software muy sofisticado que habría sido capaz de servir a una red gigantesca si hubiese agarrado vuelo.

## Contexto histórico

En los años 90, los Cypherpunks comenzaron a jugar con la idea de un dinero efectivo digital cuyo valor no dependiera de que una organización lo emita. Siguiendo a Nick Szabo, esta forma de efectivo digital se reconocería por ser limitada en la oferta, y por lo tanto utilizable como dinero, al ser demostrablemente difícil de crear. Esto podría hacerse definiendo las unidades del efectivo digital en términos de una prueba-de-trabajo. Algunas propuestas para coleccionables digitales circularon en la lista de correo cypherpunk, incluyendo [b-money](/library/b-money/) de Wei Dai y [Bit Gold](/library/bit-gold/) de Nick Szabo. RPOW fue el único coleccionable digital capaz de funcionar como una pieza de software.

## Cómo funciona

Un cliente RPOW crea un token RPOW proporcionando una secuencia de prueba de trabajo de una determinada dificultad, firmada con su clave privada. El servidor entonces registra ese token como perteneciente a la clave que firma. El cliente puede luego dar el token a otra clave firmando una orden de transferencia a una clave pública. A continuación, el servidor registra debidamente el token como perteneciente a la clave privada correspondiente.

El problema del doble gasto es fundamental para todo dinero efectivo digital. RPOW resuelve este problema manteniendo la propiedad de los tokens registrada en un servidor de confianza. Sin embargo, RPOW fue construido con un sofisticado modelo de seguridad destinado a hacer que el servidor que gestiona el registro de todos los tokens de RPOW sea más fiable que un banco ordinario. Los servidores están diseñados para funcionar en el coprocesador criptográfico seguro IBM 4758 que es capaz de verificar de forma segura el hash del software que está ejecutando. Los servidores RPOW son capaces de cooperar para atender más solicitudes.

Para más información, por favor ve la [página original](/finney/rpower/index.html), que incluye una [reseña](/finney/rpower/index.html), una [página de preguntas frecuentes](/finney/rpower/faqs.html), una [página con teoría](/finney/rpower/theory.html), una [presentación](/finney/rpower/slides/slide001.html), y una página muy interesante llamada [el mundo de RPOW](/finney/rpower/world.html), que explica cómo RPOW habría escalado para servir a todo el planeta.

El código original se puede encontrar en GitHub [here](https://github.com/NakamotoInstitute/RPOW).

_Agradecimiento especial a Fran y Jason Finney, esposa e hijo de Hal, por compartir el código original de RPOW y archivos del sitio web._
