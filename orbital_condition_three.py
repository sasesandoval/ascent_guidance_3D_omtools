import numpy as np
import omtools.api as ot

class OrbitalConditionThree(ot.Group):

    def initialize(self):
        self.options.declare('inc', default=1., types=float)

    def setup(self):
        inc = self.options['inc']

        rx = self.declare_input('rx')
        ry = self.declare_input('ry')
        rz = self.declare_input('rz')
        Vx = self.declare_input('Vx')
        Vy = self.declare_input('Vy')
        Vz = self.declare_input('Vz')

        # z = self.create_indep_var('z', shape=(3,))
        # r = self.create_output('r', shape=(3,))
        # V = self.create_output('V', shape=(3,))

        # z = [0, 0, 1]
        #
        # r[0] = rx
        # r[1] = ry
        # r[2] = rz
        #
        # V[0] = Vx
        # V[1] = Vy
        # V[2] = Vz

        # rxV = ot.cross(r,V,axis=0)

        C3 = rx*Vy - ry*Vx - np.cos(inc)*((rx*Vy - ry*Vx)**2 \
            + (rx*Vz - rz*Vx)**2 + (ry*Vz - rz*Vy)**2)**(0.5)

        #C3 = ot.dot(z, rxV, axis=1) - ot.pnorm(rxV) * np.cos(inc)

        self.register_output('C3', C3)
















#
# from numpy import linalg
# from openmdao.api import ExplicitComponent
#
# class OrbitalConditionThree(ExplicitComponent):
#
#     def initialize(self):
#         #self.options.declare('num_nodes', default=1, types=int)
#         self.options.declare('inc', default=1., types=float)
#
#     def setup(self):
#         #num = self.options['num_nodes']
#         inc = self.options['inc']
#
#         self.add_input('rx', shape=1)
#         self.add_input('ry', shape=1)
#         self.add_input('rz', shape=1)
#         self.add_input('Vx', shape=1)
#         self.add_input('Vy', shape=1)
#         self.add_input('Vz', shape=1)
#
#         self.add_output('C3', shape=1)
#
#         self.declare_partials('*','*',dependent=False)
#         self.declare_partials('C3','rx')
#         self.declare_partials('C3','ry')
#         self.declare_partials('C3','rz')
#         self.declare_partials('C3','Vx')
#         self.declare_partials('C3','Vy')
#         self.declare_partials('C3','Vz')
#
#     def compute(self,inputs,outputs):
#         inc = self.options['inc']
#
#         rx = inputs['rx'][0]
#         ry = inputs['ry'][0]
#         rz = inputs['rz'][0]
#         Vx = inputs['Vx'][0]
#         Vy = inputs['Vy'][0]
#         Vz = inputs['Vz'][0]
#
#         r = [rx, ry, rz]
#         V = [Vx, Vy, Vz]
#         rxV = np.cross(r,V)
#         z = [0, 0, 1]
#
#         #outputs['C3'] = np.dot(z,rxV) - linalg.norm(rxV,2)*np.cos(inc)
#         outputs['C3'] = rx*Vy - ry*Vx - np.cos(inc)*((rx*Vy - ry*Vx)**2 \
#             + (rx*Vz - rz*Vx)**2 + (ry*Vz - rz*Vy)**2)**(0.5)
#
#     def compute_partials(self,inputs,partials):
#         inc = self.options['inc']
#
#         rx = inputs['rx'][0]
#         ry = inputs['ry'][0]
#         rz = inputs['rz'][0]
#         Vx = inputs['Vx'][0]
#         Vy = inputs['Vy'][0]
#         Vz = inputs['Vz'][0]
#
#         r = [rx, ry, rz]
#         V = [Vx, Vy, Vz]
#         rxV = np.cross(r,V)
#
#         norm_rxV = np.sqrt((ry*Vz-rz*Vy)**2 + (rz*Vx-rx*Vz)**2 + (rx*Vy-ry*Vx)**2)
#
#         C = np.cos(inc)
#
#         du_drx =-C*(2*Vy*(rx*Vy-ry*Vx) + 2*Vz*(rx*Vz-rz*Vx))
#         du_dry = C*(2*Vx*(rx*Vy-ry*Vx) - 2*Vz*(ry*Vz-rz*Vy))
#         du_drz = C*(2*Vx*(rx*Vz-rz*Vx) + 2*Vy*(ry*Vz-rz*Vy))
#         du_dVx = C*(2*ry*(rx*Vy-ry*Vx) + 2*rz*(rx*Vz-rz*Vx))
#         du_dVy =-C*(2*rx*(rx*Vy-ry*Vx) - 2*rz*(ry*Vz-rz*Vy))
#         du_dVz =-C*(2*rx*(rx*Vz-rz*Vx) + 2*ry*(ry*Vz-rz*Vy))
#
#         den = 2*(((rx*Vy - ry*Vx)**2 + (rx*Vz - rz*Vx)**2 + (ry*Vz - rz*Vy)**2)**(1/2))
#
#         partials['C3','rx'] = du_drx/den + Vy
#         partials['C3','ry'] = du_dry/den - Vx
#         partials['C3','rz'] = du_drz/den
#         partials['C3','Vx'] = du_dVx/den - ry
#         partials['C3','Vy'] = du_dVy/den + rx
#         partials['C3','Vz'] = du_dVz/den
#
#         # norm_rxV = np.sqrt((ry*Vz-rz*Vy)**2 + (rz*Vx-rx*Vz)**2 + (rx*Vy-ry*Vx)**2)
#         #
#         # du_drx = (rz*Vx-rx*Vz)*(-Vz) + (rx*Vy-ry*Vx)*(Vy)
#         # du_dry = (ry*Vz-rz*Vy)*(Vz) + (rx*Vy-ry*Vx)*(-Vx)
#         # du_drz = (ry*Vz-rz*Vy)*(-Vy) + (rz*Vx-rx*Vz)*(Vx)
#         # du_dVx = (rz*Vx-rx*Vz)*(rz) + (rx*Vy-ry*Vx)*(-ry)
#         # du_dVy = (ry*Vz-rz*Vy)*(-rz) + (rx*Vy-ry*Vx)*(rx)
#         # du_dVz = (ry*Vz-rz*Vy)*(ry) + (rz*Vx-rx*Vz)*(-rx)
#         #
#         # partials['C3','rx'] = (1./norm_rxV) * du_drx * np.cos(inc) + Vy
#         # partials['C3','ry'] = (1./norm_rxV) * du_dry * np.cos(inc) - Vx
#         # partials['C3','rz'] = (1./norm_rxV) * du_drz * np.cos(inc) + 0.
#         # partials['C3','Vx'] = (1./norm_rxV) * du_dVx * np.cos(inc) - ry
#         # partials['C3','Vy'] = (1./norm_rxV) * du_dVy * np.cos(inc) + rx
#         # partials['C3','Vz'] = (1./norm_rxV) * du_dVz * np.cos(inc) + 0.
