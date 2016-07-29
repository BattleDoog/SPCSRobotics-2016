

#class PID(object):

# def __init__(self):
# 	print "PID initialized"

def PID_controller(kp, ki, kd, leftSensor, rightSensor):
	#Proportional 
	err = leftSensor - rightSensor
	pAdjust = kp * err
		
	#Integral
	pstErr = []
	pstErr.append(err)
	if len(pstErr) >= 5:
		errSum = sum(pstErr[-5:])    
	else:
		errSum = 0
	iAdjust = ki * errSum
	#print str(errSum)

	#Derivative
	errD = 0
	if len(pstErr) > 1:
		errD = pstErr[-1] - err
	dAdjust = kd * errD

	#return adjust value
	return pAdjust+iAdjust+dAdjust