# Riwiscrum

## Descripción

Módulo con el modelo `riwiscrum` que gestiona un flujo de estados para un registro, con trazabilidad de fechas y reglas de transición.

## Modelo: `riwiscrum`

- `name` (Char, requerido): Nombre del registro.
- `status` (Selection, readonly, default=`draft`):
  - Valores: `draft` (Borrador), `review` (En revisión), `running` (En ejecución), `paused` (Pausado), `accepted` (Aceptado), `refused` (Rechazado), `cancel` (Cancelado).
- `required_by` (Many2one `res.users`): Solicitado por.
- `accepted_by` (Many2one `res.users`): Aceptado por.
- `active` (Boolean): Activo.

### Trazabilidad de fechas (readonly)

- `fecha_review`, `fecha_running`, `fecha_paused`, `fecha_accepted`, `fecha_refused`, `fecha_cancel`.

## Transiciones y validación

- Métodos: `draft`, `review`, `running`, `paused`, `accepted`, `refused`, `cancel`.
- Cada método cambia `status` si corresponde y registra la fecha con `fields.Datetime.now()`.
- Validación `_ensure_transition_allowed(target_status)`: bloquea cualquier cambio desde estados finales `accepted`, `refused`, `cancel` hacia un estado distinto. Lanza `UserError` con mensaje acorde.

## Vistas (`riwiscrum_views.xml`)

- Vista de lista: muestra `name`, `required_by`, `accepted_by`, `active`.
- Formulario:
  - Header: `status` con `widget="statusbar"` y botones para cada transición.
  - Los botones son invisibles cuando:
    - El registro ya está en ese estado.
    - El `status` está en un estado final (`accepted`, `refused`, `cancel`).
  - Cuerpo: grupos con los campos principales y un notebook con:
    - Página "Tareas" (contenedor para futuras funciones).
    - Página "Seguimiento" con las fechas de trazabilidad.

## Uso

1. Menú: Riwiscrum → Registros.
2. Crear/editar registros y cambiar estados desde los botones del encabezado (cuando sean visibles).
3. En estados finales no se permite cambiar el estado (UI y servidor).

## Actualización

- Tras cambios de código o vistas:
  - Actualizar el módulo desde Apps (modo desarrollador) o
  - Reiniciar el servidor y refrescar el navegador (Ctrl+F5).

## Notas

- La lógica de servidor garantiza la integridad de las transiciones aunque se intente por RPC o acciones externas.
