"""
geopos.py is a Maya plugin to calculate the closest intersection to another meth in negative y direction.
Useful for tires or things that need to touch the ground.

Author Anthony J Kersten
Copyright (c) 2021
"""
import sys
from maya.api import OpenMaya as om


def maya_useNewAPI():
    pass


class GeoPos(om.MPxNode):
    """
    Maya node
    """
    ID = om.MTypeId(0x98)
    # Input Attr
    aiMesh = None
    aiPos = None
    aiPosX = None
    aiPosY = None
    aiPosZ = None
    # Output Attr
    aoPos = None
    aoPosX = None
    aoPosY = None
    aoPosZ = None

    def __init__(self):
        om.MPxNode.__init__(self)

    @staticmethod
    def cmdCreator():
        return GeoPos()

    @staticmethod
    def initNode():
        # IN ATTR
        nAttrFn = om.MFnNumericAttribute()
        # aiMesh Attr
        inMeshAttrFn = om.MFnTypedAttribute()
        GeoPos.aiMesh = inMeshAttrFn.create("inMesh", "im", om.MFnData.kMesh)
        inMeshAttrFn.storable = True
        inMeshAttrFn.keyable = False
        inMeshAttrFn.readable = False
        inMeshAttrFn.writable = True
        inMeshAttrFn.cached = False
        om.MPxNode.addAttribute(GeoPos.aiMesh)
        # aiPosX Attr
        GeoPos.aiPosX = nAttrFn.create("positionX", "px", om.MFnNumericData.kDouble)
        nAttrFn.storable = True
        nAttrFn.keyable = True
        nAttrFn.readable = True
        nAttrFn.writable = True
        om.MPxNode.addAttribute(GeoPos.aiPosX)

        # aiPosY Attr
        GeoPos.aiPosY = nAttrFn.create("positionY", "py", om.MFnNumericData.kDouble)
        nAttrFn.storable = True
        nAttrFn.keyable = True
        nAttrFn.readable = True
        nAttrFn.writable = True
        om.MPxNode.addAttribute(GeoPos.aiPosY)

        # aiPosZ Attr
        GeoPos.aiPosZ = nAttrFn.create("positionZ", "pz", om.MFnNumericData.kDouble)
        nAttrFn.storable = True
        nAttrFn.keyable = True
        nAttrFn.readable = True
        nAttrFn.writable = True
        om.MPxNode.addAttribute(GeoPos.aiPosZ)

        # aiPos Attr
        GeoPos.aiPos = nAttrFn.create(
            "position", "p", GeoPos.aiPosX, GeoPos.aiPosY, GeoPos.aiPosZ
        )
        nAttrFn.storable = True
        nAttrFn.keyable = True
        nAttrFn.readable = True
        nAttrFn.writable = True
        om.MPxNode.addAttribute(GeoPos.aiPos)

        # OUT Attr
        # aoPosX Attr
        GeoPos.aoPosX = nAttrFn.create("outX", "ox", om.MFnNumericData.kDouble)
        nAttrFn.storable = False
        nAttrFn.keyable = False
        nAttrFn.readable = True
        nAttrFn.writable = False
        om.MPxNode.addAttribute(GeoPos.aoPosX)
        # aoPosY Attr
        GeoPos.aoPosY = nAttrFn.create("outY", "oy", om.MFnNumericData.kDouble)
        nAttrFn.storable = False
        nAttrFn.keyable = False
        nAttrFn.readable = True
        nAttrFn.writable = False
        om.MPxNode.addAttribute(GeoPos.aoPosY)

        # aoPosZ Attr
        GeoPos.aoPosZ = nAttrFn.create("outZ", "oz", om.MFnNumericData.kDouble)
        nAttrFn.storable = False
        nAttrFn.keyable = False
        nAttrFn.readable = True
        nAttrFn.writable = False
        om.MPxNode.addAttribute(GeoPos.aoPosZ)

        # aoPos Attr
        GeoPos.aoPos = nAttrFn.create(
            "out", "o", GeoPos.aoPosX, GeoPos.aoPosY, GeoPos.aoPosZ
        )
        nAttrFn.storable = False
        nAttrFn.keyable = False
        nAttrFn.readable = True
        nAttrFn.writable = False
        om.MPxNode.addAttribute(GeoPos.aoPos)

        # when Mesh changes
        om.MPxNode.attributeAffects(GeoPos.aiMesh, GeoPos.aoPos)
        om.MPxNode.attributeAffects(GeoPos.aiMesh, GeoPos.aoPosX)
        om.MPxNode.attributeAffects(GeoPos.aiMesh, GeoPos.aoPosY)
        om.MPxNode.attributeAffects(GeoPos.aiMesh, GeoPos.aoPosZ)

        # when Pos changes
        om.MPxNode.attributeAffects(GeoPos.aiPos, GeoPos.aoPos)
        om.MPxNode.attributeAffects(GeoPos.aiPos, GeoPos.aoPosX)
        om.MPxNode.attributeAffects(GeoPos.aiPos, GeoPos.aoPosY)
        om.MPxNode.attributeAffects(GeoPos.aiPos, GeoPos.aoPosZ)

        # when PosX changes
        om.MPxNode.attributeAffects(GeoPos.aiPosX, GeoPos.aoPos)
        om.MPxNode.attributeAffects(GeoPos.aiPosX, GeoPos.aoPosX)
        om.MPxNode.attributeAffects(GeoPos.aiPosX, GeoPos.aoPosY)
        om.MPxNode.attributeAffects(GeoPos.aiPosX, GeoPos.aoPosZ)

        # when PosY changes
        om.MPxNode.attributeAffects(GeoPos.aiPosY, GeoPos.aoPos)
        om.MPxNode.attributeAffects(GeoPos.aiPosY, GeoPos.aoPosX)
        om.MPxNode.attributeAffects(GeoPos.aiPosY, GeoPos.aoPosY)
        om.MPxNode.attributeAffects(GeoPos.aiPosY, GeoPos.aoPosZ)

        # when PosZ changes
        om.MPxNode.attributeAffects(GeoPos.aiPosZ, GeoPos.aoPos)
        om.MPxNode.attributeAffects(GeoPos.aiPosZ, GeoPos.aoPosX)
        om.MPxNode.attributeAffects(GeoPos.aiPosZ, GeoPos.aoPosY)
        om.MPxNode.attributeAffects(GeoPos.aiPosZ, GeoPos.aoPosZ)

    def calcCloset(self, obj, pos):
        FnMesh = om.MFnMesh(obj)
        vec = om.MFloatVector(0, -1, 0)
        hit = FnMesh.closestIntersection(
            pos, vec, om.MSpace.kWorld, 9999, False, idsSorted=True, tolerance=0.0000001
        )
        return hit[0]

    def compute(self, plug, data):
        # Compute OutPut
        if plug in [GeoPos.aoPos, GeoPos.aoPosX, GeoPos.aoPosY, GeoPos.aoPosZ]:
            aiMeshDH = data.inputValue(GeoPos.aiMesh)
            aimesh = aiMeshDH.asMesh()
            aiPosDH = data.inputValue(GeoPos.aiPos)
            inPos = om.MFloatPoint(aiPosDH.asDouble3())

            outPos = self.calcCloset(aimesh, inPos)
            aoPosDH = data.outputValue(GeoPos.aoPos)
            aoPosDH.set3Double(outPos.x, outPos.y, outPos.z)
            data.setClean(plug)


# INIT PLUGIN
def initializePlugin(obj):
    plugin = om.MFnPlugin(obj)
    try:
        plugin.registerNode("geopos", GeoPos.ID, GeoPos.cmdCreator, GeoPos.initNode)
    except:
        sys.stderr.write("Failed to register node\n")
        raise


# UN INIT PLUGIN
def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)
    try:
        plugin.deregisterNode(GeoPos.ID)
    except:
        sys.stderr.write("Failed to deregister node\n")
        raise
