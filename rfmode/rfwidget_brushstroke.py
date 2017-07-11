import math
import bgl
from mathutils import Matrix, Vector
from ..common.maths import Vec, Point, Point2D, Direction
from ..lib.common_drawing_bmesh import glEnableStipple

class RFWidget_BrushStroke:
    def brushstroke_modal_main(self):
        if self.rfcontext.actions.pressed('brush size'):
            return 'size'
        
        if self.rfcontext.actions.pressed('insert'):
            self.stroke2D.clear()
            self.stroke2D_left.clear()
            self.stroke2D_right.clear()
            return 'stroke'
    
    def brushstroke_mouse_cursor(self):
        if self.mode in {'main','stroke'}:
             return 'NONE' if self.hit else 'CROSSHAIR'
        return 'MOVE_X'
    
    def brushstroke_postview(self):
        if self.mode not in {'main','stroke'}: return
        if not self.hit: return
        cx,cy,cp = self.x,self.y,self.p
        cs_outer = self.s * self.size
        cs_inner = self.s * self.size * 0.5
        cr,cg,cb = self.color
        
        bgl.glDepthRange(0, 0.999)      # squeeze depth just a bit 
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glLineWidth(2.0)
        bgl.glPointSize(3.0)
        
        ######################################
        # draw in front of geometry
        
        bgl.glDepthFunc(bgl.GL_LEQUAL)
        bgl.glDepthMask(bgl.GL_FALSE)   # do not overwrite depth
        
        bgl.glColor4f(cr, cg, cb, 1.0)       # outer ring
        bgl.glBegin(bgl.GL_LINE_STRIP)
        for x,y in self.points:
            p = (cs_outer * ((cx * x) + (cy * y))) + cp
            bgl.glVertex3f(*p)
        bgl.glEnd()
        
        bgl.glColor4f(cr, cg, cb, 0.1)     # inner ring
        bgl.glBegin(bgl.GL_LINE_STRIP)
        for x,y in self.points:
            p = (cs_inner * ((cx * x) + (cy * y))) + cp
            bgl.glVertex3f(*p)
        bgl.glEnd()
        
        bgl.glColor4f(1, 1, 1, 0.25)    # center point
        bgl.glBegin(bgl.GL_POINTS)
        bgl.glVertex3f(*cp)
        bgl.glEnd()
        
        ######################################
        # draw behind geometry (hidden below)
        
        bgl.glDepthFunc(bgl.GL_GREATER)
        bgl.glDepthMask(bgl.GL_FALSE)   # do not overwrite depth
        
        bgl.glColor4f(cr, cg, cb, 0.05)    # outer ring
        bgl.glBegin(bgl.GL_LINE_STRIP)
        for x,y in self.points:
            p = (cs_outer * ((cx * x) + (cy * y))) + cp
            bgl.glVertex3f(*p)
        bgl.glEnd()
        
        bgl.glColor4f(cr, cg, cb, 0.01)   # inner ring
        bgl.glBegin(bgl.GL_LINE_STRIP)
        for x,y in self.points:
            p = (cs_inner * ((cx * x) + (cy * y))) + cp
            bgl.glVertex3f(*p)
        bgl.glEnd()
        
        ######################################
        # reset to defaults
        
        bgl.glDepthFunc(bgl.GL_LEQUAL)
        bgl.glDepthMask(bgl.GL_TRUE)
        
        bgl.glDepthRange(0, 1)
    
    def brushstroke_postpixel(self):
        w,h = self.rfcontext.actions.size
        
        bgl.glEnable(bgl.GL_BLEND)
        
        if self.mode == 'main':
            return
        
        if self.mode == 'stroke':
            bgl.glLineWidth(2.0)
            glEnableStipple(enable=True)
            bgl.glColor4f(1,1,1,0.5)
            bgl.glBegin(bgl.GL_LINE_STRIP)
            for x,y in self.stroke2D:
                bgl.glVertex2f(x,y)
            bgl.glEnd()
            bgl.glColor4f(1,1,1,0.15)
            bgl.glBegin(bgl.GL_LINE_STRIP)
            for x,y in self.stroke2D_left:
                bgl.glVertex2f(x,y)
            bgl.glEnd()
            bgl.glColor4f(1,1,1,0.15)
            bgl.glBegin(bgl.GL_LINE_STRIP)
            for x,y in self.stroke2D_right:
                bgl.glVertex2f(x,y)
            bgl.glEnd()
            glEnableStipple(enable=False)
            return
        
        
        cx,cy,cp = Vector((1,0)),Vector((0,1)),Vector((w/2,h/2))
        cs_outer = self.size
        cs_inner = self.size * 0.5
        cr,cg,cb = self.color
        
        bgl.glLineWidth(2.0)
        
        bgl.glColor4f(cr, cg, cb, 1)                       # outer ring
        bgl.glBegin(bgl.GL_LINE_STRIP)
        for x,y in self.points:
            p = (cs_outer * ((cx * x) + (cy * y))) + cp
            bgl.glVertex2f(*p)
        bgl.glEnd()
        
        bgl.glColor4f(cr, cg, cb, 0.1)                     # inner ring
        bgl.glBegin(bgl.GL_LINE_STRIP)
        for x,y in self.points:
            p = (cs_inner * ((cx * x) + (cy * y))) + cp
            bgl.glVertex2f(*p)
        bgl.glEnd()
    