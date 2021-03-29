from odoo import models, fields, api
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="map_user_warehouse")


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    @api.model
    def default_loc(self):
        locator = geolocator.geocode(self.env.user.company_id.country_id.code.upper())
        return str(locator.latitude) + ',' + str(locator.longitude) if \
            self.env.user.company_id.country_id else ''

    latLong = fields.Char(string='Coordenadas', readonly=True, store=True, default=default_loc)

    @api.model
    def create(self, vals):
        if not vals.get('latLong', False):
            default_loc = geolocator.geocode(self.env.user.company_id.country_id.code.upper()) if \
                self.env.user.company_id.country_id else False
            vals['latLong'] = self._context.get('coordinates',
                                                default_loc.latitude + default_loc.longitude if default_loc else '')
        return super(StockWarehouse, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['latLong'] = self._context.get('coordinates', '')
        return super(StockWarehouse, self).write(vals)

    @api.multi
    def action_update_coordinates(self):
        if self._context.get('coordinates', False):
            self.write({'latLong': self._context['coordinates']})
