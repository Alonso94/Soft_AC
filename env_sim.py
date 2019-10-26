import vrep.vrep as vrep
import vrep.vrepConst as const_v
import time
import sys
import numpy as np
import cv2
import math


class MyEnv(object):

    def __init__(self):
        self.DoF = 7
        self.action_bound = [-1, 1]
        self.action_dim = self.DoF * 2
        self.state_dim = 19
        self.dt = 0.1
        self.done = False
        self.a = [0.0] * 7

        vrep.simxFinish(-1)
        # get the ID of the running simulation
        self.ID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
        # check the connection
        if self.ID != -1:
            print("Connected")
        else:
            print("Error")
            sys.exit("Error")

        self.cam_handle = self.get_handle('VisionSensor')
        self.joint_handles = []
        for i in range(self.DoF):
            tmp = self.get_handle("redundant_joint%d" % (i + 1))
            self.joint_handles.append(tmp)

    def get_handle(self, name):
        (check, handle) = vrep.simxGetObjectHandle(self.ID, name, const_v.simx_opmode_oneshot_wait)
        if check != 0:
            print("Couldn't find %s" % name)
        return handle

    def get_image(self,cam_handle):
        (code,res,im)=vrep.simxGetVisionSensorImage(self.ID,cam_handle,0,const_v.simx_opmode_streaming)
        img=np.array(im,dtype=np.uint8)
        img.resize([32,32,3])
        return img

    def move_joint(self,handle,value):
        vrep.simxSetJointPosition(self.ID, handle, value, const_v.simx_opmode_oneshot_wait)

    def sample_action(self):
        return np.random.uniform(self.action_bound,size=self.action_dim)

    def get_reward(self):
        return

    def step(self,action):
        action=np.clip(action,self.action_bound)
        for i in range(self.DoF):
            self.move_joint(self.joint_handles[i],self.a[i])
        img=self.get_image(self.cam_handle)
        reward=self.get_reward()
        return img,reward,self.done,{}

    def reset(self):
        return