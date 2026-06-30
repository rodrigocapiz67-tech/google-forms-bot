# Google Forms Bot

Bot automatizado para llenar y enviar formularios de Google Forms con datos sintéticos realistas usando Playwright.

## Requisitos

- Python 3.8+
- Playwright (`pip install playwright`)
- Navegadores Chromium instalados (`playwright install chromium`)

## Instalación

```bash
pip install -r requirements.txt
playwright install chromium
```

## Uso

```bash
python form_bot.py <URL_DE_GOOGLE_FORM> [numero_de_envios]
```

### Ejemplos

```bash
# Enviar 10 respuestas (por defecto)
python form_bot.py "https://docs.google.com/forms/d/e/..."

# Enviar 50 respuestas
python form_bot.py "https://docs.google.com/forms/d/e/..." 50
```

## Archivos principales

| Archivo | Descripción |
|---------|-------------|
| `form_bot.py` | Script principal del bot. Navega el formulario, detecta tipos de pregunta (opción múltiple, checkboxes, texto, dropdown, textarea, escala lineal, cuadrícula) y los llena con datos generados aleatoriamente. |
| `botdeformulario/form_bot.py` | Copia del script principal en una subcarpeta. |
| `requirements.txt` | Dependencia: `playwright>=1.45.0`. |
| `test_url.py` | Script de prueba rápida que abre un formulario e inspecciona sus elementos (items, botones). |
| `debug_form.py` | Script de depuración que captura un screenshot y lista en consola todos los selectores disponibles del formulario. |

### Scripts de depuración (`debug_form*.py`)

Versiones iterativas usadas durante el desarrollo para diagnosticar problemas de selectores y renderizado en diferentes formularios de Google.

## Características

- **Detección inteligente del tipo de pregunta**: soporta radio buttons, checkboxes, inputs de texto, textareas y dropdowns.
- **Generación contextual de datos**: detecta palabras clave en la pregunta (nombre, email, teléfono, edad, ciudad, empresa, fecha, DNI, etc.) y genera valores coherentes.
- **Soporte multi-página**: navega formularios con varias secciones detectando botones "Siguiente" / "Next".
- **Pantalla de bienvenida**: detecta y salta automáticamente la pantalla inicial.
- **Prevención de bucles**: detecta páginas que no cambian (errores de validación) y aborta.
- **Procesamiento por lotes**: envía las respuestas en lotes de 3, abriendo/cerrando el navegador entre lotes para evitar detección.
- **Localización**: configurado con locale `es-MX` y zona horaria `America/Mexico_City`.

## Funcionamiento interno

1. El bot abre el formulario con Playwright en modo headless.
2. Espera a que el DOM del formulario cargue completamente.
3. Detecta todas las preguntas visibles (`div[role="listitem"]`).
4. Para cada pregunta, identifica el tipo de control y aplica la estrategia de llenado correspondiente.
5. La función `smart_generate()` analiza el texto de la etiqueta para generar datos contextuales (nombres, correos, teléfonos peruanos `+51`, direcciones, etc.).
6. Navega entre páginas hasta llegar al botón "Enviar".
