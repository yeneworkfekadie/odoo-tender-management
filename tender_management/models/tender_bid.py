from odoo import models, fields, api

class TenderBid(models.Model):
    _name = 'tender.bid'
    _description = 'Tender Bid'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'

    tender_id = fields.Many2one('tender.announcement', 'Tender', required=True, ondelete='cascade')
    vendor_id = fields.Many2one('res.partner', 'Vendor', required=True, domain=[('supplier_rank', '>', 0)])
    
    bid_date = fields.Datetime('Bid Date', default=fields.Datetime.now)
    bid_reference = fields.Char('Bid Reference', readonly=True, copy=False)
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('qualified', 'Qualified'),
        ('disqualified', 'Disqualified'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ], default='draft', track_visibility='onchange')
    
    total_amount = fields.Float('Total Bid Amount', compute='_compute_total_amount', store=True)
    currency_id = fields.Many2one('res.currency', related='tender_id.currency_id', readonly=True)
    
    bid_items = fields.One2many('tender.bid.item', 'bid_id', 'Bid Items')
    
    # Evaluation Criteria
    price_score = fields.Float('Price Score', default=0)
    quality_score = fields.Float('Quality Score', default=0)
    delivery_score = fields.Float('Delivery Score', default=0)
    technical_score = fields.Float('Technical Score', default=0)
    total_score = fields.Float('Total Score', compute='_compute_total_score', store=True)
    
    # Additional info
    delivery_period = fields.Integer('Delivery Period (Days)')
    warranty_period = fields.Integer('Warranty Period (Months)')
    payment_terms = fields.Text('Payment Terms')
    remarks = fields.Text('Remarks')
    
    attachment_ids = fields.Many2many('ir.attachment', 'bid_attachment_rel', string='Attachments')
    
    company_id = fields.Many2one('res.company', related='tender_id.company_id', readonly=True)
    
    @api.model
    def create(self, vals):
        if 'bid_reference' not in vals or not vals['bid_reference']:
            vals['bid_reference'] = self.env['ir.sequence'].next_by_code('tender.bid')
        return super().create(vals)
    
    @api.depends('bid_items.amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.bid_items.mapped('amount'))
    
    @api.depends('price_score', 'quality_score', 'delivery_score', 'technical_score')
    def _compute_total_score(self):
        for record in self:
            record.total_score = (record.price_score + record.quality_score + 
                                record.delivery_score + record.technical_score) / 4
    
    def action_submit(self):
        self.write({'status': 'submitted'})
        return True
    
    def action_qualify(self):
        self.write({'status': 'qualified'})
        return True
    
    def action_disqualify(self):
        self.write({'status': 'disqualified'})
        return True
    
    def action_select(self):
        self.write({'status': 'selected'})
        return True
    
    def action_reject(self):
        self.write({'status': 'rejected'})
        return True


class TenderBidItem(models.Model):
    _name = 'tender.bid.item'
    _description = 'Tender Bid Item'
    _order = 'sequence'

    bid_id = fields.Many2one('tender.bid', 'Bid', ondelete='cascade')
    tender_item_id = fields.Many2one('tender.item', 'Tender Item')
    
    product_id = fields.Many2one('product.product', 'Product', required=True)
    description = fields.Char('Description')
    quantity = fields.Float('Quantity', required=True)
    unit_id = fields.Many2one('uom.uom', 'Unit of Measure')
    
    unit_price = fields.Float('Unit Price', required=True)
    amount = fields.Float('Amount', compute='_compute_amount', store=True)
    
    sequence = fields.Integer('Sequence', default=10)
    
    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for record in self:
            record.amount = record.quantity * record.unit_price
