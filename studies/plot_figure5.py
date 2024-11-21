"""Script to plot example2 model results."""
import matplotlib
matplotlib.use("Agg")
import numpy as np
from numpy import array, average, mean
from pylab import plot, gca, show, figure, subplots, gca, semilogy, legend, \
    tight_layout, NullLocator, savefig, setp, tight_layout
from pickle import load

with_file = "with_social_learning_rate_4.p"
wo_file ="without_social.p"

f, ((ax11, ax12), (ax21, ax22), (ax21a, ax22a), (ax31, ax32)) = \
    subplots(nrows=4, ncols=2, sharex=True, figsize=(12, 14))
lws = 2
al = 1.

# LEFT: without policy

ax11.title.set_text('example run without socio-cultural processes')

traj = load(open(wo_file,"rb"))
worlds = list(traj["World.atmospheric_carbon"].keys())
social_systems = list(traj["SocialSystem.has_fossil_ban"].keys())
cells = list(traj["Cell.fossil_carbon"].keys())
individuals = list(traj["Individual.is_environmentally_friendly"].keys())
t = np.array(traj['t']) - 2000 # to have model years

print(t)
print(social_systems, cells)

# cultural
ax11.plot(t[3:], 100*average([array(traj["Individual.is_environmentally_friendly"][i][3:]*1) for i in individuals], axis=0,
                             weights=[array(traj["Individual.represented_population"][i][3:]*1) for i in individuals]),
          color="green",lw=2, label="env. friendly individuals")
ax11.plot(t[3:], 1 + 100*mean([array(traj["SocialSystem.has_fossil_ban"][s][3:]*1) for s in social_systems], axis=0),
          color="cyan",lw=2, label="regions w/ subsidy and fossil ban")
ax11.set_ylabel('CUL:\nglobal opinions & policies\n(percent)')
ax11.set_ylim(-5,105)
# ax11.legend(title='CUL: opinions & policies')
ax11.legend(loc=7)

# metabolic
ls = ["-", ":"]
#ax21a = ax21.twinx()

for i, s in enumerate(social_systems):
    Es = array(traj["SocialSystem.secondary_energy_flow"][s][3:])
    ax21.plot(t[3:], 100*array(traj["SocialSystem.biomass_input_flow"][s][3:]) * 40e9 / Es, 
              color="green", ls=ls[i], lw=lws, alpha=al, label=None if i else "biomass")
    ax21.plot(t[3:], 100*array(traj["SocialSystem.fossil_fuel_input_flow"][s][3:]) * 47e9 / Es, 
              color="gray", ls=ls[i], lw=lws, alpha=al, label=None if i else "fossils")
    ax21.plot(t[3:], 100*array(traj["SocialSystem.renewable_energy_input_flow"][s][3:]) / Es, 
              color="darkorange", ls=ls[i], lw=lws, alpha=al, label=None if i else "renewables")
    ax21a.plot(t[3:],
               100*array(traj["SocialSystem.economic_output_flow"][s][3:]) /
               [0.25, 0.75][i] / 6e9, 
              color="red", ls=ls[i], lw=lws, alpha=al, label=None if i else "GDP")

ax21a.semilogy()
ax21.set_ylabel('MET:\nregional energy shares\n(percent)')
ax21.set_ylim(-5,105)
#ax21.legend(title='MET: regional energy shares')
ax21.legend()

ax21a.set_ylabel('MET:\nGDP/capita ($/yr)')

# environmental
atmos_carb = traj["World.atmospheric_carbon"][worlds[0]][3:] 
ocean_carb = traj["World.upper_ocean_carbon"][worlds[0]][3:]
terre_carb = sum(array(traj["Cell.terrestrial_carbon"][c][3:]) for c in cells)
fossi_carb = sum(array(traj["Cell.fossil_carbon"][c][3:]) for c in cells)
photosynth = 10 * sum(array(traj["Cell.photosynthesis_carbon_flow"][c][3:]) for c in cells)

print((atmos_carb+terre_carb+ocean_carb)[-1])
ax31.plot(t[3:], atmos_carb, 
         color="cyan", lw=2, label="atmosphere")
ax31.plot(t[3:], ocean_carb,  
         color="blue", lw=2, label="upper oceans")
ax31.plot(t[3:], terre_carb, 
         color="green", lw=2, label="plants & soils")
ax31.plot(t[3:], fossi_carb,
         color="gray", lw=2, label="fossils")

setp(ax12.get_yticklabels(), visible=False)
setp(ax22.get_yticklabels(), visible=False)
setp(ax32.get_yticklabels(), visible=False)
setp(ax22a.get_yticklabels(), visible=False)

ax31.set_ylabel('ENV:\nglobal carbon stocks\n(gigatonnes carbon)')
ax31.set_ylim(-100,3500)
ax31.legend(loc="upper left")

ax31.set_xlabel('model year') # if we subtract 2000 above
ax31.set_xlim(0,120) # (1990,2110)

# RIGHT: with policy

ax12.title.set_text('example run with socio-cultural processes')

traj = load(open(with_file,"rb"))
worlds = list(traj["World.atmospheric_carbon"].keys())
social_systems = list(traj["SocialSystem.has_fossil_ban"].keys())
cells = list(traj["Cell.fossil_carbon"].keys())
individuals = list(traj["Individual.is_environmentally_friendly"].keys())
t = np.array(traj['t']) - 2000  # to have model years

print((s,traj["SocialSystem.has_fossil_ban"][s]) for s in social_systems)

# cultural
ax12.plot(t[3:], 100*average([array(traj["Individual.is_environmentally_friendly"][i][3:]*1) for i in individuals], axis=0,
                             weights=[array(traj["Individual.represented_population"][i][3:]*1) for i in individuals]),
          color="green",lw=2, label="env. friendly individuals")
ax12.plot(t[3:], 100*mean([array(traj["SocialSystem.has_fossil_ban"][s][3:]*1) for s in social_systems], axis=0),
          color="cyan",lw=2, label="regions w/ subsidy and fossil ban")
ax12.set_ylim(-5,105)
#ax12.yaxis.set_major_locator(NullLocator())
#ax12.legend(loc=7)

# metabolic
#ax22a = ax22.twinx()
for i, s in enumerate(social_systems):
    Es = array(traj["SocialSystem.secondary_energy_flow"][s][3:])
    ax22.plot(t[3:], 100*array(traj["SocialSystem.biomass_input_flow"][s][3:]) * 40e9 / Es, 
              color="green", ls=ls[i], lw=lws, alpha=al, label=None if i else "biomass")
    ax22.plot(t[3:], 100*array(traj["SocialSystem.fossil_fuel_input_flow"][s][3:]) * 47e9 / Es, 
              color="gray", ls=ls[i], lw=lws, alpha=al, label=None if i else "fossils")
    ax22.plot(t[3:], 100*array(traj["SocialSystem.renewable_energy_input_flow"][s][3:]) / Es, 
              color="darkorange", ls=ls[i], lw=lws, alpha=al, label=None if i else "renewables")
    ax22a.plot(t[3:],
               100*array(traj["SocialSystem.economic_output_flow"][s][3:]) /
               [0.25, 0.75][i] / 6e9, 
              color="red", ls=ls[i], lw=lws, alpha=al, label=None if i else "GDP")

ax22a.semilogy()
#äax22a.legend()
ax22.set_ylim(-5,105)
#ax22.yaxis.set_major_locator(NullLocator())
#ax22.legend(loc=7)

# environmental
atmos_carb = traj["World.atmospheric_carbon"][worlds[0]][3:] 
ocean_carb = traj["World.upper_ocean_carbon"][worlds[0]][3:]
terre_carb = sum(array(traj["Cell.terrestrial_carbon"][c][3:]) for c in cells)
fossi_carb = sum(array(traj["Cell.fossil_carbon"][c][3:]) for c in cells)

print((atmos_carb+terre_carb+ocean_carb)[-1])
ax32.plot(t[3:], atmos_carb, 
          color="cyan", lw=2, label="atmosphere")
ax32.plot(t[3:], ocean_carb,  
          color="blue", lw=2, label="upper oceans")
ax32.plot(t[3:], terre_carb, 
          color="green", lw=2, label="plants & soils")
ax32.plot(t[3:], fossi_carb,
          color="gray", lw=2, label="fossils")
ax32.set_ylim(0,3500)

ax32.set_xlabel('model year')
ax32.set_xlim(0,120) #(1990,2110)
#ax32.set_xlim(t.min(), t.max())
f.subplots_adjust(hspace=0, wspace=0.05)
tight_layout()
savefig("figure5.pdf")
