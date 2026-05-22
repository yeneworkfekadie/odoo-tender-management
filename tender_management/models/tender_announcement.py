from odoo import models, fields, api
from datetime import datetime, timedelta

class TenderAnnouncement(models.Model):
    _name = 'tender.announcement'
    _description = 'Tender Announcement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'

    name = fields.Char('Tender Title', required=True, track_visibility='onchange')
    description = fields.Html('Description')
    tender_type = fields.Selection([
        ('open', 'Open Tender'),
        ('closed', 'Closed Tender'),
        ('limited', 'Limited Tender'),
        ('single', 'Single Tender'),
    ], default='open', required=True, track_visibility='onchange')
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('open', 'Accepting Bids'),
        ('closed', 'Closed'),
        ('awarded', 'Awarded'),
        ('rejected', 'Rejected'),
    ], default='draft', required=True, track_visibility='onchange')
    
    announcement_date = fields.Datetime('Announcement Date', default=fields.Datetime.now)
    bid_start_date = fields.Datetime('Bid Start Date', required=True)
    bid_end_date = fields.Datetime('Bid End Date', required=True)
    budget_amount = fields.Float('Budget Amount', required=True)
    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.company.currency_id)
    
    department_id = fields.Many2one('hr.department', 'Department', track_visibility='onchange')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users', 'Tender Manager', default=lambda self: self.env.user, required=True)
    
    bid_ids = fields.One2many('tender.bid', 'tender_id', 'Bids')
    approved_vendor_ids = fields.Many2many('res.partner', 'tender_approved_vendor_rel', string='Approved Vendors')
    
    evaluation_id = fields.One2many('tender.evaluation', 'tender_id', 'Evaluation')
    attachment_ids = fields.Many2many('ir.attachment', 'tender_attachment_rel', string='Attachments')
    
    tender_items = fields.One2many('tender.item', 'tender_id', 'Items')
    notes = fields.Text('Internal Notes')
    
    # Counters
    bid_count = fields.Integer('Bid Count', compute='_compute_bid_count')
    
    @api.depends('bid_ids')
    def _compute_bid_count(self):
        for record in self:
            record.bid_count = len(record.bid_ids)
    
    @api.constrains('bid_start_date', 'bid_end_date')
    def _check_dates(self):
        for record in self:
            if record.bid_start_date >= record.bid_end_date:
                raise ValueError('Bid End Date must be after Bid Start Date')
    
    def action_publish(self):
        self.write({'status': 'published'})
        return True
    
    def action_open_bidding(self):
        self.write({'status': 'open'})
        return True
    
    def action_close_bidding(self):
        self.write({'status': 'closed'})
        return True
    
    def action_accept(self):
        self.write({'status': 'awarded'})
        return True
    
    def action_reject(self):
        self.write({'status': 'rejected'})
        return True


class TenderItem(models.Model):
    _name = 'tender.item'
    _description = 'Tender Item'
    
    tender_id = fields.Many2one('tender.announcement', 'Tender', ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    description = fields.Char('Description')
    quantity = fields.Float('Quantity', required=True, default=1)
    unit_id = fields.Many2one('uom.uom', 'Unit of Measure')
    estimated_price = fields.Float('Estimated Price')
    sequence = fields.Integer('Sequence', default=10)
