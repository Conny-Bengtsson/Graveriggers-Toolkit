import maya.cmds as cmds
import maya.mel as mel
import pymel.core as core


'''¤**************************************************SMALL FUNCTIONS****************************************************'''


'''SnapFollicles'''

def snapFol():
    

    myJoint = cmds.ls(sl=True,typ="joint")
    myFollicleandNurb = cmds.ls(sl=True,typ="transform")
    
    
    for i in myFollicleandNurb:
        mySorting = cmds.listRelatives(i)
        mySorting = mySorting[0]
        if cmds.nodeType(mySorting) == "follicle":
            myFollacle = i
        if cmds.nodeType(mySorting) == "nurbsSurface": 
            myNurb = i
        else:
            pass    
        
    myFollacleShape = cmds.listRelatives(myFollacle, typ="shape")
    myLocatorBase = cmds.spaceLocator()
    myLocator = cmds.listRelatives(myLocatorBase)
    
    cmds.matchTransform(myLocator,myJoint)
    pointNode = mel.eval('createNode "closestPointOnSurface"')
    mel.eval(f'connectAttr -f {myLocator[0]}.worldPosition[0] {pointNode}.inPosition;')
    mel.eval(f'connectAttr -f {myNurb}.worldSpace[0] {pointNode}.inputSurface;')
    myDistance = cmds.getAttr(f"{pointNode}.result.parameterV")
    cmds.setAttr (f"{myFollacleShape[0]}.parameterV", myDistance)
    cmds.delete(myLocatorBase)






'''Hide and Unhide Attributes'''


def lockAllAttributes(lock=True):


    keyable = not lock
    
    allCtrls = cmds.listRelatives((cmds.ls(typ="nurbsCurve")), p=True)
    
    for i in allCtrls:
                       
           
        attrList=cmds.listAttr(i)
        for obj in attrList:  
                if "scale" in obj:
                    if len(obj) < 8:
                        cmds.setAttr(f"{i}.{obj}", lock=lock, keyable=keyable, channelBox=False)            
                if "visibility" in obj:
                    cmds.setAttr(f"{i}.{obj}", lock=lock, keyable=keyable, channelBox=False)           
           
        
        if "fk" in i or "result" in i or "Spine" in i or "Neck" in i or "Head" in i:
            for obj in attrList:
            
                if "translate" in obj:
                    cmds.setAttr(f"{i}.{obj}", lock=lock, keyable=keyable, channelBox=False)      
                          
        if "ik_pv" in i or "ikfkSwitch" in i:        
            for obj in attrList:
            
                if "rotate" in obj:
                    if len(obj) < 9:
                        cmds.setAttr(f"{i}.{obj}", lock=lock, keyable=keyable, channelBox=False)                            
                    
        
        if "fk_Leg_ctrl" in i:        
            for obj in attrList:
            
                if "rotateX" in obj or "rotateY" in obj:
                    if len(obj) < 9:
                        cmds.setAttr(f"{i}.{obj}", lock=lock, keyable=keyable, channelBox=False)   
                        
        if "fk_ForeArm_ctrl" in i:        
            for obj in attrList:
        
                if "rotateX" in obj or "rotateZ" in obj:
                    if len(obj) < 9:
                        cmds.setAttr(f"{i}.{obj}", lock=lock, keyable=keyable, channelBox=False)                        
                            
               


'''Mirror Joints'''

def mirrorJoints():
    
    mel.eval('mirrorJoint -mirrorYZ -mirrorBehavior -searchReplace "l_" "r_"')
    
    selectedJoint = cmds.ls(sl=True)
    jointsOnly = cmds.listRelatives(selectedJoint, ad=True, fullPath=True,typ="joint")      
    noneJoints = cmds.listRelatives(selectedJoint, ad=True, fullPath=True)    
    noneJoints = [x for x in noneJoints if x not in jointsOnly]         
    if noneJoints:
        cmds.delete(noneJoints) 
    
    if selectedJoint[0] == "r_result_Shoulder_jnt":
        if cmds.objExists("rightArm_result_grp"):
            cmds.parent("r_result_Shoulder_jnt","rightArm_result_grp")
        
    if selectedJoint[0] == "r_result_UpLeg_jnt":
        if cmds.objExists("rightLeg_result_grp"):
            cmds.parent("r_result_UpLeg_jnt","rightLeg_result_grp")       
        


'''Select Nurb Control Vertex'''

def selectNurbControlVertex():
    
    nurbs = cmds.ls(sl=True)
    cmds.select(clear=True)

    if nurbs:
        
        for nurb in nurbs:
            
            
            try:
                numberOfCvs = cmds.getAttr(f'{nurb}.degree') + cmds.getAttr(f'{nurb}.spans')
                
                if isinstance(numberOfCvs, list):
                    numberOfCvs.sort()
                    numberOfCvs=numberOfCvs[-1]+2
                    
                for i in range(numberOfCvs):
                    if cmds.objExists(f"{nurb}.cv[{i}]"):
                        cmds.select(f"{nurb}.cv[{i}]",add=True)
                    else:
                        pass    
                                
            except:    
                cmds.inViewMessage( amg='<hl>Please select a nurb shape</hl>.', pos='midCenter', fade=True, ck=True )    
        



    else:   
        cmds.inViewMessage( amg='<hl>Please select atleast one nurb shape</hl>.', pos='midCenter', fade=True, ck=True )    
        
 

'''Reset Rigg'''

def resetRigg():
    allCtrls = cmds.listRelatives((cmds.ls(typ="nurbsCurve")), p=True)
    
    for i in allCtrls:
    
        attrList=cmds.listAttr(i,k=True, v=True, u=True)
        if attrList:
            for obj in attrList:
                if "translate" in obj:
                    cmds.setAttr(f"{i}.{obj}", 0)         
                if "rotate" in obj:
                    cmds.setAttr(f"{i}.{obj}", 0)             
                if "_jnt" in obj:
                    cmds.setAttr(f"{i}.{obj}", 0)         
            


'''Change Nurb Width'''


def nurbWidth():
    
    myListParent = cmds.ls(selection=True)
    
    if myListParent:
    
        myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
        
        
        result = cmds.promptDialog(
                title='Resize',
                message='Enter Width:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')


        customNumber = cmds.promptDialog(query=True, text=True)
        customNumber = float(customNumber)     
        cmds.select(clear=True)
        
        for item in myList:
            try:
                cmds.setAttr (f"{item}.lineWidth", customNumber)
            except:
                cmds.inViewMessage( amg='<hl>Please select a nurb shape</hl>.', pos='midCenter', fade=True, ck=True )     

    
    else:   
        cmds.inViewMessage( amg='<hl>Please select atleast one nurb shape</hl>.', pos='midCenter', fade=True, ck=True )     


        
        
'''Color Nurbs Button Functions'''


def buttonBlueColor(take=1):
    
    myList = cmds.ls(selection=True)
    
    if myList:
        myList = cmds.listRelatives(myList, ad=True, fullPath=True)
       
    
        for item in myList:
    
            cmds.setAttr (f"{item}.overrideEnabled", 1)
            cmds.setAttr (f"{item}.overrideColor", 6)

    else:   
        cmds.inViewMessage( amg='<hl>Please select atleast one nurb shape</hl>.', pos='midCenter', fade=True, ck=True ) 
    
    
    
def buttonRedColor(take=1):
    
    myList = cmds.ls(selection=True)
    
    if myList:
        myList = cmds.listRelatives(myList, ad=True, fullPath=True)
        for item in myList:
        
            cmds.setAttr (f"{item}.overrideEnabled", 1)
            cmds.setAttr (f"{item}.overrideColor", 13)
            
    else:   
        cmds.inViewMessage( amg='<hl>Please select atleast one nurb shape</hl>.', pos='midCenter', fade=True, ck=True ) 


def buttonYellowColor(take=1):
   
    myList = cmds.ls(selection=True)
    if myList:
        myList = cmds.listRelatives(myList, ad=True, fullPath=True)
        
        x=0    
        
        for item in myList:
        
            cmds.setAttr (f"{item}.overrideEnabled", 1)
            cmds.setAttr (f"{item}.overrideColor", 17)
            x += 1
        
    else:   
        cmds.inViewMessage( amg='<hl>Please select atleast one nurb shape</hl>.', pos='midCenter', fade=True, ck=True ) 
   


'''¤**************************************************Connect Result to IK and FK****************************************************'''
    
def connectResultJoints():    
    
    
    selectedObjects = cmds.ls(sl=True)
    
    '''Sort the selected joints into lists'''
    
    selectedJoints = cmds.ls(sl=True,typ="joint")
    allFkJoints=[]
    allIkJoints=[]
    allResultJoints=[]
    
    for i in selectedJoints:
    
        if "|" in i:
            
            i = (f"{i[1:]}")    
        
        if "fk" in i:
            
            allFkJoints.append(i) 
                 
        if "ik" in i:
            
            allIkJoints.append(i)          
            
        if "result" in i:
            
            allResultJoints.append(i)    
            
            
    selectedJointsChildren = cmds.listRelatives(allFkJoints, ad=True, typ="joint")      
    for i in selectedJointsChildren:
    
        allFkJoints.append(i) 
            
    selectedJointsChildren = cmds.listRelatives(allIkJoints, ad=True, typ="joint")      
    for i in selectedJointsChildren:
    
        allIkJoints.append(i) 
        
    selectedJointsChildren = cmds.listRelatives(allResultJoints, ad=True, typ="joint")      
    for i in selectedJointsChildren:
    
        allResultJoints.append(i) 
                    
                
    
    '''Sort the selected controls into lists'''
    
    allCtrls = cmds.listRelatives(selectedObjects, fullPath=True)
    cmds.select(allCtrls)
    allCtrls = cmds.ls(typ="nurbsCurve", sl=True)
    allCtrls = cmds.listRelatives(allCtrls,p=True)
    
    '''Remove duplicate parents'''
    
    allCtrls = list(dict.fromkeys(allCtrls))
    
    allFkCtrls = []
    allIkCtrls = []
    
    
    '''Modify all controls'''
    
    for i in allCtrls:
        if "ikfk" in i:
            ikFkCtrl = i
            cmds.addAttr(i, longName="IKFKSwitch",niceName="IK/FK Switch", attributeType='double',keyable=True, max=1, min=0) 
            pass
    
        elif "_fk" in i:
            allFkCtrls.append(i)   
             
        else:
            allIkCtrls.append(i) 
    
    
    for i in allFkCtrls:    
        cmds.connectAttr((f'{ikFkCtrl}.IKFKSwitch'), (f'{i}.visibility'))
        
    for i in allIkCtrls:
        myReverse=cmds.shadingNode ("reverse",asUtility=True) 
        cmds.connectAttr((f'{ikFkCtrl}.IKFKSwitch'), (f'{myReverse}.input.inputX.')) 
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{i}.visibility')) 
     
     
    
    '''Modify all joints''' 
    
    x=0
    
    for i in allResultJoints: 
    
        cmds.select(allIkJoints[x],allFkJoints[x],allResultJoints[x])
        cmds.orientConstraint()
        x+=1
    
    '''Connect Switch to Constraints'''
    
    x=0
    
    for i in allResultJoints:
    
        cmds.connectAttr((f'{ikFkCtrl}.IKFKSwitch'), (f'{i}_orientConstraint1.{allFkJoints[x]}W1'))
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{i}_orientConstraint1.{allIkJoints[x]}W0'))  
        x+=1




'''¤**************************************************CREATE CUSTOM JOINT CHAINS****************************************************'''



def buttonCustomJointChain(jointAmount=1,prefix="",name="",suffix="",jointDistance=20,jointOrientation="xyz"):
        
    cmds.select(clear=True)
    if name == "":
        name = "joint"
     
    x=""
    for i in range(jointAmount+1):
        
        if x == "":
            firstJoint = cmds.joint(n=(f"{prefix}{name}{x}{suffix}"),o=(0,0,0), p=(0,0,0))
            sP = cmds.xform(q = True, t = True, ws=True)
            x=0
            x+=1
        else:
            cmds.joint(n=(f"{prefix}{name}{x}{suffix}"),o=(0,0,0), p=(0,sP[1]+jointDistance,0))
            sP = cmds.xform(q = True, t = True, ws=True)
            x+=1
     
    cmds.joint( firstJoint, e=True, zso=True,ch=True,sao="zup", oj=jointOrientation )
    lastJoint = cmds.listRelatives(firstJoint,ad=True,fullPath=True)
    if lastJoint:
        cmds.delete(lastJoint[0])
            

    
'''¤**************************************************CREATE BASIC JOINTS****************************************************'''


def buttonLegJoints(take=1):
    
    mySelection = cmds.ls(sl = True, fl = True)
    if mySelection: 
        
        myEdgeCount = len(mySelection)
        myResult = [0,0,0]
        for item in mySelection:
            pos = cmds.xform(item, q = True, t = True)
            myResult[0] += pos[0]
            myResult[1] += pos[1]
            myResult[2] += pos[2]
        selectedPosition = [myResult[0]/myEdgeCount, myResult[1]/myEdgeCount, myResult[2]/myEdgeCount]
        
        cmds.select(clear=True)
    
    else:
        selectedPosition=[0.0,0.0,0.0]
    
    '''Create Left Leg'''
    upLeg = cmds.joint(n="l_result_UpLeg_jnt",o=(90.0,0.0,-90.0), p=(selectedPosition[0],selectedPosition[1],selectedPosition[2]))
    leg = cmds.joint(n="l_result_Leg_jnt",o=(0.0,0.0,0), p=(selectedPosition[0],selectedPosition[1]-30.0,selectedPosition[2]))
    legPos=cmds.getAttr(f"{leg}.translateX")
    foot = cmds.joint(n="l_result_Foot_jnt",o=(0,0,0), p=(legPos+60,0.0,0.0),r=True)
    toeBase = cmds.joint(n="l_result_ToeBase_jnt",o=(0,0,0), p=(20,0.0,0.0),r=True) 
    toeEnd = cmds.joint(n="l_result_ToeEnd_jnt",o=(0,0,0), p=(10,0.0,0.0),r=True)
    
    if cmds.objExists('leftLeg_result_grp'):
        cmds.parent( upLeg,'leftLeg_result_grp')
    
 
'''Create Center Joints''' 
    
def buttonCenterJoints(jointAmount=4):
    
    mySelection = cmds.ls(sl = True, fl = True)
    
    if mySelection:
        myEdgeCount = len(mySelection)
        myResult = [0,0,0]
        for item in mySelection:
            pos = cmds.xform(item, q = True, t = True)
            myResult[0] += pos[0]
            myResult[1] += pos[1]
            myResult[2] += pos[2]
        selectedPosition = [myResult[0]/myEdgeCount, myResult[1]/myEdgeCount, myResult[2]/myEdgeCount]
        
        cmds.select(clear=True)
    
    else:
        selectedPosition=[0.0,0.0,0.0]
    
    jointAmount -= 3
    
    Hips = cmds.joint(n="c_Hips_jnt",o=(0.0,0.0,0.0), p=(0.0,selectedPosition[1],0.0))
    sP = cmds.xform(q = True, t = True, ws=True)
    x=""
    for i in range(jointAmount):
        Spine = cmds.joint(n=(f"c_Spine{x}_jnt"),o=(0,0,0), p=(0.0,sP[1]+40.0,0.0))
        sP = cmds.xform(q = True, t = True, ws=True)
        if x == "":
            x=0
            x+=1
        else:    
            x+=1
    
    if jointAmount > 1:
            Neck = cmds.joint(n="c_Neck_jnt",o=(0,0,0), p=(0.0,sP[1]+40,0.0))
            sP = cmds.xform(q = True, t = True, ws=True)
            
    Head = cmds.joint(n="c_Head_jnt",o=(0,0,0), p=(0.0,sP[1]+40,0.0))
    sP = cmds.xform(q = True, t = True, ws=True)
    HeadEnd = cmds.joint(n="c_Head_end",o=(0,0,0), p=(0.0,sP[1]+40,0.0))
    sP = cmds.xform(q = True, t = True, ws=True)
               
    
    if cmds.objExists('CENTER_JOINTS'):
        cmds.parent( Hips,'CENTER_JOINTS')
    

    

def buttonArmJoints(take=1):
    
    mySelection = cmds.ls(sl = True, fl = True)
    
    if mySelection:
        myEdgeCount = len(mySelection)
        myResult = [0,0,0]
        for item in mySelection:
            pos = cmds.xform(item, q = True, t = True)
            myResult[0] += pos[0]
            myResult[1] += pos[1]
            myResult[2] += pos[2]
        selectedPosition = [myResult[0]/myEdgeCount, myResult[1]/myEdgeCount, myResult[2]/myEdgeCount]
        
        cmds.select(clear=True)
        
    else:
        selectedPosition=[0.0,0.0,0.0]
    
    
    '''Create Arm'''
    shoulder = cmds.joint(n="l_result_Shoulder_jnt",o=(0.0,0.0,0.0), p=(selectedPosition[0],selectedPosition[1],selectedPosition[2]))
    arm = cmds.joint(n="l_result_Arm_jnt",o=(0.0,0.0,0), p=(selectedPosition[0]+15.0,selectedPosition[1],selectedPosition[2]))
    foreArm = cmds.joint(n="l_result_ForeArm_jnt",o=(0.0,0.0,0), p=(selectedPosition[0]+45.0,selectedPosition[1],selectedPosition[2]))
    hand = cmds.joint(n="l_result_Hand_jnt",o=(0.0,0.0,0), p=(selectedPosition[0]+72.0,selectedPosition[1],selectedPosition[2]))
    thumb = cmds.joint(n="l_result_Thumb_jnt",o=(90.0,-43.0,-20.0), p=(selectedPosition[0]+77.0,selectedPosition[1]-2.5,selectedPosition[2]+5.5))
    thumb1 = cmds.joint(n="l_result_Thumb1_jnt",o=(0.0,0.0,0.0), p=(8.0,0.0,0.0), r=True)
    thumb2 = cmds.joint(n="l_result_Thumb2_jnt",o=(0.0,0.0,0.0), p=(6.0,0.0,0.0), r=True)
    cmds.select(hand)
    inHand = cmds.joint(n="l_result_inHand_jnt",o=(0.0,0.0,0.0), p=(selectedPosition[0]+81.5,selectedPosition[1],selectedPosition[2]-5.5))
    cmds.select(hand)
    index = cmds.joint(n="l_result_Index_jnt",o=(0.0,0.0,0.0), p=(selectedPosition[0]+91.0,selectedPosition[1],selectedPosition[2]))
    index1 = cmds.joint(n="l_result_Index1_jnt",o=(0.0,0.0,0.0), p=(6.0,0.0,0.0), r=True)
    index2 = cmds.joint(n="l_result_Index2_jnt",o=(0.0,0.0,0.0), p=(6.0,0.0,0.0), r=True)
    
    if cmds.objExists('leftArm_result_grp'):
        cmds.parent( shoulder,'leftArm_result_grp')


'''¤***********************************************CREATE NURB SHAPES***********************************************'''

def createSkullNurb(variant="Skull",rotation="0"):

    '''SKULL AND IK/FK SWITCH'''
    '''Create Text and Convert to Nurb'''
    
    if variant == "Skull":
        
        topGroup = cmds.textCurves( f='Wingdings',t='N' )
        cmds.warning()
        print ('')
        createdNurbTopGroup = cmds.listRelatives(topGroup)
        cmds.parent(createdNurbTopGroup, w=True)
        cmds.delete(topGroup)
        
    else:
        topGroup = cmds.textCurves( f='Times-Roman', t='IK/FK' )
        createdNurbTopGroup = cmds.listRelatives(topGroup)
        cmds.parent(createdNurbTopGroup, w=True)
        cmds.delete(topGroup)
            
    '''Sort between shapes and parents'''
    
    createdNurbParent = cmds.listRelatives(createdNurbTopGroup , fullPath=True)[1]
    
    if variant == "Skull":
    
        createdNurbParent = cmds.listRelatives(createdNurbTopGroup , fullPath=True)[1]
        redundantNurb = cmds.listRelatives(createdNurbTopGroup , fullPath=True)[2]
        cmds.delete(redundantNurb)
                
    
    else: 
        pass
            
    createdNurbShapes = cmds.listRelatives(createdNurbTopGroup , fullPath=True, ad=True)
    nurbParentToAllShapes = createdNurbShapes[1]
    createdNurbParents = []
    
    for nurb in createdNurbShapes: 
    
        if "Shape" in nurb:
            pass
        else:
            createdNurbParents.append(nurb)
            createdNurbShapes.remove(nurb)
    
    '''Final cleanup so that we get the Nurb Parent with all child shapes alone and name it with a better name and center Pivot'''
    
    createdNurbParents.remove(nurbParentToAllShapes)
    createdNurbShapes = createdNurbShapes[1:]
    cmds.select(createdNurbShapes, nurbParentToAllShapes)
    cmds.parent(r=True, s=True)    
    cmds.delete(createdNurbParents)
    cmds.parent(nurbParentToAllShapes, w=True)
    cmds.delete(createdNurbTopGroup)
    if variant == "Skull":
    
        cmds.rename("Skull")
    else: 
        cmds.rename("IKFK_Switch")
      
    mel.eval("manipPivotReset true true;")
    
    '''Give it 1.5 Thickness'''
    
    myListParent = cmds.ls(selection=True)
    myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
    x=0
    cmds.select(clear=True)
    for item in myList:
    
        cmds.setAttr (f"{item}.lineWidth", 1.5)
        x += 1
         
    cmds.select(myListParent)        
    cmds.move (0, 0, 0,rpr=True )
    if variant == "Skull":
        cmds.scale(18.4,18.4,18.4)
    else:
        cmds.rotate(0,rotation,0)
        cmds.scale(0.5,0.5,0.5)
        
    cmds.makeIdentity (myListParent, apply = True,t=1,r=1,s=1,n=2)
    

def createMasterNurb():
    
    '''MASTER CONTROL'''
    '''Create Curve'''

    Line = mel.eval("curve -d 1 -p 36 0 0 -p 24 0 12 -p 24 0 6 -p 12 0 6 -p 6 0 12 -p 6 0 24 -p 12 0 24 -p 0 0 36 -p -12 0 24 -p -6 0 24 -p -6 0 12 -p -12 0 6 -p -24 0 6 -p -24 0 12 -p -36 0 0 -p -24 0 -12 -p -24 0 -6 -p -12 0 -6 -p -6 0 -12 -p -6 0 -24 -p -12 0 -24 -p 0 0 -36 -p 12 0 -24 -p 6 0 -24 -p 6 0 -12 -p 12 0 -6 -p 24 0 -6 -p 24 0 -12 -p 36 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 ;")
    cmds.rename("Four_Way_Arrow")
    
    '''Give it 2 Thickness'''
    
    myListParent = cmds.ls(selection=True)
    myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
    x=0
    cmds.select(clear=True)
    for item in myList:
    
        cmds.setAttr (f"{item}.lineWidth", 2)
        x += 1
        
    

    
def createPoleVector():    
        
    poleVector = cmds.circle(name=f'Orb', r=6)
    poleVectorCircle2 = cmds.circle(name='circle2', r=6)
    cmds.rotate(0,90,0)
    cmds.makeIdentity (poleVectorCircle2, apply = True,t=1,r=1,s=1,n=2)
    poleVectorCircle3 = cmds.circle(name='circle3', r=6)
    cmds.rotate(90,90,0)
    cmds.makeIdentity (poleVectorCircle3, apply = True,t=1,r=1,s=1,n=2)
    
    poleVectorParent = cmds.listRelatives(poleVector, fullPath=True, ad=True)
    poleVectorCircleShape2 = cmds.listRelatives(poleVectorCircle2, fullPath=True, ad=True)[0]
    poleVectorCircleShape3 = cmds.listRelatives(poleVectorCircle3, fullPath=True, ad=True)[0]    
            
    cmds.select(poleVectorCircleShape3,poleVectorCircleShape2, poleVector)
    cmds.parent(r=True, s=True)        
    cmds.delete(poleVectorCircle2[0],poleVectorCircle3[0])   
    cmds.select(poleVector)    
    
    '''Give it 1.5 Thickness'''
        
    myListParent = cmds.ls(selection=True)
    myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
    cmds.select(clear=True)
    for item in myList:
        
        cmds.setAttr (f"{item}.lineWidth", 1.5)  

    
def createSquare():
    
    square=cmds.circle(name='Square', r=10)
    mel.eval(f"setAttr {square[1]}.degree 1;")
    mel.eval(f"setAttr {square[1]}.sections 4;")
    cmds.rotate(90,45,0)
    myListParent = cmds.ls(selection=True)
    myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
    cmds.select(clear=True)
    for item in myList:
        
        cmds.setAttr (f"{item}.lineWidth", 1.5)  
    cmds.makeIdentity (square, apply = True,t=1,r=1,s=1,n=2)
    
    
def CreateArrow(nurbName="Arrow"): 
   
    RootMotionCtrl = cmds.curve(name=nurbName, p=[(150, 0, 150), (50, 0, 50),(100, 0, 50),(100, 0, -200), (200, 0, -200),(200, 0, 50),(250, 0, 50),(150, 0, 150)],d=1, k=[0,1,2,3,4,5,6,7] )
    mel.eval("manipPivotReset true true;")
    cmds.move (0, 0, 0,rpr=True )    
    myListParent = cmds.ls(selection=True)
    myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
    cmds.scale(0.08,0.15,0.2)
    cmds.select(clear=True)
    for item in myList:
        
        cmds.setAttr (f"{item}.lineWidth", 1.5)  
        cmds.makeIdentity (RootMotionCtrl, apply = True,t=1,r=1,s=1,n=2)
    cmds.select(RootMotionCtrl)
    

def createBentArrowNurb():

    arrowHead1 = mel.eval('curve -d 1 -p 14 0 6 -p 12 0 6 -p 16 0 10 -p 20 0 6 -p 18 0 6 -k 0 -k 1 -k 2 -k 3 -k 4 ;')
    arrowHead2 = mel.eval('curve -d 1 -p 24 0 -4 -p 24 0 -6 -p 28 0 -2 -p 24 0 2 -p 24 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 ;')
    outerCurve = mel.eval('curve -d 3 -p 14 0 6 -p 14 0 2 -p 16 0 0 -p 18 0 -2 -p 20 0 -4 -p 24 0 -4 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 3 -k 3 ;')
    innerCurve = mel.eval('curve -d 3 -p 18 0 6 -p 18 0 4 -p 20 0 2 -p 22 0 0 -p 24 0 0 -k 0 -k 0 -k 0 -k 1 -k 2 -k 2 -k 2 ;')
    cmds.select(f'{innerCurve}.cv[2]')
    mel.eval('move -r -1.314892 0.0 -1.274143 ;')
    cmds.select(f'{outerCurve}.cv[2:3]')
    mel.eval('move -r -0.957555 0.0 -0.895802 ;')
    
    nurbList=[]
    nurbList.append(arrowHead1)
    nurbList.append(arrowHead2)
    nurbList.append(outerCurve)
    nurbList.append(innerCurve)
    
    '''Create the variables'''
    nurbParent=nurbList[0]
    nurbParentShape=cmds.listRelatives(nurbParent, fullPath=True, shapes=True)[0]
    nurbChild1=nurbList[1]
    nurbChildShape1=cmds.listRelatives(nurbChild1, fullPath=True,shapes=True)
    nurbChild2=nurbList[2]
    nurbChildShape2=cmds.listRelatives(nurbChild2, fullPath=True,shapes=True)
    nurbChild3=nurbList[3]
    nurbChildShape3=cmds.listRelatives(nurbChild3, fullPath=True,shapes=True)
    
    
    '''Merge the Nurbs'''
    cmds.select(clear=True)
    cmds.select(nurbChildShape1, nurbParent)
    cmds.parent(r=True, s=True)
    cmds.select(clear=True)
    cmds.select(nurbChildShape2, nurbParent)
    cmds.parent(r=True, s=True)
    cmds.select(clear=True)
    cmds.select(nurbChildShape3, nurbParent)
    cmds.parent(r=True, s=True)
    
    '''Delete all but shapes and move pivot'''
    
    cmds.delete(nurbChild1,nurbChild2,nurbChild3)
    cmds.select(nurbParent)
    cmds.move (0, 0, 25, (f'{nurbParent}.scalePivot'),(f'{nurbParent}.rotatePivot'),rpr=True)
    cmds.scale (0.8, 0.8, 0.8)
    cmds.move (0, 0, 0,rpr=True )
    cmds.makeIdentity (nurbParent, apply = True)
    myListParent = cmds.ls(selection=True)
    myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
    cmds.select(clear=True)
    for item in myList:
        
        cmds.setAttr (f"{item}.lineWidth", 1.5)  
    cmds.makeIdentity (nurbParent, apply = True,t=1,r=1,s=1,n=2)
    
    
    cmds.select(nurbParent)    
    mel.eval("manipPivotReset true true;")
    
    cmds.rename("BentArrow")

'''¤**************************************************CREATE REFERENCE SKELETON****************************************************'''

def createReference():

    allJoints = cmds.ls(typ="joint")
    nonResult = []
    
    for i in allJoints:
        if "fk" in i:
            nonResult.append(i)
        if "ik" in i:
            nonResult.append(i)
                
    allJoints = [x for x in allJoints if x not in nonResult]      
    
    resultSelection = [] 
    
    for target in allJoints:
        parent = None
        stop = False
        
        while not stop:
            p = cmds.listRelatives(parent or target, parent=True)
            if p is None:
                stop = True
            else:
                parent = p[0]
          
        if parent:
            pass
        else:
            resultSelection.append(target)
    
    '''Sort the Result Joints so that we get them seperate and unselect everything else'''    
    if resultSelection:
        pass
    else:
        for i in allJoints:
            parentType = cmds.listRelatives(i,p=True)
            if cmds.objectType( parentType, isType='transform' ):
                resultSelection.append(i)
        
    
    cmds.select(resultSelection)
    resultSkeleton = cmds.listRelatives(resultSelection, ad=True, fullPath=True,typ="joint")   
    
    for i in resultSelection:
        resultSkeleton.append(i) 
    
    cmds.duplicate()
    
    worldIsParent = cmds.listRelatives(p=True)
    if worldIsParent:
        cmds.parent(w=True) 
    else:   
        pass
        
        
    '''Sort the Reference Joints so that we get them seperate and delete everything else'''    
        
    referenceSelection=cmds.ls(sl=True)
    referenceSelectionNoneJoints = cmds.listRelatives(referenceSelection, ad=True, fullPath=True)
    
    for i in referenceSelection:
        referenceSelectionNoneJoints.append(i) 
    
    referenceSkeleton = cmds.listRelatives(referenceSelection, ad=True, fullPath=True,typ="joint")
    
    for i in referenceSelection:
        referenceSkeleton.append(i) 
    
    
    referenceSelectionNoneJoints = [x for x in referenceSelectionNoneJoints if x not in referenceSkeleton]       
    if referenceSelectionNoneJoints:
        cmds.delete(referenceSelectionNoneJoints)
    
    
    '''Create the Arrow Nurb'''
    
    CreateArrow(nurbName='RootMotion_ctrl')
    arrowNurb=cmds.ls(sl=True)
    myList = cmds.listRelatives(arrowNurb, ad=True, fullPath=True)
    x=0
    cmds.select(clear=True)
    
    for item in myList:
    
        cmds.setAttr (f"{item}.overrideEnabled", 1)
        cmds.setAttr (f"{item}.overrideColor", 17)
        x += 1
    
    
    if cmds.objExists("RIGG"):    
        cmds.parent(arrowNurb,"RIGG")
        
    cmds.select(clear=True)
    referenceJoint = cmds.joint (name= "Reference",p= [0, 0, 0])
    cmds.parentConstraint (arrowNurb, referenceJoint)  
    cmds.setAttr (f"{referenceJoint}.drawStyle", 2)
    cmds.parent(referenceSelection,referenceJoint)
    allReferenceJoints = cmds.listRelatives(referenceJoint, ad=True)
    allReferenceJointsRealPath = cmds.listRelatives(referenceJoint, ad=True,fullPath=True)
    
    '''Rename all the Joints'''
    
    x=0
    
    for i in allReferenceJoints:
        
        if "l_" in i:
            newName = allReferenceJoints[x].replace("l_", "Left")
        else:  
            newName = allReferenceJoints[x].replace("r_", "Right")   
            newName = newName.replace("ShouldeRightjnt", "Shoulder")   
        newName = newName.replace("c_", "")
        newName = newName.replace("_jnt", "")
        newName = newName.replace("result_", "")
        newName = newName.replace("result_", "")
        cmds.rename( allReferenceJointsRealPath[x], newName )
        x+=1    
        
    
    '''Remove Primary 1:s'''
    
    x=0
    
    jointsWithNumbers = cmds.listRelatives(referenceJoint)
    jointsWithNumbersRealPath = cmds.listRelatives(referenceJoint,fullPath=True)
    
    for i in jointsWithNumbers:
        
        newName = jointsWithNumbers[x].replace("1", "")
        cmds.rename( jointsWithNumbersRealPath[x], newName )
        x+=1    
        
        
    '''Update the Variables with the correct names'''   
     
    cmds.select(referenceJoint)
    referenceSelection=cmds.ls(sl=True)
    referenceSelection = cmds.listRelatives(referenceSelection, fullPath=True,typ="joint")   
    referenceSkeleton = cmds.listRelatives(referenceSelection, ad=True, fullPath=True,typ="joint")
    
    for i in referenceSelection:
        referenceSkeleton.append(i) 
    
    referenceSelectionNoneJoints = [x for x in referenceSelectionNoneJoints if x not in referenceSkeleton]         
    
    
    for i in range(len(referenceSkeleton)):
        cmds.parentConstraint(resultSkeleton[i],referenceSkeleton[i])
     
    
    
    for i in range(25, 0, -1):
        
        if i == 1:
            i = ""
            if cmds.objExists(f'Spine{i}'):
                spine2 = (f'Spine{i}') 
                break
            
        if cmds.objExists(f'Spine{i}'):
            spine2 = (f'Spine{i}') 
            break
            
        else:
            pass
    
    
    if cmds.objExists("LeftShoulder"):              
        cmds.parent("LeftShoulder", spine2)
    if cmds.objExists("RightShoulder"):              
        cmds.parent("RightShoulder", spine2)    
    if cmds.objExists("LeftUpLeg"):              
        if cmds.objExists("Hips"):              
            cmds.parent("LeftUpLeg", "Hips")
    if cmds.objExists("RightUpLeg"):              
        if cmds.objExists("Hips"):              
            cmds.parent("RightUpLeg", "Hips")


'''¤***********************************************CREATE SINGLE FK CONTROL***********************************************'''


def CreateSingleFkCtrl():
    
    selectedJoint = cmds.ls(sl=True)
    
    if selectedJoint:
        
        selectedJoint = selectedJoint[0]   
            
        if "jnt" in selectedJoint:
            
            selectedJointName=selectedJoint.replace("_jnt", "")
                
        else:
            selectedJointName=selectedJoint
            
        selectedJoint = cmds.ls(sl=True)
        selectedJoint = selectedJoint[0]    
        try:   
            cmds.makeIdentity (apply = True,t=1,r=1,s=1,n=2)
        except:
            pass
        cmds.circle(name=f'{selectedJointName}_ctrl')
        selectedJointFixGrp = cmds.group(name=f'{selectedJointName}_fixGrp')
        cmds.select(f'{selectedJoint}', add=True)
        cmds.matchTransform()
        cmds.select(f'{selectedJointName}_ctrl')
        cmds.scale(5,5,1, r=True)
        cmds.makeIdentity (apply = True,t=1,r=1,s=1,n=2)
        cmds.select(f'{selectedJoint}', add=True)
        cmds.orientConstraint( f'{selectedJointName}_ctrl', f'{selectedJoint}', maintainOffset=False)
    
    
    else:   
        cmds.inViewMessage( amg='<hl>Please select a joint</hl>.', pos='midCenter', fade=True, ck=True )


'''¤***********************************************CREATE FK CHAIN***********************************************'''

def CreateFkChain():

    selectedJoint = cmds.ls(sl=True)
    
    if selectedJoint:
        jointChildren = cmds.listRelatives(selectedJoint,ad=True)
        jointChildren.append(selectedJoint[0])
        jointChildren.reverse()
        
        for i in jointChildren:
            if "end" in i:
                
                endPos = cmds.xform(i, q = True, t = True)
                jointChildren.remove(i)
        
        cmds.pickWalk( direction='up' )
          
        myGrpList = []
        circleList = []
        
        for current_joint in jointChildren:
            
            
            if "|" in current_joint:
                
                current_joint = (f"{current_joint[1:]}")       
    
            
            else:
                pass  
            
            
            if "jnt" in current_joint:
    
                current_jointName=current_joint.replace("_jnt", "")
                
            else:
                pass
    
            circleList.append(cmds.circle(name=f'{current_jointName}_ctrl'))
            myGrpList.append(cmds.group(name=f'{current_jointName}_fixGrp'))
            cmds.select(f'{current_joint}', add=True)
            cmds.matchTransform()
            cmds.select(f'{current_jointName}_ctrl')
                
            myListParent = cmds.ls(selection=True)
            myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
            x=0
            cmds.select(clear=True)
            
            for item in myList:
            
                cmds.setAttr (f"{item}.lineWidth", 1.5)
                x += 1
    
            cmds.select(f'{current_jointName}_ctrl')
            cmds.scale(5,5,5, r=True)
            cmds.makeIdentity(apply=True)
            cmds.select(clear=True)
            cmds.select(f'{current_joint}', add=True)
            cmds.makeIdentity(apply=True)
            cmds.orientConstraint( f'{current_jointName}_ctrl', f'{current_joint}', maintainOffset=False)
    
    
        for i in reversed(range(len(jointChildren))):
            if (i != 0):
         
                cmds.parentConstraint(jointChildren[i-1], myGrpList[i], mo=True)
       

    else:   
        cmds.inViewMessage( amg='<hl>Please select the top joint of the chain</hl>.', pos='midCenter', fade=True, ck=True ) 
        
'''¤***********************************************CREATE FINGER CURLS***********************************************'''


def createNeedle(defaultName="Needle", rotation=90):
    
    '''Create Nurbs'''
    Line=cmds.curve(name=defaultName, p=[(0, 0, 0), (0, 0, 25)], d=1, k=[0,1] )
    cmds.makeIdentity (Line, apply = True)
    Circle1=cmds.circle(r=4)
    cmds.makeIdentity (Circle1, apply = True)
    Circle2=cmds.circle(r=4)
    cmds.rotate(0,90,0)
    cmds.makeIdentity (Circle2, apply = True)
    Circle3=cmds.circle(r=4)
    cmds.rotate(90,0,0)
    cmds.makeIdentity (Circle3, apply = True)
    
    nurbList=[]
    nurbList.append(Line)
    nurbList.append(Circle1[0])
    nurbList.append(Circle2[0])
    nurbList.append(Circle3[0])
    
    '''Create the variables'''
    nurbParent=nurbList[0]
    nurbParentShape=cmds.listRelatives(nurbParent, fullPath=True, shapes=True)[0]
    nurbChild1=nurbList[1]
    nurbChildShape1=cmds.listRelatives(nurbChild1, fullPath=True,shapes=True)
    nurbChild2=nurbList[2]
    nurbChildShape2=cmds.listRelatives(nurbChild2, fullPath=True,shapes=True)
    nurbChild3=nurbList[3]
    nurbChildShape3=cmds.listRelatives(nurbChild3, fullPath=True,shapes=True)
    
    
    '''Merge the Nurbs'''
    cmds.select(clear=True)
    cmds.select(nurbChildShape1, nurbParent)
    cmds.parent(r=True, s=True)
    cmds.select(clear=True)
    cmds.select(nurbChildShape2, nurbParent)
    cmds.parent(r=True, s=True)
    cmds.select(clear=True)
    cmds.select(nurbChildShape3, nurbParent)
    cmds.parent(r=True, s=True)
    
    '''Delete all but shapes and move pivot'''
    
    cmds.delete(nurbChild1,nurbChild2,nurbChild3)
    cmds.select(nurbParent)
    cmds.move (0, 0, 25, (f'{nurbParent}.scalePivot'),(f'{nurbParent}.rotatePivot'),rpr=True)
    cmds.rotate (rotation, 0, 0)
    cmds.scale (0.2, 0.2, 0.2)
    cmds.move (0, 0, 0,rpr=True )
    cmds.makeIdentity (nurbParent, apply = True)

def createFingerCurls():
    
    allSelectedObjects = cmds.ls(selection=True)
    myinHandfixGrpList=[]
    
    if len(allSelectedObjects) > 1:
    
        selectedJoints = cmds.ls(selection=True, type='joint' )
        resultHand=selectedJoints[0]
        allSelectedObjects.remove(selectedJoints[0])
        selectedJoints=cmds.listRelatives(selectedJoints,type='joint')
        selectedJointsinHand=[]
        
        for i in selectedJoints:
            if "inHand" in i:
                inHandChildren=cmds.listRelatives(i,type='joint')
                inHandJoint = i
                selectedJoints.remove(i)
                if inHandChildren:
                    for j in inHandChildren:
                        selectedJoints.append(j)
                        selectedJointsinHand.append(j)
        
        cmds.makeIdentity (selectedJoints, apply = True)
            
        x=0
        runOnce=0
        
        ctrlGroup=selectedJoints[0]
        
        if "l" == ctrlGroup[0]:
            
                    side="LEFT"
                    ctrlGroup=cmds.group(name=f'LEFT_HAND_CTRLS', em=True)
                
        
        else:
                    side="RIGHT"
                    ctrlGroup=cmds.group(name=f'RIGHT_HAND_CTRLS', em=True)  
        
        
        for selectedJoint in selectedJoints:
          
            x+=1
                
            
            jointChildren = cmds.listRelatives(selectedJoint,ad=True)
            jointChildren.append(selectedJoint)
            jointChildren.reverse()
            cmds.pickWalk( direction='up' )
            
            myGrpList = []
            mySdkList = []
            circleList = []
            sdk = 0
            
            for current_joint in jointChildren:
                
                current_jointOrgName=current_joint
                
               
                if "jnt3" in current_joint:
                    current_joint=current_joint.replace("_jnt2", "")
                if "jnt2" in current_joint:
                    current_joint=current_joint.replace("_jnt2", "")
                if "jnt1" in current_joint:
                    current_joint=current_joint.replace("_jnt1", "")
                if "jnt" in current_joint:
                    current_joint=current_joint.replace("_jnt", "")
                
                if "l" == current_joint[0]:
                    createNeedle(f'{current_joint}_ctrl')
                    
                    '''Color Nurbs'''
                    
                    myList = (f'{current_joint}_ctrl')
                    myList = cmds.listRelatives(myList, ad=True, fullPath=True)
                    for item in myList:
                    
                        cmds.setAttr (f"{item}.overrideEnabled", 1)
                        cmds.setAttr (f"{item}.overrideColor", 6)
                        cmds.setAttr (f"{item}.lineWidth", 1.5)
                      
                
                else:
                    createNeedle(f'{current_joint}_ctrl',270)  
                    
                    '''Color Nurbs'''
                    
                    myList = (f'{current_joint}_ctrl')
                    myList = cmds.listRelatives(myList, ad=True, fullPath=True)
                    for item in myList:
                    
                        cmds.setAttr (f"{item}.overrideEnabled", 1)
                        cmds.setAttr (f"{item}.overrideColor", 13)
                        cmds.setAttr (f"{item}.lineWidth", 1.5)
        
                circleList.append(f'{current_joint}_ctrl')
                mySdkList.append(cmds.group(name=f'{current_joint}_sdk',p=ctrlGroup))
                fixGrp = (cmds.group(name=f'{current_joint}_fixGrp'))
                
                myGrpList.append(fixGrp)
                
                if current_jointOrgName in selectedJointsinHand:
                    myinHandfixGrpList.append(fixGrp)
                
                selectedObjectAttr = cmds.listAttr(allSelectedObjects, r=True, s=True )
                    
                if selectedJoint in selectedObjectAttr:
                    pass
                
                else:
                    selectedJoint=selectedJoint[2:]
                    cmds.addAttr(allSelectedObjects, longName=selectedJoint,niceName=(f"{selectedJoint} Curl"), attributeType='double',keyable=True, max=25, min=-65)
           
                        
                if "|" in mySdkList:
                    
                    mySdkList = (f"{mySdkList[1:]}")       
        
                
                else:
                    pass    
              
                cmds.connectAttr((f'{allSelectedObjects[0]}.{selectedJoint}'), (f'{current_joint}_sdk.rotateZ'))
                
                if "thumb" in selectedJoint or "Thumb" in selectedJoint and runOnce==0:
                    
                    runOnce=1
                    myMultiply=cmds.shadingNode ("multiplyDivide",asUtility=True) 
                    cmds.connectAttr((f'{allSelectedObjects[0]}.{selectedJoint}'), (f'{myMultiply}.input1.input1Z.'))   
                    cmds.disconnectAttr((f'{allSelectedObjects[0]}.{selectedJoint}'), (f'{current_joint}_sdk.rotateZ'))
                    cmds.connectAttr((f'{myMultiply}.output.outputZ'),(f'{current_joint}_sdk.rotateZ'))
                    cmds.setAttr((f'{myMultiply}.input2Z'), 0.5)
        
                else:
                    pass   
                
                
                sdk += 1
                
                cmds.select(f'{current_joint}_fixGrp')
                cmds.select(f'{current_jointOrgName}', add=True)
                cmds.matchTransform()
                cmds.select(f'{current_joint}_ctrl')
                cmds.select(f'{current_jointOrgName}', add=True)
                cmds.matchTransform()
                cmds.select(f'{current_joint}_ctrl')
                cmds.makeIdentity(apply=True)
                cmds.orientConstraint( f'{current_joint}_ctrl', f'{current_jointOrgName}', maintainOffset=False)
        
                    
        
        
            for i in reversed(range(len(jointChildren))):
                if (i != 0):
                    cmds.parentConstraint(jointChildren[i-1], myGrpList[i], mo=True)
                    
             
             

        if cmds.objExists(f"{side}_ARM_CTRLS"):
                cmds.parent(f"{side}_HAND_CTRLS",f"{side}_ARM_CTRLS")   
                

        fingerParents = cmds.listRelatives(ctrlGroup)
        for i in fingerParents:
            if "1" in i:
                fingerParents.remove(i)         
        for i in fingerParents:
            if "2" in i:
                fingerParents.remove(i)         
        for i in fingerParents:
            if i in myinHandfixGrpList:
                pass
            else:
                cmds.parentConstraint(resultHand, i, mo=True)
            
        '''Create the inHand Control and Modify it'''
        
        if side == "LEFT":
            sidePrefix="l"
        else:
            sidePrefix="r"

        if cmds.objExists(f'{sidePrefix}_result_inHand_jnt'): 
            cmds.select(inHandJoint)
    
            if "jnt3" in inHandJoint:
                inHandJointName=inHandJoint.replace("_jnt2", "")
            if "jnt2" in inHandJoint:
                inHandJointName=inHandJoint.replace("_jnt2", "")
            if "jnt1" in inHandJoint:
                inHandJointName=inHandJoint.replace("_jnt1", "")
            if "jnt" in inHandJoint:
                inHandJointName=inHandJoint.replace("_jnt", "")    
    
            createBentArrowNurb()
            
            if "l" == current_joint[0]:
                cmds.rotate (0, 46, 270)
            else:   
                cmds.rotate (0, 46, 90) 
    
            cmds.makeIdentity(apply=True)
            
            cmds.rename((f'{inHandJointName}_ctrl'))
            inHandNurb=cmds.ls(sl=True)
            
                                
            '''Color the inHand Control'''
            
            myList = (f'{inHandJointName}_ctrl')
            myList = cmds.listRelatives(myList, ad=True, fullPath=True)
            for item in myList:
            
                cmds.setAttr (f"{item}.overrideEnabled", 1)
                if "l" == current_joint[0]:
                    cmds.setAttr (f"{item}.overrideColor", 6)
                else:   
                    cmds.setAttr (f"{item}.overrideColor", 13) 
                    
                cmds.setAttr (f"{item}.lineWidth", 1.5)
            
            inHandfixGrp=cmds.group(inHandNurb,name=f'{inHandJointName}_fixGrp',p=ctrlGroup)    
            
            '''Match Transform and constraint'''
            
            cmds.select(f'{inHandJointName}_fixGrp')
            cmds.select(f'{inHandJoint}', add=True)
            cmds.matchTransform()
            cmds.select(f'{inHandJointName}_ctrl')
            cmds.select(f'{inHandJoint}', add=True)
            cmds.matchTransform()
            cmds.select(f'{inHandJointName}_ctrl')
            cmds.makeIdentity(apply=True)
    
            cmds.orientConstraint( f'{inHandJointName}_ctrl', f'{inHandJoint}', maintainOffset=False) 
            cmds.parentConstraint(resultHand, (f'{inHandJointName}_fixGrp'), mo=True)
            
            for i in myinHandfixGrpList:
                cmds.parentConstraint(inHandJoint, (f'{i}'), mo=True)    
                
             
    
    else:   
        cmds.inViewMessage( amg='<hl>Please select the IK/FK Switch and the result hand joint</hl>.', pos='midCenter', fade=True, ck=True ) 
    
    
    
'''¤**************************************************CREATE LEG FUNCTIONS****************************************************'''   


def createLegFunctions():    
      
    '''Create the IK Leg'''
    
    resultLeg=cmds.ls(sl=True)
    if resultLeg:
        
        sideCheck=cmds.ls(sl=True)
        cmds.makeIdentity (sideCheck, apply = True,t=1,r=1,s=1,n=2)
        sideCheck=sideCheck[0]
                
        myIKLeg = cmds.duplicate()
        
        if "l" in sideCheck[0]:
                    
                    side="l"
                    nurbColor=6
                    if cmds.objExists('leftLeg_ik_grp'):
                        cmds.parent( myIKLeg[0],'leftLeg_ik_grp')
        
        else:
                    side="r" 
                    nurbColor=13
                    if cmds.objExists('rightLeg_ik_grp'):
                        cmds.parent( myIKLeg[0],'rightLeg_ik_grp')
                
        myIKLeg=cmds.ls(sl=True)
        
        for i in core.ls(sl = True, dag = True):
            
            myJointName = i.nodeName().replace("result", "ik")
            core.rename(i, myJointName)
            myJointName = i.nodeName().replace("jnt1", "jnt")
            core.rename(i, myJointName)
            
        ikUpLeg = cmds.ls(sl=True)
        myIKJoints=cmds.listRelatives(ikUpLeg, ad=True,fullPath=True)
        ikUpLeg = ikUpLeg[0]
        ikLeg = myIKJoints[3]
        ikFoot = myIKJoints[2]    
        ikToeBase = myIKJoints[1]
        ikToeEnd = myIKJoints[0]
                               
        
        ikHandleAnkle = cmds.ikHandle(name=(f"{side}_poleVectorTarget"),startJoint = ikUpLeg, endEffector = ikFoot, createCurve = 0, simplifyCurve = 0, rootOnCurve = 0, parentCurve = 0, sol="ikRPsolver")
        mel.eval("toggleVisibilityAndKeepSelection `optionVar -query toggleVisibilityAndKeepSelectionBehaviour`;")
        ikHandleBall = cmds.ikHandle(startJoint = ikFoot, endEffector = ikToeBase, createCurve = 0, simplifyCurve = 0, rootOnCurve = 0, parentCurve = 0, sol="ikSCsolver")
        mel.eval("toggleVisibilityAndKeepSelection `optionVar -query toggleVisibilityAndKeepSelectionBehaviour`;")
        ikHandleToe = cmds.ikHandle(startJoint = ikToeBase, endEffector = ikToeEnd, createCurve = 0, simplifyCurve = 0, rootOnCurve = 0, parentCurve = 0, sol="ikSCsolver")
        mel.eval("toggleVisibilityAndKeepSelection `optionVar -query toggleVisibilityAndKeepSelectionBehaviour`;")
    
        '''Create the Groups and Move Them'''
        
        
        onToeGroup=cmds.group(n=(f"{side}_onToe_grp"), empty=True)    
        cmds.matchTransform(onToeGroup,ikToeEnd)
        cmds.makeIdentity( onToeGroup, apply=True, t=1, r=1, s=1, n=2 )
        onBallGroup=cmds.group(n=(f"{side}_onBall_grp"), empty=True)    
        cmds.matchTransform(onBallGroup,ikToeBase)
        cmds.makeIdentity( onBallGroup, apply=True, t=1, r=1, s=1, n=2 )
        toeFlapGroup=cmds.group(n=(f"{side}_toeFlap_grp"), empty=True)    
        cmds.matchTransform(toeFlapGroup,ikToeBase)
        cmds.makeIdentity( toeFlapGroup, apply=True, t=1, r=1, s=1, n=2 )
        onHeelGroup=cmds.group(n=(f"{side}_onHeel_grp"), empty=True)    
        cmds.matchTransform(onHeelGroup,ikFoot)
        pos = cmds.xform(onHeelGroup, q = True, t = True)
        cmds.move(0.0,-pos[1],-5.0,r=True)
        cmds.makeIdentity( onHeelGroup, apply=True, t=1, r=1, s=1, n=2 )
        BankLeftGroup=cmds.group(n=(f"{side}_bankLeft_grp"), empty=True)    
        cmds.transformLimits( BankLeftGroup,erz=[True, False],rz=[0, 0])
        cmds.matchTransform(BankLeftGroup,ikToeBase)
        pos = cmds.xform(BankLeftGroup, q = True, t = True)
        cmds.move(-5.0,-pos[1],0.0,r=True)
        cmds.makeIdentity( BankLeftGroup, apply=True, t=1, r=1, s=1, n=2 )  
        BankRightGroup=cmds.group(n=(f"{side}_bankRight_grp"), empty=True)   
        cmds.transformLimits( BankRightGroup,erz=[False, True],rz=[0, 0]) 
        cmds.matchTransform(BankRightGroup,ikToeBase)
        pos = cmds.xform(BankRightGroup, q = True, t = True)
        cmds.move(5.0,-pos[1],0.0,r=True)
        cmds.makeIdentity( BankRightGroup, apply=True, t=1, r=1, s=1, n=2 )

        '''Create the IK Ctrl and Move It'''
        
        lFootCtrl=cmds.circle(name=(f'{side}_Foot_ctrl'))
        mel.eval(f"setAttr {lFootCtrl[1]}.degree 1;")
        mel.eval(f"setAttr {lFootCtrl[1]}.sections 4;")
        cmds.rotate(90,45,0)
        cmds.makeIdentity( lFootCtrl, apply=True, t=1, r=1, s=1, n=2 )
        cmds.matchTransform(lFootCtrl,ikToeBase, pos=True, rot=False)    
        cmds.scale(20,20,40, r=True)
        pos = cmds.xform(lFootCtrl, q = True, t = True)
        cmds.move(0.0,-pos[1],0.0,r=True)
        cmds.makeIdentity( lFootCtrl, apply=True, t=1, r=1, s=1, n=2 )
        
        if side == "l":
            
                    if cmds.objExists('LEFT_IK_LEG_CTRLS'):
                        cmds.parent( lFootCtrl[0],'LEFT_IK_LEG_CTRLS')
        
        else:
                    if cmds.objExists('RIGHT_IK_LEG_CTRLS'):
                        cmds.parent( lFootCtrl[0],'RIGHT_IK_LEG_CTRLS')
       
        
        '''Edit Color and Thickness'''
        
       
        myListParent = cmds.ls(selection=True)
        myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
        x=0
        cmds.select(clear=True)
        for item in myList:
        
            cmds.setAttr (f"{item}.lineWidth", 1.5)
            x += 1
            
        
        cmds.setAttr (f"{lFootCtrl[0]}.overrideEnabled", 1)
        cmds.setAttr (f"{lFootCtrl[0]}.overrideColor", nurbColor)
        
        '''Group Everything Correctly'''
        cmds.parent(BankLeftGroup,lFootCtrl[0]) 
        cmds.parent(BankRightGroup,BankLeftGroup)  
        cmds.parent(onHeelGroup,BankRightGroup) 
        cmds.parent(onToeGroup,onHeelGroup)    
        cmds.parent(onBallGroup,toeFlapGroup,onToeGroup) 
        cmds.parent(ikHandleBall[0],ikHandleAnkle[0],onBallGroup) 
        cmds.parent(ikHandleToe[0],toeFlapGroup) 
        
        '''Add Attributes'''
        
        cmds.addAttr(lFootCtrl[0], longName="OnToe",niceName=("On Toe"), attributeType='double',keyable=True, min=0)
        cmds.addAttr(lFootCtrl[0], longName="OnHeel",niceName=("On Heel"), attributeType='double',keyable=True,min=0)
        cmds.addAttr(lFootCtrl[0], longName="OnBall",niceName=("On Ball"), attributeType='double',keyable=True,min=0)        
        cmds.addAttr(lFootCtrl[0], longName="ToeFlap",niceName=("Toe Flap"), attributeType='double',keyable=True)
        cmds.addAttr(lFootCtrl[0], longName="Bank",niceName=("Bank"), attributeType='double',keyable=True)
        
        '''Connect Attributes'''
        
        myMultiply=cmds.shadingNode ("multiplyDivide",asUtility=True) 
        cmds.connectAttr((f'{side}_Foot_ctrl.OnHeel'), (f'{myMultiply}.input1.input1Z.'))   
        cmds.connectAttr((f'{myMultiply}.output.outputZ'),(f'{side}_onHeel_grp.rotateX'))
        cmds.setAttr((f'{myMultiply}.input2Z'), -1.0)

        cmds.connectAttr((f'{side}_Foot_ctrl.Bank'), (f'{side}_bankLeft_grp.rotateZ'))
        cmds.connectAttr((f'{side}_Foot_ctrl.Bank'), (f'{side}_bankRight_grp.rotateZ'))   
        cmds.connectAttr((f'{side}_Foot_ctrl.OnToe'), (f'{side}_onToe_grp.rotateX'))
        cmds.connectAttr((f'{side}_Foot_ctrl.OnBall'), (f'{side}_onBall_grp.rotateX'))
        cmds.connectAttr((f'{side}_Foot_ctrl.ToeFlap'), (f'{side}_toeFlap_grp.rotateX'))
        
    
        '''Create PoleVector'''
            
        poleVector = cmds.circle(name=f'{side}_ik_pv_leg_ctrl', r=6)
        poleVectorCircle2 = cmds.circle(name='circle2', r=6)
        cmds.rotate(0,90,0)
        cmds.makeIdentity (poleVectorCircle2, apply = True,t=1,r=1,s=1,n=2)
        poleVectorCircle3 = cmds.circle(name='circle3', r=6)
        cmds.rotate(90,90,0)
        cmds.makeIdentity (poleVectorCircle3, apply = True,t=1,r=1,s=1,n=2)
        
        poleVectorParent = cmds.listRelatives(poleVector, fullPath=True, ad=True)
        poleVectorCircleShape2 = cmds.listRelatives(poleVectorCircle2, fullPath=True, ad=True)[0]
        poleVectorCircleShape3 = cmds.listRelatives(poleVectorCircle3, fullPath=True, ad=True)[0]    
                
        cmds.select(poleVectorCircleShape3,poleVectorCircleShape2, poleVector)
        cmds.parent(r=True, s=True)        
        cmds.delete(poleVectorCircle2[0],poleVectorCircle3[0])   
        cmds.select(poleVector)    
        
        '''Give it 1.5 Thickness'''
            
        myListParent = cmds.ls(selection=True)
        myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
        x=0
        cmds.select(clear=True)
        for item in myList:
            
            cmds.setAttr (f"{item}.lineWidth", 1.5)
            x += 1
            
        '''Color it'''
        
        x=0    
        
        for item in myList:
        
            cmds.setAttr (f"{item}.overrideEnabled", 1)
            cmds.setAttr (f"{item}.overrideColor", nurbColor)
            x += 1
        
        
        
        cmds.matchTransform(poleVector,ikLeg, pos=True, rot=False)  
        cmds.makeIdentity( poleVector, apply=True, t=1, r=1, s=1, n=2 )
        cmds.select(poleVector)
        cmds.makeIdentity( poleVector, apply=True, t=1, r=1, s=1, n=2 )
        
        '''Create Fix Group and Parent it'''
        
        poleVectorGroup = cmds.group( poleVector, name=f'{side}_ik_pv_leg_grp')
        cmds.matchTransform(poleVectorGroup,ikLeg, pos=True, rot=False)  
        cmds.makeIdentity( poleVectorGroup, apply=True, t=1, r=1, s=1, n=2 )

        
        if side == "l":
            
                    if cmds.objExists('LEFT_IK_LEG_CTRLS'):
                        cmds.parent( poleVectorGroup,'LEFT_IK_LEG_CTRLS')
        
        else:
                    if cmds.objExists('RIGHT_IK_LEG_CTRLS'):
                        cmds.parent( poleVectorGroup,'RIGHT_IK_LEG_CTRLS')
        
        
        cmds.poleVectorConstraint(poleVector, ikHandleAnkle[0])
        
        '''Create the FK Leg'''
        
        cmds.select(clear=True)
        cmds.select(resultLeg)    
        myFKLeg = cmds.duplicate()            
            
        if side=="l":
                    if cmds.objExists('leftLeg_fk_grp'):
                        cmds.parent( myFKLeg[0],'leftLeg_fk_grp')
        
        else:
                    if cmds.objExists('rightLeg_fk_grp'):
                        cmds.parent( myFKLeg[0],'rightLeg_fk_grp')    
            

        for i in core.ls(sl = True, dag = True):
            
            myJointName = i.nodeName().replace("result", "fk")
            core.rename(i, myJointName)
            myJointName = i.nodeName().replace("jnt1", "jnt")
            core.rename(i, myJointName)
            
        myFKLeg=cmds.ls(sl=True)
        
        
        jointChildren = cmds.listRelatives(myFKLeg,ad=True)
        jointChildren.append(myFKLeg[0])
        jointChildren.reverse()
        cmds.pickWalk( direction='up' )
        
        
        myGrpList = []
        circleList = []
        
        for current_joint in jointChildren:
            
            
            if "|" in current_joint:
                
                current_joint = (f"{current_joint[1:]}")       
    
            
            else:
                pass  
            
            
            if "jnt" in current_joint:
    
                current_jointName=current_joint.replace("_jnt", "")
                
            else:
                pass
             
            if myFKLeg[0] == current_joint: 
                
                cmds.circle(name=f'{side}_fk_UpLeg_ctrl')
                upperLegNurb=cmds.ls(sl=True)
                
                if side == "l":
                    
                    cmds.rotate(-180,0,0)
                else:
                    pass
                
                cmds.scale(4,12,2)
                cmds.select ((f"{side}_fk_UpLeg_ctrl.cv[5]"), r=True)
                cmds.move(0, 0, -18, r=True, cs=True, wd=True )
                cmds.select ((f"{side}_fk_UpLeg_ctrl.cv[1]"), r=True)
                cmds.move(0, 0, -18, r=True, cs=True, wd=True )
                cmds.select(upperLegNurb)
                mel.eval("manipPivotReset true true;")
                cmds.makeIdentity (apply = True,t=1,r=1,s=1,n=2)
                     
            
            if myFKLeg[0] == current_joint:
                circleList.append(upperLegNurb)
                
            else:
                circleList.append(cmds.circle(name=f'{current_jointName}_ctrl'))
                
            nurb=cmds.ls(sl=True)
            
            myList = cmds.listRelatives(nurb, ad=True, fullPath=True)
            for item in myList:
                cmds.setAttr (f"{item}.lineWidth", 1.5)
                x += 1
            
            
            cmds.setAttr (f"{nurb[0]}.overrideEnabled", 1)
            cmds.setAttr (f"{nurb[0]}.overrideColor", nurbColor)        
            
            
            myGrpList.append(cmds.group(name=f'{current_jointName}_fixGrp'))
            cmds.select(f'{current_joint}', add=True)
            
            if myFKLeg[0] == current_joint:
                cmds.matchTransform()
                cmds.matchTransform((f"{side}_fk_UpLeg_ctrl"),(f"{side}_fk_UpLeg_jnt"))
                cmds.makeIdentity ((f"{side}_fk_UpLeg_ctrl"), apply = True,t=1,r=1,s=1,n=2)
                cmds.select(f'{current_jointName}_ctrl')
            
            else:
                cmds.matchTransform()
                cmds.select(f'{current_jointName}_ctrl')
                cmds.rotate(0,90,0)
                cmds.scale(5,5,1, r=True)
                cmds.makeIdentity(apply=True)
                

            cmds.delete(constructionHistory = True)
            cmds.select(f'{current_joint}', add=True)
            cmds.orientConstraint( f'{current_jointName}_ctrl', f'{current_joint}', maintainOffset=False)
                
    
    
        for i in reversed(range(len(jointChildren))):
            if (i != 0):
                cmds.parentConstraint(jointChildren[i-1], myGrpList[i], mo=True)
                
        if side == "l":
                    if cmds.objExists('LEFT_FK_LEG_CTRLS'):
                        for i in myGrpList:
                            cmds.parent( i,'LEFT_FK_LEG_CTRLS')
        
        else:
                    if cmds.objExists('RIGHT_FK_LEG_CTRLS'):
                        for i in myGrpList:
                            cmds.parent( i,'RIGHT_FK_LEG_CTRLS')
       
        
        for i in myGrpList:
            if "End" in i:
                cmds.delete(i)
                
        
        '''Create the IKFK Ctrl'''
        
        createSkullNurb()        
        iKFKSwitch = cmds.ls(sl=True)
        
        cmds.matchTransform(iKFKSwitch,ikFoot, pos=True, rot=False)
        cmds.xform(t=[0,0,-20],r=True)
        cmds.rotate(0,90,0)
        cmds.makeIdentity (iKFKSwitch, apply = True,t=1,r=1,s=1,n=2)
        
        cmds.rename(f"{side}_leg_ikfkSwitch")
        iKFKSwitch = cmds.ls(sl=True)    
        iKFKSwitchList = cmds.listRelatives(iKFKSwitch, ad=True, fullPath=True)
        
        for item in iKFKSwitchList:
        
            cmds.setAttr (f"{item}.overrideEnabled", 1)
            cmds.setAttr (f"{item}.overrideColor", nurbColor)
    
        if side == "l":
            
                    if cmds.objExists('LEFT_LEG_CTRLS'):
                        cmds.parent( iKFKSwitch,'LEFT_LEG_CTRLS')
        
        else:
                    if cmds.objExists('RIGHT_LEG_CTRLS'):
                        cmds.parent( iKFKSwitch,'RIGHT_LEG_CTRLS')    
    
    
        '''Add and Connect Attributes'''
    
        iKFKSwitch = cmds.ls(sl=True)
        cmds.parentConstraint((f"{side}_result_Foot_jnt"),iKFKSwitch[0], mo=True)
        cmds.addAttr(iKFKSwitch, longName="IKFKSwitch",niceName="IK/FK Switch", attributeType='double',keyable=True, max=1, min=0)
        cmds.connectAttr((f'{side}_leg_ikfkSwitch.IKFKSwitch'), (f'{side}_fk_UpLeg_ctrl.visibility'))
        cmds.connectAttr((f'{side}_leg_ikfkSwitch.IKFKSwitch'), (f'{side}_fk_Leg_ctrl.visibility'))
        cmds.connectAttr((f'{side}_leg_ikfkSwitch.IKFKSwitch'), (f'{side}_fk_Foot_ctrl.visibility'))
        cmds.connectAttr((f'{side}_leg_ikfkSwitch.IKFKSwitch'), (f'{side}_fk_ToeBase_ctrl.visibility'))
        myReverse=cmds.shadingNode ("reverse",asUtility=True) 
        cmds.connectAttr((f'{side}_leg_ikfkSwitch.IKFKSwitch'), (f'{myReverse}.input.inputX.')) 
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{side}_ik_pv_leg_ctrl.visibility')) 
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{side}_Foot_ctrl.visibility')) 
    
        '''Parent Result Leg to IK and FK'''
        
        cmds.select(ikUpLeg,myFKLeg,resultLeg)
        cmds.orientConstraint()
        cmds.pickWalk( direction='down' )
        cmds.orientConstraint()
        cmds.pickWalk( direction='down' )
        cmds.orientConstraint()
        cmds.pickWalk( direction='down' )
        cmds.orientConstraint()
        cmds.pickWalk( direction='down' )
        cmds.orientConstraint()
            
        
        '''Connect Switch to Constraints'''
    
        cmds.connectAttr((f'{side}_leg_ikfkSwitch.IKFKSwitch'), (f'{side}_result_UpLeg_jnt_orientConstraint1.{side}_fk_UpLeg_jntW1'))
        cmds.connectAttr((f'{side}_leg_ikfkSwitch.IKFKSwitch'), (f'{side}_result_Leg_jnt_orientConstraint1.{side}_fk_Leg_jntW1'))
        cmds.connectAttr((f'{side}_leg_ikfkSwitch.IKFKSwitch'), (f'{side}_result_Foot_jnt_orientConstraint1.{side}_fk_Foot_jntW1'))
        cmds.connectAttr((f'{side}_leg_ikfkSwitch.IKFKSwitch'), (f'{side}_result_ToeBase_jnt_orientConstraint1.{side}_fk_ToeBase_jntW1'))
        cmds.connectAttr((f'{side}_leg_ikfkSwitch.IKFKSwitch'), (f'{side}_result_ToeEnd_jnt_orientConstraint1.{side}_fk_ToeEnd_jntW1'))
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{side}_result_UpLeg_jnt_orientConstraint1.{side}_ik_UpLeg_jntW0')) 
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{side}_result_Leg_jnt_orientConstraint1.{side}_ik_Leg_jntW0'))
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{side}_result_Foot_jnt_orientConstraint1.{side}_ik_Foot_jntW0'))
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{side}_result_ToeBase_jnt_orientConstraint1.{side}_ik_ToeBase_jntW0'))
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{side}_result_ToeEnd_jnt_orientConstraint1.{side}_ik_ToeEnd_jntW0'))
  
        
        
        if cmds.objExists('c_Hips_ctrl'):
            if cmds.objExists(f'{side}_fk_UpLeg_fixGrp_parentConstraint1'):
                pass
            else:    
                cmds.parentConstraint('c_Hips_ctrl', f'{side}_fk_UpLeg_fixGrp', mo=True)  
                
    else:   
        cmds.inViewMessage( amg='<hl>Please select the top leg joint</hl>.', pos='midCenter', fade=True, ck=True ) 
 
 
 
'''¤**************************************************CREATE ARM FUNCTIONS****************************************************'''   
 
def createArmFunctions():    
      
    
    '''Create the IK Arm'''
    
    resultShoulder=cmds.ls(sl=True)
    
    if resultShoulder:
        cmds.makeIdentity (resultShoulder, apply = True,t=1,r=1,s=1,n=2)
        cmds.pickWalk( direction='down' )
        resultArm=cmds.ls(sl=True)
        sideCheck=cmds.ls(sl=True)
        sideCheck=sideCheck[0]
        cmds.select(resultShoulder)
        ikArm=cmds.duplicate()
        
        if "l" in sideCheck[0]:
                    
                    side="l"
                    nurbColor=6
                    if cmds.objExists('leftArm_ik_grp'):
                        cmds.parent( ikArm[0],'leftArm_ik_grp')
        
        else:
                    side="r" 
                    nurbColor=13
                    if cmds.objExists('rightArm_ik_grp'):
                        cmds.parent( ikArm[0],'rightArm_ik_grp')
        
        ikArm =cmds.ls(sl=True)
            
        for i in core.ls(sl = True, dag = True):
            
            myJointName = i.nodeName().replace("result", "ik")
            core.rename(i, myJointName)
            myJointName = i.nodeName().replace("jnt1", "jnt")
            core.rename(i, myJointName)
            
        ikShoulder = cmds.ls(sl=True)
        cmds.pickWalk( direction='down' )
        cmds.pickWalk( direction='down' )
        cmds.pickWalk( direction='down' )
        
        iKHand=cmds.ls(sl=True)
        iKFingers=cmds.listRelatives(iKHand, fullPath=True)
        cmds.delete(iKFingers)
    
        myIKJoints=cmds.listRelatives(ikShoulder, ad=True,fullPath=True)
        ikArm = myIKJoints[2]
        ikForeArm = myIKJoints[1]
        ikHand = myIKJoints[0]    

        
        ikHandleArm = cmds.ikHandle(name=(f"{side}_ArmpoleVectorTarget"),startJoint = ikArm, endEffector = ikHand, createCurve = 0, simplifyCurve = 0, rootOnCurve = 0, parentCurve = 0, sol="ikRPsolver")
        mel.eval("toggleVisibilityAndKeepSelection `optionVar -query toggleVisibilityAndKeepSelectionBehaviour`;")
    
        
        '''Create the IK Ctrl and Move It'''
    
        ikHandFixGrp=cmds.group(n=(f"{side}_ikHand_fixgrp"), empty=True) 
        handIKCtrl=cmds.circle(name=(f'{side}_Hand_ctrl'))
        mel.eval(f"setAttr {handIKCtrl[1]}.degree 1;")
        mel.eval(f"setAttr {handIKCtrl[1]}.sections 4;")
        cmds.scale(20,20,20, r=True)
        cmds.matchTransform(ikHandFixGrp,ikHand, pos=True, rot=True) 
        cmds.matchTransform(handIKCtrl,ikHand, pos=True, rot=True) 
        
        if side == "l":
            
            cmds.rotate(90,45,20)
       
        else:
            cmds.rotate(90,45,-20)  
            
        cmds.parent(handIKCtrl[0],ikHandFixGrp) 
        cmds.makeIdentity( handIKCtrl, apply=True, t=1, r=1, s=1, n=2 )   
        if side == "l":
            
                    if cmds.objExists('LEFT_IK_ARM_CTRLS'):
                        cmds.parent( ikHandFixGrp,'LEFT_IK_ARM_CTRLS')
        
        else:
                    if cmds.objExists('RIGHT_IK_ARM_CTRLS'):
                        cmds.parent( ikHandFixGrp,'RIGHT_IK_ARM_CTRLS')
       
        
        '''Edit Color and Thickness'''
        
       
        myListParent = cmds.ls(selection=True)
        myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
        x=0
        cmds.select(clear=True)
        for item in myList:
        
            cmds.setAttr (f"{item}.lineWidth", 1.5)
            x += 1
            
        
        cmds.setAttr (f"{handIKCtrl[0]}.overrideEnabled", 1)
        cmds.setAttr (f"{handIKCtrl[0]}.overrideColor", nurbColor)
        
        '''Group Everything Correctly'''
        cmds.parent(ikHandleArm[0],handIKCtrl[0]) 
    
        '''Create PoleVector'''
            
        poleVector = cmds.circle(name=f'{side}_ik_pv_arm_ctrl', r=6)
        poleVectorCircle2 = cmds.circle(name='circle2', r=6)
        cmds.rotate(0,90,0)
        cmds.makeIdentity (poleVectorCircle2, apply = True,t=1,r=1,s=1,n=2)
        poleVectorCircle3 = cmds.circle(name='circle3', r=6)
        cmds.rotate(90,90,0)
        cmds.makeIdentity (poleVectorCircle3, apply = True,t=1,r=1,s=1,n=2)
        
        poleVectorParent = cmds.listRelatives(poleVector, fullPath=True, ad=True)
        poleVectorCircleShape2 = cmds.listRelatives(poleVectorCircle2, fullPath=True, ad=True)[0]
        poleVectorCircleShape3 = cmds.listRelatives(poleVectorCircle3, fullPath=True, ad=True)[0]    
                
        cmds.select(poleVectorCircleShape3,poleVectorCircleShape2, poleVector)
        cmds.parent(r=True, s=True)        
        cmds.delete(poleVectorCircle2[0],poleVectorCircle3[0])   
        cmds.select(poleVector)    
                
        
        '''Give it 1.5 Thickness'''
            
        myListParent = cmds.ls(selection=True)
        myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
        x=0
        cmds.select(clear=True)
        for item in myList:
            
            cmds.setAttr (f"{item}.lineWidth", 1.5)
            x += 1
            
        '''Color it'''
        
        x=0    
        
        for item in myList:
        
            cmds.setAttr (f"{item}.overrideEnabled", 1)
            cmds.setAttr (f"{item}.overrideColor", nurbColor)
            x += 1
        
        
        
        cmds.matchTransform(poleVector,ikForeArm, pos=True, rot=False)  
        cmds.makeIdentity( poleVector, apply=True, t=1, r=1, s=1, n=2 )
        cmds.select(poleVector)
        cmds.makeIdentity( poleVector, apply=True, t=1, r=1, s=1, n=2 )
        
        '''Create Fix Group and put it in the right category'''
        
        poleVectorGroup = cmds.group( poleVector, name=f'{side}_ik_pv_arm_grp')
        cmds.matchTransform(poleVectorGroup,ikForeArm, pos=True, rot=False)  
        cmds.makeIdentity( poleVectorGroup, apply=True, t=1, r=1, s=1, n=2 )
        

        if side == "l":
                    
                    if cmds.objExists('LEFT_IK_ARM_CTRLS'):
                        cmds.parent( poleVectorGroup,'LEFT_IK_ARM_CTRLS') 
        else:
                    if cmds.objExists('RIGHT_IK_ARM_CTRLS'):
                        cmds.parent( poleVectorGroup,'RIGHT_IK_ARM_CTRLS')  
        
        
        cmds.poleVectorConstraint(poleVector, ikHandleArm[0])
        
        '''Create the FK Arm'''
        
        cmds.select(clear=True)
        cmds.select(resultShoulder)    
        myFKShoulder = cmds.duplicate()
         
        if side == "l":
                    if cmds.objExists('leftArm_fk_grp'):
                        cmds.parent( myFKShoulder[0],'leftArm_fk_grp') 
        else:
                    if cmds.objExists('rightArm_fk_grp'):
                        cmds.parent( myFKShoulder[0],'rightArm_fk_grp')   
    
        for i in core.ls(sl = True, dag = True):
            
            myJointName = i.nodeName().replace("result", "fk")
            core.rename(i, myJointName)
            myJointName = i.nodeName().replace("jnt1", "jnt")
            core.rename(i, myJointName)
        
        myFKShoulder=cmds.ls(sl=True)    
        cmds.pickWalk( direction='down' )
        myFKArm=cmds.ls(sl=True)
        cmds.pickWalk( direction='down' )
        cmds.pickWalk( direction='down' )
        
        fKHand=cmds.ls(sl=True)
        fKFingers=cmds.listRelatives(fKHand, fullPath=True)
        cmds.delete(fKFingers)
            
        
        jointChildren = cmds.listRelatives(myFKArm,ad=True)
        jointChildren.append(myFKArm[0])
        jointChildren.reverse()
        cmds.pickWalk( direction='up' )
        
        
        myGrpList = []
        circleList = []
        
        '''Shape the Upper Arm Controller'''
        
        cmds.circle(name=f'{side}_fk_Arm_ctrl')
        upperArmNurb=cmds.ls(sl=True)
   
        if side == "l":
            
            cmds.rotate(-90,0,20)
        else:
            cmds.rotate(-90,0,-160)
 
        cmds.scale(4,12,2)
        cmds.select ((f"{side}_fk_Arm_ctrl.cv[5]"), r=True)
        cmds.move(0, 0, -18, r=True, cs=True, wd=True )
        cmds.select ((f"{side}_fk_Arm_ctrl.cv[1]"), r=True)
        cmds.move(0, 0, -18, r=True, cs=True, wd=True )
        cmds.select(upperArmNurb)
        mel.eval("manipPivotReset true true;")
        cmds.makeIdentity (apply = True,t=1,r=1,s=1,n=2)

        
        for current_joint in jointChildren:
            
            
            if "|" in current_joint:
                
                current_joint = (f"{current_joint[1:]}")       
    
            
            else:
                pass  
            
            
            if "jnt" in current_joint:
    
                current_jointName=current_joint.replace("_jnt", "")
                
            else:
                pass
            
            '''Replace normal Nurb Circle with Upper Arm Control'''
            
            if myFKArm[0] == current_joint:
                circleList.append(upperArmNurb)
                
            else:
                circleList.append(cmds.circle(name=f'{current_jointName}_ctrl'))
            
            nurb=cmds.ls(sl=True)
            
            '''Give it 1.5 Thickness and Color'''
            
            myList = cmds.listRelatives(nurb, ad=True, fullPath=True)
            for item in myList:
                cmds.setAttr (f"{item}.lineWidth", 1.5)
                x += 1
            
            cmds.setAttr (f"{nurb[0]}.overrideEnabled", 1)
            cmds.setAttr (f"{nurb[0]}.overrideColor", nurbColor)        
            
            
            myGrpList.append(cmds.group(name=f'{current_jointName}_fixGrp'))
            cmds.select(f'{current_joint}', add=True)
            
            if myFKArm[0] == current_joint:
                cmds.matchTransform()
                cmds.matchTransform((f"{side}_fk_Arm_ctrl"),(f"{side}_fk_Arm_jnt"))
                cmds.makeIdentity ((f"{side}_fk_Arm_ctrl"), apply = True,t=1,r=1,s=1,n=2)
                
            else:
                cmds.matchTransform()
                
            cmds.select(f'{current_jointName}_ctrl')
            
            if myFKArm[0] == current_joint:
                pass
                
            else:
                cmds.rotate(0,90,0)
                cmds.scale(5,5,1, r=True)
                cmds.makeIdentity(apply=True)
                cmds.delete(constructionHistory = True)
            
            cmds.select(f'{current_joint}', add=True)
            cmds.orientConstraint( f'{current_jointName}_ctrl', f'{current_joint}', maintainOffset=False)
                
    
    
        for i in reversed(range(len(jointChildren))):
            if (i != 0):
                cmds.parentConstraint(jointChildren[i-1], myGrpList[i], mo=True)
                
        for i in myGrpList:
            if "End" in i:
                cmds.delete(i)
                
        '''Create the Shoulder Ctrl'''
            
        cmds.select(resultShoulder)  
        resultShoulderJnt=resultShoulder
        resultShoulder=resultShoulder[0] 
        
        if "jnt" in current_joint:
            resultShoulder=resultShoulder.replace("_jnt", "")
                
        else:
            pass
        
    
        cmds.circle(name=f'{side}_fk_Shoulder_ctrl')
        nurb=cmds.ls(sl=True)
        
        myList = cmds.listRelatives(nurb, ad=True, fullPath=True)
        for item in myList:
            cmds.setAttr (f"{item}.lineWidth", 1.5)
            x += 1
        
        
        
        cmds.setAttr (f"{nurb[0]}.overrideEnabled", 1)
        cmds.setAttr (f"{nurb[0]}.overrideColor", nurbColor) 
        
        '''Shape the Shoulder Ctrl'''
               
        cmds.select ((f"{side}_fk_Shoulder_ctrl.cv[4]"), r=True)
        cmds.move(-1.516998, -0.237034, 0.148868, r=True, cs=True, wd=True )
        cmds.move(-0.227935, 0.146544, 0.00825853, r=True, cs=True, wd=True )
        cmds.select ((f"{side}_fk_Shoulder_ctrl.cv[5]"), r=True)
        cmds.move(-0.0519661, 0.484336, 0.0120431, r=True, cs=True, wd=True )
        cmds.select ((f"{side}_fk_Shoulder_ctrl.cv[1]"), r=True)
        cmds.move(-0.129391, -0.0274352, -0.0155815, r=True, cs=True, wd=True )
        cmds.select ((f"{side}_fk_Shoulder_ctrl.cv[3]"), r=True)
        cmds.move(0.164035, -0.152046, 0.0293713, r=True, cs=True, wd=True )
        cmds.select ((f"{side}_fk_Shoulder_ctrl.cv[7]"), r=True)
        cmds.move(-0.256596, 0.00788812, 0.00105699, r=True, cs=True, wd=True )
        cmds.select ((f"{side}_fk_Shoulder_ctrl.cv[1]"), r=True)
        cmds.move(0.460983, -0.0312034, -0.0196191, r=True, cs=True, wd=True )
    
    
        shoulderfixGrp = cmds.group(name=f'{side}_fk_Shoulder_fixGrp', empty=True)
        
        cmds.matchTransform(shoulderfixGrp,resultShoulderJnt)  
        cmds.select(f'{side}_fk_Shoulder_ctrl')
        cmds.scale(5,5,1, r=True)
        
        if side == "l":
            
            cmds.rotate(0,180,0)
       
        else:
            cmds.rotate(0,180,180)    
        
        cmds.makeIdentity(apply=True)
        cmds.matchTransform((f'{side}_fk_Shoulder_ctrl'),resultShoulderJnt, scl=False, rot=False)  
        cmds.makeIdentity(apply=True)
        cmds.parent((f'{side}_fk_Shoulder_ctrl'),shoulderfixGrp)
        cmds.makeIdentity(apply=True)
        cmds.orientConstraint( f'{side}_fk_Shoulder_ctrl', f'{resultShoulderJnt[0]}', maintainOffset=False)
        cmds.orientConstraint( f'{side}_fk_Shoulder_ctrl', f'{ikShoulder[0]}', maintainOffset=False)
        cmds.orientConstraint( f'{side}_fk_Shoulder_ctrl', f'{myFKShoulder[0]}', maintainOffset=False)
        poleConstraint = cmds.parentConstraint( f'{resultShoulderJnt[0]}', f'{side}_fk_Arm_fixGrp', maintainOffset=True)
        cmds.disconnectAttr((f'{poleConstraint[0]}.constraintRotateX'), (f'{side}_fk_Arm_fixGrp.rotateX'))    
        cmds.disconnectAttr((f'{poleConstraint[0]}.constraintRotateZ'), (f'{side}_fk_Arm_fixGrp.rotateZ'))       
        cmds.disconnectAttr((f'{poleConstraint[0]}.constraintRotateY'), (f'{side}_fk_Arm_fixGrp.rotateY'))   
        
        if side == "l":
                    if cmds.objExists('LEFT_FK_ARM_CTRLS'):
                        cmds.parent( shoulderfixGrp,'LEFT_FK_ARM_CTRLS')
                        for i in myGrpList:
                            cmds.parent( i,'LEFT_FK_ARM_CTRLS')
        
        else:
                    if cmds.objExists('RIGHT_FK_ARM_CTRLS'):
                        cmds.parent( shoulderfixGrp,'RIGHT_FK_ARM_CTRLS')
                        for i in myGrpList:
                            cmds.parent( i,'RIGHT_FK_ARM_CTRLS')
           
        
        '''Create the IKFK Ctrl'''
        
        createSkullNurb()        
        iKFKSwitch = cmds.ls(sl=True)        
        cmds.matchTransform(iKFKSwitch,ikHand, pos=True, rot=False)
        cmds.xform(t=[0,0,-20],r=True)
        cmds.rotate(0,90,0)
        cmds.makeIdentity (iKFKSwitch, apply = True,t=1,r=1,s=1,n=2)
        
        cmds.rename(f"{side}_arm_ikfkSwitch")
        iKFKSwitch = cmds.ls(sl=True)    
        iKFKSwitchList = cmds.listRelatives(iKFKSwitch, ad=True, fullPath=True)
        
        for item in iKFKSwitchList:
        
            cmds.setAttr (f"{item}.overrideEnabled", 1)
            cmds.setAttr (f"{item}.overrideColor", nurbColor)
    
        '''Add and Connect Attributes'''
    
        iKFKSwitch = cmds.ls(sl=True) 
        cmds.addAttr(iKFKSwitch, longName="IKFKSwitch",niceName="IK/FK Switch", attributeType='double',keyable=True, max=1, min=0)

        
        cmds.connectAttr((f'{side}_arm_ikfkSwitch.IKFKSwitch'), (f'{side}_fk_Arm_ctrl.visibility'))
        cmds.connectAttr((f'{side}_arm_ikfkSwitch.IKFKSwitch'), (f'{side}_fk_ForeArm_ctrl.visibility'))
        cmds.connectAttr((f'{side}_arm_ikfkSwitch.IKFKSwitch'), (f'{side}_fk_Hand_ctrl.visibility'))
        myReverse=cmds.shadingNode ("reverse",asUtility=True) 
        cmds.connectAttr((f'{side}_arm_ikfkSwitch.IKFKSwitch'), (f'{myReverse}.input.inputX.')) 
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{side}_ik_pv_arm_ctrl.visibility')) 
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{side}_Hand_ctrl.visibility')) 
        
        if side == "l":
                    
                    if cmds.objExists('LEFT_ARM_CTRLS'):
                        cmds.parent( iKFKSwitch,'LEFT_ARM_CTRLS') 
        else:
                    if cmds.objExists('RIGHT_ARM_CTRLS'):
                        cmds.parent( iKFKSwitch,'RIGHT_ARM_CTRLS')  
        
        cmds.parentConstraint((f"{side}_result_Hand_jnt"),iKFKSwitch[0], mo=True)
    
        '''Parent Result Arm to IK and FK, Also Parent IK Ctrl to IK Hand'''
        
        cmds.select(ikArm,myFKArm,resultArm)
        cmds.orientConstraint()
        cmds.pickWalk( direction='down' )
        cmds.orientConstraint()
        cmds.pickWalk( direction='down' )
        cmds.orientConstraint()
        
        
        cmds.select(handIKCtrl,ikHand) 
        cmds.orientConstraint()
    
    
        '''Connect Switch to Constraints'''
    
        cmds.connectAttr((f'{side}_arm_ikfkSwitch.IKFKSwitch'), (f'{side}_result_Arm_jnt_orientConstraint1.{side}_fk_Arm_jntW1'))
        cmds.connectAttr((f'{side}_arm_ikfkSwitch.IKFKSwitch'), (f'{side}_result_ForeArm_jnt_orientConstraint1.{side}_fk_ForeArm_jntW1'))
        cmds.connectAttr((f'{side}_arm_ikfkSwitch.IKFKSwitch'), (f'{side}_result_Hand_jnt_orientConstraint1.{side}_fk_Hand_jntW1'))
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{side}_result_Arm_jnt_orientConstraint1.{side}_ik_Arm_jntW0')) 
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{side}_result_ForeArm_jnt_orientConstraint1.{side}_ik_ForeArm_jntW0'))
        cmds.connectAttr((f'{myReverse}.output.outputX.'), (f'{side}_result_Hand_jnt_orientConstraint1.{side}_ik_Hand_jntW0'))
        
        '''Constraint Across Joint Chains'''
        
        for i in range(25, 0, -1):
                
            if i == 1:
                i = ""
                spine2 = (f'c_Spine{i}_ctrl') 
                break
                
            if cmds.objExists(f'c_Spine{i}_ctrl'):
                spine2 = (f'c_Spine{i}_ctrl') 
                break
   
        
        if cmds.objExists(spine2):
            
            if cmds.objExists("ARM_JOINTS"):
            
                if side == "l":
                
                    if cmds.objExists('l_fk_Shoulder_fixGrp_parentConstraint1'):
                        pass
                    else:    
                        cmds.parentConstraint(spine2, 'l_fk_Shoulder_fixGrp', mo=True)
                        
                    if cmds.objExists('l_fk_Arm_fixGrp_orientConstraint1'):
                        pass
                    else:    
                        cmds.orientConstraint(spine2, 'l_fk_Arm_fixGrp', mo=True)    
    
                else:    
                    if cmds.objExists('r_fk_Shoulder_fixGrp_parentConstraint1'):
                        pass
                    else:    
                        cmds.parentConstraint(spine2, 'r_fk_Shoulder_fixGrp', mo=True)
        
                    if cmds.objExists('r_fk_Arm_fixGrp_orientConstraint1'):
                        pass
                    else:    
                        cmds.orientConstraint(spine2, 'r_fk_Arm_fixGrp', mo=True)

    
    else:   
        cmds.inViewMessage( amg='<hl>Please select the shoulder joint</hl>.', pos='midCenter', fade=True, ck=True ) 
    
    
    

 
'''¤**************************************************CREATE CENTER FK FUNCTIONS****************************************************'''   

def CreateCenterFk():
    selectedJoint = cmds.ls(sl=True)
    if selectedJoint:
        cmds.makeIdentity (selectedJoint, apply = True,t=1,r=1,s=1,n=2)
        jointChildren = cmds.listRelatives(selectedJoint,ad=True)
        jointChildren.append(selectedJoint[0])
        jointChildren.reverse()
        
        for i in jointChildren:
            if "end" in i:
                
                endPos = cmds.xform(i, q = True, t = True)
                jointChildren.remove(i)
        
        cmds.pickWalk( direction='up' )
          
        myGrpList = []
        circleList = []
    
        y=0
        
        
        for current_joint in jointChildren:
            
            
            if "|" in current_joint:
                
                current_joint = (f"{current_joint[1:]}")       
    
            
            else:
                pass  
            
            
            if "jnt" in current_joint:
    
                current_jointName=current_joint.replace("_jnt", "")
                
            else:
                pass
            
            if y == len(jointChildren)-1: 
                Line = mel.eval("curve -d 1 -p 36 0 0 -p 24 0 12 -p 24 0 6 -p 12 0 6 -p 6 0 12 -p 6 0 24 -p 12 0 24 -p 0 0 36 -p -12 0 24 -p -6 0 24 -p -6 0 12 -p -12 0 6 -p -24 0 6 -p -24 0 12 -p -36 0 0 -p -24 0 -12 -p -24 0 -6 -p -12 0 -6 -p -6 0 -12 -p -6 0 -24 -p -12 0 -24 -p 0 0 -36 -p 12 0 -24 -p 6 0 -24 -p 6 0 -12 -p 12 0 -6 -p 24 0 -6 -p 24 0 -12 -p 36 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 ;")
                cmds.rename(f'{current_jointName}_ctrl')
                circleList.append(Line)
            else:
                circleList.append(cmds.circle(name=f'{current_jointName}_ctrl'))
            
            myGrpList.append(cmds.group(name=f'{current_jointName}_fixGrp'))
            cmds.select(f'{current_joint}', add=True)
            cmds.matchTransform()
            cmds.select(f'{current_jointName}_ctrl')
    
            '''Sort the controls so that we can turn them correctly'''
            
            if y == len(jointChildren)-1: 
            
                   
                '''Head Controller'''
              
                myListParent = cmds.ls(selection=True)
                myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
                x=0
                cmds.select(clear=True)
                
                for item in myList:
                
                    cmds.setAttr (f"{item}.lineWidth", 1.5)
                    cmds.setAttr (f"{item}.overrideEnabled", 1)
                    cmds.setAttr (f"{item}.overrideColor", 17)
                    x += 1
        
                cmds.select(f'{current_jointName}_ctrl')
                cmds.makeIdentity(apply=True)    
                cmds.rotate(0,45,0)            
                cmds.scale(0.8,0.8,0.8, r=True)
                cmds.makeIdentity(apply=True)
                cmds.select(clear=True)
                
                for i in range(29):
                    cmds.select ((f"{current_jointName}_ctrl.cv[{i}]"))
                    cmds.xform(r=True, t=(0,endPos[1],0))
                    
                cmds.orientConstraint( f'{current_jointName}_ctrl', f'{current_joint}', maintainOffset=False)      
            
            elif y != 0:
                
                myListParent = cmds.ls(selection=True)
                myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
                x=0
                cmds.select(clear=True)
                
                for item in myList:
                
                    cmds.setAttr (f"{item}.lineWidth", 1.5)
                    cmds.setAttr (f"{item}.overrideEnabled", 1)
                    cmds.setAttr (f"{item}.overrideColor", 17)
                    x += 1
        
                cmds.select(f'{current_jointName}_ctrl')
                cmds.scale(10,5,1, r=True)
                cmds.makeIdentity(apply=True)
                cmds.select(clear=True)
                for i in range(8):
                    cmds.select ((f"{current_jointName}_ctrl.cv[{i}]"))
                    cmds.xform(r=True, t=(0,0,-15))
                    
                cmds.orientConstraint( f'{current_jointName}_ctrl', f'{current_joint}', maintainOffset=False)  
    
                
            else: 
                
                '''Hip Control'''  
                
                myListParent = cmds.ls(selection=True)
                myList = cmds.listRelatives(myListParent, ad=True, fullPath=True)
                x=0
                cmds.select(clear=True)
                
                for item in myList:
                
                    cmds.setAttr (f"{item}.lineWidth", 5)
                    cmds.setAttr (f"{item}.overrideEnabled", 1)
                    cmds.setAttr (f"{item}.overrideColor", 17)
                    x += 1
        
                cmds.select(f'{current_jointName}_ctrl')
                
                historyList=cmds.listHistory()
                
                for i in historyList:
                    
                    if "makeNurbCircle" in i:
                        cmds.setAttr (f"{i}.sections", 16)
    
                cmds.rotate(90,0,0)
                cmds.scale(6,6,6, r=True)
                cmds.makeIdentity(apply=True)
                cmds.select(clear=True)
                
                for i in range(0,16,2):
                    cmds.select ((f"{current_jointName}_ctrl.cv[{i}]"))
                    cmds.xform(r=True, t=(0,30,0))
                    
                cmds.select(clear=True)
                
                for i in range(16):
                    cmds.select ((f"{current_jointName}_ctrl.cv[{i}]"))
                    cmds.xform(r=True, s=(7,1,7))
                    cmds.xform(r=True, t=(0,-15,0))
                    
                cmds.select(clear=True)
                cmds.select ((f"{current_jointName}_ctrl.cv[1]"))
                cmds.xform(r=True, t=(0,0,15))
                cmds.makeIdentity(apply=True)
                cmds.select(clear=True)
                if cmds.objExists('LEG_JOINTS'):
                        cmds.parentConstraint((f'{current_jointName}_ctrl'), 'LEG_JOINTS', mo=True)
    
                cmds.parentConstraint( f'{current_jointName}_ctrl', f'{current_joint}', maintainOffset=False)
                
                if cmds.objExists('l_fk_UpLeg_fixGrp'):
                    if cmds.objExists('l_fk_UpLeg_fixGrp_parentConstraint1'):
                        pass
                    else:    
                        cmds.parentConstraint((f'{current_jointName}_ctrl'), 'l_fk_UpLeg_fixGrp', mo=True)   
                            
                if cmds.objExists('r_fk_UpLeg_fixGrp'):
                    if cmds.objExists('r_fk_UpLeg_fixGrp_parentConstraint1'):
                        pass
                    else:    
                        cmds.parentConstraint((f'{current_jointName}_ctrl'), 'r_fk_UpLeg_fixGrp', mo=True)  
                
               
    
            y+=1
            cmds.select(f'{current_joint}', add=True)
        
        '''Constraint Across Joint Chains'''
        
        if cmds.objExists('ARM_JOINTS'):
                    
            for i in range(25, 0, -1):
                
                if i == 1:
                    i = ""
                    if cmds.objExists(f'c_Spine{i}_ctrl'):
                        cmds.parentConstraint(f'c_Spine{i}_ctrl', 'ARM_JOINTS', mo=True)
                        spine2 = (f'c_Spine{i}_ctrl') 
                        break
                
                if cmds.objExists(f'c_Spine{i}_ctrl'):
                    cmds.parentConstraint(f'c_Spine{i}_ctrl', 'ARM_JOINTS', mo=True)
                    spine2 = (f'c_Spine{i}_ctrl') 
                    break
    
                
            else:
                pass
            
                
            if cmds.objExists('l_fk_Shoulder_fixGrp'):
                if cmds.objExists('l_fk_Shoulder_fixGrp_parentConstraint1'):
                    pass
                else:    
                    cmds.parentConstraint(spine2, 'l_fk_Shoulder_fixGrp', mo=True)
            if cmds.objExists('r_fk_Shoulder_fixGrp'):
                if cmds.objExists('r_fk_Shoulder_fixGrp_parentConstraint1'):
                    pass
                else:    
                    cmds.parentConstraint(spine2, 'r_fk_Shoulder_fixGrp', mo=True)
            if cmds.objExists('l_fk_Arm_fixGrp'):
                if cmds.objExists('l_fk_Arm_fixGrp_orientConstraint1'):
                    pass
                else:    
                    cmds.orientConstraint(spine2, 'l_fk_Arm_fixGrp', mo=True)
            if cmds.objExists('r_fk_Arm_fixGrp'):
                if cmds.objExists('r_fk_Arm_fixGrp_orientConstraint1'):
                    pass
                else:    
                    cmds.orientConstraint(spine2, 'r_fk_Arm_fixGrp', mo=True)
                    
        
        for i in reversed(range(len(jointChildren))):
            if (i != 0):
                cmds.parentConstraint(jointChildren[i-1], myGrpList[i], mo=True)
                
        if cmds.objExists('CENTER_CTRLS'):
            for i in myGrpList:
                cmds.parent( i,'CENTER_CTRLS')

            
    else:   
        cmds.inViewMessage( amg='<hl>Please select the hip joint</hl>.', pos='midCenter', fade=True, ck=True ) 

 
'''¤**************************************************CREATE RIG MENUS****************************************************''' 

 
def createRigMenus():
    
    '''First Tier Joints'''
    leftArmResultJoint = cmds.group( empty=True, n="leftArm_result_grp")
    leftArmFkJoint = cmds.group( empty=True, n="leftArm_fk_grp")
    leftArmIkJoint = cmds.group( empty=True, n="leftArm_ik_grp")
    rightArmResultJoint = cmds.group( empty=True, n="rightArm_result_grp")
    rightArmFkJoint = cmds.group( empty=True, n="rightArm_fk_grp")
    rightArmIkJoint = cmds.group( empty=True, n="rightArm_ik_grp")
    leftLegResultJoint = cmds.group( empty=True, n="leftLeg_result_grp")
    leftLegFkJoint = cmds.group( empty=True, n="leftLeg_fk_grp")
    leftLegIkJoint = cmds.group( empty=True, n="leftLeg_ik_grp")
    rightLegResultJoint = cmds.group( empty=True, n="rightLeg_result_grp")
    rightLegFkJoint = cmds.group( empty=True, n="rightLeg_fk_grp")
    rightLegIkJoint = cmds.group( empty=True, n="rightLeg_ik_grp")
    '''First Tier Ctrls'''
    leftArmFkJointCtrls = cmds.group( empty=True, n="LEFT_FK_ARM_CTRLS")
    leftArmIkJointCtrls = cmds.group( empty=True, n="LEFT_IK_ARM_CTRLS")
    rightArmFkJointCtrls = cmds.group( empty=True, n="RIGHT_FK_ARM_CTRLS")
    rightArmIkJointCtrls = cmds.group( empty=True, n="RIGHT_IK_ARM_CTRLS")
    leftLegFkJointCtrls = cmds.group( empty=True, n="LEFT_FK_LEG_CTRLS")
    leftLegIkJointCtrls = cmds.group( empty=True, n="LEFT_IK_LEG_CTRLS")
    rightLegFkJointCtrls = cmds.group( empty=True, n="RIGHT_FK_LEG_CTRLS")
    rightLegIkJointCtrls = cmds.group( empty=True, n="RIGHT_IK_LEG_CTRLS")
    
    '''Second Tier Joints'''
    leftArmJoints = cmds.group( leftArmResultJoint,leftArmFkJoint,leftArmIkJoint, n="LEFT_ARM_JOINTS")
    rightArmJoints = cmds.group( rightArmResultJoint,rightArmFkJoint,rightArmIkJoint, n="RIGHT_ARM_JOINTS")
    leftLegJoints = cmds.group( leftLegResultJoint,leftLegFkJoint,leftLegIkJoint, n="LEFT_LEG_JOINTS")
    rightLegJoints = cmds.group( rightLegResultJoint,rightLegFkJoint,rightLegIkJoint, n="RIGHT_LEG_JOINTS")
    '''Second Tier Ctrls'''
    leftArmCtrls = cmds.group( leftArmIkJointCtrls,leftArmFkJointCtrls, n="LEFT_ARM_CTRLS")
    rightArmCtrls = cmds.group( rightArmIkJointCtrls,rightArmFkJointCtrls, n="RIGHT_ARM_CTRLS")
    leftLegCtrls = cmds.group( leftLegIkJointCtrls,leftLegFkJointCtrls, n="LEFT_LEG_CTRLS")
    rightLegCtrls = cmds.group( rightLegIkJointCtrls,rightLegFkJointCtrls, n="RIGHT_LEG_CTRLS")
    '''Third Tier Joints'''
    armJoints = cmds.group( leftArmJoints,rightArmJoints, n="ARM_JOINTS")
    centerJoints = cmds.group( empty=True, n="CENTER_JOINTS")
    legJoints = cmds.group( leftLegJoints,rightLegJoints, n="LEG_JOINTS")
    '''Third Tier Ctrls'''
    armCtrls = cmds.group( leftArmCtrls,rightArmCtrls, n="ARM_CTRLS")
    legCtrls = cmds.group( leftLegCtrls,rightLegCtrls, n="LEG_CTRLS")
    centerCtrls = cmds.group( empty=True, n="CENTER_CTRLS")
    '''Fourth Tier'''
    joints = cmds.group( armJoints,centerJoints,legJoints, n="JOINTS")
    cmds.setAttr (f"{joints}.overrideEnabled", 1)
    ctrls = cmds.group( armCtrls,legCtrls,centerCtrls, n="CTRLS")
    cmds.setAttr (f"{ctrls}.overrideEnabled", 1)
    '''Fifth Tier'''

    masterCtrl = mel.eval("curve -d 1 -p 36 0 0 -p 24 0 12 -p 24 0 6 -p 12 0 6 -p 6 0 12 -p 6 0 24 -p 12 0 24 -p 0 0 36 -p -12 0 24 -p -6 0 24 -p -6 0 12 -p -12 0 6 -p -24 0 6 -p -24 0 12 -p -36 0 0 -p -24 0 -12 -p -24 0 -6 -p -12 0 -6 -p -6 0 -12 -p -6 0 -24 -p -12 0 -24 -p 0 0 -36 -p 12 0 -24 -p 6 0 -24 -p 6 0 -12 -p 12 0 -6 -p 24 0 -6 -p 24 0 -12 -p 36 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 ;")
    cmds.rename("master_ctrl")
    masterCtrl=cmds.ls(sl=True)[0]
    

    '''Color it and give it thickness'''
       
    myList = cmds.listRelatives(masterCtrl, ad=True, fullPath=True)
    cmds.select(clear=True)
    for item in myList:
        
        cmds.setAttr (f"{item}.lineWidth", 3)
        cmds.setAttr (f"{masterCtrl}.overrideEnabled", 1)
        cmds.setAttr (f"{masterCtrl}.overrideColor", 17)
        
    '''Final Tier'''
    cmds.parent( joints,ctrls, masterCtrl)
    rigg = cmds.group( masterCtrl, n="RIGG")
    


 
'''¤**************************************************MERGE NURBS****************************************************''' 


    
def mergeNurbs():
    
    nurbList=cmds.ls(sl=True)
    
    if len(nurbList) > 1:
    
        nurbParent=nurbList[1]
        nurbParentTopGroup=cmds.listRelatives(nurbParent,ap=True, fullPath=True)
        nurbParentShape=cmds.listRelatives(nurbParent, fullPath=True, shapes=True,ad=True)
        nurbChild=nurbList[0]
        nurbChildShape=cmds.listRelatives(nurbChild, fullPath=True,shapes=True)
        nurbChildTopGroup=cmds.listRelatives(nurbChild,ap=True, fullPath=True)
        
        
        if "|" in nurbChild:
                nurbChild = (f"{nurbChild[1:]}")  
        
        if nurbParentTopGroup != nurbChildTopGroup:
            cmds.parent(nurbChild,nurbParentTopGroup)
            
        else:
            pass    
        
        cmds.makeIdentity (nurbChild, apply = True,t=1,r=1,s=1,n=2)
        
        try:
            for child in nurbChildShape:
                
                if "|" in child[0]:
                    child = (f"{child[1:]}")       
                    cmds.select([child], nurbParent)
                    cmds.parent(r=True, s=True)
                
                else:
                    cmds.select([child], nurbParent)
                    cmds.parent(r=True, s=True)
            
            
            
            cmds.delete(nurbChild, nurbParentShape)
            nurbParentShape=cmds.listRelatives(nurbParent, fullPath=True, shapes=True)[0]
            
        except:    
            cmds.inViewMessage( amg='<hl>Please select only nurb shapes</hl>.', pos='midCenter', fade=True, ck=True ) 
    else:   
        cmds.inViewMessage( amg='<hl>Please select your shape, then what you want to replace</hl>.', pos='midCenter', fade=True, ck=True ) 
    
    
    
    
    
    
    
'''¤**************************************************INTERFACE****************************************************'''





    

def createCustomWorkspaceControlUI():
    
    buttonWidth=275
    blankAreaSmall=5
    blankAreaBig=20
    windowHeight=470
   
    form = cmds.formLayout()
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
    
    '''Startup'''
    
    createJointsTab = cmds.columnLayout(co=["left", 20], height=windowHeight)
    

    cmds.text( label=' ', height=blankAreaBig  )
    cmds.text( label='Create Premade Groups', height=20  )
    cmds.button(label='Rig Menus', command="createRigMenus()",width=buttonWidth, ann='Creates a Starting Collection of Groups')
    
    cmds.text( label=' ', height=blankAreaSmall  )
    cmds.text( label='Create Joints', height=20 )
    cmds.button(label='Arm', command=buttonArmJoints,width=buttonWidth, ann='Creates a Joint Chain at Selected Edge Loop')
    cmds.button(label='Leg', command="buttonLegJoints()",width=buttonWidth, ann='Creates a Joint Chain at Selected Edge Loop')
    
    cmds.button(label='Center', command="jointAmount = cmds.intSliderGrp('centerJointAmount', query=True, value=True)\nbuttonCenterJoints(jointAmount)", width=buttonWidth, ann='Creates a Joint Chain at Selected Edge Loop')
    cmds.text( label=' ', height=blankAreaSmall  )
    cmds.intSliderGrp( 'centerJointAmount', field=True, label='Center Joints:        ', width=280,height=20, minValue=4, maxValue=25, value=6, adj=1 )
    
    cmds.text( label=' Small Functions', height=20 )
    cmds.button(label='Mirror Joints', command="mirrorJoints()",width=buttonWidth, ann='Mirrors the Selected Joints and Replaces "l" with "r"')
    cmds.button(label='Toggle Axes Visibility', command="cmds.SelectHierarchy()\nonlyJoints=cmds.ls(sl=True, typ='joint')\ncmds.select(onlyJoints)\nmel.eval('ToggleLocalRotationAxes')",width=buttonWidth, ann='Toggles Local Axes Visibility for an Entire Joint Chain')
    cmds.button(label='Match Transform', command="mel.eval('MatchTransform')",width=buttonWidth, ann='Matches all Transformations, the First Selected Object Matches to the Second')
    cmds.button(label='Freeze Transform', command="mel.eval('FreezeTransformations')",width=buttonWidth, ann='Freezes all Transformations on the Selected Object')
    cmds.button(label="Reset the Rigg's Pose", command="resetRigg()",width=buttonWidth, ann='Resets Movement and Attibutes on Rigg Controls')
    cmds.button(label="Lock/Unlock Attributes on Controls", command="lockCheckbox = cmds.checkBoxGrp('lockOrUnlock', query=True, valueArray2=True)\nlockCheckbox=lockCheckbox[0]\nlockAllAttributes(lock=lockCheckbox)",width=buttonWidth, ann='Resets Movement and Attibutes on Rigg Controls')
    cmds.text( label=' ', height=blankAreaSmall  )
    cmds.checkBoxGrp( 'lockOrUnlock', numberOfCheckBoxes=1, label='',label1='Lock Attributes', width=105,height=20, adj=1  )   

    cmds.setParent( '..' )
    
    '''Joint Functions'''
   
    jointFunctionsTab = cmds.columnLayout(co=["both", 20], height=windowHeight)
    cmds.text( label=' ', height=blankAreaBig  )
    cmds.text( label='Create FK/IK Function', height=20  )
    cmds.button(label='Create Arm Functions', command="createArmFunctions()",width=buttonWidth, ann='Creates FK/IK from top of a Selected Joint Chain')
    cmds.button(label='Create Leg Functions', command="createLegFunctions()",width=buttonWidth, ann='Creates FK/IK from top of a Selected Joint Chain')
    cmds.text( label=' ', height=blankAreaSmall  )
    cmds.text( label='Create FK Function', height=20  )
    cmds.button(label='Create Center FK Function', command="CreateCenterFk()",width=buttonWidth, ann="Creates FK from top of Selected Joint Chain")
    cmds.button(label='Create Single Joint FK Function', command="CreateSingleFkCtrl()",width=buttonWidth, ann="Creates a FK Controller on a Single Joint")
    cmds.button(label='Create FK Chain', command="CreateFkChain()",width=buttonWidth, ann="Creates a FK Chain from the selected joint down, parenting all to eachother")
    cmds.text( label=' ', height=blankAreaSmall  )
    cmds.text( label='Create Special Function', height=20  )
    cmds.button(label='Create Finger Curls', command="createFingerCurls()",width=buttonWidth, ann="Select Hand Joint and IK/FK Switch")
    cmds.button(label='Create Reference Skeleton', command="createReference()",width=buttonWidth, ann="Creates a Copy of the Result Joints and Makes a Reference Skeleton Parented to Those Joints")
    cmds.button(label='Connect Result Joints to IK/FK', command="connectResultJoints()",width=buttonWidth, ann="Select all your FK/IK/Result joints and all controls")
 
    cmds.text( label=' ', height=blankAreaSmall  )
    cmds.text( label='Ribbon Snap', height=20  )
    cmds.button(label='Snap Follicle to Joint', command="snapFol()",width=buttonWidth, ann="Select the Nurb Plane, the joint and the Follicle")
    

    cmds.setParent( '..' )
    
    
    '''Custom Joint Chain Tab'''
    
    
    customJointChainTab = cmds.columnLayout(co=["left", 20], height=windowHeight)
    

    cmds.text( label=' ', height=blankAreaBig  )
    cmds.text( label='Create Custom Joint Chains', height=20  )
    cmds.text( label=' ', height=blankAreaSmall  )
    cmds.textFieldGrp("prefixBox", label='Prefix:                     ', pht="c_" ,adj=1, width=280,cw=[2,177])
    cmds.textFieldGrp("nameBox", label='Name:                     ', pht="MyJointName" ,adj=1, width=280,cw=[2,177])
    cmds.textFieldGrp("suffixBox", label='Suffix:                     ', pht="_jnt" ,adj=1, width=280,cw=[2,177])
    cmds.textFieldGrp("distanceBox", label='Joint Distance:      ', pht="20" ,adj=1, width=280,cw=[2,177])
    cmds.intSliderGrp( "jointAmountBox", field=True, label="Amount of Joints: ", width=280,height=20, minValue=1, maxValue=25, value=1, adj=1)
    cmds.text( label=' ', height=4  )
    cmds.attrEnumOptionMenuGrp( "jointOrientationBox", l='Joint Orientation:',at='defaultRenderGlobals.imageFormat',ei=[(0,'xyz      '),(1,'yzx      '),(2,'zxy      '),(3,'xzy      '),(4,'yxz      '),(5,'zyx      ')], width=280,height=20, cal=[1, "left" ],cw=[1, 94])
    cmds.setAttr ("defaultRenderGlobals.imageFormat", 0)
    
    cmds.text( label=' ', height=blankAreaBig  )
    cmds.button(label='Create Chain', command='jointOrientationList = ["xyz","yzx","zxy","xzy","yxz","zyx"]\njointOrient = cmds.getAttr("defaultRenderGlobals.imageFormat")\njointOrient=jointOrientationList[jointOrient]\nprefixText = cmds.textFieldGrp("prefixBox", query=True, text=True)\ndistanceText = cmds.textFieldGrp("distanceBox", query=True, text=True)\nif distanceText == "":\n    distanceText = "20"\ndistanceText=float(distanceText)\nnameText = cmds.textFieldGrp("nameBox", query=True, text=True)\nsuffixText = cmds.textFieldGrp("suffixBox", query=True, text=True)\nprefixText = cmds.textFieldGrp("prefixBox", query=True, text=True)\njointAmount = cmds.intSliderGrp("jointAmountBox", query=True, value=True)\nbuttonCustomJointChain(jointAmount=(jointAmount),prefix=(prefixText),name=(nameText),suffix=(suffixText),jointDistance=(distanceText),jointOrientation=(jointOrient))',width=buttonWidth, ann='Creates a Joint Chain Using Your Inputs. Has the Name "Joint" and no Pre/Suf and a Joint Distance of 20 if All Spaces are Left Blank')



    cmds.setParent( '..' )
    

    
    '''Nurbs'''
    
    nurbsTab=cmds.columnLayout(co=["left", 20], height=windowHeight)
    cmds.text( label=' ', height=blankAreaBig  )
    cmds.text( label='Recolor Nurbs', height=20  )
    cmds.button(label='Blue', command=buttonBlueColor, width=buttonWidth, ann='Recolors Selected Nurbs')
    cmds.button(label='Red', command=buttonRedColor, width=buttonWidth, ann='Recolors Selected Nurbs')
    cmds.button(label='Yellow', command=buttonYellowColor, width=buttonWidth, ann='Recolors Selected Nurbs')
       
    cmds.button(label='Custom', command='controlColor = cmds.colorIndexSliderGrp("controlColorInput", query=True, value=True)-1\nmyList = cmds.ls(selection=True)\nif myList:\n    myList = cmds.listRelatives(myList, ad=True, fullPath=True)\n    for item in myList:\n        cmds.setAttr (f"{item}.overrideEnabled", 1)\n        cmds.setAttr (f"{item}.overrideColor", controlColor)\nelse:\n    cmds.inViewMessage( amg="<hl>Please select atleast one nurb shape</hl>.", pos="midCenter", fade=True, ck=True ) ',width=buttonWidth, ann='Recolors Selected Nurbs to Custom Color')
    cmds.text( label=' ', height=blankAreaSmall  )
    myColorIndex = cmds.colorIndexSliderGrp('controlColorInput', label='Custom Color :      ', width=279,height=20, min=1, max=32, value=6, adj=1)   
        
    
    cmds.text( label=' ', height=blankAreaSmall  )
    cmds.text( label='Edit Nurbs', height=20  )
    cmds.button(label='Select Nurb Control Vertex', command="selectNurbControlVertex()",width=buttonWidth, ann='Selects All Control Vertices for Your Selected Nurbs')    
    cmds.button(label='Change Width', command="nurbWidth()",width=buttonWidth, ann='Changes Width of Selected Nurbs, Default is 1')
    cmds.button(label='Replace Nurb Shape', command="mergeNurbs()",width=buttonWidth, ann='Select the Desired Shape Then the Target')

    
    cmds.text( label=' ', height=blankAreaSmall  )
    cmds.text( label='Create Nurbs', height=20  )
    cmds.text( label=' ', height=3  )
    cW=46
    cmds.rowLayout( numberOfColumns=6,columnWidth6=(cW, cW, cW, cW, cW, cW))
    cmds.symbolButton( image='SkullNurb.png', command="createSkullNurb()" )
    cmds.symbolButton( image='MasterNurb.png', command="createMasterNurb()" )
    cmds.symbolButton( image='PoleVectorNurb.png', command="createPoleVector()" )
    cmds.symbolButton( image='SquareNurb.png', command="createSquare()" )
    cmds.symbolButton( image='NeedleNurb.png', command="createNeedle(defaultName='Needle', rotation=90)" )
    cmds.symbolButton( image='ArrowNurb.png', command="CreateArrow()" )
    
    cmds.setParent( '..' )
      
    
    cmds.tabLayout( tabs, edit=True, tabLabel=((createJointsTab, 'Startup'), (jointFunctionsTab, 'Joint Functions'), (customJointChainTab, 'Custom Joints'),(nurbsTab, 'Nurbs')) )

    
cmds.workspaceControl("Graverigger's Toolkit", retain=False, floating=True, uiScript="createCustomWorkspaceControlUI()");

