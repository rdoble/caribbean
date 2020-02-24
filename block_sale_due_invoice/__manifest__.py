# © 2020 Anthony Martinez <anthonyame02@gmail.com>

# It under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# NCF Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# See <https://www.gnu.org/licenses/>.


{
    'name': "Block Sales Due Invoice",
    'version': '12.0.1.1.0',
    'summary': """
        Este módulo permite bloquear las ordenes de ventas si el cliente tiene facturas vencidas
    """,
    'author': "Anthony Martinez (anthonyame02@gmail.com)",
    'license': 'LGPL-3',
    'category': 'Sales',
    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management'],
    'data': [
        'views/res_partner_view.xml',
    ],
    'demo': [],
    'qweb': []
}
