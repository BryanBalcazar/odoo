from odoo import models, fields

class RiwiLine(models.Model):
    _name = 'riwi.line'
    _description = 'Líneas de Tareas de Riwi'

    # Relación que conecta con el archivo riwi.py
    riwi_id = fields.Many2one('riwiscrum', string='Riwi Referencia', ondelete='cascade')

    # Selección de tareas solicitadas
    tipo_tarea = fields.Selection([
        ('back', 'Backend'),
        ('front', 'Frontend'),
        ('cicd', 'CI/CD'),
        ('cloud', 'Cloud Inf'),
        ('db', 'Database'),
        ('analisis', 'Análisis de Datos')
    ], string='Tipo de Tarea', required=True)

    fecha_inicio = fields.Date(string='Fecha Inicio')
    fecha_fin = fields.Date(string='Fecha Fin')
    
    # Many2many permite elegir varios usuarios (3 o 4 como pediste)
    asignado_a_ids = fields.Many2many('res.users', string='Asignado a')
    
    prioridad = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Media'),
        ('2', 'Alta')
    ], string='Prioridad', default='1')

    descripcion = fields.Text(string='Descripción')
    tiempo_estimado = fields.Float(string='Tiempo Estimado (Horas)')

    # Este campo trae el estado del "padre" para que se vea en la tabla
    status = fields.Selection(related='riwi_id.status', string="Estado", store=True)