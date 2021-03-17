import numpy as np
import matplotlib.pyplot as plt
import pickle

from numpy import linalg
from openmdao.api import Problem, IndepVarComp, ExecComp, ScipyOptimizer, pyOptSparseDriver
from ozone.api import ODEIntegrator
from ascent_function import AscentFunction
from orbital_condition_one import OrbitalConditionOne
from orbital_condition_two import OrbitalConditionTwo
from orbital_condition_three import OrbitalConditionThree
from thrust_vector_constraint import ThrustVectorConstraint
# from lsdo_viz.api import Problem
# from matplotlib.patches import FancyArrowPatch
# from mpl_toolkits.mplot3d.proj3d import proj_transform
# from mpl_toolkits.mplot3d.axes3d import Axes3D

num = 51 # number of nodes

# ---------------------------------------------------------------------------------------------------------
# integrator group

ode_function = AscentFunction(system_init_kwargs={'g0': 1.625,'R0':1738100.,'vex':3047.80,'w2':1.,'T':45000.})
formulation = 'solver-based'
method_name = 'GaussLegendre2'
# method_name = 'RK4'
initial_time = 0.
normalized_times = np.linspace(0., 1., num)
initial_conditions = {'rx': 1., 'ry': 0., 'rz': 0., 'Vx': 0., 'Vy': 0., 'Vz': 0., 'm': 11414.}
#initial_conditions = {'rx': 1.005736762859885, 'ry': 0., 'rz': -0.005786478684830, 'Vx': -0.005840861873744, 'Vy': 0., 'Vz': -1.015189000628493, 'm': 15102.376679463554} # Abort Scenario 1
#initial_conditions = {'rx': 1.005736762859885, 'ry': 0., 'rz': -0.005786478684830, 'Vx': -0.005840861873744, 'Vy': 0., 'Vz': -1.015189000628493, 'm': 15102.376679463554} # Abort Scenario 2
#initial_conditions = {'rx': 1.005736762859885, 'ry': 0., 'rz': -0.005786478684830, 'Vx': -0.005840861873744, 'Vy': 0., 'Vz': -1.015189000628493, 'm': 15102.376679463554} # Abort Scenario 3

integrator = ODEIntegrator(ode_function, formulation, method_name,
    initial_time=initial_time, normalized_times=normalized_times,
    initial_conditions=initial_conditions)

# ---------------------------------------------------------------------------------------------------------
# passing in constraints

constraint_one = OrbitalConditionOne(a=1.04603,ecc=0.0385)
constraint_two = OrbitalConditionTwo(a=1.04603)
constraint_three = OrbitalConditionThree(inc=np.pi/2)
constraint_thrust = ThrustVectorConstraint(num_nodes=num)

# ---------------------------------------------------------------------------------------------------------
# problem formulation 1 - Using connections

prob = Problem()

# Define independent variable components
prob.model.add_subsystem('final_time_comp', IndepVarComp('final_time', val=1.0))
prob.model.add_subsystem('ux_comp', IndepVarComp('ux', val=0.1, shape=(num,1)))
prob.model.add_subsystem('uy_comp', IndepVarComp('uy', val=0.1, shape=(num,1)))
prob.model.add_subsystem('uz_comp', IndepVarComp('uz', val=0.1, shape=(num,1)))
# prob.model.add_subsystem('T_comp', IndepVarComp('T', shape=(num,1))) # Add thrust as indep. var.

# Add integrator group
prob.model.add_subsystem('integrator_group', integrator)

# Add constraint groups
prob.model.add_subsystem('ConstraintOne', constraint_one)
prob.model.add_subsystem('ConstraintTwo', constraint_two)
prob.model.add_subsystem('ConstraintThree', constraint_three)
prob.model.add_subsystem('ConstraintThrust', constraint_thrust)

# Issue connections of independent components
prob.model.connect('final_time_comp.final_time', 'integrator_group.final_time')
prob.model.connect('ux_comp.ux', 'integrator_group.dynamic_parameter:ux')
prob.model.connect('uy_comp.uy', 'integrator_group.dynamic_parameter:uy')
prob.model.connect('uz_comp.uz', 'integrator_group.dynamic_parameter:uz')

# Issue connections of constraint 1
prob.model.connect('integrator_group.state:rx', 'ConstraintOne.rx', src_indices=-1)
prob.model.connect('integrator_group.state:ry', 'ConstraintOne.ry', src_indices=-1)
prob.model.connect('integrator_group.state:rz', 'ConstraintOne.rz', src_indices=-1)
prob.model.connect('integrator_group.state:Vx', 'ConstraintOne.Vx', src_indices=-1)
prob.model.connect('integrator_group.state:Vy', 'ConstraintOne.Vy', src_indices=-1)
prob.model.connect('integrator_group.state:Vz', 'ConstraintOne.Vz', src_indices=-1)

# Issue connections of constraint 2
prob.model.connect('integrator_group.state:rx', 'ConstraintTwo.rx', src_indices=-1)
prob.model.connect('integrator_group.state:ry', 'ConstraintTwo.ry', src_indices=-1)
prob.model.connect('integrator_group.state:rz', 'ConstraintTwo.rz', src_indices=-1)
prob.model.connect('integrator_group.state:Vx', 'ConstraintTwo.Vx', src_indices=-1)
prob.model.connect('integrator_group.state:Vy', 'ConstraintTwo.Vy', src_indices=-1)
prob.model.connect('integrator_group.state:Vz', 'ConstraintTwo.Vz', src_indices=-1)

# Issue connections of constraint 3
prob.model.connect('integrator_group.state:rx', 'ConstraintThree.rx', src_indices=-1)
prob.model.connect('integrator_group.state:ry', 'ConstraintThree.ry', src_indices=-1)
prob.model.connect('integrator_group.state:rz', 'ConstraintThree.rz', src_indices=-1)
prob.model.connect('integrator_group.state:Vx', 'ConstraintThree.Vx', src_indices=-1)
prob.model.connect('integrator_group.state:Vy', 'ConstraintThree.Vy', src_indices=-1)
prob.model.connect('integrator_group.state:Vz', 'ConstraintThree.Vz', src_indices=-1)

# Issue connections of constraint 4
prob.model.connect('ux_comp.ux', 'ConstraintThrust.ux')
prob.model.connect('uy_comp.uy', 'ConstraintThrust.uy')
prob.model.connect('uz_comp.uz', 'ConstraintThrust.uz')

prob.model.add_design_var('final_time_comp.final_time', lower=1./1034.2)
prob.model.add_design_var('ux_comp.ux',lower=0.,upper=1.)
prob.model.add_design_var('uy_comp.uy',lower=0.,upper=1.)
prob.model.add_design_var('uz_comp.uz',lower=0.,upper=1.)
prob.model.add_objective('final_time_comp.final_time')
prob.model.add_constraint('ConstraintOne.C1', equals=0.)
prob.model.add_constraint('ConstraintTwo.C2', equals=0.)
prob.model.add_constraint('ConstraintThree.C3', equals=0.)
prob.model.add_constraint('ConstraintThrust.CT', upper=1.)
prob.model.add_constraint('integrator_group.state:m', lower=1., indices=[-1])

# ---------------------------------------------------------------------------------------------------------
# problem formulation 2 - Using promote

# prob = Problem()
#
# # Define independent variable components
# prob.model.add_subsystem('final_time_comp', IndepVarComp('final_time', val=1.0))
# prob.model.add_subsystem('ux_comp', IndepVarComp('ux', shape=(num,1)))
# prob.model.add_subsystem('uy_comp', IndepVarComp('uy', shape=(num,1)))
# prob.model.add_subsystem('uz_comp', IndepVarComp('uz', shape=(num,1)))
# # prob.model.add_subsystem('T_comp', IndepVarComp('T', shape=(num,1))) # Add thrust as indep. var.
#
# # Add integrator group
# prob.model.add_subsystem('integrator_group', integrator)
#
# # Add constraint groups
# prob.model.add_subsystem('ConstraintOne', constraint_one, promotes=['rx','ry','rz','Vx','Vy','Vz','C1'])
# prob.model.add_subsystem('ConstraintTwo', constraint_two, promotes=['rx','ry','rz','Vx','Vy','Vz','C2'])
# prob.model.add_subsystem('ConstraintThree', constraint_three, promotes=['rx','ry','rz','Vx','Vy','Vz','C3'])
# prob.model.add_subsystem('ConstraintThrust', constraint_thrust, promotes=['ux','uy','uz',CT'])
#
# # Issue connections of independent components
# prob.model.connect('final_time_comp.final_time', 'integrator_group.final_time')
# prob.model.connect('ux_comp.ux', 'integrator_group.dynamic_parameter:ux')
# prob.model.connect('ux_comp.uy', 'integrator_group.dynamic_parameter:uy')
# prob.model.connect('ux_comp.uz', 'integrator_group.dynamic_parameter:uz')
#
# prob.model.add_design_var('final_time_comp.final_time', lower=1./806.)
# prob.model.add_design_var('ux_comp.ux')
# prob.model.add_design_var('uy_comp.uy')
# prob.model.add_design_var('uz_comp.uz')
# prob.model.add_objective('final_time_comp.final_time')
# prob.model.add_constraint('ConstraintOne.C1', equals=0.)
# prob.model.add_constraint('ConstraintOne.C2', equals=0.)
# prob.model.add_constraint('ConstraintOne.C3', equals=0.)
# prob.model.add_constraint('ConstraintOne.CT', equals=0.)

# ---------------------------------------------------------------------------------------------------------
# problem optimizer

prob.driver = pyOptSparseDriver()
prob.driver.options['optimizer'] = 'SNOPT'

# ---------------------------------------------------------------------------------------------------------
# problem setup
prob.setup(check=False)

if 0:
    prob.run_model()
    prob.check_partials(compact_print=True)
    exit()

prob.run()

t = prob['integrator_group.times']
rx = prob['integrator_group.state:rx']
ry = prob['integrator_group.state:ry']
rz = prob['integrator_group.state:rz']
Vx = prob['integrator_group.state:Vx']
Vy = prob['integrator_group.state:Vy']
Vz = prob['integrator_group.state:Vz']
ux = prob['integrator_group.dynamic_parameter:ux']
uy = prob['integrator_group.dynamic_parameter:uy']
uz = prob['integrator_group.dynamic_parameter:uz']
m = prob['integrator_group.state:m']

# data = [rx, ry, rz, Vx, Vy, Vz, m, ux, uy, uz, t]
# print("All data")
# print(data)
# pickle.dump(data,open("data_om.dat","wb"))

if 1:
    r = np.zeros(num)
    for i in range(0,num):
        r[i] = linalg.norm([rx[i],ry[i],rz[i]],2)

    print(r)
    plt.plot(1034.2*prob['integrator_group.times'], (1738100.*r - 1738100.))
    plt.xlabel('time')
    plt.ylabel('altitude')
    plt.grid()
    plt.show()
print(' ')
if 0:
    V = np.zeros(num)
    for i in range(0,num):
        V[i] = linalg.norm([Vx[i],Vy[i],Vz[i]],2)

    print(V)
    plt.plot(1034.2*prob['integrator_group.times'], 1680.6*V)
    plt.xlabel('time')
    plt.ylabel('velocity')
    plt.grid()
    plt.show()
print(' ')
if 0:
    u = np.zeros(num)
    for i in range(0,num):
        u[i] = linalg.norm([ux[i],uy[i],uz[i]],2)

    print(u)
    plt.plot(1034.2*prob['integrator_group.times'], u)
    plt.xlabel('time')
    plt.ylabel('control')
    plt.ylim(-0.2,1.2)
    plt.grid()
    plt.show()
print(' ')
if 0:
    plt.plot(1034.2*prob['integrator_group.times'], m)
    plt.xlabel('time')
    plt.ylabel('mass')
    plt.grid()
    plt.show()
print(' ')
if 0:
    plt.plot(1034.2*prob['integrator_group.times'], ux)
    plt.xlabel('time')
    plt.ylabel('control x')
    plt.ylim(-0.2,1.2)
    plt.grid()
    plt.show()
print(' ')
if 0:
    plt.plot(1034.2*prob['integrator_group.times'], uy)
    plt.xlabel('time')
    plt.ylabel('control y')
    plt.ylim(-0.2,1.2)
    plt.grid()
    plt.show()
print(' ')
if 0:
    plt.plot(1034.2*prob['integrator_group.times'], uz)
    plt.xlabel('time')
    plt.ylabel('control z')
    plt.ylim(-0.2,1.2)
    plt.grid()
    plt.show()

# class Arrow3D(FancyArrowPatch):
#     def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
#         super().__init__((0,0), (0,0), *args, **kwargs)
#         self._xyz = (x,y,z)
#         self._dxdydz = (dx,dy,dz)
#
#     def draw(self, renderer):
#         x1,y1,z1 = self._xyz
#         dx,dy,dz = self._dxdydz
#         x2,y2,z2 = (x1+dx,y1+dy,z1+dz)
#
#         xs, ys, zs = proj_transform((x1,x2),(y1,y2),(z1,z2), renderer.M)
#         self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
#         super().draw(renderer)
#
# def _arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
#     '''Add an 3d arrow to an `Axes3D` instance.'''
#
#     arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
#     ax.add_artist(arrow)
#
# setattr(Axes3D,'arrow3D',_arrow3D)
#
# if 0:
#     ax = plt.axes(projection='3d')
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     ax.plot3D(rx[:,0], ry[:,0], rz[:,0], 'gray')
#     scaling = 0.1 \
#         * np.max([
#             np.max(rx[:, 0]) - np.min(rx[:, 0]),
#             np.max(ry[:, 0]) - np.min(ry[:, 0]),
#             np.max(rz[:, 0]) - np.min(rz[:, 0]),
#         ]) \
#         / np.max([
#             np.max(ux[:, 0]) - np.min(ux[:, 0]),
#             np.max(uy[:, 0]) - np.min(uy[:, 0]),
#             np.max(uz[:, 0]) - np.min(uz[:, 0]),
#         ])
#     for ind in range(num):
#         ax.arrow3D(
#             rx[ind, 0],
#             ry[ind, 0],
#             rz[ind, 0],
#             scaling * ux[ind, 0],
#             scaling * uy[ind, 0],
#             scaling * uz[ind, 0],
#             fc='blue',
#             ec='blue',
#             arrowstyle='->',
#         )
#     ax.set_xlabel('x axis')
#     ax.set_ylabel('y axis')
#     ax.set_zlabel('z axis')
#     plt.ylim(-0.2,0.2)
#     plt.show()



# ------------------------------------------------------------------------------
#                                SAVE DATA
# ------------------------------------------------------------------------------
# print("size Check")
# print(np.shape(r))
# print(np.shape(V))
# print(np.shape(m))
# print(np.shape(u))
# print(np.shape(t))
# data = [r, V, u, t]
# pickle.dump(data,open("data_om.dat","wb"))
