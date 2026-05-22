from odoo import models, fields, api
from datetime import datetime

class TenderEvaluation(models.Model):
    _name = 'tender.evaluation'
    _description = 'Tender Evaluation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    tender_id = fields.Many2one('tender.announcement', 'Tender', required=True, ondelete='cascade')
    evaluation_date = fields.Datetime('Evaluation Date', default=fields.Datetime.now)
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('approved', 'Approved'),
    ], default='draft', track_visibility='onchange')
    
    # Evaluation Parameters
    price_weight = fields.Float('Price Weight (%)', default=40)
    quality_weight = fields.Float('Quality Weight (%)', default=30)
    delivery_weight = fields.Float('Delivery Weight (%)', default=20)
    technical_weight = fields.Float('Technical Weight (%)', default=10)
    
    evaluation_lines = fields.One2many('tender.evaluation.line', 'evaluation_id', 'Evaluation Details')
    
    # Results
    best_bid_id = fields.Many2one('tender.bid', 'Best Bid')
    best_price_bid_id = fields.Many2one('tender.bid', 'Best Price Bid')
    winner_id = fields.Many2one('res.partner', 'Winner')
    
    recommendation = fields.Text('Recommendation')
    evaluator_id = fields.Many2one('res.users', 'Evaluator', default=lambda self: self.env.user)
    notes = fields.Text('Evaluation Notes')
    
    company_id = fields.Many2one('res.company', related='tender_id.company_id', readonly=True)
    
    def action_start_evaluation(self):
        for tender in self.mapped('tender_id'):
            if tender.status != 'closed':
                tender.write({'status': 'closed'})
        self.write({'status': 'in_progress'})
        return True
    
    def action_complete_evaluation(self):
        self.write({'status': 'completed'})
        return True
    
    def action_approve_evaluation(self):
        self.write({'status': 'approved'})
        return True


class TenderEvaluationLine(models.Model):
    _name = 'tender.evaluation.line'
    _description = 'Tender Evaluation Line'

    evaluation_id = fields.Many2one('tender.evaluation', 'Evaluation', ondelete='cascade')
    bid_id = fields.Many2one('tender.bid', 'Bid', required=True)
    vendor_id = fields.Many2one('res.partner', related='bid_id.vendor_id', readonly=True)
    
    # Scoring
    price_score = fields.Float('Price Score')
    quality_score = fields.Float('Quality Score')
    delivery_score = fields.Float('Delivery Score')
    technical_score = fields.Float('Technical Score')
    
    weighted_score = fields.Float('Weighted Score', compute='_compute_weighted_score', store=True)
    rank = fields.Integer('Rank')
    
    # Comments
    price_remarks = fields.Text('Price Remarks')
    quality_remarks = fields.Text('Quality Remarks')
    technical_remarks = fields.Text('Technical Remarks')
    
    @api.depends('price_score', 'quality_score', 'delivery_score', 'technical_score')
    def _compute_weighted_score(self):
        for record in self:
            evaluation = record.evaluation_id
            if evaluation:
                record.weighted_score = (
                    record.price_score * (evaluation.price_weight / 100) +
                    record.quality_score * (evaluation.quality_weight / 100) +
                    record.delivery_score * (evaluation.delivery_weight / 100) +
                    record.technical_score * (evaluation.technical_weight / 100)
                )
