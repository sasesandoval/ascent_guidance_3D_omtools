import numpy as np
import omtools.api as ot
from numpy import linalg

class OrbitalConditionTwo(ot.Group):

    def initialize(self):
        self.options.declare('a', default=1., types=float)

    def setup(self):
        a = self.options['a']

        rx = self.declare_input('rx')
        ry = self.declare_input('ry')
        rz = self.declare_input('rz')
        Vx = self.declare_input('Vx')
        Vy = self.declare_input('Vy')
        Vz = self.declare_input('Vz')

        r = self.create_output('r', shape=(3,))
        V = self.create_output('V', shape=(3,))

        r[0] = rx
        r[1] = ry
        r[2] = rz
        V[0] = Vx
        V[1] = Vy
        V[2] = Vz

        #r_norm = (rx**2 + ry**2 + rz**2)**0.5
        #V_norm = (Vx**2 + Vy**2 + Vz**2)**0.5

        # C2 = (((ot.sum(V**2))**0.5)**2)/2. - 1./((ot.sum(r**2))**0.5) + 1./(2*a)
        C2 = ((ot.pnorm(V))**2)/2. - 1./(ot.pnorm(r)) + 1./(2*a)
        #C2 = (V_norm**2)/2. - 1./(r_norm) + 1./(2*a)

        self.register_output('C2', C2)




# from openmdao.api import ExplicitComponent
#
# class OrbitalConditionTwo(ExplicitComponent):
#
#     def initialize(self):
#         #self.options.declare('num_nodes', default=1, types=int)
#         self.options.declare('a', default=1., types=float)
#
#     def setup(self):
#         #num = self.options['num_nodes']
#         a = self.options['a']
#
#         self.add_input('rx', shape=1)
#         self.add_input('ry', shape=1)
#         self.add_input('rz', shape=1)
#         self.add_input('Vx', shape=1)
#         self.add_input('Vy', shape=1)
#         self.add_input('Vz', shape=1)
#
#         self.add_output('C2', shape=1)
#
#         self.declare_partials('*','*',dependent=False)
#         self.declare_partials('C2','rx')
#         self.declare_partials('C2','ry')
#         self.declare_partials('C2','rz')
#         self.declare_partials('C2','Vx')
#         self.declare_partials('C2','Vy')
#         self.declare_partials('C2','Vz')
#
#     def compute(self,inputs,outputs):
#         a = self.options['a']
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
#
#         outputs['C2'] = linalg.norm(V,2)**2/2. - 1./linalg.norm(r,2) + 1./(2*a)
#
#     def compute_partials(self,inputs,partials):
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
#         norm_r = linalg.norm(r)
#         norm_V = linalg.norm(V)
#
#         dnorm_r_drx = rx / norm_r
#         dnorm_r_dry = ry / norm_r
#         dnorm_r_drz = rz / norm_r
#         dnorm_V_dVx = Vx / norm_V
#         dnorm_V_dVy = Vy / norm_V
#         dnorm_V_dVz = Vz / norm_V
#
#         partials['C2','rx'] = dnorm_r_drx / norm_r ** 2
#         partials['C2','ry'] = dnorm_r_dry / norm_r ** 2
#         partials['C2','rz'] = dnorm_r_drz / norm_r ** 2
#         partials['C2','Vx'] = Vx
#         partials['C2','Vy'] = Vy
#         partials['C2','Vz'] = Vz
