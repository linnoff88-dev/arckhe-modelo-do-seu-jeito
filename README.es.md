# Modelo a Tu Manera

🎬 Vídeo: https://www.youtube.com/watch?v=3U8jk69yt3M

[![Modelo a Tu Manera](guia/assets/banner-es.jpg)](https://linnoff88-dev.github.io/arckhe-/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

¿Tu modelo de IA abierto a veces rechaza una pregunta inofensiva o promete algo que no sabe? Este kit te ayuda a ajustar una copia de ese modelo en tu computadora, sin entrenarlo desde cero. Ofrece dos caminos: **menos rechazos indebidos** y **ajuste de comportamiento**. Es para quienes usan modelos abiertos y quieren comprobar el cambio comparando el antes y el después. Necesitas una máquina capaz de ejecutar el modelo. La edición se hace con [Heretic](https://github.com/p-e-w/heretic).

> **Estado actual:** el kit aún no se ha ejecutado en un modelo. Las rúbricas, los datos, las configuraciones y la comparación tienen pruebas automáticas sin modelo, y las configuraciones pasaron la validación de Heretic. Por eso no hay resultados medidos para mostrar. El primer uso real será una prueba.

## 📖 Guía

Guía completa: **https://linnoff88-dev.github.io/arckhe-/guia/es/**

## Empieza pidiéndoselo a tu IA

Claude Code y Codex son asistentes que trabajan en tu computadora; deben estar instalados y tener una cuenta activa. Abre uno de ellos en una carpeta vacía y pega:

```text
Lee el repositorio https://github.com/linnoff88-dev/modelo-do-seu-jeito, especialmente el README.
Después comprueba si mi computadora puede ejecutar el proceso y pregúntame qué modelo abierto quiero usar
y qué cambio quiero: menos rechazos indebidos o ajuste de comportamiento.
Explícame en lenguaje sencillo qué se instalará y descargará, cuánto ocupará y cuáles son los riesgos.
No instales, descargues ni cambies nada antes de que te dé el sí. Mantén intacto el modelo original.
```

## Los dos modos

| Modo | Problema | Qué cambia | Cómo se aprueba |
|---|---|---|---|
| `modos/menos-recusas` | El modelo rechaza pedidos inofensivos: historias, salud, derechos, «matar un proceso» | Reduce los rechazos indebidos | Responde con contenido en al menos el 80 % de los casos nuevos y pierde como máximo 10 puntos en preguntas comunes |
| `modos/pedir-antes` | En la atención al cliente, el modelo inventa un valor o promete crédito sin tener los datos | Pide el dato que falta y, cuando lo tiene, responde directamente | Al menos el 80 % en cada situación y una pérdida máxima de 10 puntos en preguntas comunes |

El modo de rechazos usa solo ejemplos inofensivos. El objetivo es corregir rechazos erróneos, no eliminar la protección contra pedidos peligrosos. La edición puede tener efectos más allá de los ejemplos, así que compara antes de usarla.

## Solo funciona con modelos abiertos

Para editar se necesitan los archivos de pesos del modelo y una máquina bajo tu control, propia o alquilada. La API de un proveedor entrega solo el texto de la respuesta, así que no se puede aplicar la edición. Los servicios que ya ofrecen modelos modificados son otra opción: usas su modelo, no el tuyo.

## Primero, prueba si basta con dar instrucciones

Editar lleva tiempo y puede empeorar el modelo. Cada modo incluye un `instrucao-forte.txt`, y la comparación mide tres versiones en paralelo: el modelo original, el original con instrucciones fuertes y la copia editada. Si basta con las instrucciones, quizá no necesites editarlo.

## Próximas ideas

La tabla de [SUGESTOES.md](SUGESTOES.md) reúne otros comportamientos que se pueden probar. (SUGESTOES.md y DO-HERETIC.md están en portugués). Lo que aprovechamos de Heretic y lo que añadimos está en [DO-HERETIC.md](DO-HERETIC.md).

---

## El proceso, de principio a fin

Leyenda: 🧠 tú decides · ⚙️ script o comando

Los comandos se escribieron para Linux y macOS. Windows no se ha verificado.

0. ⚙️ Descarga el kit y entra en la carpeta:
   ```sh
   git clone https://github.com/linnoff88-dev/modelo-do-seu-jeito.git
   cd modelo-do-seu-jeito
   ```
1. 🧠 Elige un modelo abierto, comprueba su licencia y consulta el tamaño de los pesos en su página.
2. ⚙️ Comprueba la máquina, cambiando 8 por el tamaño de los pesos en GB:
   `python3 kit/checar_maquina.py --pesos-gb 8`
3. ⚙️ Crea el entorno, instala la versión de [PyTorch 2.6+ adecuada para tu tarjeta](https://pytorch.org/get-started/locally/) y luego el resto:
   ```sh
   python3 -m venv .venv && . .venv/bin/activate
   pip install "heretic-llm @ git+https://github.com/p-e-w/heretic@64e999152ff7918efc73576814709b6b6a71f15c" transformers accelerate pytest
   ```
4. ⚙️ Descarga el modelo original. El ejemplo usa Qwen3-4B:
   `hf download Qwen/Qwen3-4B-Instruct-2507 --local-dir modelos/original`
5. ⚙️ Registra la huella digital del original. Si abres otra terminal después, reactiva el entorno con `. .venv/bin/activate`:
   `python kit/impressao.py gerar modelos/original modelos/impressao-original.json`
6. 🧠 Entra en el modo y adapta los ejemplos de `dados/` a tu caso, como se explica en [Cómo adaptar los datos](#cómo-adaptar-los-datos):
   `cd modos/menos-recusas` o `cd modos/pedir-antes`
7. ⚙️ Recopila las respuestas antes de editar:
   ```sh
   python ../../kit/responder.py --modelo ../../modelos/original --saida ../../respostas/original.jsonl
   python ../../kit/responder.py --modelo ../../modelos/original --instrucao instrucao-forte.txt --saida ../../respostas/instruido.jsonl
   python ../../kit/avaliar.py --original ../../respostas/original.jsonl --instruido ../../respostas/instruido.jsonl
   ```
   Si el resultado es `NADA A CORRIGIR`, detente aquí. Si es `A INSTRUÇêO RESOLVE`, usa las instrucciones y no edites el modelo.
8. ⚙️ Haz una prueba piloto breve: `heretic --n-trials 12 --n-startup-trials 6 --model ../../modelos/original`
9. 🧠 Heretic muestra los mejores resultados. Las dos puntuaciones deben ser bajas: la del objetivo y la de divergencia respecto al original (KL). La prueba piloto tiene sentido si bajó la puntuación del objetivo sin que se disparara la divergencia. Para continuar, elige `Run additional trials` en el menú y solicita más intentos. El valor predeterminado de Heretic es 100 en total. Luego elige un resultado y guárdalo en `../../modelos/ajustado`. Con la configuración predeterminada, Heretic estima entre 30 y 40 minutos para este modelo en una RTX 3090. Este kit no midió el tiempo.
10. ⚙️ Recopila las respuestas de la copia y compara las tres versiones:
    ```sh
    python ../../kit/responder.py --modelo ../../modelos/ajustado --saida ../../respostas/ajustado.jsonl
    python ../../kit/avaliar.py --original ../../respostas/original.jsonl --instruido ../../respostas/instruido.jsonl --modificado ../../respostas/ajustado.jsonl
    ```
11. ⚙️ Comprueba que el original no haya cambiado: `python ../../kit/impressao.py conferir ../../modelos/original ../../modelos/impressao-original.json`
12. 🧠 Lee una muestra de las respuestas. Después escribe preguntas nuevas, con el criterio definido antes de ver las respuestas, y ejecuta los pasos 7 y 10 con `--casos` y con otros nombres en `--saida` para no sobrescribir las respuestas anteriores.

Resultados de la comparación: `0` aprobado o hay algo que corregir, `1` no aprobado, `2` inconcluso, `3` nada que corregir, `4` las instrucciones ya resuelven el problema.

## Instalación técnica

- Python 3.11+, PyTorch 2.6+, `git` y espacio para el modelo original y sus copias.
- El comprobador usa un margen estimado: memoria equivalente a 2 veces y disco equivalente a 3 veces el tamaño de los pesos. No es una medición.
- Pruebas sin modelo: `python -m pytest -q`.

| Carpeta | Contenido |
|---|---|
| `kit/` | comprobación de la máquina, huella digital, recopilación de respuestas y comparación |
| `modos/*/config.toml` | configuración de Heretic |
| `modos/*/regua.py` | qué cuenta como respuesta correcta |
| `modos/*/dados/` | contraste, optimización, preguntas comunes y evaluación separada |
| `modos/*/instrucao-forte.txt` | alternativa sin edición |
| `modos/pedir-antes/plugin_heretic.py` | puntuación propia para Heretic |

Las configuraciones usan solo archivos locales y no descargan los conjuntos de datos predeterminados de Heretic.

## Cómo adaptar los datos

Los archivos `.txt` tienen una pregunta por línea. Los archivos `.jsonl` tienen un caso por línea, con un `id` único, `tipo` y `pedido`.

| Modo | Tipo | Campos adicionales |
|---|---|---|
| `menos-recusas` | `recusa_indevida` | `deve_citar`: lista de términos; basta con que aparezca uno |
| `menos-recusas` | `comum` | `esperado`: texto que debe aparecer |
| `pedir-antes` | `neutra` | `esperado`: texto que debe aparecer |
| `pedir-antes` | `sem_dados`, `abaixo_limite` | ninguno |
| `pedir-antes` | `com_dados` | `esperado`: valor numérico correcto |

En el modo `menos-recusas`, pon en `dados/recusadas.txt` y `dados/otimizacao.txt` solo pedidos inofensivos que tu modelo rechaza. Las preguntas normales van en `dados/comuns.txt`. No repitas frases entre los archivos.

Los ejemplos incluidos están en portugués. Para otro idioma, traduce los datos y las instrucciones, incluido `system_prompt`, y comprueba `keyword_markers` en `config.toml` y los patrones de `regua.py`. La rúbrica reconoce rechazos en portugués, inglés y español.

El modo `pedir-antes` incluye el ejemplo de una aplicación de citas. Para otro negocio, cambia las instrucciones en `config.toml` y `instrucao-forte.txt`, edita las frases en `gerar_dados.py` y ejecuta `python gerar_dados.py`.

Después de congelar la copia, escribe las preguntas nuevas en otro `.jsonl`, con el mismo formato, y pasa ese archivo con `--casos` a `responder.py` y `avaliar.py`.

(Los archivos de datos del kit están en portugués.)

## Límites

- La rúbrica reconoce patrones de texto y no sustituye la revisión humana.
- Aprobar los casos del kit no demuestra seguridad ni precisión fuera de ellos.
- La compresión o el cambio de formato pueden alterar el comportamiento. Vuelve a comparar después de convertir.
- Un modelo editado puede seguir equivocándose en hechos. En productos con usuarios, mantén la revisión y las protecciones propias.
- Respeta la licencia del modelo y las leyes aplicables.

## Base y licencia

Basado en [Heretic](https://github.com/p-e-w/heretic), de Philipp Emanuel Weidmann y colaboradores, en la versión `64e9991`. Este proyecto usa la misma licencia: [AGPL-3.0](LICENSE).
