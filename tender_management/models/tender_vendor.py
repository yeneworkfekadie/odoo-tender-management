from odoo import models, fields

class TenderVendor(models.Model):
    _name = 'tender.vendor'
    _description = 'Tender Vendor Profile'

    partner_id = fields.Many2one('res.partner', 'Vendor', required=True, ondelete='cascade')
    
    registration_number = fields.Char('Registration Number')
    category = fields.Selection([
        ('goods', 'Goods'),
        ('services', 'Services'),
        ('works', 'Works'),
        ('mixed', 'Mixed'),
    ])
    
    rating = fields.Float('Rating', default=0)
    total_bids = fields.Integer('Total Bids')
    successful_bids = fields.Integer('Successful Bids')
    failed_bids = fields.Integer('Failed Bids')
    
    # Compliance
    tax_compliant = fields.Boolean('Tax Compliant')
    insurance_compliant = fields.Boolean('Insurance Compliant')
    certification_ids = fields.Many2many('tender.certification', string='Certifications')
    
    # Financial
    financial_capacity = fields.Float('Financial Capacity')
    bank_references = fields.Text('Bank References')
    
    # Performance
    on_time_delivery_rate = fields.Float('On-Time Delivery Rate (%)')
    quality_rating = fields.Float('Quality Rating')
    
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)


class TenderCertification(models.Model):
    _name = 'tender.certification'
    _description = 'Vendor Certification'

    name = fields.Char('Certification Name', required=True)
    issue_date = fields.Date('Issue Date')
    expiry_date = fields.Date('Expiry Date')
    issuing_body = fields.Char('Issuing Body')
    certificate_url = fields.Char('Certificate URL')
