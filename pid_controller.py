import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from tkinter import *

#***********************************************
                                                  #REGULATOR PREDKOSCI 1DOF
def regulator_predkosci(current_value):

   global Integrator_s,Derivator_s,set_point_s,Kd_s,Ki_s,Kp_s

   error = set_point_s - current_value
   P_value = Kp_s * error
   Integrator_s = Integrator_s + error *kr
   I_value = Integrator_s * Ki_s
   PI = (P_value + I_value)
   D_value = Kd_s * (current_value - Derivator_s) /kr
   Derivator_s = current_value
   PI_D=PI-D_value

   return PI_D

#***********************************************
                                              #REGULATOR PRADU PI
Kp_i = 0.1
Ki_i = 30
def regulator_pradu(current_value):
   global Integrator_i
   error = set_point_i - current_value
   P_value = Kp_i * error
   Integrator_i = Integrator_i + error *kr
   I_value = Integrator_i * Ki_i
   PI = (P_value + I_value)
   if PI > 300:
      PI = 300
   if PI < 0:
      PI = 0
   return PI

#***********************************************
                                                #SILNIK DC
u=300.0
R=3.0
kfi=2.23
L=0.01
mop=0.0
J=0.11

def silnik_DC(y,t,u,R,kfi,L,mop,J):
   i,w=y
   dydt=[(u-i*R-kfi*w)/L,(kfi*i-mop)/J]
   return dydt

#***********************************************
                                                #PRZEKSZTA£TNIK
k_p=1.0
T_p=0.05
def przeksztaltnik(s_we,k,T,kr):
   global s_wy
   s_wy = 1.0/T *kr*(s_we*k-s_wy)+s_wy
   return s_wy



kr=0.001
time= np.arange(0.0, 4.0, kr)

def generuj():
   global set_point_s, set_point_i, Derivator_s, Integrator_s, Integrator_i,s_wy,Kd_s,Ki_s,Kp_s,licznik

   s_wy = 0.0
   Integrator_i=0.0
   Derivator_s = 0.0
   Integrator_s = 0.0
   y0=[0.0,0.0]
   i_t,w_t=y0
   f_prad = []
   f_predkosc = []
   f_napiecie = []

   Kp_s = float(ui_kp.get())
   Ki_s = float(ui_ki.get())
   Kd_s = float(ui_kd.get())
   set_point_s = float(setpoint.get())

   for t in time:
      if t < 2.0:
          mop = 0.0
      else:
          mop = 20 * 2.23
      sygnal_Rw=regulator_predkosci(w_t)
      set_point_i=sygnal_Rw
      sygnal_Ri=regulator_pradu(i_t)
      syg_ster = przeksztaltnik(sygnal_Ri, k_p, T_p, kr)

      SILNIK = odeint(silnik_DC, y0,[0.0,kr],args=(syg_ster,R,kfi,L,mop,J))
      SILNIK = SILNIK[1, :]
      y0 = SILNIK
      i_t,w_t=y0

      f_prad.append(i_t)
      f_predkosc.append(w_t)
      f_napiecie.append(syg_ster)

   plt.figure()
   plt.subplot(311)
   plt.plot(time,f_predkosc,color="b")
   plt.legend(['prêdkoœæ'])
   plt.subplot(312)
   plt.plot(time,f_prad,color="r")
   plt.legend(['pr¹d'])
   plt.subplot(313)
   plt.plot(time, f_napiecie,color="g")
   plt.legend(['napiêcie'])
   plt.show()

def update():
   if wybor_strR_predkosci.get()=="P":
      ui_kp.set(2.0)
      ui_ki.set(0)
      ui_kd.set(0)
   elif wybor_strR_predkosci.get()=='PI':
      ui_kp.set(2.0)
      ui_ki.set(4.0)
      ui_kd.set(0)
   else:
      ui_kp.set(35.0)
      ui_ki.set(2.2)
      ui_kd.set(6.0)

root = Tk()
bttn_zatwierdz = Button(root, text="Akceptuj", command=generuj)

ui_kp = StringVar()
ui_kp.set(0)
ui_ki = StringVar()
ui_ki.set(0)
ui_kd = StringVar()
ui_kd.set(0)
setpoint = StringVar()
setpoint.set(100)

var = IntVar()
var.set(0)

wybor_strR_predkosci = StringVar()
wybor_strR_predkosci.set(None)

pole_wyboru_1 = Radiobutton(root, text="P", variable=wybor_strR_predkosci, value="P",command=update)
pole_wyboru_2 = Radiobutton(root, text="PI", variable=wybor_strR_predkosci, value="PI",command=update)
pole_wyboru_3 = Radiobutton(root, text="PI_D", variable=wybor_strR_predkosci, value="PI_D",command=update)

entry_1=Entry(root, textvariable=ui_kp,width=5)
entry_2=Entry(root, textvariable=ui_ki,width=5)
entry_3=Entry(root, textvariable=ui_kd,width=5)
entry_4=Entry(root, textvariable=setpoint,width=5)

Label(root, text="Wybór struktury regulatora").grid(row=0, columnspan=3)
pole_wyboru_1.grid(row=1, column=0)
pole_wyboru_2.grid(row=1, column=1)
pole_wyboru_3.grid(row=1, column=2)
Label(root, text="Wybór parametrów").grid(row=0, column=4,columnspan=2)
Label(root, text="kP").grid(row=1, column=4)
entry_1.grid(row=1, column=5)
Label(root, text="kI").grid(row=2, column=4)
entry_2.grid(row=2, column=5)
Label(root, text="kD").grid(row=3, column=4)
entry_3.grid(row=3, column=5)

Label(root, text="setpoint: ").grid(row=2, column=0,columnspan=2)
entry_4.grid(row=2, column=2)

bttn_zatwierdz.grid(row=6, column=0)

root.mainloop()

