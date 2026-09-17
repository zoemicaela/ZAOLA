import flet as ft

def main(page: ft.Page):
    page.title = "AhorraYa - Tu Banco Digital"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#F8F9FA"
    page.window_width = 400
    page.window_height = 750
    page.window_resizable = False

    # Variables de estado globales para el usuario y sus finanzas
    user_state = {
        "nombre": "",
        "saldo": 1250.50,
        "movimientos": [
            {"titulo": "Comida / Snacks", "sub": "Ayer", "monto": "- S/ 25.00", "color": ft.colors.RED},
            {"titulo": "Útiles de estudio", "sub": "Hace 3 días", "monto": "- S/ 45.00", "color": ft.colors.RED},
        ],
        "candados": [
            {"titulo": "Recibo de Luz", "icono": ft.icons.LIGHTBULB, "monto": "S/ 120.00", "fecha": "28 de cada mes"},
            {"titulo": "Recibo de Agua", "icono": ft.icons.WATER_DROP, "monto": "S/ 80.00", "fecha": "30 de cada mes"},
        ],
        "viaje": {
            "destino": "Paracas / Playa 🏖️",
            "meta": 1200.00,
            "integrantes": [
                {"nombre": "Tú", "monto": 200.00},
                {"nombre": "Juan", "monto": 150.00},
                {"nombre": "Lucía", "monto": 100.00}
            ]
        },
        "empresa": {
            "ingresos_totales": 3500.00,
            "gastos_operativos": 1200.00,
            "porcentaje_reinversion": 40.00
        },
        "meta_actual": 320.0,
        "meta_total": 500.0,
        "medallas": [
            {"titulo": "Primer Ahorro", "desc": "Distintivo por dar tu primer paso financiero.", "icono": ft.icons.MILITARY_TECH, "obtenida": True},
            {"titulo": "Orgullo Arequipeño 🌋", "desc": "Alcanza tu meta de ahorro con garra y tradición.", "icono": ft.icons.LOCAL_FIRE_DEPARTMENT, "obtenida": False},
        ],
        "mascotas": [
            {"nombre": "Monstruito Ahorrador", "nivel": "Nivel 2 🦖", "desc": "Te felicita cada vez que dejas un sol en tu alcancía.", "icono": ft.icons.BUG_REPORT, "activo": True},
            {"nombre": "Dino Financiero", "nivel": "Nivel 1 🦕", "desc": "Te avisa si estás gastando de más en snacks.", "icono": ft.icons.PETS, "activo": False}
        ]
    }

    body_container = ft.Container(expand=True)

    # -------------------------------------------------------------
    # PANTALLA 1: LOGIN (Nombre, DNI, Contraseña)
    # -------------------------------------------------------------
    input_nombre = ft.TextField(
        label="Nombre completo", 
        border_color="#FF7A00", 
        focused_border_color="#FF7A00",
        text_style=ft.TextStyle(color=ft.colors.BLACK, weight=ft.FontWeight.W_500)
    )
    input_dni = ft.TextField(
        label="DNI", 
        keyboard_type=ft.KeyboardType.NUMBER, 
        max_length=8, 
        border_color="#FF7A00", 
        focused_border_color="#FF7A00",
        text_style=ft.TextStyle(color=ft.colors.BLACK, weight=ft.FontWeight.W_500)
    )
    input_pass = ft.TextField(
        label="Contraseña", 
        password=True, 
        can_reveal_password=True, 
        border_color="#FF7A00", 
        focused_border_color="#FF7A00",
        text_style=ft.TextStyle(color=ft.colors.BLACK, weight=ft.FontWeight.W_500)
    )

    def ir_al_dashboard(e):
        if not input_nombre.value or not input_dni.value or not input_pass.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor completa todos los campos de seguridad"))
            page.snack_bar.open = True
            page.update()
            return
        
        user_state["nombre"] = input_nombre.value
        construir_dashboard()
        page.update()

    login_view = ft.Container(
        content=ft.Column([
            ft.Icon(ft.icons.LOCK_PERSON, size=60, color="#FF7A00"),
            ft.Text("Bienvenido a AhorraYa", size=22, weight=ft.FontWeight.BOLD, color="#212529"),
            ft.Text("Ingresa tus datos para acceder de forma segura", size=13, color="#6C757D"),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            input_nombre,
            input_dni,
            input_pass,
            ft.Divider(height=10, color=ft.colors.TRANSPARENT),
            ft.ElevatedButton(
                "Ingresar a mi cuenta",
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor="#FF7A00"
                ),
                width=320,
                on_click=ir_al_dashboard
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=30
    )

    # -------------------------------------------------------------
    # PANTALLAS DEL BANCO
    # -------------------------------------------------------------
    def construir_dashboard():
        
        candado_container = ft.Container(expand=True)
        viaje_container = ft.Container(expand=True)
        empresa_container = ft.Container(expand=True)

        def vista_enviar_dinero():
            txt_celular = ft.TextField(label="Número de celular (9 dígitos)", keyboard_type=ft.KeyboardType.NUMBER, max_length=9, border_color="#FF7A00")
            txt_monto = ft.TextField(label="Monto a transferir o pagar (S/)", keyboard_type=ft.KeyboardType.NUMBER, border_color="#FF7A00")
            
            def ejecutar_envio(ev):
                if not txt_celular.value or not txt_monto.value:
                    page.snack_bar = ft.SnackBar(ft.Text("Ingresa el celular y el monto por favor"))
                    page.snack_bar.open = True
                    page.update()
                    return
                
                try:
                    monto_num = float(txt_monto.value)
                except ValueError:
                    page.snack_bar = ft.SnackBar(ft.Text("Ingresa un monto válido en números"))
                    page.snack_bar.open = True
                    page.update()
                    return

                if monto_num > user_state["saldo"]:
                    page.snack_bar = ft.SnackBar(ft.Text("❌ Saldo insuficiente para realizar esta transferencia"))
                    page.snack_bar.open = True
                    page.update()
                    return

                user_state["saldo"] -= monto_num
                nuevo_movimiento = {
                    "titulo": f"Transferencia a {txt_celular.value}",
                    "sub": "Hoy",
                    "monto": f"- S/ {monto_num:.2f}",
                    "color": ft.colors.RED
                }
                user_state["movimientos"].insert(0, nuevo_movimiento)

                page.snack_bar = ft.SnackBar(ft.Text(f"✅ ¡Transferencia exitosa de S/ {monto_num:.2f} al {txt_celular.value}!"))
                page.snack_bar.open = True
                
                body_container.content = vista_inicio()
                page.update()

            return ft.Column([
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda e: setattr(body_container, 'content', vista_inicio()) or page.update()),
                    ft.Text("Transferir o Pagar Dinero", size=18, weight=ft.FontWeight.BOLD, color="#FF7A00")
                ]),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Text("Escribe el número de la persona a quien deseas transferir o pagar:", size=13, color="#6C757D"),
                ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                txt_celular,
                txt_monto,
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.ElevatedButton(
                    "Realizar Transferencia / Pago", 
                    style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor="#FF7A00"), 
                    width=320, 
                    on_click=ejecutar_envio
                )
            ], spacing=10)

        def vista_recibir_qr():
            return ft.Column([
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda e: setattr(body_container, 'content', vista_inicio()) or page.update()),
                    ft.Text("Recibir Dinero (Código QR)", size=18, weight=ft.FontWeight.BOLD, color="#FF7A00")
                ]),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Text("Muestra tu código QR para que te depositen al instante:", size=13, color="#6C757D"),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.QR_CODE_2, size=130, color="#FF7A00"),
                        ft.Text(f"Titular: {user_state['nombre']}", weight=ft.FontWeight.BOLD, size=16),
                        ft.Text("AhorraYa - Banco Digital", size=12, color="#6C757D")
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.colors.WHITE, padding=25, border_radius=20,
                    shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.BLACK12),
                    alignment=ft.alignment.Alignment(0, 0)
                )
            ], spacing=10)

        def comprobar_meta_lograda():
            if user_state["meta_actual"] >= user_state["meta_total"]:
                for m in user_state["medallas"]:
                    if "Arequipeño" in m["titulo"]:
                        m["obtenida"] = True

                dialogo_insignia = ft.AlertDialog(
                    title=ft.Text("🎉 ¡Felicidades! Meta Alcanzada 🌋", color="#FF7A00", weight=ft.FontWeight.BOLD),
                    content=ft.Column([
                        ft.Icon(ft.icons.LOCAL_FIRE_DEPARTMENT, size=70, color="#FF7A00"),
                        ft.Text("¡Has completado tu meta de ahorro mensual con éxito!", size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text("Has ganado la insignia exclusiva:\n🏆 Orgullo Arequipeño", size=13, color="#6C757D", text_align=ft.TextAlign.CENTER),
                        ft.Text("¡Con esfuerzo y punche se logran las grandes metas!", size=11, color=ft.colors.GREY_600, text_align=ft.TextAlign.CENTER)
                    ], width=300, height=210, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    actions=[
                        ft.ElevatedButton(
                            "¡Genial!", 
                            style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor="#FF7A00"), 
                            on_click=lambda ev: setattr(page.dialog, 'open', False) or page.update()
                        )
                    ]
                )
                page.dialog = dialogo_insignia
                dialogo_insignia.open = True
                page.update()

        def abonar_ahorro_rapido(e):
            user_state["meta_actual"] += 90.0
            if user_state["meta_actual"] > user_state["meta_total"]:
                user_state["meta_actual"] = user_state["meta_total"]
            
            comprobar_meta_lograda()
            body_container.content = vista_inicio()
            page.update()

        def vista_inicio():
            lista_controles = []
            for mov in user_state["movimientos"]:
                lista_controles.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.SEND_TO_MOBILE, color="#FF7A00"),
                        title=ft.Text(mov["titulo"]),
                        subtitle=ft.Text(mov["sub"]),
                        trailing=ft.Text(mov["monto"], color=mov["color"])
                    )
                )

            progreso_meta = user_state["meta_actual"] / user_state["meta_total"]
            falta_meta = user_state["meta_total"] - user_state["meta_actual"]

            return ft.Column([
                ft.Row([
                    ft.Row([
                        ft.IconButton(
                            icon=ft.icons.MENU, 
                            icon_color="#FF7A00",
                            tooltip="Menú de Opciones",
                            on_click=lambda e: setattr(body_container, 'content', vista_menu_lateral()) or page.update()
                        ),
                        ft.Column([
                            ft.Text(f"Hola, {user_state['nombre']} 👋", size=15, color="#6C757D", weight=ft.FontWeight.W_500),
                            ft.Text("AhorraYa", size=20, color="#FF7A00", weight=ft.FontWeight.BOLD),
                        ], spacing=0)
                    ], spacing=2),
                    ft.CircleAvatar(content=ft.Icon(ft.icons.PERSON, color=ft.colors.WHITE), bgcolor="#FF7A00")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Dinero Disponible", color=ft.colors.WHITE70, size=14),
                        ft.Text(f"S/ {user_state['saldo']:,.2f}", color=ft.colors.WHITE, size=30, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.Chip(label=ft.Text("Ingresos: S/ 1,800"), bgcolor=ft.colors.WHITE12, label_text_style=ft.TextStyle(color=ft.colors.WHITE)),
                            ft.Chip(label=ft.Text("Gastos: S/ 550"), bgcolor=ft.colors.WHITE12, label_text_style=ft.TextStyle(color=ft.colors.WHITE)),
                        ], alignment=ft.MainAxisAlignment.START)
                    ]),
                    bgcolor="#FF7A00", padding=20, border_radius=20,
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.ORANGE_300)
                ),
                
                ft.Row([
                    ft.ElevatedButton(
                        "Transferir / Pagar", 
                        icon=ft.icons.SEND_AND_ARCHIVE, 
                        style=ft.ButtonStyle(color="#FF7A00", bgcolor="#FFE5D0"),
                        on_click=lambda e: setattr(body_container, 'content', vista_enviar_dinero()) or page.update()
                    ),
                    ft.ElevatedButton(
                        "Recibir (QR)", 
                        icon=ft.icons.QR_CODE, 
                        style=ft.ButtonStyle(color="#FF7A00", bgcolor="#FFE5D0"),
                        on_click=lambda e: setattr(body_container, 'content', vista_recibir_qr()) or page.update()
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),

                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.SAVINGS, color="#FF7A00"), 
                            ft.Text("Meta de Ahorro Mensual", size=16, weight=ft.FontWeight.BOLD)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([
                            ft.Text(f"S/ {user_state['meta_actual']:,.0f}", size=20, weight=ft.FontWeight.BOLD, color="#FF7A00"), 
                            ft.Text(f"/ S/ {user_state['meta_total']:,.0f}", size=14, color="#6C757D")
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.ProgressBar(value=progreso_meta, width=320, color="#FF7A00", bgcolor="#FFE5D0", height=8),
                        ft.Row([
                            ft.Text(f"Faltan S/ {falta_meta:,.0f} para tu meta" if falta_meta > 0 else "¡Meta cumplida con éxito! 🎉", size=12, color="#6C757D"),
                            ft.TextButton("Abonar S/ 90", on_click=abonar_ahorro_rapido)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]),
                    bgcolor=ft.colors.WHITE, padding=15, border_radius=20,
                    shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.BLACK12)
                ),
                
                ft.Text("Detalle de Gastos Recientes", size=15, weight=ft.FontWeight.BOLD),
                ft.ListView(expand=1, spacing=5, controls=lista_controles)
            ], spacing=10)

        # -------------------------------------------------------------
        # MENÚ DESPLEGABLE (TRES RAYITAS): PERFIL, MEDALLAS Y MONSTRITOS
        # -------------------------------------------------------------
        def vista_menu_lateral():
            lista_medallas_controles = []
            for med in user_state["medallas"]:
                lista_medallas_controles.append(
                    ft.ListTile(
                        leading=ft.Icon(med["icono"], color="#FF7A00" if med["obtenida"] else ft.colors.GREY, size=32),
                        title=ft.Text(med["titulo"], weight=ft.FontWeight.BOLD, color=ft.colors.BLACK if med["obtenida"] else ft.colors.GREY),
                        subtitle=ft.Text(med["desc"], size=12),
                        trailing=ft.Text("🏆 Obtenida" if med["obtenida"] else "🔒 Bloqueada", size=11, color="#FF7A00" if med["obtenida"] else ft.colors.GREY)
                    )
                )

            lista_mascotas_controles = []
            for mas in user_state["mascotas"]:
                lista_mascotas_controles.append(
                    ft.ListTile(
                        leading=ft.Icon(mas["icono"], color="#FF7A00", size=32),
                        title=ft.Text(mas["nombre"], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"{mas['nivel']} - {mas['desc']}", size=12),
                        trailing=ft.Text("🦖 Activo" if mas["activo"] else "💤 Durmiendo", size=11, color="#FF7A00" if mas["activo"] else ft.colors.GREY)
                    )
                )

            return ft.Column([
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda e: setattr(body_container, 'content', vista_inicio()) or page.update()),
                    ft.Text("Mi Perfil, Medallas y Monstritos", size=18, weight=ft.FontWeight.BOLD, color="#FF7A00")
                ]),
                ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                
                ft.Container(
                    content=ft.Column([
                        ft.CircleAvatar(content=ft.Icon(ft.icons.PERSON, color=ft.colors.WHITE, size=30), bgcolor="#FF7A00", radius=30),
                        ft.Text(user_state["nombre"], weight=ft.FontWeight.BOLD, size=16),
                        ft.Text("Usuario Verificado • Arequipa, Perú", size=12, color="#6C757D"),
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.colors.WHITE, padding=12, border_radius=15, alignment=ft.alignment.Alignment(0, 0),
                    shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.BLACK12)
                ),
                
                ft.Text("Tus Mascotas / Monstritos 🦖", size=14, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.ListView(expand=1, spacing=2, controls=lista_mascotas_controles),
                    bgcolor=ft.colors.WHITE, padding=5, border_radius=15, height=120,
                    shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.BLACK12)
                ),

                ft.Text("Insignias y Medallas del Perú", size=14, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.ListView(expand=1, spacing=2, controls=lista_medallas_controles),
                    bgcolor=ft.colors.WHITE, padding=5, border_radius=15, height=130,
                    shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.BLACK12)
                )
            ], spacing=8)

        # -------------------------------------------------------------
        # GESTIÓN DE CANDADOS (SERVICIOS)
        # -------------------------------------------------------------
        def actualizar_lista_candados():
            elementos = [
                ft.Row([
                    ft.Column([
                        ft.Text("🔒 Fondo Candado (Servicios)", size=20, weight=ft.FontWeight.BOLD, color="#FF7A00"),
                        ft.Text("Dinero inamovible protegido para tus pagos importantes.", size=13, color="#6C757D"),
                    ]),
                    ft.IconButton(
                        icon=ft.icons.ADD_CIRCLE, 
                        icon_size=32, 
                        icon_color="#FF7A00", 
                        tooltip="Añadir nuevo candado",
                        on_click=lambda e: abrir_dialogo_nuevo_candado(e)
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=5, color=ft.colors.TRANSPARENT)
            ]

            for c in user_state["candados"]:
                elementos.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Row([ft.Icon(c["icono"], color="#FF7A00"), ft.Text(c["titulo"], weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Text(f"Monto bloqueado: {c['monto']}", size=14),
                            ft.Text(f"Fecha de pago: {c['fecha']}", size=12, color=ft.colors.RED_400),
                            ft.ElevatedButton("Candado Activo 🔒", style=ft.ButtonStyle(color="#FF7A00", bgcolor="#FFE5D0"), disabled=True)
                        ]),
                        bgcolor=ft.colors.WHITE, padding=15, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.BLACK12)
                    )
                )
            
            candado_container.content = ft.ListView(expand=1, spacing=10, controls=elementos)
            page.update()

        def abrir_dialogo_nuevo_candado(e):
            txt_nombre_serv = ft.TextField(label="¿A qué va dirigido? (Ej. Colegio, Universidad...)", border_color="#FF7A00")
            txt_monto_serv = ft.TextField(label="¿Cuánto cuesta? (Ej. 250.00)", keyboard_type=ft.KeyboardType.NUMBER, border_color="#FF7A00")
            txt_fecha_serv = ft.TextField(label="Fecha límite (Ej. 15 de cada mes)", border_color="#FF7A00")

            def guardar_nuevo_candado(ev):
                if not txt_nombre_serv.value or not txt_monto_serv.value or not txt_fecha_serv.value:
                    page.snack_bar = ft.SnackBar(ft.Text("Por favor completa todos los campos"))
                    page.snack_bar.open = True
                    page.update()
                    return
                
                monto_formateado = f"S/ {txt_monto_serv.value}" if not txt_monto_serv.value.startswith("S/") else txt_monto_serv.value

                user_state["candados"].append({
                    "titulo": txt_nombre_serv.value,
                    "icono": ft.icons.VERIFIED_USER,
                    "monto": monto_formateado,
                    "fecha": txt_fecha_serv.value
                })

                page.dialog.open = False
                page.update()

                page.snack_bar = ft.SnackBar(ft.Text(f"✅ ¡Candado para '{txt_nombre_serv.value}' creado con éxito!"))
                page.snack_bar.open = True
                
                actualizar_lista_candados()

            dialogo = ft.AlertDialog(
                title=ft.Text("➕ Añadir Nuevo Gasto Protegido", color="#FF7A00", weight=ft.FontWeight.BOLD),
                content=ft.Column([
                    txt_nombre_serv,
                    txt_monto_serv,
                    txt_fecha_serv,
                    ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                    ft.ElevatedButton(
                        "Guardar Candado", 
                        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor="#FF7A00"), 
                        width=280, 
                        on_click=guardar_nuevo_candado
                    )
                ], width=300, height=240, spacing=10),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda ev: setattr(page.dialog, 'open', False) or page.update())
                ]
            )
            
            page.dialog = dialogo
            dialogo.open = True
            page.update()

        def vista_candado():
            actualizar_lista_candados()
            return candado_container

        # -------------------------------------------------------------
        # GESTIÓN DE VIAJES
        # -------------------------------------------------------------
        def actualizar_vista_viajes():
            total_acumulado = sum(item["monto"] for item in user_state["viaje"]["integrantes"])
            meta_viaje = user_state["viaje"]["meta"]
            progreso = min(total_acumulado / meta_viaje, 1.0)

            texto_integrantes = ""
            for integ in user_state["viaje"]["integrantes"]:
                texto_integrantes += f"• {integ['nombre']}: S/ {integ['monto']:.2f}\n"
            texto_integrantes = texto_integrantes.strip()

            elementos_viaje = [
                ft.Row([
                    ft.Column([
                        ft.Text("✈️ Fondo de Viaje Compartido", size=20, weight=ft.FontWeight.BOLD, color="#FF7A00"),
                        ft.Text("Ahorra en grupo con tus amigos para el gran viaje.", size=13, color="#6C757D"),
                    ]),
                    ft.IconButton(
                        icon=ft.icons.PERSON_ADD, 
                        icon_size=32, 
                        icon_color="#FF7A00", 
                        tooltip="Añadir amigo o aporte al viaje",
                        on_click=lambda e: abrir_dialogo_nuevo_integrante(e)
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Destino: {user_state['viaje']['destino']}", weight=ft.FontWeight.BOLD, size=16),
                        ft.Text(f"Acumulado grupal: S/ {total_acumulado:,.2f} / S/ {meta_viaje:,.2f}", size=13),
                        ft.ProgressBar(value=progreso, width=300, color="#FF7A00", bgcolor="#FFE5D0", height=8),
                        ft.Divider(),
                        ft.Text("Integrantes aportando:", weight=ft.FontWeight.BOLD, size=12),
                        ft.Text(texto_integrantes, size=12, color="#6C757D"),
                        ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                        ft.ElevatedButton(
                            "Aportar rápido (+S/ 20 al fondo)", 
                            style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor="#FF7A00"), 
                            on_click=lambda e: aporte_rapido(e)
                        )
                    ]),
                    bgcolor=ft.colors.WHITE, padding=15, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.BLACK12)
                )
            ]

            viaje_container.content = ft.ListView(expand=1, spacing=10, controls=elementos_viaje)
            page.update()

        def aporte_rapido(e):
            if user_state["saldo"] < 20.00:
                page.snack_bar = ft.SnackBar(ft.Text("❌ No tienes suficiente saldo disponible para aportar S/ 20"))
                page.snack_bar.open = True
                page.update()
                return

            user_state["saldo"] -= 20.00
            encontrado = False
            for integ in user_state["viaje"]["integrantes"]:
                if integ["nombre"] == "Tú":
                    integ["monto"] += 20.00
                    encontrado = True
                    break
            if not encontrado:
                user_state["viaje"]["integrantes"].append({"nombre": "Tú", "monto": 20.00})

            page.snack_bar = ft.SnackBar(ft.Text("✅ ¡Has aportado S/ 20.00 con éxito al viaje!"))
            page.snack_bar.open = True
            actualizar_vista_viajes()

        def abrir_dialogo_nuevo_integrante(e):
            txt_nombre_amigo = ft.TextField(label="Nombre del amigo o participante", border_color="#FF7A00")
            txt_monto_amigo = ft.TextField(label="Monto inicial aportado (S/)", keyboard_type=ft.KeyboardType.NUMBER, border_color="#FF7A00")

            def guardar_integrante(ev):
                if not txt_nombre_amigo.value or not txt_monto_amigo.value:
                    page.snack_bar = ft.SnackBar(ft.Text("Por favor completa todos los campos"))
                    page.snack_bar.open = True
                    page.update()
                    return

                try:
                    monto_num = float(txt_monto_amigo.value)
                except ValueError:
                    page.snack_bar = ft.SnackBar(ft.Text("Ingresa un monto válido en números"))
                    page.snack_bar.open = True
                    page.update()
                    return

                user_state["viaje"]["integrantes"].append({
                    "nombre": txt_nombre_amigo.value,
                    "monto": monto_num
                })

                page.dialog.open = False
                page.update()

                page.snack_bar = ft.SnackBar(ft.Text(f"✅ ¡Se añadió a {txt_nombre_amigo.value} al viaje con S/ {monto_num:.2f}!"))
                page.snack_bar.open = True
                
                actualizar_vista_viajes()

            dialogo = ft.AlertDialog(
                title=ft.Text("➕ Añadir Amigo al Viaje", color="#FF7A00", weight=ft.FontWeight.BOLD),
                content=ft.Column([
                    txt_nombre_amigo,
                    txt_monto_amigo,
                    ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                    ft.ElevatedButton(
                        "Guardar Participante", 
                        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor="#FF7A00"), 
                        width=280, 
                        on_click=guardar_integrante
                    )
                ], width=300, height=200, spacing=10),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda ev: setattr(page.dialog, 'open', False) or page.update())
                ]
            )
            
            page.dialog = dialogo
            dialogo.open = True
            page.update()

        def vista_viajes():
            actualizar_vista_viajes()
            return viaje_container

        # -------------------------------------------------------------
        # SECCIÓN: FINANZAS PARA EMPRESAS
        # -------------------------------------------------------------
        def actualizar_vista_empresas():
            ingresos = user_state["empresa"]["ingresos_totales"]
            gastos = user_state["empresa"]["gastos_operativos"]
            ganancia_neta = ingresos - gastos
            reinv_porcentaje = user_state["empresa"]["porcentaje_reinversion"]
            monto_reinversion = ganancia_neta * (reinv_porcentaje / 100)
            dinero_libre = ganancia_neta - monto_reinversion

            txt_ingresos = ft.TextField(label="Ingresos Totales (S/)", value=str(ingresos), keyboard_type=ft.KeyboardType.NUMBER, border_color="#FF7A00")
            txt_gastos = ft.TextField(label="Gastos Operativos (S/)", value=str(gastos), keyboard_type=ft.KeyboardType.NUMBER, border_color="#FF7A00")
            
            lbl_resultado_neto = ft.Text(f"Ganancia Neta: S/ {ganancia_neta:,.2f}", color=ft.colors.GREEN_700, weight=ft.FontWeight.BOLD, size=15)
            lbl_reinversion = ft.Text(f"Monto a Reinvertir ({reinv_porcentaje}%): S/ {monto_reinversion:,.2f}", size=14)
            lbl_disponible = ft.Text(f"Disponible para repartir/ahorrar: S/ {dinero_libre:,.2f}", color="#FF7A00", weight=ft.FontWeight.BOLD, size=14)

            def calcular_finanzas(ev):
                try:
                    nuevo_ingreso = float(txt_ingresos.value)
                    nuevo_gasto = float(txt_gastos.value)
                    
                    user_state["empresa"]["ingresos_totales"] = nuevo_ingreso
                    user_state["empresa"]["gastos_operativos"] = nuevo_gasto
                    
                    neto = nuevo_ingreso - nuevo_gasto
                    reinv = neto * (user_state["empresa"]["porcentaje_reinversion"] / 100)
                    libre = neto - reinv

                    lbl_resultado_neto.value = f"Ganancia Neta: S/ {neto:,.2f}"
                    lbl_reinversion.value = f"Monto a Reinvertir ({user_state['empresa']['porcentaje_reinversion']}%): S/ {reinv:,.2f}"
                    lbl_disponible.value = f"Disponible para repartir/ahorrar: S/ {libre:,.2f}"
                    page.update()
                except ValueError:
                    pass

            elementos_empresa = [
                ft.Row([
                    ft.Column([
                        ft.Text("💼 Asesor Financiero para Empresas", size=20, weight=ft.FontWeight.BOLD, color="#FF7A00"),
                        ft.Text("Gestiona las ganancias y reinversión de tu emprendimiento.", size=13, color="#6C757D"),
                    ])
                ]),
                ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                ft.Container(
                    content=ft.Column([
                        txt_ingresos,
                        txt_gastos,
                        ft.ElevatedButton(
                            "Calcular Distribución", 
                            style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor="#FF7A00"), 
                            width=280, 
                            on_click=calcular_finanzas
                        )
                    ], spacing=10),
                    bgcolor=ft.colors.WHITE, padding=15, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.BLACK12)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("📊 Resultados del Negocio", weight=ft.FontWeight.BOLD, color="#FF7A00", size=15),
                        lbl_resultado_neto,
                        lbl_reinversion,
                        lbl_disponible
                    ], spacing=8),
                    bgcolor=ft.colors.WHITE, padding=15, border_radius=15, shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.BLACK12)
                )
            ]

            empresa_container.content = ft.ListView(expand=1, spacing=10, controls=elementos_empresa)
            page.update()

        def vista_empresas():
            actualizar_vista_empresas()
            return empresa_container

        # Control de navegación inferior
        def cambiar_pestana(e):
            index = e.control.selected_index
            if index == 0:
                body_container.content = vista_inicio()
            elif index == 1:
                body_container.content = vista_candado()
            elif index == 2:
                body_container.content = vista_viajes()
            elif index == 3:
                body_container.content = vista_empresas()
            page.update()

        nav_bar = ft.NavigationBar(
            selected_index=0,
            bgcolor=ft.colors.WHITE,
            indicator_color="#FFE5D0",
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.HOME, label="Cuenta"),
                ft.NavigationBarDestination(icon=ft.icons.LOCK, label="Candado"),
                ft.NavigationBarDestination(icon=ft.icons.FLIGHT, label="Viajes"),
                ft.NavigationBarDestination(icon=ft.icons.BUSINESS_CENTER, label="Empresas"),
            ],
            on_change=cambiar_pestana
        )

        body_container.content = vista_inicio()
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    body_container,
                    nav_bar
                ], spacing=10),
                padding=15, expand=True
            )
        )
        page.update()

    page.add(login_view)

def main_app():
    ft.app(target=main)

if __name__ == "__main__":
    main_app()