from ozone.api import ODEFunction
from ascent_system import AscentSystem

class AscentFunction(ODEFunction):
    def initialize(self, system_init_kwargs=None):
        self.set_system(AscentSystem, system_init_kwargs)

        self.declare_state('rx','drx_dt', shape=1, targets=['rx'])
        self.declare_state('ry','dry_dt', shape=1, targets=['ry'])
        self.declare_state('rz','drz_dt', shape=1, targets=['rz'])
        self.declare_state('Vx','dVx_dt', shape=1, targets=['Vx'])
        self.declare_state('Vy','dVy_dt', shape=1, targets=['Vy'])
        self.declare_state('Vz','dVz_dt', shape=1, targets=['Vz'])
        self.declare_state('m','dm_dt', shape=1, targets=['m'])

        self.declare_parameter('ux', 'ux', shape=1)
        self.declare_parameter('uy', 'uy', shape=1)
        self.declare_parameter('uz', 'uz', shape=1)
