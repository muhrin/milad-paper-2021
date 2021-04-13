#include "colors.inc"
#include "finish.inc"

global_settings {assumed_gamma 1 max_trace_level 6}
background {color White transmit 1.0}
camera {perspective
  right -7.41*x up 7.35*y
  direction 50.00*z
  location <0,0,50.00> look_at <0,0,0>}
light_source {<  2.00,   3.00,  40.00> color White
  area_light <0.70, 0, 0>, <0, 0.70, 0>, 3, 3
  adaptive 1 jitter}

#declare simple = finish {phong 0.7}
#declare pale = finish {ambient 0.5 diffuse 0.85 roughness 0.001 specular 0.200 }
#declare intermediate = finish {ambient 0.3 diffuse 0.6 specular 0.1 roughness 0.04}
#declare vmd = finish {ambient 0.0 diffuse 0.65 phong 0.1 phong_size 40.0 specular 0.5 }
#declare jmol = finish {ambient 0.2 diffuse 0.6 specular 1 roughness 0.001 metallic}
#declare ase2 = finish {ambient 0.05 brilliance 3 diffuse 0.6 metallic specular 0.7 roughness 0.04 reflection 0.15}
#declare ase3 = finish {ambient 0.15 brilliance 2 diffuse 0.6 metallic specular 1.0 roughness 0.001 reflection 0.0}
#declare glass = finish {ambient 0.05 diffuse 0.3 specular 1.0 roughness 0.001}
#declare glass2 = finish {ambient 0.01 diffuse 0.3 specular 1.0 reflection 0.25 roughness 0.001}
#declare Rcell = 0.100;
#declare Rbond = 0.100;

#macro atom(LOC, R, COL, TRANS, FIN)
  sphere{LOC, R texture{pigment{color COL transmit TRANS} finish{FIN}}}
#end
#macro constrain(LOC, R, COL, TRANS FIN)
union{torus{R, Rcell rotate 45*z texture{pigment{color COL transmit TRANS} finish{FIN}}}
      torus{R, Rcell rotate -45*z texture{pigment{color COL transmit TRANS} finish{FIN}}}
      translate LOC}
#end

cylinder {<  0.00,   0.00,  -3.24>, <  2.87,   0.00,  -3.24>, Rcell pigment {Black}}
cylinder {<  0.00,   2.84,  -2.84>, <  2.87,   2.84,  -2.84>, Rcell pigment {Black}}
cylinder {<  0.00,   2.44,   0.00>, <  2.87,   2.44,   0.00>, Rcell pigment {Black}}
cylinder {<  0.00,  -0.40,  -0.40>, <  2.87,  -0.40,  -0.40>, Rcell pigment {Black}}
cylinder {<  0.00,   0.00,  -3.24>, <  0.00,   2.84,  -2.84>, Rcell pigment {Black}}
cylinder {<  2.87,   0.00,  -3.24>, <  2.87,   2.84,  -2.84>, Rcell pigment {Black}}
cylinder {<  2.87,  -0.40,  -0.40>, <  2.87,   2.44,   0.00>, Rcell pigment {Black}}
cylinder {<  0.00,  -0.40,  -0.40>, <  0.00,   2.44,   0.00>, Rcell pigment {Black}}
cylinder {<  0.00,   0.00,  -3.24>, <  0.00,  -0.40,  -0.40>, Rcell pigment {Black}}
cylinder {<  2.87,   0.00,  -3.24>, <  2.87,  -0.40,  -0.40>, Rcell pigment {Black}}
cylinder {<  2.87,   2.84,  -2.84>, <  2.87,   2.44,   0.00>, Rcell pigment {Black}}
cylinder {<  0.00,   2.84,  -2.84>, <  0.00,   2.44,   0.00>, Rcell pigment {Black}}
atom(<  0.00,   0.00,  -3.24>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #0 
atom(<  1.44,   1.22,  -1.62>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #1 
atom(< -1.44,  -1.22,  -4.86>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #2 
atom(< -1.44,  -1.62,  -2.02>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #3 
atom(< -1.44,   1.62,  -4.46>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #4 
atom(< -2.87,   0.00,  -3.24>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #5 
atom(< -1.44,   1.22,  -1.62>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #6 
atom(<  1.44,  -1.22,  -4.86>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #7 
atom(<  0.00,  -2.84,  -3.64>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #8 
atom(<  1.44,  -1.62,  -2.02>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #9 
atom(<  0.00,   0.40,  -6.08>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #10 
atom(<  1.44,   1.62,  -4.46>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #11 
atom(<  0.00,   2.84,  -2.84>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #12 
atom(<  2.87,   0.00,  -3.24>, 0.66, rgb <0.88, 0.40, 0.20>, 0.0, ase3) // #13 
