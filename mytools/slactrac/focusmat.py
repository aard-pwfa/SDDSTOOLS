import scipy as sp
import numpy as _np
from driftmat import driftmat
from baseclass import baseclass

class Focus(baseclass):
	def __init__(self,length=0,K1=0,order=1):
		self._order = int(order)
		self._type = 'focus'
		self._length = _np.float64(length)
		self.K1 = _np.float64(K1)

	def _get_K1(self):
		return self._K1
	def _set_K1(self,val):
		self._K1 = val
	K1 = property(_get_K1,_set_K1)

	def _getR(self):
		return focusmat(L=self._length,K1=self.K1,order=self._order)
	R = property(_getR,doc='The transfer matrix R for the focus.')

	def _get_length(self):
		return self._length
	length = property(_get_length)

	def change_E(self,old_gamma,new_gamma):
		old_gamma = _np.float64(old_gamma)
		new_gamma = _np.float64(new_gamma)
		self.K1 *= old_gamma / new_gamma

def focusmat(K1=0,L=0,order=1):
	if ( K1 == 0 ):
		R = driftmat(L,order)
	else:
		rtK = _np.sqrt(_np.abs(K1))
		rtK_L = rtK * L
		sin_rtK_L = _np.sin(rtK_L)
		cos_rtK_L = _np.cos(rtK_L)
		sinh_rtK_L = _np.sinh(rtK_L)
		cosh_rtK_L = _np.cosh(rtK_L)
		R_f = _np.array(
				[[ cos_rtK_L    , sin_rtK_L/rtK ],
				[  -rtK*sin_rtK_L , cos_rtK_L   ]]
			)
		R_d = R_f
		if ( K1 > 0 ):
			R = _np.zeros([6,6])
			R[0:2,0:2] = R_f
			R[2:4,2:4] = R_d
			R[4:6,4:6] = _np.identity(2)
		elif ( K1 < 0 ):
			R = _np.zeros([6,6])
			R[0:2,0:2] = R_d
			R[2:4,2:4] = R_f
			R[4:6,4:6] = _np.identity(2)
		else:
			print 'Uhm who said what now??'
			print K1

	return R
