import numpy as np
import omtools.api as ot

class ThrustVectorConstraint(ot.Group):
    def initialize(self):
        self.options.declare('num_nodes', default=1, types=int)

    def setup(self):
        num = self.options['num_nodes']

        ux = self.declare_input('ux', shape=(num,1))
        uy = self.declare_input('uy', shape=(num,1))
        uz = self.declare_input('uz', shape=(num,1))

        CT = ux**2 + uy**2 + uz**2

        self.register_output('CT', CT)












# from numpy import linalg
# from openmdao.api import ExplicitComponent
#
# class ThrustVectorConstraint(ExplicitComponent):
#
#     def initialize(self):
#         self.options.declare('num_nodes', default=1, types=int)
#
#     def setup(self):
#         num = self.options['num_nodes']
#
#         self.add_input('ux', shape=(num,1))
#         self.add_input('uy', shape=(num,1))
#         self.add_input('uz', shape=(num,1))
#
#         self.add_output('CT', shape=(num,1))
#
#         arange = np.arange(num)
#         self.declare_partials('CT','ux', rows=arange, cols=arange)
#         self.declare_partials('CT','uy', rows=arange, cols=arange)
#         self.declare_partials('CT','uz', rows=arange, cols=arange)
#
#     def compute(self,inputs,outputs):
#
#         ux = inputs['ux']
#         uy = inputs['uy']
#         uz = inputs['uz']
#
#         u = [ux, uy, uz]
#
#         #outputs['CT'] = linalg.norm(u,2) - 1.
#         # outputs['CT'] = np.sqrt(ux**2 + uy**2 + uz**2)
#         outputs['CT'] = ux**2 + uy**2 + uz**2
#         print(ux**2 + uy**2 + uz**2)
#         print('-'*40)
#
#     def compute_partials(self,inputs,partials):
#
#         ux = inputs['ux'].flatten()
#         uy = inputs['uy'].flatten()
#         uz = inputs['uz'].flatten()
#
#         partials['CT','ux'] = 2 * ux
#         partials['CT','uy'] = 2 * uy
#         partials['CT','uz'] = 2 * uz
