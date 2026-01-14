from odoo import models, fields
from odoo.exceptions import UserError

class Riwiscrum(models.Model):
    _name = 'riwiscrum'
    _description = 'riwiscrum'

    name = fields.Char(string='Nombre', required=True)

    status = fields.Selection(
        [
            ("draft","Borrador"),
            ("review","En revisión"),
            ("running","En ejecución"),
            ("paused","Pausado"),
            ("accepted","Aceptado"),
            ("refused","Rechazado"),
            ("cancel","Cancelado"),
            
        ],
        string="Estado",
        required=True,
        readonly=True,
        default="draft"
    )

    required_by = fields.Many2one("res.users",string="Solicitado por", required=False)
    accepted_by = fields.Many2one("res.users",string="Aceptado por", required=False)
    active = fields.Boolean(string='Activo', default=True)

    fecha_review = fields.Datetime("Fecha a review", readonly=True)
    fecha_running = fields.Datetime("Fecha a ejecución", readonly=True)
    fecha_paused = fields.Datetime("Fecha a pausa", readonly=True)
    fecha_accepted = fields.Datetime("Fecha a aceptado", readonly=True)
    fecha_refused = fields.Datetime("Fecha a rechazado", readonly=True)
    fecha_cancel = fields.Datetime("Fecha a cancelado", readonly=True)


    def _ensure_transition_allowed(self, target_status):
        terminal_statuses = ("accepted", "refused", "cancel")
        for record in self:
            if record.status in terminal_statuses and record.status != target_status:
                raise UserError("No se puede cambiar de estado desde un estado final (Aceptado, Rechazado o Cancelado).")

    def review(self):
        for record in self:
            record._ensure_transition_allowed("review")
            if record.status != "review":
                record.status = "review"
                record.fecha_review = fields.Datetime.now()
            
    def draft(self):
        for record in self:
            record._ensure_transition_allowed("draft")
            if record.status != "draft":
                record.status = "draft"
                
    def running(self):
        for record in self:
            record._ensure_transition_allowed("running")
            if record.status != "running":
                record.status = "running"
                record.fecha_running = fields.Datetime.now()
    
    def paused(self):
        for record in self:
            record._ensure_transition_allowed("paused")
            if record.status != "paused":
                record.status = "paused"
                record.fecha_paused = fields.Datetime.now()
                
    def accepted(self):
        for record in self:
            record._ensure_transition_allowed("accepted")
            if record.status != "accepted":
                record.status = "accepted"
                record.fecha_accepted = fields.Datetime.now()
    
    def refused(self):
        for record in self:
            record._ensure_transition_allowed("refused")
            if record.status != "refused":
                record.status = "refused"
                record.fecha_refused = fields.Datetime.now()
    
    def cancel(self):
        for record in self:
            record._ensure_transition_allowed("cancel")
            if record.status != "cancel":
                record.status = "cancel"
                record.fecha_cancel = fields.Datetime.now()

