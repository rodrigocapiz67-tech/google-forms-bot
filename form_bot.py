import asyncio
import random
import string
import sys
import re
from datetime import datetime

from playwright.async_api import async_playwright, TimeoutError as PTimeout


FIRST_NAMES = [
    "Lucas", "Emma", "Sofia", "Mateo", "Isabella", "Santiago", "Valentina",
    "Benjamin", "Gabriela", "Daniel", "Camila", "Sebastian", "Mia", "Joaquin",
    "Luna", "Alejandro", "Victoria", "Diego", "Martina", "Nicolas",
    "James", "Maria", "John", "Lisa", "Michael", "Sarah", "David", "Emily",
    "Robert", "Jessica", "William", "Ashley", "Joseph", "Amanda", "Thomas",
]

LAST_NAMES = [
    "Garcia", "Rodriguez", "Martinez", "Lopez", "Gonzalez", "Hernandez",
    "Perez", "Torres", "Ramirez", "Flores", "Smith", "Johnson", "Williams",
    "Brown", "Jones", "Davis", "Miller", "Wilson", "Moore", "Taylor",
    "Andersen", "O'Brien", "Mueller", "Schmidt", "Fischer", "Weber",
]

COMPANIES = [
    "TechCorp", "DataFlow", "Innovate Inc", "CloudBase", "NexGen Solutions",
    "Alpha Digital", "StartupLab", "WebCraft", "SmartSoft", "GreenLeaf Tech",
]

CITIES = [
    "Mexico City", "Buenos Aires", "Bogota", "Santiago", "Lima",
    "New York", "Los Angeles", "Chicago", "Miami", "Austin",
    "Madrid", "Barcelona", "Valencia", "Seville", "Bilbao",
]

DOMAINS = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com", "testmail.com"]

# Academic/Likert scale responses in Spanish
LIKERT_OPTIONS = [
    "Totalmente en desacuerdo", "En desacuerdo", "Neutral",
    "De acuerdo", "Totalmente de acuerdo"
]
FREQUENCY_OPTIONS = [
    "Nunca", "Casi nunca", "Ocasionalmente", "Frecuentemente", "Muy frecuentemente"
]
SATISFACTION_OPTIONS = [
    "Muy insatisfecho", "Insatisfecho", "Neutral", "Satisfecho", "Muy satisfecho"
]


def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def random_email(name=None):
    if name:
        base = name.lower().replace(" ", ".").replace("'", "")
    else:
        base = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 12)))
    num = random.randint(1, 999)
    return f"{base}{num}@{random.choice(DOMAINS)}"

def random_phone():
    return f"+51{random.randint(900000000, 999999999)}"

def random_number(max_val=100):
    return str(random.randint(1, max_val))

def random_paragraph(min_words=5, max_words=30):
    words = []
    for _ in range(random.randint(min_words, max_words)):
        words.append(''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10))))
    return ' '.join(words).capitalize() + '.'

def random_company():
    return random.choice(COMPANIES)

def random_city():
    return random.choice(CITIES)

def random_date():
    year = random.randint(2020, 2025)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"


def smart_generate(label_text):
    label_lower = label_text.lower()

    if any(w in label_lower for w in ['nombre', 'name', 'apellido', 'nombres']):
        return random_name()
    if any(w in label_lower for w in ['email', 'correo', 'mail', 'electrónico']):
        return random_email()
    if any(w in label_lower for w in ['tel', 'phone', 'celular', 'movil', 'whatsapp', 'telefono']):
        return random_phone()
    if any(w in label_lower for w in ['edad', 'age']):
        return random_number(65)
    if any(w in label_lower for w in ['ciudad', 'city', 'pais', 'country', 'state', 'estado', 'distrito', 'provincia', 'departamento']):
        return random.choice(["Arequipa", "Lima", "Cusco", "Trujillo", "Cercado", "San Juan de Dios", "Yanahuara", "Cayma", "Socabaya", "Jose Luis Bustamante"])
    if any(w in label_lower for w in ['empresa', 'company', 'compania', 'trabajo', 'organización', 'organizacion']):
        return random_company()
    if any(w in label_lower for w in ['fecha', 'date', 'dia', 'año', 'a�o']):
        return random_date()
    if any(w in label_lower for w in ['direccion', 'address', 'domicilio']):
        return f"Calle {random.choice(['Los Olivos', 'Las Flores', 'Arequipa', 'Peru', 'San Martin', 'Bolivar'])} #{random.randint(100, 9999)}"
    if any(w in label_lower for w in ['dni', 'documento', 'identidad', 'id', 'identif']):
        return ''.join(random.choices(string.digits, k=8))
    if any(w in label_lower for w in ['ingreso', 'sueldo', 'salario', 'gana']):
        return str(random.randint(1130, 6000))
    if any(w in label_lower for w in ['en total']) and any(w in label_lower for w in ['gasta', 'gasto']):
        return str(random.randint(200, 400))
    if any(w in label_lower for w in ['gasta', 'gasto', 'dinero', 'total']):
        return str(random.randint(50, 3000))
    if any(w in label_lower for w in ['cuantas', 'cuantas', 'cuanto', 'cuanto', 'frecuencia', 'veces']):
        return str(random.randint(1, 20))
    if any(w in label_lower for w in ['producto', 'articulo', 'distintos', 'adquiere']):
        return str(random.randint(1, 10))

    return random.choice([
        "Si", "No", "Tal vez",
        "Muy satisfecho", "Satisfecho", "Neutral", "Insatisfecho",
        "Excelente", "Bueno", "Regular", "Malo",
    ])


async def get_question_label(page, question_el):
    """Extract the question label/text from a question element."""
    for selector in ['[role="heading"]', '.M7eMe', '.Qr7Oae', '.Y6L3X', 'div[role="listitem"] > div:first-child']:
        try:
            el = question_el.locator(selector).first
            if await el.count() > 0:
                return await el.inner_text()
        except:
            pass
    try:
        text = await question_el.inner_text()
        return text[:100]
    except:
        return ""


async def fill_visible_questions(page):
    """Find and fill all visible questions on the current page."""
    filled_count = 0

    q_selectors = [
        'div[role="listitem"]',
    ]

    questions = page.locator('div[role="listitem"]')
    q_count = await questions.count()

    if q_count == 0:
        return 0

    for i in range(q_count):
        q = questions.nth(i)
        if not await q.is_visible():
            continue

        label = await get_question_label(page, q)
        print(f"    Pregunta {i+1}: {label[:60]}")

        filled = False

        # Try radio groups (multiple choice, scale, grid rows)
        radio_groups = q.locator('div[role="radiogroup"]')
        rg_count = await radio_groups.count()
        if rg_count > 0:
            did_click = False
            for rg_idx in range(rg_count):
                rg = radio_groups.nth(rg_idx)
                radios = rg.locator('div[role="radio"]')
                r_count = await radios.count()
                if r_count >= 1:
                    idx = random.randint(0, r_count - 1)
                    for attempt in range(3):
                        try:
                            await radios.nth(idx).click()
                            await asyncio.sleep(0.2)
                            checked = await radios.nth(idx).get_attribute('aria-checked')
                            if checked == 'true':
                                did_click = True
                                break
                        except:
                            await asyncio.sleep(0.3)
            if did_click:
                filled = True

        if not filled:
            try:
                label_el = q.locator('label[for]').first
                if await label_el.count() > 0:
                    await label_el.click(force=True)
                    await asyncio.sleep(0.5)
                    # Verify it registered
                    radio = q.locator('[role="radio"]').first
                    if await radio.count() > 0:
                        checked = await radio.get_attribute('aria-checked')
                        if checked == 'true':
                            filled = True
                    else:
                        filled = True
            except:
                pass

        if not filled:
            radios = q.locator('div[role="radio"]')
            r_count = await radios.count()
            if r_count >= 1:
                idx = random.randint(0, r_count - 1)
                for attempt in range(3):
                    try:
                        await radios.nth(idx).click()
                        filled = True
                        break
                    except:
                        await asyncio.sleep(0.3)

        # Checkboxes
        if not filled:
            chk_labels = q.locator('label[for]')
            c_count = await chk_labels.count()
            if c_count > 1:
                num_to_check = random.randint(1, min(c_count, 3))
                indices = random.sample(range(c_count), num_to_check)
                for idx in indices:
                    for attempt in range(3):
                        try:
                            await chk_labels.nth(idx).click()
                            await asyncio.sleep(0.2)
                            break
                        except:
                            await asyncio.sleep(0.3)
                filled = True

        if not filled:
            checkboxes = q.locator('div[role="checkbox"]')
            c_count = await checkboxes.count()
            if c_count > 1:
                num_to_check = random.randint(1, min(c_count, 3))
                indices = random.sample(range(c_count), num_to_check)
                for idx in indices:
                    for attempt in range(3):
                        try:
                            is_checked = await checkboxes.nth(idx).get_attribute('aria-checked')
                            if is_checked != 'true':
                                await checkboxes.nth(idx).click()
                                await asyncio.sleep(0.2)
                            break
                        except:
                            await asyncio.sleep(0.3)
                filled = True

        # Text inputs
        if not filled:
            text_input = q.locator('input[type="text"]').first
            if await text_input.count() > 0:
                value = smart_generate(label)
                for attempt in range(3):
                    try:
                        await text_input.click()
                        await text_input.fill(value)
                        await asyncio.sleep(0.3)
                        current_val = await text_input.input_value()
                        if current_val == value:
                            filled = True
                            break
                    except:
                        await asyncio.sleep(0.3)

        # Textareas
        if not filled:
            textarea = q.locator('textarea').first
            if await textarea.count() > 0:
                value = random_paragraph(8, 20) if not label else smart_generate(label)
                for attempt in range(3):
                    try:
                        await textarea.fill(value)
                        filled = True
                        break
                    except:
                        await asyncio.sleep(0.3)

        # Dropdown
        if not filled:
            listbox = q.locator('div[role="listbox"]').first
            if await listbox.count() > 0:
                for attempt in range(3):
                    try:
                        await listbox.click()
                        await asyncio.sleep(0.5)
                        options = page.locator('div[role="option"]:not([aria-disabled="true"])')
                        opt_count = await options.count()
                        if opt_count > 0:
                            idx = random.randint(0, opt_count - 1)
                            opt_text = await options.nth(idx).inner_text()
                            if opt_text.strip() and 'Seleccionar' not in opt_text:
                                await options.nth(idx).click()
                                filled = True
                                break
                        await page.keyboard.press('Escape')
                    except:
                        await asyncio.sleep(0.3)

        status = "OK" if filled else "SKIP"
        if not filled:
            tag_name = await q.locator('*').first.evaluate('el => el.tagName')
            class_list = await q.get_attribute('class') or ""
            print(f"    [{status}] Pregunta {i+1} - tag={tag_name} class={class_list[:50]}")
        else:
            print(f"    [{status}] Pregunta {i+1}")
            filled_count += 1

        await asyncio.sleep(random.uniform(0.3, 0.6))

    return filled_count


async def click_btn(page, text):
    for sel in [
        f'div[role="button"]:has-text("{text}")',
        f'span.NPEfkd:has-text("{text}")',
    ]:
        try:
            btn = page.locator(sel).first
            if await btn.count() > 0:
                await btn.click(force=True, timeout=5000)
                return True
        except:
            pass
    return False


async def click_siguiente(page):
    return await click_btn(page, "Siguiente") or await click_btn(page, "Next")


async def click_enviar(page):
    return await click_btn(page, "Enviar") or await click_btn(page, "Submit")


async def fill_form(page, url):
    await page.goto(url, wait_until="networkidle")
    current_url = page.url
    print(f"  URL actual: {current_url[:100]}")
    title = await page.title()
    print(f"  Titulo: {title[:80]}")

    # Wait for the form to render fully
    await asyncio.sleep(3)

    list_count = await page.locator('[role="list"]').count()
    o3_count = await page.locator('.o3Dpx').count()
    print(f"  [role=list]: {list_count}, .o3Dpx: {o3_count}")

    if list_count == 0 and o3_count == 0:
        print("  Error: No se encontro el contenedor del formulario")
        await page.screenshot(path=r"C:\Users\Asus\Desktop\google-forms-bot\error.png")
        body_text = await page.locator('body').inner_text()
        print(f"  Body text (first 500): {body_text[:500]}")
        return False

    await asyncio.sleep(2)

    # Check if we're on a welcome screen. If the list is empty and there's a Siguiente button,
    # click it to proceed to the questions.
    list_el = page.locator('[role="list"]')
    list_children = await list_el.locator('> *').count()
    tiene_siguiente = False
    for sel in ['span.NPEfkd:has-text("Siguiente")', 'div[role="button"]:has-text("Siguiente")']:
        if await page.locator(sel).first.count() > 0 and await page.locator(sel).first.is_visible():
            tiene_siguiente = True
            break

    if list_children == 0 and tiene_siguiente:
        print("  Pantalla de bienvenida detectada, avanzando...")
        await click_siguiente(page)
        await asyncio.sleep(2)

    max_pages = 10
    page_count = 0

    prev_signature = ""

    while page_count < max_pages:
        page_count += 1
        print(f"  --- Pagina {page_count} ---")

        await asyncio.sleep(1)

        try:
            await page.wait_for_selector('div[role="listitem"]', timeout=10000)
        except PTimeout:
            print("  No se encontraron preguntas en esta pagina")
            break

        # Get current page signature
        items = page.locator('div[role="listitem"]')
        sig_parts = []
        for k in range(min(5, await items.count())):
            t = await items.nth(k).inner_text()
            sig_parts.append(t[:40])
        current_sig = "|".join(sig_parts)

        if prev_signature and current_sig == prev_signature:
            print("  La pagina no cambio, probablemente hay un error de validacion")
            break
        prev_signature = current_sig

        filled = await fill_visible_questions(page)

        await asyncio.sleep(0.5)

        # Debug: show all buttons on page
        btns = page.locator('div[role="button"]')
        btn_texts = []
        for k in range(await btns.count()):
            t = (await btns.nth(k).inner_text()).strip()
            if t:
                btn_texts.append(t)
        print(f"  Botones disponibles: {btn_texts[:5]}")

        if await click_btn(page, "Enviar"):
            print("  Formulario enviado!")
            await asyncio.sleep(2)
            return True

        if await click_btn(page, "Siguiente"):
            await asyncio.sleep(3)
            items_count = await page.locator('div[role="listitem"]').count()
            first_text = (await page.locator('div[role="listitem"]').first.inner_text())[:50] if items_count > 0 else ""
            new_count = items_count
            for _ in range(14):
                await asyncio.sleep(0.5)
                new_count = await page.locator('div[role="listitem"]').count()
                new_first = (await page.locator('div[role="listitem"]').first.inner_text())[:50] if new_count > 0 else ""
                if new_count != items_count or new_first != first_text:
                    break
            print(f"  Siguiente ({items_count}->{new_count})")
            continue

        print("  No se encontro boton de navegacion")
        break

    return False


BATCH_SIZE = 3


async def main():
    if len(sys.argv) < 2:
        print("Uso: python form_bot.py <URL_DE_GOOGLE_FORM> [numero_de_envios]")
        print("")
        print("Ejemplo:")
        print('  python form_bot.py "https://docs.google.com/forms/d/e/..."')
        print('  python form_bot.py "https://docs.google.com/forms/d/e/..." 50')
        sys.exit(1)

    url = sys.argv[1]
    num_submissions = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    if "docs.google.com/forms" not in url:
        print("Error: La URL debe ser un Google Forms valido")
        sys.exit(1)

    print("=" * 50)
    print("Google Forms Bot - Generador de Datos de Prueba")
    print(f"URL: {url}")
    print(f"Envios a realizar: {num_submissions}")
    print(f"Inicio: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)

    success_count = 0

    async with async_playwright() as p:
        for batch_start in range(0, num_submissions, BATCH_SIZE):
            batch_count = min(BATCH_SIZE, num_submissions - batch_start)
            print(f"\n--- Lote {(batch_start // BATCH_SIZE) + 1} ({batch_start+1}-{batch_start+batch_count}) ---")

            try:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    locale="es-MX",
                    timezone_id="America/Mexico_City",
                )

                for i in range(batch_count):
                    num = batch_start + i + 1
                    print(f"\n[{num}/{num_submissions}] Enviando...")
                    page = await context.new_page()
                    try:
                        ok = await fill_form(page, url)
                        if ok:
                            success_count += 1
                        wait_time = random.uniform(3, 6)
                        print(f"  Esperando {wait_time:.1f}s...")
                        await asyncio.sleep(wait_time)
                    except Exception as e:
                        print(f"  Error: {e}")
                    finally:
                        await page.close()

                await browser.close()
            except Exception as e:
                print(f"  Error en lote: {e}")
                await asyncio.sleep(5)

            await asyncio.sleep(3)

    print("=" * 50)
    print(f"Finalizado: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Envios exitosos: {success_count}/{num_submissions}")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
